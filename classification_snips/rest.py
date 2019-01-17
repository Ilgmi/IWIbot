# -*- coding: utf-8 -*-
import atexit
import json
import os
import sys

import cf_deployment_tracker
import metrics_tracker_client
# use natural language toolkit
import nltk
from classifier.classifier import Classifier
from classifier.startup import populate_intents, populate_entities_for_meal, populate_entities_for_timetables, \
    populate_entities_for_navigation
from classifier.trainer import Trainer #TODO: remove old solution
from classifier.trainer_new import SnipsNluTrainer
from classifier.cos_context import CosContext
from classifier.database_context import DatabaseContext
from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify

###
# Text Classification using Snips NLU
#
###

nltk.download('punkt')

# Emit Bluemix deployment event
cf_deployment_tracker.track()
metrics_tracker_client.DSX('org/repo')

app = Flask(__name__, static_url_path='')

client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        client.create_database('trainer', throw_on_exists=False)
        client.create_database('synapse', throw_on_exists=False)
        #Cloud Object Storage
        creds_cos = vcap['cloud-object-storage'][0]['credentials']
        api_key_cos = creds_cos['apikey']
        #:TODO create envir before deploy!!!
        auth_endpoint_cos = creds_cos['auth_endpoint']
        #:TODO create envir before deploy!!!
        service_endpoint_cos = creds_cos['service_endpoint']
        service_instance_id_cos = creds_cos['resource_instance_id']
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        #Cloudant
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        client.create_database('trainer', throw_on_exists=False)
        client.create_database('synapse', throw_on_exists=False)
        #Cloud Object Storage
        creds_cos = vcap['services']['cloud-object-storage'][0]['credentials']
        api_key_cos = creds_cos['api_key']
        auth_endpoint_cos = creds_cos['auth_endpoint']
        service_endpoint_cos = creds_cos['service_endpoint']
        service_instance_id_cos = creds_cos['service_instance_id']

# init client, Classifier
cache = dict()
cache["classifier"] = Classifier()
cache["classifier"].load()
# cache classifier
# cache trainer


# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


def get_database_context() -> DatabaseContext:
    return DatabaseContext(client)

def get_cos_context() -> CosContext:
    return CosContext(api_key_cos, service_instance_id_cos, auth_endpoint_cos, service_endpoint_cos)

def get_trainer() -> SnipsNluTrainer:
    return SnipsNluTrainer(get_database_context(), get_cos_context())

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/api/trainEngine', methods=['GET'])
def train_Engine():
    result = get_trainer().start_training()
    if result:
        return jsonify("Success! Engine was trained"), 200
    else:
        return jsonify("Error! Engine wasn't trained.."), 404

@app.route('/api/rollbackEngine', methods=['GET'])
def rollback_Engine():
    result = get_trainer().rollback_nlu()
    if result:
        return jsonify("Success! Engine was restored"), 200
    else:
        return jsonify("Error! Engine rollback is not possible.."), 404

@app.route('/api/intent/<string:name>', methods=['GET'])
def get_intent(name):
    intents = get_database_context().get_intents()
    if name in intents:
        return jsonify(intents[name]), 200
    else:
        return jsonify("Intent Not Found"), 404


@app.route('/api/intent', methods=['GET'])
def get_intents():
    database_context = get_database_context()
    print(database_context, file=sys.stderr)
    intents = database_context.get_intents()
    return jsonify(intents)


@app.route('/api/intent/<string:name>', methods=['POST'])
def create_intent(name):
    intent = request.json
    print(intent, file=sys.stderr)
    if len(name) > 0 and len(intent) > 0:
        return jsonify(get_database_context().create_intent(name, intent)), 201
    return "Name:( " + name + " ): Or Intent:( " + intent + " ): Not set"


@app.route('/api/intent/<string:name>', methods=['PUT'])
def update_intent(name):
    intent = request.json
    if len(name) > 0 and len(intent) > 0:
        return jsonify(get_database_context().update_intent(name, intent)), 200
    return "Name:( " + name + " ): Or Intent:( " + intent + " ): Not set"


@app.route('/api/intent/<string:name>', methods=['DELETE'])
def delete_intent(name):
    intents = get_database_context().get_intents()
    if len(name) > 0 and name in intents:
        success = get_database_context().delete_intent(name)
        if success:
            return jsonify(success), 200
        else:
            return jsonify(success), 400
    else:
        return jsonify(False), 404


@app.route('/api/entity/<string:name>', methods=['POST'])
def create_entity(name):
    entity = request.json
    if len(name) > 0 and len(entity) > 0:
        return jsonify(get_database_context().create_entity(name, entity)), 201
    return "Name:( " + name + " ): Or entity:( " + entity + " ): Not set"


@app.route('/api/entity/<string:name>', methods=['PUT'])
def update_entity(name):
    entity = request.json
    if len(name) > 0 and len(entity) > 0:
        if entity['matching_strictness'] == 0:
            entity['matching_strictness'] = 0.0
        if entity['matching_strictness'] == 1:
            entity['matching_strictness'] = 1.0

        return jsonify(get_database_context().update_entity(name, entity)), 200
    return "Name:( " + name + " ): Or entity:( " + entity + " ): Not set"


@app.route('/api/entity/<string:name>', methods=['DELETE'])
def delete_entity(name):
    intents = get_database_context().get_entities()
    if len(name) > 0 and name in intents:
        success = get_database_context().delete_entity(name)
        if success:
            return jsonify(success), 200
        else:
            return jsonify(success), 400
    else:
        return jsonify(False), 404


@app.route('/api/entity/<string:name>', methods=['GET'])
def get_entity(name):
    entities = get_database_context().get_entities()
    if name in entities:
        return jsonify(entities[name]), 200
    else:
        return "Intent Not Found", 404


@app.route('/api/entity', methods=['GET'])
def get_entities():
    database_context = get_database_context()
    print(database_context, file=sys.stderr)
    entities = database_context.get_entities()
    return jsonify(entities)

@app.route('/api/sentences', methods=['GET'])
def get_sentences():
    sentences = get_database_context().get_sentences()
    return jsonify(sentences)

@app.route('/api/entity/snips/<string:name>', methods=['POST'])
def add_build_in_entity(name):
    name = "snips/" + name
    get_database_context().create_entity(name, {})
    return jsonify(True)


@app.route('/api/entity/snips/<string:name>', methods=['DELETE'])
def delete_build_in_entity(name):
    name = "snips/" + name
    return delete_entity(name)


@app.route('/api/entity/snips', methods=['GET'])
def get_build_in_entity():
    return jsonify(['amountOfMoney', 'datetime', 'duration', 'musicAlbum', 'musicArtist', 'musicTrack',
            'number', 'ordinal', 'percentage', 'temperature'])


@app.route('/api/add/sentence/<string:sentence>', methods=['PUT'])
def update_sentences(sentence):
    if len(sentence) > 0:
        return jsonify(get_database_context().add_not_found_sentence(sentence)), 200
    return "NO SENTENCE FOUND"


# /**
#  * Endpoint to classify a conversation service request JSON for the intent.
#  *
#  * @return A JSON response with the classification
#  */
@app.route('/api/testIntent', methods=['POST'])
def testIntent():
    request_object = request.json
    sentence = request.json['sentence']
    if client is not None:
        if sentence == 'populate':
            # populate database with base data and train all neuronal netwroks
            populate_intentspopulate_intents(client)
            populate_entities_for_meal(client)
            populate_entities_for_timetables(client)
            populate_entities_for_navigation(client)
            cache["intents"].load()
            cache["entities@timetables"].load()
            cache["entities@meal"].load()

            classification = dict()
            classification['intent'] = "Populated"
        else:
            if 'intents' not in cache.keys():
                cache["intents"] = Classifier("intents", client)
                get_database_context().add_not_found_sentence(sentence)

            classifier = cache["intents"]

            results = classifier.classify(sentence)

            classification = dict()
            if len(results) > 0:
                classification['intent'] = results[0][0]
            else:
                classification['intent'] = ""
    else:
        print("NO DATABASE")

        classification = dict()
        classification['intent'] = "NO DATABASE"

    response_object = removekey(request_object, "sentence")
    response_object["classifications"] = classification

    return 'Results: %s' % classification['intent']


# /**
#  * Endpoint to classify a conversation service request JSON for the intent.
#  *
#  * @return A JSON response with the classification
#  */
@app.route('/api/getIntent', methods=['POST'])
def getIntent():
    request_object = request.json
    sentence = request.json['sentence']
    if client is not None:
        if 'classifier' not in cache.keys():
            cache["classifier"] = Classifier()

        classifier = cache["classifier"]

        result = classifier.classifyIntent(sentence)

        if result[0][1] < classifier.ERROR_THRESHOLD:
            get_database_context().add_not_found_sentence(sentence)

        classification = dict()
        if len(result) > 0:
            classification['intent'] = result[0][0]
        else:
            classification['intent'] = ""
    else:
        print("NO DATABASE")

        classification = dict()
        classification['intent'] = "NO DATABASE"

    response_object = removekey(request_object, "sentence")
    response_object["classifications"] = classification

    return jsonify(response_object)


# /**
#  * Endpoint to classify a conversation service request JSON for its entity
#  * based on the priorIntent given.
#  *
#  * @return A JSON response with the classification
#  */
@app.route('/api/getEntity', methods=['POST'])
def getEntity():
    request_object = request.json
    sentence = request.json['sentence']

    if client is not None:
        if 'classifier' not in cache.keys():
            cache["classifier"] = Classifier()

        classifier = cache["classifier"]
        # keep
        results = classifier.classify(sentence)
        # strip keep only name of entity
        classification = dict()
        if len(results) > 0:
            classification['entity'] = results[0][0]
        else:
            classification['entity'] = ""
    else:
        print("NO DATABASE")

        classification = dict()
        classification['entity'] = "NO DATABASE"

    response_object = removekey(request_object, "sentence")
    response_object["classifications"] = classification

    return jsonify(response_object)


# /**
#  * Endpoint to add a classification to a training set for classifying
#  * the intent.
#  *
#  * @return No response
#  */
@app.route('/api/addIntent', methods=['POST'])
def addIntent():
    sentence = request.json['sentence']
    intent = request.json['intent']
    if client is not None:
        intents = Trainer("intents", client)
        intents.add_to_traingset(sentence, intent, True)
        return jsonify([])
    else:
        print("NO DATABASE")
        return "NO DATABASE"


# /**
#  * Endpoint to train a neural network for classifying an intent.
#  *
#  * @return No response
#  */
@app.route('/api/trainIntents', methods=['POST'])
def trainIntents():
    if client is not None:
        intents = Trainer("intents", client)
        intents.start_training()
        if 'intents' not in cache.keys():
            cache['intents'] = Classifier('intents', client)
        else:
            cache['intents'].load()
        return jsonify([])
    else:
        print("NO DATABASE")
        return "NO DATABASE"


# /**
#  * Endpoint to add a classification to a training set for classifying
#  * the entities of an intent.
#  *
#  * @return No response
#  */
@app.route('/api/addEntity', methods=['POST'])
def addEntity():
    intent = request.json['intent']
    sentence = request.json['sentence']
    entity = request.json['entity']
    if client is not None:
        classifier_name = "entities@" + intent
        entities = Trainer(classifier_name, client)
        entities.add_to_traingset(sentence, entity, True)
        return jsonify([])
    else:
        print("NO DATABASE")
        return "NO DATABASE"


# /**
#  * Endpoint to train a neural network for classifying the entities of an intent.
#  *
#  * @return No response
#  */
@app.route('/api/trainEntity', methods=['POST'])
def trainEntity():
    intent = request.json['intent']
    if client is not None:
        classifier_name = "entities@" + intent
        entities = Trainer(classifier_name, client)
        entities.start_training()
        if classifier_name not in cache.keys():
            cache[classifier_name] = Classifier(classifier_name, client)
        else:
            cache[classifier_name].load()
        return jsonify([])
    else:
        print("NO DATABASE")
        return "NO DATABASE"


@atexit.register
def shutdown():
    if client is not None:
        client.disconnect()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

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
from classifier.trainer import SnipsNluTrainer
from classifier.cos_context import CosContext
from classifier.database_context import DatabaseContext
from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify

###
# Text Classification using Snips NLU
#
###

# TODO: Aufsetzen in Cloud

nltk.download('punkt')
os.system("snips-nlu download de")
os.system("snips-nlu download en")

# Emit Bluemix deployment event
cf_deployment_tracker.track()
metrics_tracker_client.DSX('org/repo')

app = Flask(__name__, static_url_path='')

client = None

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
        # Cloud Object Storage
    if 'cloud-object-storage' in vcap:
        creds_cos = vcap['cloud-object-storage'][0]['credentials']
        api_key_cos = creds_cos['apikey']  # reads from instance env
        auth_endpoint_cos = "https://iam.bluemix.net/oidc/token"  # hardcode parameter
        service_endpoint_cos = "https://s3.eu.cloud-object-storage.appdomain.cloud"  # hardcode parameter, EU Cross Region Endpoints
        service_instance_id_cos = creds_cos['resource_instance_id']  # reads from instance env
        bucket_name = os.getenv('bucket_name')  # User defined env by Cloud Foundry App

elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        # Cloudant
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        client.create_database('trainer', throw_on_exists=False)
        client.create_database('synapse', throw_on_exists=False)
        # Cloud Object Storage
        creds_cos = vcap['services']['cloud-object-storage'][0]['credentials']
        api_key_cos = creds_cos['api_key']
        auth_endpoint_cos = creds_cos['auth_endpoint']
        service_endpoint_cos = creds_cos['service_endpoint']
        service_instance_id_cos = creds_cos['service_instance_id']
        bucket_name = creds_cos['bucket_name']

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


def get_database_context() -> DatabaseContext:
    return DatabaseContext(client)

def get_cos_context() -> CosContext:
    return CosContext(api_key_cos, service_instance_id_cos, auth_endpoint_cos, service_endpoint_cos, bucket_name)

def get_trainer() -> SnipsNluTrainer:
    return SnipsNluTrainer(get_database_context(), get_cos_context())

# init client, Classifier
cache = dict()
cache["classifier"] = Classifier()
cache["classifier"].load(DatabaseContext(client), get_cos_context())
# cache classifier
# cache trainer

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
        cache["classifier"] = Classifier()
        cache["classifier"].load(DatabaseContext(client), get_cos_context())
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
    entities = database_context.get_entities()
    return jsonify(entities)


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


@app.route('/api/sentence/', methods=['GET'])
def get_sentences():
    return jsonify(get_database_context().get_sentences())


@app.route('/api/sentence/', methods=['PUT'])
def update_sentences():
    sentence = request.json
    print(request)
    if len(sentence) >= 0:
        return jsonify(get_database_context().update_sentences(sentence)), 200
    return jsonify('NO Content'), 204


# /**
#  * Endpoint to classify a conversation service request JSON for the intent.
#  *
#  * @return A JSON response with the classification
#  */
@app.route('/api/getIntent', methods=['POST'])
def getIntent():
    print(request.json)
    print(request.json['sentence'])
    request_object = request.json
    sentence = request.json['sentence']
    if client is not None:
        if 'classifier' not in cache.keys():
            cache["classifier"] = Classifier()

        classifier = cache["classifier"]

        result = classifier.classifyIntent(sentence)
        classification = dict()
        print(result)
        if len(result) > 0:

            print(result)
            if result[1] < classifier.ERROR_THRESHOLD:
                get_database_context().add_not_found_sentence(sentence)

            classification['intent'] = result[0]
        else:
            classification['intent'] = ""
            get_database_context().add_not_found_sentence(sentence)
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
        results = classifier.classifyEntity(sentence)
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

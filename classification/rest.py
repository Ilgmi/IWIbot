import atexit
import json
import os

import cf_deployment_tracker
import metrics_tracker_client
# use natural language toolkit
import nltk
from classifier.classifier import Classifier
from classifier.startup import populate_intents, populate_entities_for_meal, populate_entities_for_timetables, populate_entities_for_navigation
from classifier.trainer import Trainer
from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify

###
# Text Classification using Artificial Neural Networks (ANN)
# Based on https://machinelearnings.co/text-classification-using-neural-networks-f5cd7b8765c6
###


nltk.download('punkt')

# Emit Bluemix deployment event
cf_deployment_tracker.track()
metrics_tracker_client.DSX('org/repo')

app = Flask(__name__)

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
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        client.create_database('trainer', throw_on_exists=False)
        client.create_database('synapse', throw_on_exists=False)

cache = dict()
if client is not None:
    # create Classifier cache on startup
    cache["intents"] = Classifier("intents", client)
    cache["intents"].load()
    cache["entities@timetables"] = Classifier("entities@timetables", client)
    cache["entities@timetables"].load()
    cache["entities@meal"] = Classifier("entities@meal", client)
    cache["entities@meal"].load()

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


@app.route('/')
def home():
    return render_template('index.html')


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
            populate_intents(client)
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
        if 'intents' not in cache.keys():
            cache["intents"] = Classifier("intents", client)

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
    prior_intents = request.json['context']["priorIntent"]["intent"]
    if client is not None:
        classifier_name = "entities@" + prior_intents

        if classifier_name not in cache.keys():
            cache[classifier_name] = Classifier(classifier_name, client)

        classifier = cache[classifier_name]

        results = classifier.classify(sentence)

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

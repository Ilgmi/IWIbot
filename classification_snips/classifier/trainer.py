import datetime
import time

import nltk
import numpy as np
from cloudant.document import Document
from nltk.stem.lancaster import LancasterStemmer


###
# Define ANN training
###

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output * (1 - output)


# compute sigmoid non-linearity
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


# trains a neuronal network
def train(context, db, X, y, classes, words, hidden_neurons=10, alpha=1.0, epochs=50000, dropout=False,
          dropout_percent=0.5):
    print("Training with %s neurons, alpha:%s, dropout:%s %s" % (
        hidden_neurons, str(alpha), dropout, dropout_percent if dropout else ''))
    print("Input matrix: %sx%s    Output matrix: %sx%s" % (len(X), len(X[0]), 1, len(classes)))
    np.random.seed(1)

    last_mean_error = 1
    # randomly initialize our weights with mean 0
    synapse_0 = 2 * np.random.random((len(X[0]), hidden_neurons)) - 1
    synapse_1 = 2 * np.random.random((hidden_neurons, len(classes))) - 1

    prev_synapse_0_weight_update = np.zeros_like(synapse_0)
    prev_synapse_1_weight_update = np.zeros_like(synapse_1)

    synapse_0_direction_count = np.zeros_like(synapse_0)
    synapse_1_direction_count = np.zeros_like(synapse_1)

    for j in iter(range(epochs + 1)):

        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))

        if dropout:
            layer_1 *= np.random.binomial([np.ones((len(X), hidden_neurons))], 1 - dropout_percent)[0] * (
                    1.0 / (1 - dropout_percent))

        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = y - layer_2

        if (j % 10000) == 0 and j > 5000:
            # if this 10k iteration's error is greater than the last iteration, break out
            if np.mean(np.abs(layer_2_error)) < last_mean_error:
                print("delta after " + str(j) + " iterations:" + str(np.mean(np.abs(layer_2_error))))
                last_mean_error = np.mean(np.abs(layer_2_error))
            else:
                print("break:", np.mean(np.abs(layer_2_error)), ">", last_mean_error)
                break

        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)

        synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
        synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))

        if j > 0:
            synapse_0_direction_count += np.abs(
                ((synapse_0_weight_update > 0) + 0) - ((prev_synapse_0_weight_update > 0) + 0))
            synapse_1_direction_count += np.abs(
                ((synapse_1_weight_update > 0) + 0) - ((prev_synapse_1_weight_update > 0) + 0))

        synapse_1 += alpha * synapse_1_weight_update
        synapse_0 += alpha * synapse_0_weight_update

        prev_synapse_0_weight_update = synapse_0_weight_update
        prev_synapse_1_weight_update = synapse_1_weight_update

    now = datetime.datetime.now()

    # persist synapses
    synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(),
               'datetime': now.strftime("%Y-%m-%d %H:%M"),
               'words': words,
               'classes': classes
               }

    # Create a document using the Database API
    if Document(db, context).exists():
        synapses = db[context]
        synapses['synapse'] = synapse
        synapses.save()
    else:
        data = dict([('_id', context), ('context', context),
                     ('synapse', synapse)])
        synapses = db.create_document(data)

    # Check that the document exists in the database
    if synapses.exists():
        print("saved synapses to database")
    else:
        print("saving synapses to database FAILED!")


def do_training(context, synapse_db, classes, words, _x, _y, show_details=True):
    X = np.array(_x)
    y = np.array(_y)

    start_time = time.time()
    train(context, synapse_db, X, y, classes, words, hidden_neurons=20, alpha=0.2,
          epochs=100000, dropout=False, dropout_percent=0.2)
    elapsed_time = time.time() - start_time

    if show_details:
        print("processing time:", elapsed_time, "seconds")


class Trainer:
    context = ""
    client = []
    trainer_db = []
    synapse_db = []
    training_data = []
    words = []
    classes = []
    documents = []
    bag = []

    # /**
    #  * Constructor that creates a new Trainer for a neuronal network
    #  */
    def __init__(self, context, client):
        self.context = context
        self.client = client
        self.trainer_db = client["trainer"]
        if Document(self.trainer_db, self.context).exists():
            trainer = self.trainer_db[self.context]
            self.training_data = list(trainer['training_data'])
        else:
            self.training_data = list()
            data = dict([('_id', self.context), ('context', self.context),
                         ('training_data', self.training_data)])

            # Create a document using the Database API
            self.trainer_db.create_document(data)
        self.synapse_db = client["synapse"]

    # /**
    #  * Adds a new example for an intent to the training set and retrains the neuronal network for the context and
    #  * persists it in the database
    #  */
    def add_to_traingset_and_retrain(self, sentence, intend, trusted=False):
        self.add_to_traingset(sentence, intend, trusted)
        self.start_training()

    # /**
    #  * Adds a new example for an intent to the training set.
    #  */
    def add_to_traingset(self, sentence, intend, trusted=False):
        entry = dict([('class', intend), ('sentence', sentence)])
        if entry not in self.training_data:
            self.training_data.append(entry)

            trainer = self.trainer_db[self.context]
            trainer['training_data'] = self.training_data
            trainer.save()

    # /**
    #  * Removes an example for an intent from the training set and retrains the neuronal network for the context and
    #  * persists it in the database
    #  */
    def remove_from_trainingset_and_retrain(self, sentence, intend, trusted=False):
        self.remove_from_trainingset(sentence, intend, trusted)
        self.start_training()

    # /**
    #  * Removes an example for an intent from the training set.
    #  */
    def remove_from_trainingset(self, sentence, intend, trusted=False):
        entry = dict([('class', intend), ('sentence', sentence)])
        if entry in self.training_data:
            self.training_data.remove(entry)

            trainer = self.trainer_db[self.context]
            trainer['training_data'] = self.training_data
            trainer.save()

    # /**
    #  * Trains the neuronal network for the context and persists it in the database
    #  */
    def start_training(self):
        stemmer = LancasterStemmer()

        print("%s sentences in training data" % len(self.training_data))

        self.words = []
        self.classes = []
        self.documents = []
        ignore_words = ['?']
        # loop through each sentence in our training data
        for pattern in self.training_data:
            # tokenize each word in the sentence
            w = nltk.word_tokenize(pattern['sentence'])
            # add to our words list
            self.words.extend(w)
            # add to documents in our corpus
            self.documents.append((w, pattern['class']))
            # add to our classes list
            if pattern['class'] not in self.classes:
                self.classes.append(pattern['class'])

        # stem and lower each word and remove duplicates
        self.words = [stemmer.stem(w.lower()) for w in self.words if w not in ignore_words]
        self.words = list(set(self.words))

        # remove duplicates
        self.classes = list(set(self.classes))

        print(len(self.documents), "documents")
        print(len(self.classes), "classes", self.classes)
        print(len(self.words), "unique stemmed words", self.words)

        # create our training data
        training = []
        output = []
        # create an empty array for our output
        output_empty = [0] * len(self.classes)

        # training set, bag of words for each sentence
        for self.doc in self.documents:
            # initialize our bag of words
            self.bag = []
            # list of tokenized words for the pattern
            pattern_words = self.doc[0]
            # stem each word
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            # create our bag of words array
            for w in self.words:
                self.bag.append(1) if w in pattern_words else self.bag.append(0)

            training.append(self.bag)
            # output is a '0' for each tag and '1' for current tag
            output_row = list(output_empty)
            output_row[self.classes.index(self.doc[1])] = 1
            output.append(output_row)

        # sample training/output
        i = 0
        w = self.documents[i][0]
        print([stemmer.stem(word.lower()) for word in w])
        print(training[i])
        print(output[i])

        ###
        # play
        ###

        do_training(self.context, self.synapse_db, self.classes, self.words, training, output)

import nltk
import numpy as np
from nltk.stem.lancaster import LancasterStemmer


# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output * (1 - output)


def clean_up_sentence(sentence):
    stemmer = LancasterStemmer()
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def think(sentence, words, synapse_0, synapse_1, show_details=False):
    x = bow(sentence.lower(), words, show_details)
    if show_details:
        print("sentence:", sentence, "\n bow:", x)

    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(np.dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2


class Classifier:
    context = ""
    client = []
    synapse_db = []
    synapse = []
    words = []
    classes = []
    synapse_0 = []
    synapse_1 = []
    # probability threshold
    ERROR_THRESHOLD = 0.2

    # /**
    #  * Constructor that creates a new Classifier and loads the current neuronal network from the database
    #  */
    def __init__(self, context, client, error_threshold=0.2):
        self.ERROR_THRESHOLD = error_threshold
        self.context = context
        self.client = client
        self.synapse_db = client["synapse"]
        if not self.synapse_db.exists():
            self.synapse_db = client.create_database('synapse', throw_on_exists=False)
        self.load()

    # /**
    #  * Classifies a sentence.
    #  *
    #  * @return A list of intents with a confidences.
    #  */
    def classify(self, sentence, show_details=False):
        results = think(sentence, self.words, self.synapse_0, self.synapse_1, show_details)
        results = [[i, r] for i, r in enumerate(results) if r > self.ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_results = [[self.classes[r[0]], r[1]] for r in results]
        print("%s \n classification: %s" % (sentence, return_results))
        return return_results

    # /**
    #  * Reloads the neuronal network for the classifier from the database.
    #  */
    def load(self):
        synapses = self.synapse_db[self.context]
        if synapses.exists():
            self.synapse = synapses['synapse']
            self.synapse_0 = np.asarray(self.synapse['synapse0'])
            self.synapse_1 = np.asarray(self.synapse['synapse1'])
            self.classes = np.asarray(self.synapse['classes'])
            self.words = np.asarray(self.synapse['words'])
        else:
            print("retrieving synapses from database FAILED!")

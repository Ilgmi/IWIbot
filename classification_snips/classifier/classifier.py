import numpy as np
import os
import snips_nlu
from snips_nlu import load_resources, SnipsNLUEngine

from .trainer import SnipsNluTrainer



#TODO: Classifier
# 1. Init mit daten aus nlu_data -> nlu
# 2. Falls nicht vorhanden --> nlu_data -> nlu_old
# 3. Methode  um Intent auszulesen
# 4. Methode um Entity auszulesen
# 5. Wird eine Intent nicht erkannt, wird er über eine Methode
#    in die Dataenbank mit aufgenommen um die sie gegebenen falls hinzuzufügen
#    Dies wird im Rest hinzugefügt.




class Classifier:
    # engine
    nlu_engine = SnipsNLUEngine()
    # probability threshold
    ERROR_THRESHOLD = 0.2

    # /**
    #  * Constructor that creates a new Classifier and loads the current neuronal network from the database
    #  */
    def __init__(self):
        x = 1

    # /**
    #  * Classifies a sentence.
    #  *
    #  * @return A list of intents with a confidences.
    #  */
    def classifyIntent(self, sentence):
        result = self.nlu_engine.parse(sentence)
        return_result = []
        print("classifyIntent",result)
        if result['intent'] is not None:
            return_result = [result["intent"]["intentName"], result["intent"]["probability"]]
        return return_result

    # /**
    #  * Classifies a sentence.
    #  *
    #  * @return A list of entities with a confidences.
    #  */
    def classifyEntity(self, sentence):
        result = self.nlu_engine.parse(sentence)
        return_result = []
        print(result)
        if result['slots'] is not None:
            for slot in result["slots"]:
                return_result.append([slot['value']['value'], result["intent"]["probability"]])
            return return_result
        else:
            return return_result

    # /**
    #  * Reloads the neuronal network for the classifier from the database.
    #  */
    # def load(self):
    #     if len(os.listdir('../nlu_data/nlu')) != 0:
    #         self.nlu_engine = SnipsNLUEngine.from_path("../nlu_data/nlu")
    #     elif len(os.listdir('../nlu_data/nlu_old')) != 0:
    #         print("Directory is not empty")
    #         self.nlu_engine = SnipsNLUEngine.from_path("../nlu_data/nlu_old")
    #     else:
    #         print("retrieving trained engine FAILED!")

    def load(self, database_context, cos_context):
        trainer = SnipsNluTrainer(database_context, cos_context)
        trainer.get_nlu_engine()
        self.nlu_engine = trainer.nlu_engine
        print("Classifier loaded")



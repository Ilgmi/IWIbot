import datetime
import zlib
import base64
import os

from snips_nlu import SnipsNLUEngine, load_resources
from cloudant.document import Document  #Temp. Database_context part



#TODO: Trainer
# 1. Laden der Trainingsdaten
# 2. NLU Trainieren
# 3. NLU in nlu_new persistieren
# 4. aktuelles nlu in nlu_old umbenen
# 5. nlu_new in nlu umbenenen
# Es soll immer eine alte Version zum RoleBack da sein.
# Methode für einen RoleBack sein.
# Methode um zu Trainieren --> Parameter DatabaseContext um daten zu holen

class SnipsNluTrainer:
    """Class to train NLU"""
    def __init__(self, database_context):
        self.context = database_context
        self.training_data = ""
        os.system("snips-nlu download de")
        os.system("snips-nlu download en")
        load_resources("de")
        load_resources("en")
        self.nlu_engine = SnipsNLUEngine()

    def start_training(self):
        self._load_training_data()
        self._train_nlu()
        self._persist_nlu()


    def _load_training_data(self):
        self.training_data = self.context.get_trainings_data()

    def _train_nlu(self):
        self.nlu_engine.fit(self.training_data)

    def _persist_nlu(self):
        engine_as_bytearray = self.nlu_engine.to_byte_array()
        formatted_engine = self._serializable_engine(engine_as_bytearray)
        now = datetime.datetime.now()
        engine = {'datetime': now.strftime("%Y-%m-%d %H:%M"), 'engine': formatted_engine}
        #TODO: persist engine to cloudant
        #TODO: if engine exist => rename it to old, persist new engine as new


    def serializable_engine(self, engine_as_bytearray):
        compressed_engine = zlib.compress(engine_as_bytearray) #compressed bytes
        engine_base64 = base64.b64encode(compressed_engine) #encode binary to base64 =>bytes
        engine_str = engine_base64.decode("utf-8") #encode base64 to ascii =>str
        return engine_str

    def deserializable_engine(self, engine_str ):
        compressed_engine = base64.b64decode(engine_str)
        engine_as_bytearray = zlib.decompress(compressed_engine)
        return engine_as_bytearray

    def _roleback_nlu(self):
        pass #TODO: cut engine_old to engine_new, return engine_new

    #TODO: Temp. Database_context part

    #TODO:Die Idee: Es werden 2 Versionen von Engine in DB gespeichert(old,new)
    #TODO: 1)Init&first_leart(engine_new <-), 2)Train again (engine_new -> engine_old, engine_new <-) in DB
    def _create_doc_engine(self, client, engine_str, data_now):
        engine_db = client["synapse"] #rename synapse to 'engine'
        if not Document(engine_db, 'engine_new').exist():
            engine_doc = dict([('_id', 'engine_new'), ('date', data_now), ('engine', engine_str)])
            engine_db.create_document(engine_doc)
            return True
        else:
            return False


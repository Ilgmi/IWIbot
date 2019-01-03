from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_DE

from .database_context import DatabaseContext

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
    def __init__(self, client):
        self.context = DatabaseContext(client)
        load_resources("de")
        load_resources("en")
        self.nlu_engine = SnipsNLUEngine(config=CONFIG_DE)


    def _load_training_data(self):
        data = self.context.get_trainings_data();
        return data

    def _train_nlu(self):
        self.nlu_engine.fit(self._load_training_data())

    def _persist_nlu(self):
        # TODO: Es gibt eine Methode um die SnipsNLU zu sichern.....
        engine_bytes = self.nlu_engine.to_byte_array()

    def _roleback_nlu(self):
        pass
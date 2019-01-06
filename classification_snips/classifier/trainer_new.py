import os
import shutil
import zipfile


from snips_nlu import SnipsNLUEngine, load_resources
from pathlib import Path
from cos_context import CosContext

ENGINE_PATH_OLD = Path(__file__).parents[1] / "engine/nlu_old"
ENGINE_PATH_NEW = Path(__file__).parents[1] / "engine/nlu_new"

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

        load_resources("de")
        load_resources("en")
        self.nlu_engine = SnipsNLUEngine()

    def start_training(self):
        self._load_training_data()
        self._train_nlu()
        self._persist_nlu()

    def get_nlu_engine(self):
        if not ENGINE_PATH_NEW.exists():
            print("Engine must be fitted! Please run 'start training'")
        else:
            loaded_engine = SnipsNLUEngine.from_path(ENGINE_PATH_NEW)
            self.nlu_engine = loaded_engine
        return self.nlu_engine

    def rollback_nlu(self):
        result = False
        if not ENGINE_PATH_OLD.exists():
            print("No backups exist..")
        else:
            loaded_engine = SnipsNLUEngine.from_path(ENGINE_PATH_OLD)
            self.nlu_engine = loaded_engine
            #Save backup as new engine
            #Save version before backup as old
            result_persist = self._persist_nlu()
            print("Engine rollback was successful")
        return result


    def _load_training_data(self):
        self.training_data = self.context #.get_trainings_data()
        if self.training_data == "":
            print("There are no training data!")
        else:
            print("Training data were loaded successfully")

    def _train_nlu(self):
        self.nlu_engine.fit(self.training_data)
        print("Engine was trained successfully")

    def _persist_nlu(self):
        result = False
        # first save engine attempt
        if not (ENGINE_PATH_NEW.exists()):
            self.nlu_engine.persist(ENGINE_PATH_NEW)
            result = True
        else:
            #Remove&override old backup
            if ENGINE_PATH_OLD.exists():
                shutil.rmtree(ENGINE_PATH_OLD)
                print("Removed old engine backup...")
            os.rename(ENGINE_PATH_NEW, ENGINE_PATH_OLD)
            self.nlu_engine.persist(ENGINE_PATH_NEW)
            result = True
        if result:
            print("Engine was saved successfully")
        return result

    #Persist engine as zip to bucket to decrease up/download time (5-6 MB vs 1.5 MB compressed)
    def _compress_engine(self, source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        print(source, destination, archive_from, archive_to)
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s' % (name, format), destination)

    def _decompress_engine(self, source, destination):
        zip_ref = zipfile.ZipFile(source, 'r')
        zip_ref.extractall(destination)


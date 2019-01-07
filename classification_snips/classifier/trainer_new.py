import os
import shutil
import zipfile


from snips_nlu import SnipsNLUEngine, load_resources
from pathlib import Path
from cos_context import CosContext

ENGINE_PATH_OLD = Path(__file__).parents[1] / "engine/nlu_old"
ENGINE_PATH_NEW = Path(__file__).parents[1] / "engine/nlu_new"
ENGINE_PATH_ZIP = Path(__file__).parents[1] / "engine"

NEW_ENGINE_NAME_ZIP = "engine_new.zip"
OLD_ENGINE_NAME_ZIP = "engine_old.zip"

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
        self.cos_context = CosContext()

        load_resources("de")
        load_resources("en")
        self.nlu_engine = SnipsNLUEngine()

    def start_training(self):
        self._load_training_data()
        self._train_nlu()
        self._persist_nlu()

    def get_nlu_engine(self):
        #TODO: load engine from bucket
        if not ENGINE_PATH_NEW.exists():
            print("Engine must be fitted! Please run 'start training'")
        else:
            loaded_engine = SnipsNLUEngine.from_path(ENGINE_PATH_NEW)
            self.nlu_engine = loaded_engine
        return self.nlu_engine

    def _load_training_data(self):
        #TODO: remove for deployment
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
            result = self._persist_to_bucket(ENGINE_PATH_NEW, ENGINE_PATH_ZIP, NEW_ENGINE_NAME_ZIP)
        else:
            #Remove&override old backup
            if ENGINE_PATH_OLD.exists():
                shutil.rmtree(ENGINE_PATH_OLD)
                self.cos_context.remove_file(OLD_ENGINE_NAME_ZIP)
                print("Removed old engine backup...")
            #save(rename) new engine as old local and in persist
            os.rename(ENGINE_PATH_NEW, ENGINE_PATH_OLD)
            self.cos_context.rename_file(NEW_ENGINE_NAME_ZIP, OLD_ENGINE_NAME_ZIP)
            #create new new engine
            self.nlu_engine.persist(ENGINE_PATH_NEW)
            result = self._persist_to_bucket(ENGINE_PATH_NEW, ENGINE_PATH_ZIP, NEW_ENGINE_NAME_ZIP)
        if result:
            print("Engine was saved successfully")
        return result

    def rollback_nlu(self):
        #TODO: rollback with ibm persist
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
        print("Engine was zipped...")

    # trainer.decompress_engine(str(ENGINE_PATH_NEW_ZIP/"engine.zip"), "/home/anon/Downloads")
    def _decompress_engine(self, source, destination):
        zip_ref = zipfile.ZipFile(source, 'r')
        zip_ref.extractall(destination)
        print("Engine was unzipped..")

    #Engine folder -> zip -> save to ibm bucket
    def _persist_to_bucket(self, source, destination, file_name):
        source = str(source)
        destination = str(destination)
        file_name = str(file_name)
        self._compress_engine(source, destination + "/" + file_name)
        result = self.cos_context.upload_file(destination + "/" + file_name, file_name)
        return result



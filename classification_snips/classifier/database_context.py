from cloudant.document import Document
import sys


class DatabaseContext:

    trainings_data = dict()

    def __init__(self, client):
        self.client = client
        self.trainer_db = client["trainer"]

        if Document(self.trainer_db, "training_data").exists():
            trainer = Document(self.trainer_db, "training_data")
            trainer.fetch()
            self.trainings_data = trainer['training_data']
        else:
            self.create_table()

        if not Document(self.trainer_db, 'notFoundSentence').exists():
            self.trainer_db.create_document({'_id': 'notFoundSentence', 'sentences': []})

    def create_table(self):
        self.trainings_data = dict([
            ('intents', dict()),
            ('entities', dict())
        ])
        data = dict([('_id', 'training_data'), ('training_data', self.trainings_data
                                       )])
        # Create a document using the Database API
        doc = self.trainer_db.create_document(data)
        self.log(self.trainer_db)
        doc.save()


    def add_not_found_sentence(self, sentence):
        sentences = Document(self.trainer_db, 'notFoundSentence')
        sentences['sentences'].append(sentence)
        sentences.save()

    def get_sentences(self):
        s = Document(self.trainer_db, 'notFoundSentence')
        return s['sentences']

    def update_sentences(self, new_sentences):
        sentences = Document(self.trainer_db, 'notFoundSentence')
        sentences['sentences'] = new_sentences
        sentences.save()

    def set_trainings_data(self, data):
        trainer = Document(self.trainer_db, "training_data")
        trainer.fetch()
        trainer['training_data'] = data
        trainer.save()

    def get_trainings_data(self):
        return self.trainings_data

    def save_trainings_data(self):
        self.set_trainings_data(self.trainings_data)

    def log(self, value):
        print(value, file=sys.stderr)

    def get_intents(self):
        data = self.get_trainings_data()
        self.log(data)
        return data["intents"]

    def get_intent(self, name):
        intents = self.get_intents()
        if name in intents:
            return intents[name]
        else:
            return dict()

    def get_entities(self):
        data = self.get_trainings_data()
        return data['entities']

    def get_entity(self, name):
        entities = self.get_entities()
        if name in entities:
            return entities[name]
        else:
            return dict()

    def create_entity(self, name, entity):
        entities = self.get_entities()
        success = False
        if name not in entities:
            entities[name] = entity
            self.save_trainings_data()
            success = True
        return success

    def create_intent(self, name, intent):
        intents = self.get_intents()
        success = False
        if name not in intents:
            intents[name] = intent
            self.save_trainings_data()
            success = True
        return success

    def update_intent(self, name, intent):
        intents = self.get_intents()
        success = False
        if name in intents:
            intents[name] = intent
            self.save_trainings_data()
            success = True
        return success

    def update_entity(self, name, entity):
        entities = self.get_entities()
        success = False
        if name in entities:
            entities[name] = entity
            self.save_trainings_data()
            success = True
        return success

    def delete_intent(self, name):
        intents = self.get_intents()
        success = False
        self.log(intents)
        if name in intents:
            intents.pop(name)
            self.save_trainings_data()
            success = True
        return success

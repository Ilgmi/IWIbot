from cloudant.document import Document


class DatabaseContext:

    def __init__(self, client):
        self.client = client
        self.trainer_db = client["trainer"]

        if Document(self.trainer_db, "data").exists():
            self.trainings_data = Document(self.trainer_db, "data")
        else:
            data = {'_id': 'data', 'data': {
                'intents': dict,
                'entities': dict
            }}
            self.trainings_data = self.trainer_db.create_document(data)

        if not Document(self.trainer_db, 'notFoundSentence').exists():
            self.trainer_db.create_document({'_id': 'notFoundSentence', 'sentences': []})

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
        self.trainings_data['data'] = data
        self.trainings_data.save()

    def get_trainings_data(self):
        return self.trainings_data['data']

    def save_trainings_data(self):
        self.trainings_data.save()

    def create_intent(self, name, intent):
        intents = self.get_intents()
        success = False
        if name not in intents:
            intents[name] = intent
            self.save_trainings_data()
            success = True
        return success

    def get_intents(self):
        data = self.get_trainings_data()
        return data['intents']

    def get_entities(self):
        data = self.get_trainings_data()
        return data['entities']

    def create_entity(self, name, entity):
        entities = self.get_entities()
        success = False
        if name not in entities:
            entities[name] = entity
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

    def get_trainings_data(self):


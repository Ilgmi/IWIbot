from cloudant.document import Document
from cloudant.database import CloudantDatabase
import sys


class DatabaseContext:
    trainings_data = dict()

    entity_key = 'entity_'
    intent_key = 'intent_'

    def __init__(self, client):
        self.client = client
        self.trainer_db = client["trainer"]

    def doc_exist(self, key):
        return Document(self.trainer_db, key).exists()

    def create_doc(self, doc_id, key, value, data_type):
        if not self.doc_exist(doc_id):
            doc = dict([('_id', doc_id), ('key', key), ('value', value), ('type', data_type)])
            self.trainer_db.create_document(doc)
            return True
        else:
            return False

    def save_doc(self, doc: Document, key, value):
        doc.fetch()
        doc['key'] = key
        doc['value'] = value
        doc.save()

    def get_doc(self, doc_id):
        return Document(self.trainer_db, doc_id)

    def add_not_found_sentence(self, sentence):

        if not self.doc_exist('sentences'):
            self.create_doc('sentences', 'sentences', [], 'not_found')

        doc = self.get_doc('sentences')
        if 'value' not in doc:
            doc['value'] = list()
        values = list(doc['value'])
        values.append(sentence)
        self.save_doc(doc, 'sentences', values)

    def get_sentences(self):
        doc = self.get_doc('sentences')
        doc.fetch()
        print(doc)
        if 'value' in doc:
            return doc['value']
        else:
            return list()

    def update_sentences(self, sentences):
        doc = self.get_doc('sentences')
        print(sentences)
        self.save_doc(doc, 'sentences', sentences)
        return self.get_sentences()

    def log(self, value):
        print(value, file=sys.stderr)

    def get_docs_values(self, selector):
        result_list = dict()
        docs = self.trainer_db.get_query_result(selector)
        for doc in docs:
            if 'key' in doc and 'value' in doc:
                result_list[doc['key']] = doc['value']
        self.log(docs)
        return result_list

    def get_intents(self):
        selector = {'type': {'$eq': 'intent'}}
        return self.get_docs_values(selector)

    def get_intent(self, name):
        doc_id = self.intent_key + name
        if self.doc_exist(doc_id):
            return self.get_doc(doc_id)[name]
        else:
            return dict()

    def get_entities(self):
        selector = {'type': {'$eq': 'entity'}}
        return self.get_docs_values(selector)

    def get_entity(self, name):
        doc_id = self.entity_key + name
        if self.doc_exist(doc_id):
            return self.get_doc(doc_id)[name]
        else:
            return dict()

    def create_entity(self, name, entity):
        return self.create_doc(self.entity_key + name, name, entity, 'entity')

    def create_intent(self, name, intent):
        return self.create_doc(self.intent_key + name, name, intent, 'intent')

    def update_doc(self, doc_id, key, value):
        success = False
        if self.doc_exist(doc_id):
            doc = self.get_doc(doc_id)
            self.save_doc(doc, key, value)
            success = True
        return success

    def update_intent(self, name, intent):
        return self.update_doc(self.intent_key + name, name, intent)

    def update_entity(self, name, entity):
        return self.update_doc(self.entity_key + name, name, entity)

    def delete_doc(self, key):
        if self.doc_exist(key):
            doc = self.get_doc(key)
            doc.fetch()
            doc.delete()
            return True
        else:
            return False

    def delete_intent(self, name):
        return self.delete_doc(self.intent_key + name)

    def delete_entity(self, name):
        return self.delete_doc(self.entity_key + name)

    def get_trainings_data(self):
        intents = self.get_intents()
        entities = self.get_entities()
        data = {
            'intents': intents,
            'entities': entities,
            'language': 'en'
        }

        return data

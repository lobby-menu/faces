from pymongo import MongoClient

class FaceDatabase:
    def __init__(self, **kwargs):
        self.connection_string = kwargs.get('connection_string', '')
        self.database_name = kwargs.get('database', 'facesdatabase')
        self.client = MongoClient(self.connection_string)
        self.database = self.client[self.database_name]

        self.faces =  self.database.faces
        self.people = self.database.people
        self.originals = self.database.originals
        pass

    def insert_face_with_represehtation(self, reps, metadata):
        return self.faces.insert_one({ 'metadata': metadata, 'reps': reps }).inserted_id

    def get_face_representation(self, id):
        return self.faces.find_one({ "_id": id })

    def add_relation(self, person_id, face_ids):
        pass
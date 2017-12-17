from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

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

    def insert_face_with_represehtation(self, reps, metadata, extra=None):
        return self.faces.insert_one({
            'metadata': metadata,
            'reps': reps,
            'creation_date': datetime.utcnow(),
            'extra': extra if extra is not None else {}
        }).inserted_id

    def insert_original_with_faces(self, original_meta, faces):
        return self.originals.insert_one({
            'metadata': original_meta,
            'faces': faces,
            'creation_date': datetime.utcnow()
        }).inserted_id

    def get_face_representation(self, id):
        return self.faces.find_one({ "_id": ObjectId(id) })

    def get_face_metadata(self, id):
        return self.faces.find_one({ "_id": ObjectId(id) }, { '_id': 0, 'metadata': 1, 'creation_date': 1, 'extra': 1 })

    def add_relation(self, person_id, face_ids):
        pass
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

def convertToIdArray(strIds):
    return map(lambda str_id: ObjectId(str_id), strIds)

class FaceDatabase:
    def __init__(self, **kwargs):
        self.connection_string = kwargs.get('connection_string', '')
        self.database_name = kwargs.get('database', 'lobbyface')
        self.client = MongoClient(self.connection_string)
        self.database = self.client[self.database_name]

        self.faces =  self.database.faces
        self.people = self.database.people
        self.originals = self.database.originals
        pass

    def __set_faces_person(self, face_ids, person_id):
        return self.faces.update_many({ '_id': { '$in': face_ids }}, { '$set': { 'person': person_id }})

    def get_original(self, id):
        return self.originals.find_one({ "_id": ObjectId(id) })

    def get_person(self, id):
        return self.people.find_one({ "_id": ObjectId(id) })

    def get_faces(self, face_ids):
        faces = convertToIdArray(face_ids)
        return self.faces.find({ "_id": { "$in": faces }})

    def set_faces_for_original(self, original_id, face_ids):
        faces = convertToIdArray(face_ids)
        return self.originals.update_one({ "_id": ObjectId(original_id) }, { '$set': { 'faces': faces }})

    def insert_face_with_representation(self, reps, metadata, original_id, extra=None):
        return self.faces.insert_one({
            'metadata': metadata,
            'reps': reps,
            'creation_date': datetime.utcnow(),
            'original': original_id,
            'extra': extra if extra is not None else {}
        }).inserted_id

    def insert_original_with_faces(self, original_meta):
        return self.originals.insert_one({
            'metadata': original_meta,
            'creation_date': datetime.utcnow()
        }).inserted_id


    def get_face_representations(self, face_ids):
        ids = convertToIdArray(face_ids)
        return self.faces.find({ '_id': { '$in': ids }}, { '_id': 1, 'reps': 1 })

    def get_labeled_face_representations(self, excludeIds=[]):
        ids = convertToIdArray(excludeIds)
        return self.faces.find(
            {
                'person': { '$exists': True, '$not': { '$size': 0 }},
                '_id': { '$not': { '$in': ids }}
            },
            { '_id': 0, 'person': 1, 'reps': 1 }
        )

    def get_face_metadata(self, id):
        """
        For a single face, gets meta data of it.
        """
        return self.faces.find_one(
            { "_id": ObjectId(id) },
            { '_id': 0, 'metadata': 1, 'creation_date': 1, 'extra': 1, 'person': 1, 'original': 1 }
        )

    def create_person_with_faces(self, face_ids):
        """
        Creates a new person with the given faces.
        :param face_ids: the ids of the faces.
        """
        faces = convertToIdArray(face_ids)
        person_id = self.people.insert_one({
            'creation_date': datetime.utcnow(),
            'update_time': datetime.utcnow(),
            'faces': faces
        }).inserted_id

        updateResult = self.__set_faces_person(faces, person_id)

        if updateResult.acknowledged is False:
            return { 'ok': False, 'reason': "Couldn't set person on faces." }

        return { 'ok': True, 'person': str(person_id) }

    def add_relation(self, person_id, face_ids, clean_previous=False):
        """
        Given a person id and a list of face ids, creates a relation between them.

        :param person_id: the person to attach the faces to.
        :param clean_previous: to clean the previous relations of faces or not
        :param face_ids: the ids of the faces.
        :return:
        """
        faces = convertToIdArray(face_ids)

        if clean_previous:
            # TODO: implement clearing the previous person relations from the face_ids
            pass

        updateResult = self.people.update_one(
            { '_id': ObjectId(person_id) },
            {
                '$addToSet': { 'faces': { '$each': faces }},
                '$set': { 'update_time': datetime.utcnow() }
            }
        )

        if updateResult.acknowledged is False:
            return { 'ok': False, 'reason': "Couldn't add faces to person." }

        updateResult = self.__set_faces_person(faces, ObjectId(person_id))

        if updateResult.acknowledged is False:
            return { 'ok': False, 'reason': "Couldn't set person on faces." }

        return { 'ok': True, 'person': person_id }

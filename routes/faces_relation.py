def faces_relation(database, face_ids, person_id=None):
    if person_id is None:
        return database.create_person_with_faces(face_ids)
    else:
        return database.add_relation(person_id, face_ids)

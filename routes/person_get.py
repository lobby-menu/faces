from faces_get import map_face_result_to_obj


def person_get(storage, database, person_id):
    result = database.get_person(person_id)
    person_id = result.get('_id', '')
    faces = database.get_faces(result.get('faces', []))

    return {
        'id': str(person_id),
        'faces': list(map(lambda face_meta: map_face_result_to_obj(storage, str(face_meta['_id']), face_meta), faces))
    }

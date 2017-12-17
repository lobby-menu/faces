from faces_get import mapFaceResultToObj

def person_get(storage, database, id):
    result = database.get_person(id)
    id = result.get('_id', '')
    faces = database.get_faces(result.get('faces', []))

    return {
        'id': str(id),
        'faces': list(map(lambda faceMeta: mapFaceResultToObj(storage, str(faceMeta['_id']), faceMeta), faces))
    }

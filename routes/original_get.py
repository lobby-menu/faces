from faces_get import mapFaceResultToObj

def original_get(storage, database, id):
    result = database.get_original(id)
    id = result.get('_id', '')
    original_meta = result.get('metadata', {})
    faces = database.get_faces(result.get('faces', []))

    return {
        'id': str(id),
        'accessible_url': storage.get_user_acessible_url_for_image(original_meta),
        'faces': list(map(lambda faceMeta: mapFaceResultToObj(storage, str(faceMeta['_id']), faceMeta), faces))
    }

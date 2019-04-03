from faces_get import map_face_result_to_obj


def original_get(storage, database, original_id):
    result = database.get_original(original_id)
    original_id = result.get('_id', '')
    original_meta = result.get('metadata', {})
    faces = database.get_faces(result.get('faces', []))

    return {
        'id': str(original_id),
        'accessible_url': storage.get_user_accessible_url_for_image(original_meta),
        'faces': list(map(lambda face_meta: map_face_result_to_obj(storage, str(face_meta['_id']), face_meta), faces))
    }

def map_face_result_to_obj(storage, face_id, meta):
    accessible_url = storage.get_user_accessible_url_for_image(meta.get('metadata', {}))
    extra = meta.get('extra', {})
    original = meta.get('original', "")
    creation_date = meta.get('creation_date', None)

    return {
        'id': face_id,
        'accessible_url': accessible_url,
        'creation_date': creation_date,
        'original': str(original),
        'extra': extra
    }


def faces_get(storage, database, face_id):
    meta = database.get_face_metadata(face_id)

    if meta is None:
        return meta

    return map_face_result_to_obj(storage, face_id, meta)

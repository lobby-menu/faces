def mapFaceResultToObj(storage, id, meta):
    accessible_url = storage.get_user_acessible_url_for_image(meta.get('metadata', {}))
    extra = meta.get('extra', {})
    original = meta.get('original', "")
    creation_date = meta.get('creation_date', None)

    return {
        'id': id,
        'accessible_url': accessible_url,
        'creation_date': creation_date,
        'original': str(original),
        'extra': extra
    }

def faces_get(storage, database, id):
    meta = database.get_face_metadata(id)

    if meta is None:
        return meta

    return mapFaceResultToObj(storage, id, meta)

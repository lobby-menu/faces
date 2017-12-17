def faces_get(storage, database, id):
    meta = database.get_face_metadata(id)

    if meta is None:
        return meta

    accessible_url = storage.get_user_acessible_url_for_image(meta.get('metadata', {}))
    extra = meta.get('extra', {})
    creation_date = meta.get('creation_date', None)

    return {
        'id': id,
        'accessible_url': accessible_url,
        'creation_data': creation_date,
        'extra': extra
    }


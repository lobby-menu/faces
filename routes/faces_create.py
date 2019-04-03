from image_utils import read_rgb_image, snap_rectangle, rgb_to_png_bytes


def faces_create(storage, face_ops, database, temp_path):
    # TODO: remove copy if not necessary.
    original_meta = storage.upload_original_image(temp_path, True)
    original_image_rgb = read_rgb_image(temp_path)
    if original_image_rgb is None:
        return None
    original_database_id = database.insert_original_with_faces(original_meta)

    faces = face_ops.find_faces(original_image_rgb)
    if faces is None or len(faces) == 0:
        return None
    face_ids, face_results = [], []
    for rect in faces:
        face_image = snap_rectangle(original_image_rgb, rect)
        aligned_face = face_ops.align(face_image)
        if aligned_face is None:
            continue
        reps = face_ops.extract(aligned_face)

        # Write the image to disk, get the metadata for accessing it later.
        face_meta = storage.write_face_image(rgb_to_png_bytes(aligned_face))
        # Insert face representation and metadata into database.
        # TODO: maybe send some extra data to database aswell?
        database_id = database.insert_face_with_representation(list(reps), face_meta, original_database_id)

        left, top = rect[0]
        width, height = rect[1]
        face_ids.append(database_id)
        face_results.append({
            'id': str(database_id),
            'accessible_url': storage.get_user_accessible_url_for_image(face_meta),
            'position': {'left': left, 'top': top, 'width': width, 'height': height}
        })

    database.set_faces_for_original(original_database_id, face_ids)
    return {
        'id': str(original_database_id),
        'accessible_url': storage.get_user_accessible_url_for_image(original_meta),
        'faces': face_results
    }

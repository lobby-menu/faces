from image_utils import readRGBImage, snapRectangle, rgbToPNGBytes

def faces_create(storage, faceOps, database, temp_path):
    # TODO: remove copy if not necessary.
    original_meta = storage.upload_original_image(temp_path, True)
    originalImageRGB = readRGBImage(temp_path)
    if originalImageRGB is None:
        return None
    original_database_id = database.insert_original_with_faces(original_meta)

    faces = faceOps.find_faces(originalImageRGB)
    if faces is None or len(faces) == 0:
        return None
    faceIds, faceResults = [], []
    for rect in faces:
        faceImage = snapRectangle(originalImageRGB, rect)
        alignedFace = faceOps.align(faceImage)
        if alignedFace is None:
            continue
        reps = faceOps.extract(alignedFace)

        # Write the image to disk, get the metadata for accessing it later.
        face_meta = storage.write_face_image(rgbToPNGBytes(alignedFace))
        # Insert face representation and metadata into database.
        # TODO: maybe send some extra data to database aswell?
        database_id = database.insert_face_with_representation(list(reps), face_meta, original_database_id)

        left, top = rect[0]
        width, height = rect[1]
        faceIds.append(database_id)
        faceResults.append({
            'id': str(database_id),
            'accessible_url': storage.get_user_acessible_url_for_image(face_meta),
            'position': { 'left': left, 'top': top, 'width': width, 'height': height }
        })

    database.set_faces_for_original(original_database_id, faceIds)
    return {
        'id': str(original_database_id),
        'accessible_url': storage.get_user_acessible_url_for_image(original_meta),
        'faces': faceResults
    }
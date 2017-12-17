from image_utils import readRGBImage, snapRectangle, rgbToPNGBytes

def faces_create(storage, faceOps, database, temp_path):
    # TODO: remove copy if not necessary.
    original_meta = storage.upload_original_image(temp_path, True)
    originalImageRGB = readRGBImage(temp_path)

    faces = faceOps.find_faces(originalImageRGB)
    faceIds, faceResults = [], []
    for rect in faces:
        faceImage = snapRectangle(originalImageRGB, rect)
        alignedFace = faceOps.align(faceImage)
        reps = faceOps.extract(alignedFace)

        # Write the image to disk, get the metadata for accessing it later.
        face_meta = storage.write_face_image(rgbToPNGBytes(alignedFace))
        # Insert face representation and metadata into database.
        # TODO: maybe send some extra data to database aswell?
        database_id = database.insert_face_with_represehtation(list(reps), face_meta)

        left, top = rect[0]
        width, height = rect[1]
        faceIds.append(database_id)
        faceResults.append({
            'id': str(database_id),
            'position': { 'left': left, 'top': top, 'width': width, 'height': height }
        })

    original_database_id = database.insert_original_with_faces(original_meta, faceIds)
    return { 'id': str(original_database_id), 'faces': faceResults }
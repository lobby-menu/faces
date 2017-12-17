def faces_identify(database, faceOps, face_ids, grouping=True):
    # get face representations and group them
    faces = list(database.get_face_representations(face_ids))
    groups = faceOps.group(map(lambda face: face['reps'], faces)) if grouping else [0] * len(faces)
    groupScores = list(map(lambda _: { 'faces': [], 'scores': {} }, range(0, max(groups) + 1)))

    for idx, group in enumerate(groups):
        face = faces[idx]
        groupScore = groupScores[group]

        groupScore['faces'].append(str(face['_id']))


    for faceToCompare in database.get_labeled_face_representations(face_ids):
        person = str(faceToCompare['person'])

        for idx, face in enumerate(faces):
            # TODO: you can have a better algorithm that stops comaring after going over some treshold for some face/person pair.
            compareResult = faceOps.compare(faceToCompare['reps'], face['reps'])
            groupScore = groupScores[groups[idx]]

            if person not in groupScore['scores']:
                groupScore['scores'][person] = { 'average': 0, 'count': 0 }
            personScore = groupScore['scores'][person]

            personScore['average'] += compareResult
            personScore['count'] += 1

    for groupScore in groupScores:
        scores = []

        # Divide each score by the compare count, and each compare count by the face count to achieve the good results.
        for person in groupScore['scores']:
            score = groupScore['scores'][person]

            scores.append({
                'person': person,
                'average': score['average'] / score['count'],
                'count': score['count'] / len(groupScore['faces'])
            })

        scores.sort(key=lambda score: score['average'])
        groupScore['scores'] = scores

    return groupScores
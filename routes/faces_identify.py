def faces_identify(database, face_ops, face_ids, grouping=True):
    # get face representations and group them
    faces = list(database.get_face_representations(face_ids))
    groups = face_ops.group(map(lambda f: f['reps'], faces)) if grouping else [0] * len(faces)
    group_scores = list(map(lambda _: {'faces': [], 'scores': {}}, range(0, max(groups) + 1)))

    # For each group, add faces to them
    for idx, group in enumerate(groups):
        face = faces[idx]
        group_score = group_scores[group]

        group_score['faces'].append(str(face['_id']))

    # Calculate similarity scores for each person's face and our grouped faces.
    for face_to_compare in database.get_labeled_face_representations(face_ids):
        person = str(face_to_compare['person'])

        for idx, face in enumerate(faces):
            # TODO: you can have a better algorithm that stops comparing after going over some threshold
            compare_result = face_ops.compare(face_to_compare['reps'], face['reps'])
            group_score = group_scores[groups[idx]]

            if person not in group_score['scores']:
                group_score['scores'][person] = {'average': 0, 'count': 0}
            person_score = group_score['scores'][person]

            person_score['average'] += compare_result
            person_score['count'] += 1

    # group and sort scores per person per group.
    for group_score in group_scores:
        scores = []

        # Divide each score by the compare count, and each compare count by the face count to achieve the good results.
        for person in group_score['scores']:
            score = group_score['scores'][person]

            scores.append({
                'person': person,
                'average': score['average'] / score['count'],
                'count': score['count'] / len(group_score['faces'])
            })

        scores.sort(key=lambda s: s['average'])
        group_score['scores'] = scores

    return group_scores

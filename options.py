imgDim = 96
options = {
    'database': {
        'connection_string': 'mongodb://172.17.0.1:27017',
        'database': 'lobbyface'
    },
    'storage': {
        'path': 'uploads',
        'host': 'http://localhost:8080'
    },
    'face': {
        'model_directory': '/root/openface/models',
        'prefered_img_dim': imgDim,
        'align': {
            'algorithm': 'dlib',
            'model': 'dlib/shape_predictor_68_face_landmarks.dat',
        },
        'feature': {
            'model': 'openface/nn4.small2.v1.t7',
            'options': {
                'imgDim': imgDim,
                'cuda': False
            }
        }
    }
}
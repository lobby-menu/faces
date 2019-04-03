from os import getenv

img_dim = 96
options = {
    'database': {
        'connection_string': getenv('FACE_DATABASE_CONNECTION_STRING', 'mongodb://172.17.0.1:27017'),
        'database': getenv('FACE_DATABASE_NAME', 'lobbyface')
    },
    'storage': {
        'path': getenv('STORAGE_PATH', 'uploads'),
        'host': getenv('STORAGE_BASE_URL', 'http://localhost:8080')
    },
    'face': {
        'model_directory': '/root/openface/models',
        'prefered_img_dim': img_dim,
        'align': {
            'algorithm': 'dlib',
            'model': 'dlib/shape_predictor_68_face_landmarks.dat',
        },
        'feature': {
            'model': 'openface/nn4.small2.v1.t7',
            'options': {
                'imgDim': img_dim,
                'cuda': False
            }
        }
    }
}

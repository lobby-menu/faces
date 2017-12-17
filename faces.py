import os
from options import options
from flask import Flask, request, jsonify, send_from_directory
from operations import FaceOperations
from database import FaceDatabase
from storage import FaceStorage
from uuid import uuid4
from image_utils import readRGBImage, snapRectangle, rgbToPNGBytes

app = Flask(__name__, static_url_path='/')

@app.route('/uploads/<path:path>')
def send_files(path):
    return app.send_static_file(os.path.join('uploads', path))

faceOps = FaceOperations(**options.get('face', {}))
database = FaceDatabase(**options.get('database', {}))
storage = FaceStorage(**options.get('storage', {}))

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/faces/create', methods=['POST'])
def faces_create():
    # TODO: make sure its or jpeg.
    imageFile = request.files['image']
    if imageFile is None:
        raise InvalidUsage("No image is sent with the request.")

    temp_path = "/tmp/" + str(uuid4()) + ".png"
    imageFile.save(temp_path)
    # TODO: Save the original photo with the face information?
    original_meta = storage.upload_original_image(temp_path, True)
    original_meta['faces'] = []
    originalImageRGB = readRGBImage(temp_path)

    faces = faceOps.find_faces(originalImageRGB)
    for rect in faces:
        faceImage = snapRectangle(originalImageRGB, rect)
        alignedFace = faceOps.align(faceImage)
        reps = faceOps.extract(alignedFace)

        face_meta = storage.write_face_image(rgbToPNGBytes(alignedFace))
        original_meta['faces'].append(face_meta)
        # TODO: save reps and face_meta

    return jsonify(original_meta)

if __name__ == '__main__':

    app.run(host="0.0.0.0")

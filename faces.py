import os
from options import options
from flask import Flask, request, jsonify
from flask_cors import CORS
from operations import FaceOperations
from database import FaceDatabase
from storage import FaceStorage
from uuid import uuid4
from routes.faces_create import faces_create
from routes.faces_get import faces_get
from routes.faces_relation import faces_relation
from routes.faces_identify import faces_identify
from routes.original_get import original_get
from routes.person_get import person_get


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


app = Flask(__name__, static_url_path='/')
CORS(app)


@app.route('/uploads/<path:path>')
def send_files(path):
    return app.send_static_file(os.path.join('uploads', path))


server_options = options.get('server', {})
face_ops = FaceOperations(**options.get('face', {}))
database = FaceDatabase(**options.get('database', {}))
storage = FaceStorage(**options.get('storage', {}))


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def hello_world():
    return 'Hello World!'


def get_file_extension(file_path):
    split = file_path.rsplit('.', 1)
    return None if len(split) < 2 else split[1].lower()


@app.route('/faces/create', methods=['POST'])
def faces_create_route():
    image_file = request.files['image']
    if image_file is None:
        raise InvalidUsage("No image is sent with the request.")

    extension = get_file_extension(image_file.filename)
    if extension not in ["png", "jpeg", "jpg"]:
        raise InvalidUsage("Expected to find png, jpeg or jpg file.")

    temp_path = "/tmp/" + str(uuid4()) + "." + extension
    image_file.save(temp_path)
    result = faces_create(storage, face_ops, database, temp_path)

    if result is None:
        raise InvalidUsage("An invalid response returned by the server. Probably no face detected.", 406)
    return jsonify(result)


@app.route('/faces/<face_id>', methods=['GET'])
def faces_get_route(face_id):
    result = faces_get(storage, database, face_id)
    if result is None:
        raise InvalidUsage("Wrong id number.", 404)
    return jsonify(result)


@app.route('/originals/<original_id>', methods=['GET'])
def originals_get_route(original_id):
    result = original_get(storage, database, original_id)
    if result is None:
        raise InvalidUsage("Wrong id number.", 404)
    return jsonify(result)


@app.route('/person/<person_id>', methods=['GET'])
def person_get_route(person_id):
    result = person_get(storage, database, person_id)
    if result is None:
        raise InvalidUsage("Wrong id number.", 404)
    return jsonify(result)


@app.route('/faces/relation', methods=['POST'])
def faces_relation_route():
    data = request.get_json()
    if data is None or 'faces' not in data:
        raise InvalidUsage("This endpoint requires data in json format to be posted. With faces key.")
    faces = data.get('faces', [])
    person = data.get('person', None)

    return jsonify(faces_relation(database, faces, person))


@app.route('/faces/identify', methods=['POST'])
def faces_identify_route():
    data = request.get_json()
    if data is None or 'faces' not in data:
        raise InvalidUsage("This endpoint requires data in json format to be posted. With faces key.")
    faces = data.get('faces', [])
    grouping = data.get('grouping', True)

    return jsonify(faces_identify(database, face_ops, faces, grouping is not False))


if __name__ == '__main__':
    app.run(**server_options)

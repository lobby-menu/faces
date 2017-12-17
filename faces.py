from options import options
from flask import Flask
from operations import FaceOperations
from database import FaceDatabase

app = Flask(__name__)
faceOps = FaceOperations(**options.get('face', {}))
database = FaceDatabase(**options.get('database', {}))

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':

    app.run(host="0.0.0.0")

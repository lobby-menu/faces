# Extracts features from a given image.
# Does things like finding faces in a given image, extracting a one dimensional array for the given face.
# also group
from sklearn import cluster
import os
import cv2
import scipy
import openface

def map_rectangle_to_tuple(rect):
    if rect is None:
        return None
    return ((rect.left(), rect.top()), (rect.width(), rect.height()))

class FaceOperations:
    def __init__(self, **options):
        models_path = options.get('model_directory', '/')
        align_options = options.get('align', {})
        dlib_model_path = os.path.join(
            models_path,
            align_options.get(
                'model',
                'dlib/shape_predictor_68_face_landmarks.dat'
            )
        )
        self.init_align(dlib_model_path, align_options.get('options', {}))


        feature_options = options.get('feature', {})
        of_model_path = os.path.join(
            models_path,
            feature_options.get(
                'model',
                'openface/nn4.small2.v1.t7'
            )
        )
        self.init_feature(of_model_path, feature_options.get('options', {}))

        self.cluster_options = options.get('cluster', { 'threshold': 0.35, 'n_clusters': None })

    def init_align(self, align_model_path, options):
        self.__align = openface.AlignDlib(align_model_path, **options)

    def init_feature(self, of_model_path, options):
        self.net = openface.TorchNeuralNet(of_model_path, **options)

    # Finds faces in the given image, returns middle points and sizes of them.
    # the returned list of tuples are in the format: [((left, top), (width, height))]
    def find_faces(self, image, multiple=True):
        if multiple:
            return list(map(map_rectangle_to_tuple, self.__align.getAllFaceBoundingBoxes(image)))
        else:
            bb = map_rectangle_to_tuple(self.__align.getLargestFaceBoundingBox(image))
            return None if bb is None else [bb]

    def align(self, image, imgDim=96, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE):
        return self.__align.align(
            imgDim,
            image,
            landmarkIndices = landmarkIndices
        )

    # Extracts 128d vector of the given face. Having the property of, when comparing two faces, you will have
    # closer euclidian distance between their features.
    def extract(self, image):
        return self.net.forward(image)

    # Returns a numerical value by comparing the features of two faces.
    # Lower the value, higher the chance that two faces belong to the same person.
    def compare(self, first, second):
        return scipy.spatial.distance.cosine(first, second)

    # Returns list of numbers that represent which group the face in the input array belongs to.
    # Groups are dynamically created according to the input data with a treshold.
    # Given a list of 128d face representations, groups each of the reps.
    def group(self, reps):
        birch = cluster.Birch(**self.cluster_options)
        return birch.fit_predict(reps)

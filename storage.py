from uuid import uuid4
import urlparse
import os
from shutil import copyfile


class FaceStorage:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host', '')
        self.upload_path = kwargs.get('path', 'uploads')
        self.full_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'static', self.upload_path
        )

    def __create_file_descriptors(self, extension=".png"):
        filename = str(uuid4()) + extension
        full_path = os.path.join(self.full_path, filename)

        return filename, full_path

    def __write_image(self, image):
        filename, full_path = self.__create_file_descriptors()

        with open(full_path, 'wb') as file_handle:
            file_handle.write(image)
            file_handle.close()

        return {'name': filename}

    def write_face_image(self, image):
        """
        Writes a given face to the storage backend for further access.

        :param image: bytes of the image to be written. considered png.
        :return: metadata on how to create access url for user. Save this.
        """
        return self.__write_image(image)

    def write_original_image(self, image):
        """
        Writes a given original image, to the storage backend.

        :param image: bytes of the image to be written. considered png.
        :return: metadata on how to create access url for user. Save this.
        """
        return self.__write_image(image)

    def upload_original_image(self, path, copy=False):
        extension = os.path.splitext(path)[1]
        filename, full_path = self.__create_file_descriptors(extension)

        if copy:
            copyfile(path, full_path)
        else:
            os.rename(path, full_path)

        return {'name': filename}

    def get_user_accessible_url_for_image(self, metadata):
        upload_url = urlparse.urljoin(self.host, self.upload_path)
        return urlparse.urljoin(upload_url + '/', metadata['name'])

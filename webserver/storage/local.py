import datetime
import os

from werkzeug.utils import secure_filename


class LocalStorage:

    TIMESTAMP = "%Y-%m-%dT%H:%M:%S"

    def __init__(self):
        pass

    @staticmethod
    def now():
        return datetime.datetime.utcnow().strftime(LocalStorage.TIMESTAMP)

    def save_file(self, file, root, add_timestamp=True):
        """
        Saves a file object in the root folder
        :param file:
        :param root:
        :param add_timestamp:
        :return full_path str:
        """

        filename = file.filename
        full_path = os.path.join(root, filename)

        if add_timestamp:
            filename = self.now() + '_' + filename

        # make sure file name is ok
        secure_filename(filename)

        # save the file locall and return the path
        file.save(full_path)

        return full_path

    def save_folder(self, source, dest):
        pass

    def get_file(self, remote_path):
        pass

    def get_folder(self, remote_path):
        pass
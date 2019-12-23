import ntpath
import os

from cloud_storage_client import storage
from utils.utils import from_env, get_root


class CloudStorage:

    def __init__(self):

        self.client = storage.StorageClient(
            from_env('STORAGE_PROVIDER', "GCS"),
            # GOOGLE_CLOUD_STORAGE = 'GCS', AMAZON_S3 = 'S3', AZURE_BLOB_STORAGE = 'ABS'
            from_env('STORAGE_BUCKET_NAME', "accent-bot-models"),
            # For geshet account
            from_env('STORAGE_ACCESS_KEY', "GOOG1EM6OWXWJMJQZP6DENNCJB62GGTSH3UZJ3TYTXLDOS3QXSIUFI2VEI3VA"),
            from_env('STORAGE_SECRET_KEY', "A94hpcFfAb4ddfbEbeLo96pTJ2Vnt7x3f5RsNmwM")
        )

    @staticmethod
    def _get_status(status):
        return "failure" if int(status) == 1 else "success"

    @staticmethod
    def _uploads_folder():
        return "uploads"

    @staticmethod
    def _dataset_folder():
        return "dataset"

    @staticmethod
    def _models_folder():
        return "models"

    @staticmethod
    def _base_name(source):
        return ntpath.basename(source)

    def load_model(self, model_type, model_num):

        # set the bucket path
        model_path = "/".join((self._models_folder(),
                               model_type, model_num))

        # set the local path
        dest_path = os.path.join(get_root(), "saved_models",
                                 model_type, model_num)

        # get the file
        self.client.download_file(model_path, "model.h5", dest_path)

        return os.path.join(dest_path, "model.h5")

    def upload_prediction(self, source, model_type, model_num, status):
        dest_path = "/".join((self._uploads_folder(),
                              model_type,
                              model_num,
                              self._get_status(status),
                              self._base_name(source)))
        self.client.upload_file(source, dest_path)

    def upload_wav(self, source):
        dest_path = "/".join((self._dataset_folder(),
                              self._base_name(source)))
        self.client.upload_file(source, dest_path)

    def save_file(self, source, dest):
        pass

    def save_models_folder(self, source, exp_type, exp_id):

        dest = "/".join((self._models_folder(), exp_type, exp_id))

        self.client.upload_folder(dest, source)

    def get_file(self, remote_path):
        pass

    def get_folder(self, remote_path):
        pass


# test cloud
if __name__ == "__main__":

    storage = CloudStorage()
    storage.upload_prediction(source="/tmp/text.txt",
                              model="usa_speakers_only",
                              status=1)


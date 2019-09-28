import ntpath
import os
from cloud_storage_client import storage

import gswrap

# storage_client = storage.Client.from_service_account_json(os.path.join(get_root(),
#                                                                        'creds.json'))
from utils.utils import get_root, from_env


class CloudStorage:

    def __init__(self):

        self.client = storage.StorageClient(
            from_env('STORAGE_PROVIDER', "GCS"),
            # GOOGLE_CLOUD_STORAGE = 'GCS', AMAZON_S3 = 'S3', AZURE_BLOB_STORAGE = 'ABS'
            from_env('STORAGE_BUCKET_NAME', "accent-models"),
            from_env('STORAGE_ACCESS_KEY', "GOOG1EUKXA2YGGFNU55LZZNUDPUUELFJ4RYERL5NFYO4R6EXT6NTBAP3VZB6I"),
            from_env('STORAGE_SECRET_KEY', "hA5nTOouw/u59yWBq/XcBuL6BhEkfJAiIvqFoxzu")
        )

    @staticmethod
    def _get_status(status):
        return "failure" if status else "success"

    @staticmethod
    def _uploads_folder():
        return "uploads"

    @staticmethod
    def _base_name(source):
        return ntpath.basename(source)

    def upload_prediction(self, source, model, status):
        dest_path = "/".join((self._uploads_folder(),
                              model,
                              self._get_status(status),
                              self._base_name(source)))
        self.client.upload_file(source, dest_path)

    def save_file(self, source, dest):
        pass

    def save_folder(self, source, dest):
        pass

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


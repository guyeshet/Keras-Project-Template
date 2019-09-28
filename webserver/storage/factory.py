from webserver.storage.cloud import CloudStorage
from webserver.storage.local import LocalStorage

DEFAULT = "default"
CLOUD = "cloud"
LOCAL = "local"

cloud_storage = CloudStorage()


class StorageFactory:
    """
    A factory class that generates search engines
    """

    @staticmethod
    def default(engine_type=DEFAULT):

        if engine_type == DEFAULT:
            return cloud_storage
        elif engine_type == CLOUD:
            return cloud_storage
        elif engine_type == LOCAL:
            return LocalStorage()

    @staticmethod
    def cloud():
        return cloud_storage

    @staticmethod
    def local():
        return LocalStorage()

from webserver.storage.cloud import CloudStorage
from webserver.storage.local import LocalStorage

DEFAULT = "default"
CLOUD = "cloud"
LOCAL = "local"


class StorageFactory:
    """
    A factory class that generates search engines
    """

    @staticmethod
    def default(engine_type=DEFAULT):

        if engine_type == DEFAULT:
            return CloudStorage()
        elif engine_type == CLOUD:
            return CloudStorage()
        elif engine_type == LOCAL:
            return LocalStorage()

    @staticmethod
    def cloud():
        return CloudStorage()

    @staticmethod
    def local():
        return LocalStorage()

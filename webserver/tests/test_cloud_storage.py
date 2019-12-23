
from webserver.storage.factory import StorageFactory

def test_connect_to_cloud_storage():

    storage = StorageFactory.cloud()
    print(storage)


test_connect_to_cloud_storage()
from m2x.v2.resource import Resource
from m2x.v2.devices import Device
from m2x.v2.metadata import Metadata


class CollectionDevice(Device):
    COLLECTION_PATH = 'collections/{collection_id}/devices'


# Wrapper for AT&T M2X Collections API
# https://m2x.att.com/developer/documentation/v2/collections
class Collection(Resource, Metadata):
    COLLECTION_PATH = 'collections'
    ITEM_PATH = 'collections/{id}'
    ITEMS_KEY = 'collections'

    def devices(self, **params):
        return CollectionDevice.list(self.api, collection_id=self.id, **params)

    def add_device(self, device_id):
        path = self.subpath('/devices/{device_id}'.format(device_id=device_id))
        return self.api.put(path)

    def remove_device(self, device_id):
        path = self.subpath('/devices/{device_id}'.format(device_id=device_id))
        return self.api.delete(path)

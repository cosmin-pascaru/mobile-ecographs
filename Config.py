from Singleton import Singleton


class Config(metaclass=Singleton):

    __MAPS_API_KEY_PATH = 'data/googleapi_key.txt'

    def __init__(self):
        with open(Config.__MAPS_API_KEY_PATH) as key_file:
            self._maps_api_key = key_file.read().strip()

    def get_maps_api_key(self):
        return self._maps_api_key

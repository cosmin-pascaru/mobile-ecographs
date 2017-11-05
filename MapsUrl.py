import urllib

import copy
import requests

from Singleton import Singleton


class MapsUrl(metaclass=Singleton):
    def __init__(self):
        pass

    def generate_from(self, arr):
        assert len(arr) >= 2

        arr = copy.deepcopy(arr)
        arr = [requests.utils.quote(s) for s in arr]

        print(arr)

        begin = r'https://www.google.com/maps/dir/?api=1&'

        origin = 'origin=' + arr[0]
        dest = 'destination=' + arr[-1]
        travelmode = 'travelmode=driving'
        waypoints = 'waypoints=' + '|'.join(arr[1:-1])

        args = [origin, dest, waypoints, travelmode]

        url = begin + '&'.join(args)

        return url

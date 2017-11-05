from datetime import datetime
import time
import googlemaps

from Config import Config
from Singleton import Singleton


class MapsApi(metaclass=Singleton):
    __CHUNK_SIZE = 50

    def __init__(self, key=Config().get_maps_api_key()):
        self.__client = googlemaps.Client(key)

    def get_dist_and_times_matrix(self, locations):
        matrix = self._read_previous_matrix()

        next_i = len(matrix)

        try:
            for i in range(next_i, len(locations) - 1):
                new_row = [None for j in range(i + 1)]
                new_row += (self._get_dist_and_times_row(locations[i], locations[i + 1:]))
                matrix.append(new_row)
        except Exception:
            if len(matrix[-1]) < len(locations):
                matrix.pop()
        finally:
            with open('distances.txt', 'w') as f:
                f.write(str(matrix))
            return matrix

    def get_distance_matrix(self, locations):
        pass

    def get_times_matrix(self, locations):
        pass

    def _get_dist_and_times_row(self, start, ends):
        row = []
        chunk_size = self.__CHUNK_SIZE

        for i in range(0, len(ends), chunk_size):
            row = row + self._get_dist_and_times_chunk(start, ends[i:i + chunk_size])

        return row

    def _get_dist_and_times_chunk(self, start, ends):

        if __debug__:
            print('Sending request for chunk...')
            print(start)
            print(ends)

        matrix = self.__client.distance_matrix([start], ends,
                                               mode="driving",
                                               language="ro",
                                               units="metric",
                                               departure_time=datetime.now(),
                                               traffic_model="optimistic")
        time.sleep(1)
        if __debug__:
            print('Received response for chunk.')

        return [matrix['rows'][0]['elements'][j] for j in range(len(ends))]

    @staticmethod
    def get_distance_from_element(element):
        return element['distance']['value']

    @staticmethod
    def get_duration_from_element(element):
        return element['duration']['value']

    def _read_previous_matrix(self):
        try:
            with open('distances.txt') as f:
                return eval(f.read())
        except:
            return []

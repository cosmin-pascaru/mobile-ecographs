from Singleton import Singleton


class NatalityDataReader(metaclass=Singleton):
    def __init__(self):
        pass

    def read(self):
        with open('data/date_natalitate.txt', 'r') as f:
            return [tuple(map(int, x)) for x in map(str.split, f.readlines()) if len(x) >= 2]

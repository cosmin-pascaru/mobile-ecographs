from MapsUrl import MapsUrl
from NatalityDataReader import NatalityDataReader
from ToursFinder import ToursFinder

print(NatalityDataReader().read())
ToursFinder().compute_tours(1, 0.000025)

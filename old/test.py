from NatalityDataReader import NatalityDataReader

from old.ToursFinder import ToursFinder

print(NatalityDataReader().read())
ToursFinder().compute_tours(2, 0.000025)

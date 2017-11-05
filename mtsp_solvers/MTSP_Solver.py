from abc import ABC, abstractmethod


class MTSP_Solver(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def solve(self, distance_matrix, nr_tours, time_limit, tour_limit=float('inf')):
        pass


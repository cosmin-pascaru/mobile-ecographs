from abc import ABC, abstractmethod


class IMtspSolver(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def solve(self, distance_matrix, nr_tours, time_limit):
        pass


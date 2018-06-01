from abc import ABC, abstractmethod


class IMtspSolver(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run_mtsp(self, params):
        pass


from abc import ABC, abstractmethod


class IGreedySolver(ABC):
    def __init__(self):
        pass

    def greedy_run(self):
        while not self._done():
            self._apply_best_option()

    @abstractmethod
    def _done(self):
        pass

    @abstractmethod
    def _apply_best_option(self):
        pass

from abc import ABC, abstractmethod
from src.params.tour_selector_params import TourSelectorParams


class TourSelector(ABC):
    def __init__(self, tours, params : TourSelectorParams):
        self.tours = tours
        self.params = params

    @abstractmethod
    def run(self):
        pass

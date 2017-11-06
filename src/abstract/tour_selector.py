from abc import ABC, abstractmethod

from src.abstract.planner import Planner
from src.params.tour_selector_params import TourSelectorParams


class TourSelector(ABC):
    def __init__(self, tours, params : TourSelectorParams, planner : Planner):
        self.tours = tours
        self.params = params
        self.planner = planner

    @abstractmethod
    def run(self):
        pass



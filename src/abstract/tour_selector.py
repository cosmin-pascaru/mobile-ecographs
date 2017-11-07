from abc import ABC, abstractmethod

from src.abstract.planner import Planner
from src.concrete.planning_manager import Manager
from src.params.tour_selector_params import TourSelectorParams


class TourSelector(ABC):
    def __init__(self, manager: Manager, tours, params : TourSelectorParams, planner : Planner):
        self.manager = manager

        self.tours = tours
        self.params = params
        self.planner = planner

    @abstractmethod
    def run(self):
        pass



from abc import ABC, abstractmethod

from src.abstract.planner import Planner
from src.concrete.planning_manager import Manager
from src.params.constants import MAX_TIME_ON_ROAD
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

    def _filter_too_long_tours(self):
        prev_len = len(self.tours)
        tours = [tour for tour in self.tours if self.manager.compute_tour_distance(tour) <= MAX_TIME_ON_ROAD]

        if self.params.debug:
            print('Filtered {} useless tours!'.format(prev_len - len(tours)))



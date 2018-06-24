from abc import ABC, abstractmethod

from src.alg.abstract.planner import Planner
from src.alg.concrete.planning_manager import Manager
from src.alg.params.tour_selector_params import TourSelectorParams
from src.common.constants import MAX_TIME_ON_ROAD


class TourSelector(ABC):
    def __init__(self, manager: Manager, tours, params : TourSelectorParams, planner : Planner):
        self.manager = manager

        self.tours = tours
        self.params = params
        self.planner = planner

    @abstractmethod
    def run_tour_selector(self):
        pass

    def _filter_too_long_tours(self):
        prev_len = len(self.tours)
        tours = [tour for tour in self.tours if self.manager.compute_tour_distance(tour) <= MAX_TIME_ON_ROAD]

        if self.params.debug:
            print('Filtered {} useless tours!'.format(prev_len - len(tours)))



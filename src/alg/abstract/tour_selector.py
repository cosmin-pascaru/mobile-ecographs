from abc import ABC, abstractmethod

from src.alg.params.tour_selector_params import CTourSelectorParams
from src.alg.abstract.planner import CPlanner
from src.alg.concrete.planning_manager import CManager
from src.alg.params.constants import MAX_TIME_ON_ROAD


class CTourSelector(ABC):
    def __init__(self, manager: CManager, tours, params : CTourSelectorParams, planner : CPlanner):
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



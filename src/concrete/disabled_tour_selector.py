from src.abstract.planner import Planner
from src.abstract.tour_selector import TourSelector
from src.concrete.planning_manager import Manager
from src.params.constants import MAX_TIME_ON_ROAD
from src.params.tour_selector_params import DisabledTourSelectorParams


class DisabledTourSelector(TourSelector):
    def __init__(self, manager: Manager, tours, params: DisabledTourSelectorParams, planner : Planner):
        TourSelector.__init__(self, manager, tours, params, planner)

        self._filter_too_long_tours()
        self.all = [1 for _ in tours]
        self.params = params

    def run(self):
        all_tours = [self.tours[i] for i in range(len(self.tours))]

        for iter_idx in range(self.params.cnt_iterations):
            self.planner.compute_cost(all_tours)


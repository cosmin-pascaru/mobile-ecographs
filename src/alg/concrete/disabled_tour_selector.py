import time

from src.alg.abstract.planner import Planner
from src.alg.abstract.tour_selector import TourSelector
from src.alg.concrete.planning_manager import Manager
from src.alg.params.tour_selector_params import DisabledTourSelectorParams


class DisabledTourSelector(TourSelector):
    def __init__(self, manager: Manager, tours, params: DisabledTourSelectorParams, planner : Planner):
        TourSelector.__init__(self, manager, tours, params, planner)

        self._filter_too_long_tours()
        self.all = [1 for _ in tours]
        self.params = params

    def run_tour_selector(self):
        all_tours = [self.tours[i] for i in range(len(self.tours))]

        if self.params.cnt_iterations:
            for iter_idx in range(self.params.cnt_iterations):
                self.planner.run_planner(all_tours)
        elif self.params.max_time:
            start_time = time.time()
            while time.time() - start_time <= self.params.max_time:
                self.planner.run_planner(all_tours)
        else:
            assert False

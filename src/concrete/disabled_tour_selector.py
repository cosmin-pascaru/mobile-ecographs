from src.abstract.planner import CPlanner
from src.abstract.tour_selector import CTourSelector
from src.concrete.planning_manager import CManager
from src.params.constants import MAX_TIME_ON_ROAD
from src.params.tour_selector_params import CDisabledTourSelectorParams


class CDisabledTourSelector(CTourSelector):
    def __init__(self, manager: CManager, tours, params: CDisabledTourSelectorParams, planner : CPlanner):
        CTourSelector.__init__(self, manager, tours, params, planner)

        self._filter_too_long_tours()
        self.all = [1 for _ in tours]
        self.params = params

    def run_tour_selector(self):
        all_tours = [self.tours[i] for i in range(len(self.tours))]

        for iter_idx in range(self.params.cnt_iterations):
            self.planner.compute_cost(all_tours)


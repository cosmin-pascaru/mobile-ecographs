import random

import copy

from src.abstract.planner import CPlanner
from src.abstract.sa_solver import CSaSolver
from src.abstract.tour_selector import CTourSelector
from src.concrete.planning_manager import CManager
from src.params.constants import MAX_TIME_ON_ROAD
from src.params.tour_selector_params import TourSelectorParams, SSaTourSelectorParams
from src.utils import SECONDS_PER_HOUR


class CSaTourSelector(CTourSelector, CSaSolver):
    def __init__(self, manager: CManager, tours, params: SSaTourSelectorParams, planner : CPlanner):
        CTourSelector.__init__(self, manager, tours, params, planner)
        CSaSolver.__init__(self, params.sa_cooling_rate)

        self.all = None

    def run(self):
        self._filter_too_long_tours()
        self.all = [1 for _ in self.tours]
        self.run_sa(self.params.sa_cooling_rate)

    def _existing_tour_indexes(self, sol):
        return tuple(i for i, x in enumerate(sol) if x)

    def _missing_tour_indexes(self, sol):
        return tuple(i for i, x in enumerate(sol) if x)

    def _get_random_sol(self) -> tuple:
        sol = [random.choice((True, False)) for _ in self.all]

        while sol.count(True) == 0:
            sol = [random.choice((True, False)) for _ in self.all]

        return sol, self._compute_cost(sol)

    def _get_random_neighbour(self, sol) -> tuple:
        new_sol = copy.deepcopy(sol)

        p = random.random()

        if p < 0.5:
            # add element to sol
            new_elem = random.choice(self._missing_tour_indexes(sol))
            new_sol[new_elem] = True
        else:
            # remove element from sol
            old_elem = random.choice(self._existing_tour_indexes(sol))
            new_sol[old_elem] = False

        return new_sol, self._compute_cost(new_sol)

    def _compute_cost(self, sol):
        tours = [self.tours[i] for i in self._existing_tour_indexes(sol)]
        return self.planner.compute_cost(tours)

import random

import copy

from src.abstract.planner import Planner
from src.abstract.sa_solver import SaSolver
from src.abstract.tour_selector import TourSelector
from src.params.tour_selector_params import TourSelectorParams


class SaTourSelector(TourSelector, SaSolver):
    def __init__(self, tours, params: TourSelectorParams, planner : Planner):
        TourSelector.__init__(self, tours, params, planner)
        SaSolver.__init__(self, params.sa_cooling_rate)
        # super(SaTourSelector, self).__init__(tours, params, planner)
        self.all = [1 for _ in tours]

    def run(self):
        self.run_sa(self.params.sa_cooling_rate)

    def _existing_tour_indexes(self, sol):
        return (i for i, x in enumerate(sol) if x)

    def _missing_tour_indexes(self, sol):
        return (i for i, x in enumerate(sol) if x)

    def _get_random_sol(self) -> tuple:
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
        return self.planner.score(tours)


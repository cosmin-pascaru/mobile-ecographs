import copy
import random

from src.alg.abstract.planner import CPlanner
from src.alg.abstract.sa_solver import ISaSolver
from src.alg.abstract.tour_selector import CTourSelector
from src.alg.concrete.planning_manager import CManager
from src.alg.params.tour_selector_params import CSaTourSelectorParams


class CSaTourSelector(CTourSelector, ISaSolver):
    def __init__(self, manager: CManager, tours, params: CSaTourSelectorParams, planner : CPlanner):
        CTourSelector.__init__(self, manager, tours, params.tour_sel_params, planner)
        ISaSolver    .__init__(self)

        self.params = params
        self.all = None

    def run_tour_selector(self):
        self._filter_too_long_tours()
        self.all = [1 for _ in self.tours]

        ISaSolver.run_sa(self, self.params.sa_params)

    def _existing_tour_indexes(self, sol):
        return tuple(i for i, x in enumerate(sol) if x)

    def _missing_tour_indexes(self, sol):
        return tuple(i for i, x in enumerate(sol) if x)

    def _get_initial_sol(self) -> tuple:
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
        return self.planner.run_planner(tours)

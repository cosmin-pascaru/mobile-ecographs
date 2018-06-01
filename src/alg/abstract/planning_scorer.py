import copy
from abc import ABC, abstractmethod

from src.alg.abstract.planning import CFullPlanning, CPlanning
from src.alg.concrete.planning_manager import CManager
from src.alg.input.planning_input import CPlanningInput
from src.alg.params.planning_scorer_params import CPlanningScorerParams


class CPlanningScorer(ABC):
    def __init__(self, manager:CManager, params: CPlanningScorerParams, input: CPlanningInput):
        self.manager = manager
        self.params = params
        self.input = input

    @abstractmethod
    def compute_cost_full(self, planning : CFullPlanning):
        pass

    @abstractmethod
    def compute_cost(self, planning : CPlanning):
        pass

    def compute_not_visited_cnt(self, planning : CFullPlanning):
        remaining = copy.deepcopy(self.input.consults_per_node)

        for day in planning.days:
            for tour in day.tours:
                if tour is None:
                    continue
                for i, cnt in enumerate(tour.cnt_visits):
                    remaining[tour.tour[i]] -= cnt

        return remaining
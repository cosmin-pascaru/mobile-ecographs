from abc import ABC, abstractmethod

import copy

from src.abstract.planning import CPlanning
from src.concrete.planning_manager import CManager
from src.input.planning_input import PlanningInput
from src.params.planning_scorer_params import PlanningScorerParams


class CPlanningScorer(ABC):
    def __init__(self, manager:CManager, params: PlanningScorerParams, input: PlanningInput):
        self.manager = manager
        self.params = params
        self.input = input

    @abstractmethod
    def compute_cost(self, planning : CPlanning):
        pass

    def compute_not_visited_cnt(self, planning : CPlanning):
        remaining = copy.deepcopy(self.input.consults_per_node)

        for day in planning.days:
            for tour in day.tours:
                if tour is None:
                    continue
                for i, cnt in enumerate(tour.cnt_visits):
                    remaining[tour.tour[i]] -= cnt

        return remaining
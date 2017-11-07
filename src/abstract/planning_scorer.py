from abc import ABC, abstractmethod

from src.abstract.planning import Planning
from src.concrete.planning_manager import Manager
from src.input.planning_input import PlanningInput
from src.params.planning_scorer_params import PlanningScorerParams


class PlanningScorer(ABC):
    def __init__(self, manager:Manager, params: PlanningScorerParams, input_: PlanningInput):
        self.manager = manager
        self.params = params
        self.input = input_

    @abstractmethod
    def compute_cost(self, planning : Planning):
        pass


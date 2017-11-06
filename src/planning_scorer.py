from abc import ABC, abstractmethod

from src.input.planning_input import PlanningInput
from src.params.planning_scorer_params import PlanningScorerParams
from src.planning import Planning


class PlanningScorer(ABC):
    def __init__(self, params: PlanningScorerParams, input_: PlanningInput):
        self.params = params
        self.input = input_

    @abstractmethod
    def score(self, planning : Planning):
        pass


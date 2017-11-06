from abc import ABC, abstractmethod

from src.abstract.planning import Planning
from src.input.planning_input import PlanningInput
from src.params.planning_scorer_params import PlanningScorerParams


class PlanningScorer(ABC):
    def __init__(self, params: PlanningScorerParams, input_: PlanningInput):
        self.params = params
        self.input = input_

    @abstractmethod
    def score(self, planning : Planning):
        pass


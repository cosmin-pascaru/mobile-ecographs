from abc import ABC, abstractmethod

from src.input.planning_input import PlanningInput
from src.params.planner_params import PlannerParams


class Planner(ABC):
    def __init__(self, input_ : PlanningInput, params : PlannerParams):
        self.input = input_
        self.params = params

    @abstractmethod
    def run(self, tours):
        pass

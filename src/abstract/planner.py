from abc import ABC, abstractmethod

from src.concrete.planning_manager import Manager
from src.input.planning_input import PlanningInput
from src.params.planner_params import PlannerParams


class Planner(ABC):
    def __init__(self, manager : Manager, input_ : PlanningInput, params : PlannerParams):
        self.manager = manager

        self.input = input_
        self.params = params
        self.tours = None

        self.best_plan = None

    @abstractmethod
    def score(self, tours) -> float:
        pass
from abc import ABC, abstractmethod

from src.abstract.planning_scorer import PlanningScorer
from src.concrete.planning_manager import Manager
from src.input.planning_input import PlanningInput
from src.params.planner_params import PlannerParams


class Planner(ABC):
    def __init__(self, manager : Manager, input : PlanningInput, params : PlannerParams, scorer : PlanningScorer):
        self.manager = manager

        self.input = input
        self.params = params
        self.scorer = scorer
        self.tours = None

        self.best_plan = None
        self.best_cost = None

    @abstractmethod
    def compute_cost(self, tours) -> float:
        pass
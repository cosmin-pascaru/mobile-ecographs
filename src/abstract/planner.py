from abc import ABC, abstractmethod

from src.abstract.planning_scorer import CPlanningScorer
from src.concrete.planning_manager import CManager
from src.input.planning_input import PlanningInput
from src.params.planner_params import PlannerParams


class CPlanner(ABC):
    def __init__(self, manager : CManager, input : PlanningInput, params : PlannerParams, scorer : CPlanningScorer):
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
from abc import ABC, abstractmethod

from src.alg.abstract.planning_scorer import PlanningScorer
from src.alg.concrete.planning_manager import Manager
from src.alg.input.planning_input import PlanningInput
from src.alg.params.planner_params import PlannerParams


class Planner(ABC):
    def __init__(self, manager : Manager, input : PlanningInput, params : PlannerParams, scorer : PlanningScorer, new_planning_callback):
        self.manager = manager

        self.input = input
        self.params = params
        self.scorer = scorer
        self.new_planning_callback = new_planning_callback

        self.tours = None
        self.best_plan = None
        self.best_cost = None

    @abstractmethod
    def run_planner(self, tours) -> float:
        pass
from abc import ABC, abstractmethod

from src.alg.abstract.planning_scorer import CPlanningScorer
from src.alg.concrete.planning_manager import CManager
from src.alg.input.planning_input import CPlanningInput
from src.alg.params.planner_params import CPlannerParams


class CPlanner(ABC):
    def __init__(self, manager : CManager, input : CPlanningInput, params : CPlannerParams, scorer : CPlanningScorer, new_planning_callback):
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
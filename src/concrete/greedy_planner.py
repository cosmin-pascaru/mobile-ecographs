import random

from src.abstract.greedy_solver import GreedySolver
from src.abstract.planner import Planner
from src.abstract.planning import Planning
from src.abstract.planning_scorer import PlanningScorer
from src.concrete.planning_manager import Manager
from src.input.planning_input import PlanningInput
from src.params.planner_params import PlannerParams
from src.utils import weighted_choice, SECONDS_PER_HOUR, list_sub


class GreedyPlanner(Planner, GreedySolver):
    KEEP_FACTOR = 0.3
    COST_CORRECTION_BIAS  = 3 * SECONDS_PER_HOUR # ??? random value... 3 hours
    MAX_TIME_PER_DAY = 8 * SECONDS_PER_HOUR # 8 hours

    def __init__(self, manager: Manager, input_: PlanningInput, params: PlannerParams, scorer : PlanningScorer):
        Planner.__init__(self, manager, input_, params, scorer)
        GreedySolver.__init__(self)

        self.get_dist = lambda s, d: self.manager.compute_distance(s, d)

        self.current_plan = None
        self.day = None
        self.car = None

        self.remaining_visits = None

    def score(self, tours):
        self.tours = tours
        self.current_plan = Planning(self.input.cnt_days, self.input.cnt_cars)

        self.day = 0
        self.car = 0

        self.remaining_visits = self.input.consults_per_node

        self.greedy_run()

        return self.scorer.compute_cost(self.current_plan)

    def _apply_best_option(self):
        choices = [(tour, self._compute_option_cost(tour)) for tour in self.tours]
        choices.sort(key = lambda t: t[1])

        new_len = max(int(len(choices) * self.KEEP_FACTOR), 1)

        # Filter tours with too low score
        choices = choices[:new_len]

        choice = weighted_choice(choices)

        self._apply_choice(choice)

    def _apply_choice(self, choice):
        dist_on_road = self.manager.compute_tour_distance(choice)
        visits_per_node = self._compute_visits_per_node(choice, dist_on_road)

        for i, cnt in enumerate(visits_per_node):
            self.remaining_visits[choice[i]] -= cnt

        self.current_plan[self.day][self.car] = Planning.Tour(choice, visits_per_node)

        self._next()

    def _next(self):
        if self.day >= self.input.cnt_days:
            self.day = 0
            self.car += 1
        else:
            self.day += 1

    def _done(self):
        return all(x == 0 for x in self.remaining_visits)
        # return self.day >= self.input.cnt_days

    def _compute_option_cost(self, tour):
        visit_duration = self.input.consult_time

        get_dist_at_idx = lambda i: self.manager.compute_distance(self.manager.source_node, tour[i])
        normalize_dist  = lambda d: (-d + self.COST_CORRECTION_BIAS) * visit_duration

        dist_on_road = self.manager.compute_tour_distance(tour)
        visits_per_node = self._compute_visits_per_node(tour, dist_on_road)
        visits_cost = sum(cnt * normalize_dist(get_dist_at_idx(i)) for i, cnt in enumerate(visits_per_node))
        """Cost should be higher with more visits, but lower as you visit places further away?"""

        return dist_on_road + visits_cost

    def _compute_visits_per_node(self, tour, dist_on_road):
        node_importances = [(i, self.get_dist(self.manager.src, x)) for i, x in enumerate(tour)]
        node_importances.sort(key = lambda t: t[1], reverse=True)

        remaining_time = self.MAX_TIME_PER_DAY - dist_on_road

        visits = [0 for _ in tour]

        for i, imp in node_importances:
            if remaining_time < self.input.consult_time:
                break

            if self.remaining_visits[i] > 0:
                visits[i] += min(self.remaining_visits[tour[i]], remaining_time // self.input.consult_time)
                remaining_time -= self.input.consult_time * visits[i]

        return visits

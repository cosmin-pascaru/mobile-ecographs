import random

import copy

from src.abstract.greedy_solver import GreedySolver
from src.abstract.planner import Planner
from src.abstract.planning import Planning
from src.abstract.planning_scorer import PlanningScorer
from src.concrete.planning_manager import Manager
from src.input.planning_input import PlanningInput
from src.params.planner_params import PlannerParams
from src.utils import weighted_choice, SECONDS_PER_HOUR, list_sub


class GreedyPlanner(Planner, GreedySolver):
    NR_ITERATIONS = 5
    KEEP_FACTOR = 0.2
    COST_CORRECTION_BIAS = 3 * SECONDS_PER_HOUR  # ??? random value... 3 hours
    MAX_TIME_PER_DAY = 8 * SECONDS_PER_HOUR  # 8 hours

    def __init__(self, manager: Manager, input: PlanningInput, params: PlannerParams, scorer: PlanningScorer):
        Planner.__init__(self, manager, input, params, scorer)
        GreedySolver.__init__(self)

        self.get_dist = lambda s, d: self.manager.get_distance(s, d)

        self.current_plan = None
        self.current_cost = None

        self.day = None
        self.car = None

        self.remaining_visits = None

    def compute_cost(self, tours):
        if self.params.debug:
            print('Greedy planner computing cost for {}'.format(tours))

        if not tours:
            return float('inf')

        self.tours = tours

        avg = 0
        for _ in range(self.NR_ITERATIONS):
            self._reset()

            self.greedy_run()

            self.current_cost = self.scorer.compute_cost(self.current_plan)
            avg += self.current_cost

            self._update_best()

        avg /= self.NR_ITERATIONS

        if self.params.debug:
            print('Average is {}'.format(avg))

        return avg

    def _reset(self):
        self.current_plan = Planning(self.input.cnt_days, self.input.cnt_cars)

        self.day = 0
        self.car = 0

        self.remaining_visits = copy.deepcopy(self.input.consults_per_node)

    def _update_best(self):
        if self.best_cost is None or self.current_cost < self.best_cost:
            if self.params.debug:
                print('Found better planning, cost = {}'.format(self.current_cost))
                not_visited = sum(self.scorer.compute_not_visited_cnt(self.current_plan))
                print('Not visited = {}'.format(not_visited))

            self.best_plan, self.best_cost = self.current_plan, self.current_cost

    def _apply_best_option(self):
        choices = [(tour, self._compute_option_cost(tour)) for tour in self.tours]
        choices.sort(key=lambda t: t[1])

        new_len = max(int(len(choices) * self.KEEP_FACTOR), 1)

        # Filter tours with too low score
        choices = choices[:new_len]
        choice = weighted_choice(choices)

        self._apply_choice(choice)

    def _apply_choice(self, tour):
        dist_on_road = self.manager.compute_tour_distance(tour)
        visits_per_node = self._compute_visits_per_node(tour, dist_on_road)

        for i, cnt in enumerate(visits_per_node):
            self.remaining_visits[tour[i]] -= cnt
            assert self.remaining_visits[tour[i]] >= 0

        self.current_plan[self.day][self.car] = Planning.Tour(tour, visits_per_node)
        self._next()

    def _next(self):
        self.day += 1

        if self.day >= self.input.cnt_days:
            self.day = 0
            self.car += 1

    def _done(self):
        return all(x == 0 for x in self.remaining_visits) or self.car >= self.input.cnt_cars

    def _compute_option_cost(self, tour):
        visit_duration = self.input.consult_time
        src = 0  # source node

        get_dist_at_idx = lambda i: self.manager.get_distance(src, tour[i])
        normalize_dist = lambda d: (-d + self.COST_CORRECTION_BIAS) * visit_duration

        dist_on_road = self.manager.compute_tour_distance(tour)
        visits_per_node = self._compute_visits_per_node(tour, dist_on_road)

        if sum(visits_per_node) == 0:
            return float('inf')  # a cost for a road where we do nothing is infinite

        visits_cost = sum(cnt * normalize_dist(get_dist_at_idx(i)) for i, cnt in enumerate(visits_per_node))
        """Cost should be higher with more visits, but lower as you visit places further away?"""

        return dist_on_road + visits_cost

    def _compute_visits_per_node(self, tour, dist_on_road):
        if tour is None:
            return []

        src = 0  # start node

        node_importances = [(i, self.get_dist(src, x)) for i, x in enumerate(tour)]
        node_importances.sort(key=lambda t: t[1], reverse=True)

        remaining_time = self.MAX_TIME_PER_DAY - dist_on_road

        visits = [0 for _ in tour]

        for i, imp in node_importances:
            if remaining_time < self.input.consult_time:
                break

            if self.remaining_visits[tour[i]] > 0:
                visits[i] += min(self.remaining_visits[tour[i]], remaining_time // self.input.consult_time)
                remaining_time -= self.input.consult_time * visits[i]
        return visits

import copy
import os

from src.abstract.greedy_solver import IGreedySolver
from src.abstract.planner import CPlanner
from src.abstract.planning import CPlanning
from src.abstract.planning_scorer import CPlanningScorer
from src.concrete.planning_manager import CManager
from src.input.planning_input import PlanningInput
from src.params.constants import CONSULT_TIME, MAX_TIME_PER_DAY
from src.params.planner_params import PlannerParams
from src.utils import weighted_choice


class CGreedyPlanner(CPlanner, IGreedySolver):
    # COST_CORRECTION_BIAS = 3 * SECONDS_PER_HOUR  # ??? random value... 3 hours

    def __init__(self, manager: CManager, input: PlanningInput, params: PlannerParams, scorer: CPlanningScorer):
        CPlanner.__init__(self, manager, input, params, scorer)
        IGreedySolver.__init__(self)

        self.CNT_ITERATIONS = params.cnt_iterations
        self.KEEP_PERCENT   = params.keep_percent

        self.get_dist = lambda source, destination: self.manager.get_distance(source, destination)

        self.current_plan = None
        self.current_cost = None

        self.day = None
        self.car = None

        self.remaining_visits = None
        self.done = None

    def compute_cost(self, tours):
        if self.params.debug:
            print('Greedy planner computing cost for {}'.format(tours))

        if not tours:
            return float('inf')

        self.tours = tours

        avg = 0
        for _ in range(self.CNT_ITERATIONS):
            self._reset()

            self.greedy_run()

            self.current_cost = self.scorer.compute_cost(self.current_plan)
            avg += self.current_cost

            self._update_best()

        avg /= self.CNT_ITERATIONS

        if self.params.debug:
            print('Average is {}'.format(avg))

        return avg

    def _reset(self):
        self.current_plan = CPlanning(self.input.cnt_days, self.input.cnt_cars)

        self.day = 0
        self.car = 0

        self.done = False
        self.remaining_visits = copy.deepcopy(self.input.consults_per_node)

    def _update_best(self):
        if self.best_cost is None or self.current_cost < self.best_cost:
            print('Found better planning, cost = {}'.format(self.current_cost))
            not_visited = sum(self.scorer.compute_not_visited_cnt(self.current_plan))
            print('Not visited = {}'.format(not_visited))

            self.best_plan, self.best_cost = self.current_plan, self.current_cost

            self.write_best_plan()

    def _apply_best_option(self):
        choices = [(tour, self._compute_option_cost(tour)) for tour in self.tours]
        choices.sort(key=lambda t: t[1])

        new_len = max(int(len(choices) * self.KEEP_PERCENT), 1)

        # Filter tours with too low score
        choices = choices[:new_len]
        while choices and choices[-1][1] == float('inf'):
            choices.pop()

        if not choices:
            self.done = True

        choice = weighted_choice(choices)

        self._apply_choice(choice)

    def _apply_choice(self, tour):
        visits_per_node = self._compute_visits_per_node(tour)

        for i, cnt in enumerate(visits_per_node):
            self.remaining_visits[tour[i]] -= cnt
            assert self.remaining_visits[tour[i]] >= 0

        self.current_plan[self.day][self.car] = CPlanning.Tour(tour, visits_per_node)
        self._next()

    def _next(self):
        self.day += 1

        if self.day >= self.input.cnt_days:
            self.day = 0
            self.car += 1

    def _done(self):
        return self.done or all(x == 0 for x in self.remaining_visits) or self.car >= self.input.cnt_cars

    def _compute_option_cost(self, tour):
        # get_dist_at_idx = lambda i: self.manager.get_distance(src, tour[i])
        # normalize_dist = lambda d: (-d + self.COST_CORRECTION_BIAS) * visit_duration

        visits_per_node = self._compute_visits_per_node(tour)

        if sum(visits_per_node) == 0:
            return float('inf')  # a cost for a road where we do nothing is infinite

        # visits_cost = -sum(visits_per_node)
        visits_cost = -sum(visits_per_node) * CONSULT_TIME
        # visits_cost = sum(cnt * dist(get_dist_at_idx(i)) for i, cnt in enumerate(visits_per_node))
        """Cost should be higher with more visits, but lower as you visit places further away?"""

        return self.manager.compute_tour_distance(tour, visits_per_node) + visits_cost

    def _compute_visits_per_node(self, tour):
        if tour is None:
            return []

        src = 0  # start node

        node_importances = [(i, self.get_dist(src, x)) for i, x in enumerate(tour)]
        node_importances.sort(key=lambda t: t[1], reverse=True)

        visits = [0 for _ in tour]

        remaining_time = MAX_TIME_PER_DAY

        for i, imp in node_importances:

            if remaining_time < 2 * CONSULT_TIME:
                break

            if self.remaining_visits[tour[i]] > 0:
                # self.remaining_visits[tour[i]] -= 1
                visits[i] += 1

                temp_remaining_time  = MAX_TIME_PER_DAY
                temp_remaining_time -= self.manager.compute_tour_distance(tour, visits)
                temp_remaining_time -= sum(visits) * CONSULT_TIME

                if temp_remaining_time >= 0:
                    temp = min(self.remaining_visits[tour[i]] - 1, temp_remaining_time // CONSULT_TIME)

                    visits[i] += temp
                    # self.remaining_visits[tour[i]] -= temp

                    # temp_remaining_time = self.manager.input.max_time_per_day
                    # temp_remaining_time -= self.manager.compute_tour_distance(tour, visits)
                    # temp_remaining_time -= sum(visits) * self.input.consult_time

                    temp_remaining_time -= temp * CONSULT_TIME

                    remaining_time = temp_remaining_time
                else:
                    visits[i] -= 1

        return visits

    def write_best_plan(self):
        if not self.params.write_best_plan:
            return

        folder = 'data/plans'
        html_folder = 'data/html'
        tours_html_file = 'tours_{}.html'.format(self.best_cost)

        tours_file = 'tours_{}.txt'.format(self.best_cost)
        days_file  = 'days_{}.txt'.format(self.best_cost)

        tours_html_path = os.path.join(html_folder, tours_html_file)
        tours_path = os.path.join(folder, tours_file)
        days_path = os.path.join(folder, days_file)

        CPlanning.CWriter().write_tours_html(self.best_plan, tours_html_path, self.manager)
        CPlanning.CWriter().write           (self.best_plan, tours_path, days_path, self.manager)

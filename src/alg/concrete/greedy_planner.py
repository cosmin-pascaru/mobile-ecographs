import copy
import os

from src.alg.abstract.planner import Planner
from src.alg.abstract.planning import FullPlanning, Planning, Tour
from src.alg.abstract.planning_scorer import PlanningScorer
from src.alg.concrete.planning_manager import Manager
from src.alg.input.planning_input import PlanningInput
from src.alg.params.planner_params import PlannerParams
from src.common.constants import CONSULT_TIME, MAX_TIME_PER_DAY
from src.common.utils import weighted_choice


class GreedyPlanner(Planner):
    def __init__(self, manager: Manager, input: PlanningInput, params: PlannerParams, scorer: PlanningScorer, new_plan_callback):
        Planner.__init__(self, manager, input, params, scorer, new_plan_callback)

        self.cnt_iterations = params.cnt_iterations
        self.keep_percent   = params.keep_percent

        self.get_dist = lambda source, destination: self.manager.get_distance(source, destination)

        self.current_plan = None

        self.remaining_visits = None
        self.done = None

    def run_planner(self, tours):
        if self.params.debug:
            print('Greedy planner computing cost for {}'.format(tours))

        if not tours:
            return float('inf')

        self.tours = tours

        for _ in range(self.cnt_iterations):
            self._reset()

            while not self._done():
                self._apply_best_option()

            self.on_new_planning(self.current_plan)

    def _reset(self):
        self.current_plan = Planning()
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

        new_len = max(int(len(choices) * self.keep_percent), 1)

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

        new_tour = Tour(tour, visits_per_node)
        self.current_plan.tours.append(new_tour)

    def _done(self):
        return all(x == 0 for x in self.remaining_visits)

    def _compute_option_cost(self, tour):
        # get_dist_at_idx = lambda i: self.manager.get_distance(src, tour[i])
        # normalize_dist = lambda d: (-d + self.COST_CORRECTION_BIAS) * visit_duration

        visits_per_node = self._compute_visits_per_node(tour)

        if sum(visits_per_node) == 0:
            return float('inf')  # a cost for a road where we do nothing is infinite

        visits_cost = -sum(visits_per_node) * CONSULT_TIME

        # TODO: Cost should be higher with more visits, but lower as you visit places further away?
        # TODO: probably what's below is better

        # TODO: cost might make sense to be different;
        # TODO: cost = total_dist / nr_visits
        # TODO: basically, it's a metric of how much distance per visit you would have to spend by following this tour

        return self.manager.compute_tour_distance(tour, visits_per_node) + visits_cost
        # return self.manager.compute_tour_distance(tour, visits_per_node) / sum(visits_per_node)

    def _compute_visits_per_node(self, tour):
        if tour is None:
            return []

        src = 0  # start node

        node_importances = [(i, self.get_dist(src, x)) for i, x in enumerate(tour)]
        node_importances.sort(key=lambda t: t[1], reverse=True)  # Furthest townships first
        # node_importances.sort(key=lambda t: t[1])  # Closest townships first

        visits = [0 for _ in tour]

        remaining_time = MAX_TIME_PER_DAY

        for i, imp in node_importances:

            # TODO: inspect and remember the reason why this is 2 *, and not just CONSULT_TIME
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
                    temp_remaining_time -= temp * CONSULT_TIME

                    remaining_time = temp_remaining_time
                else:
                    visits[i] -= 1

        return visits

    def on_new_planning(self, new_planning):
        self.new_planning_callback(new_planning)

    def write_best_plan(self):
        if not self.params.write_best_plan:
            return

        folder          = 'data/plans'
        html_folder     = 'data/html'
        tours_html_file = 'tours_{}.html'.format(self.best_cost)

        tours_file = 'tours_{}.txt'.format(self.best_cost)
        days_file  = 'days_{}.txt' .format(self.best_cost)

        tours_html_path = os.path.join( html_folder , tours_html_file )
        tours_path      = os.path.join( folder      , tours_file      )
        days_path       = os.path.join( folder      , days_file       )

        FullPlanning.CWriter().write_tours_html(self.best_plan, tours_html_path, self.manager)
        FullPlanning.CWriter().write           (self.best_plan, tours_path, days_path, self.manager)

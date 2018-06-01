import copy

from src.alg.abstract.planning_scorer import CPlanningScorer
from src.alg.params.planning_scorer_params import CPlanningScorerParams
from src.alg.abstract.planning import CFullPlanning, CPlanning
from src.alg.concrete.planning_manager import CManager
from src.alg.input.planning_input import CPlanningInput
from src.alg.params.constants import CONSULT_TIME


class CSimplePlanningScorer (CPlanningScorer):
    def __init__(self, manager: CManager, params: CPlanningScorerParams, input: CPlanningInput):
        super().__init__(manager, params, input)

        self.remaining_visits = None

    def compute_cost(self, planning: CPlanning):
        self._init_remaining_visits()

        time_on_road     = 0
        time_on_consults = 0

        for tour in planning.tours:
            locations      = tour.locations
            visits_per_loc = tour.visits_per_loc

            time_on_road     += self.manager.compute_tour_distance(locations, visits_per_loc)
            time_on_consults += sum(visits_per_loc) * CONSULT_TIME

        nr_tours = len(planning.tours)

        cost = 0
        cost += nr_tours         * self.params.tour_cost
        cost += time_on_road     * self.params.road_cost_factor
        cost += time_on_consults * self.params.consult_time_factor

        if self.params.debug:
            print('time_on_road:    ', time_on_road    )
            print('time_on_consults:', time_on_consults)
            print('nr_tours:        ', nr_tours        )

        return cost

    def compute_cost_full(self, planning: CFullPlanning):
        self._init_remaining_visits()

        time_on_road = 0
        time_on_consults = 0
        max_cars = 0

        # print('remaining visits: {}'.format(self.remaining_visits))

        for day in planning.days:
            cars = len(day)
            max_cars = max(max_cars, cars)

            for tour in day.tours:
                if tour is None:
                    continue

                time_on_road += self.manager.compute_tour_distance(tour.tour)
                time_on_consults += sum(tour.cnt_visits) * CONSULT_TIME

                for i, cnt in enumerate(tour.cnt_visits):
                    self.remaining_visits[tour.tour[i]] -= cnt

        cnt_not_visited = sum(self.remaining_visits)

        cost  = 0
        cost += cnt_not_visited * self.params.not_visited_cost
        cost += max_cars * self.params.car_cost
        cost += time_on_road * self.params.road_cost_factor

        if self.params.debug:
            print('cnt_not_visited = {}'.format(cnt_not_visited))
            print('max_cars = {}'.format(max_cars))
            print('time_on_road = {}'.format(time_on_road))
            print('time_on_consults = {}'.format(time_on_consults))
            print('total cost = {}'.format(cost))
            print()
        return cost

    def _init_remaining_visits(self):
        self.remaining_visits = copy.deepcopy(self.input.consults_per_node)

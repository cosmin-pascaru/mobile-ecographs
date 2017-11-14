import copy

from src.abstract.planning import Planning
from src.abstract.planning_scorer import PlanningScorer
from src.concrete.planning_manager import Manager
from src.input.planning_input import PlanningInput
from src.params.planning_scorer_params import PlanningScorerParams


class PlanningScorerV1 (PlanningScorer):
    NOT_VISITED_COST = 10000000
    CAR_COST         = 10000

    def __init__(self, manager:Manager, params: PlanningScorerParams, input: PlanningInput):
        super().__init__(manager, params, input)

        self.remaining_visits = None

    def compute_cost(self, planning: Planning):
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
                time_on_consults += sum(tour.cnt_visits) * self.input.consult_time

                for i, cnt in enumerate(tour.cnt_visits):
                    self.remaining_visits[tour.tour[i]] -= cnt

        cnt_not_visited = sum(self.remaining_visits)

        cost  = 0
        cost += cnt_not_visited * self.NOT_VISITED_COST
        cost += max_cars * self.CAR_COST
        cost += time_on_road

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
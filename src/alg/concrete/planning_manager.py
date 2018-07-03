import itertools

from src.alg.concrete.hall_of_fame import HallOfFame
from src.alg.concrete.maps_url import CMapsUrlConverter
from src.common.constants import MAX_TIME_PER_DAY, CONSULT_TIME
from src.common.read_input import read_visits_cnt


class SManagerInput:
    def __init__(self):
        self.input = None

        self.manager_params = None

        self.tours = None

        self.tour_selector_cls = None
        self.tour_selector_params = None

        self.planner_cls = None
        self.planner_params = None

        self.scorer_cls = None
        self.scorer_params = None


class Manager:

    def __init__(self, init_struct : SManagerInput):
        self.input = init_struct.input
        self.params = init_struct.manager_params

        self.scorer = init_struct.scorer_cls(manager=self,
                                             input=init_struct.input,
                                             params=init_struct.scorer_params)
        self.planner = init_struct.planner_cls(manager=self,
                                               input=init_struct.input,
                                               params=init_struct.planner_params,
                                               scorer=self.scorer,
                                               new_plan_callback=self.on_new_plan)
        self.tour_selector = init_struct.tour_selector_cls(manager=self,
                                                           tours=init_struct.tours,
                                                           params=init_struct.tour_selector_params,
                                                           planner=self.planner)
        self.hof = HallOfFame()

    def run(self):
        self.tour_selector.run_tour_selector()

        with open('data/runs_{}.txt'.format(self.tour_selector.params.max_time), 'a') as f:
            f.write('{} {}\n'.format(*self.hof.best_cost))

    def get_distance(self, x, y):
        return self.input.distance_matrix[x][y]

    def on_new_plan(self, plan):
        cost = self.scorer.compute_cost(plan)

        self.hof.update(plan, cost)

    def compute_tour_distance(self, tour, visits=None):
        if tour is None:
            return 0

        if visits is None:
            return sum(self.get_distance(i, j) for i, j in zip(tour[:-1], tour[1:]))

        actual_tour = [0] + [t for t, v in zip(tour, visits) if v > 0] + [0]

        return self.compute_tour_distance(actual_tour)

    def get_url(self, tour):
        return CMapsUrlConverter().generate_from(self.input.places_names[i] + self.input.places_suffix for i in tour)

    def get_embed_url(self, tour):
        return CMapsUrlConverter().generate_embed(self.params.maps_api_key, (self.input.places_names[i] + self.input.places_suffix for i in tour))

    # def compute_unique_tours(self, planning : CFullPlanning):
    #     unique_tours = {}
    #     for day in planning.days:
    #         if day is None:
    #             continue
    #
    #         for tour in day.tours:
    #             if tour is None:
    #                 continue
    #             if tour.tour is None:
    #                 continue
    #             tuple_tour = tuple(tour.tour)
    #             if unique_tours.get(tuple_tour, None) is None:
    #                 unique_tours[tuple_tour] = len(unique_tours)
    #     return unique_tours

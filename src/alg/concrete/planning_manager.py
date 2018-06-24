import itertools

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
        self.best_cost = None
        self.best_plan = None

    def run(self):
        self.tour_selector.run_tour_selector()

        with open('data/runs_{}.txt'.format(self.tour_selector.params.max_time), 'a') as f:
            f.write('{} {}\n'.format(*self.best_cost))

    def get_distance(self, x, y):
        return self.input.distance_matrix[x][y]

    def on_new_plan(self, plan):
        cost = self.scorer.compute_cost(plan)

        if self.best_cost is None or cost < self.best_cost:
            self.best_cost = cost
            self.best_plan = plan

            self.output_best()
            print('best cost so far:', self.best_cost)

    def output_best_as_permutation(self):
        all_visits_per_location = read_visits_cnt()
        all_visits_duplicated   = list(itertools.chain.from_iterable([[i] * v for i, v in enumerate(all_visits_per_location)]))

        correct_cnt_visits = sum(all_visits_per_location)

        all_tours_joined = []
        lens = []

        for tour in self.best_plan.tours:

            dist = self.compute_tour_distance(tour.locations, tour.visits_per_loc)
            dist += sum(tour.visits_per_loc) * CONSULT_TIME
            if dist > MAX_TIME_PER_DAY:
                assert False

            # print(dist)
            # print(CONSULT_TIME)
            # print(MAX_TIME_PER_DAY)

            duplicated = [[location] * nr_visits for location, nr_visits in zip(tour.locations, tour.visits_per_loc)]
            duplicated = list(itertools.chain.from_iterable(duplicated))

            all_tours_joined += duplicated
            lens += [len(duplicated)]

        print('nr tours = {}'.format(len(self.best_plan.tours)))

        assert len(all_tours_joined) == correct_cnt_visits
        assert sorted(all_tours_joined) == all_visits_duplicated

        all_tours_with_idx = [(v, i) for i, v in enumerate(all_tours_joined)]
        all_tours_with_idx.sort()

        temp = [e[1] for e in all_tours_with_idx]
        perm = [-1] * len(temp)

        for i in range(len(temp)):
            perm[temp[i]] = i

        assert all(all_visits_duplicated[perm_e] == tour_e for perm_e, tour_e in zip(perm, all_tours_joined))

        with open("data/perm/perm_{}.txt".format(self.best_cost), 'w') as f:
            f.write(str(perm) + '\n' + str(lens))


    def output_best_to_console(self):
        print('---------------------------------PLAN:')
        for tour in self.best_plan.tours:
            print('TOUR:')
            for loc, cnt in zip(tour.locations, tour.visits_per_loc):
                if cnt:
                    print((loc, cnt), sep=' ', end=' ')
            print()

        print('Best is {}'.format(len(self.best_plan.tours)))
        # self.best_plan.to_full_planning()

    def output_best(self):
        self.output_best_as_permutation()
        # self.output_best_to_console()

    def compute_tour_distance(self, tour, visits=None):
        if tour is None:
            return 0

        if visits is None:
            return sum(self.get_distance(i, j) for i, j in zip(tour[:-1], tour[1:]))
            # return sum(self.get_distance(tour[i - 1], tour[i]) for i in range(1, len(tour))) + self.get_distance(tour[-1], tour[0])

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

import itertools

from src.alg.concrete.maps_url import CMapsUrlConverter
from src.common.constants import MAX_TIME_PER_DAY, CONSULT_TIME
from src.common.read_input import read_visits_cnt


class HallOfFame:
    def __init__(self):
        self.best_cost = None
        self.best_plan = None

    def update(self, new_plan, new_cost):
        if self.best_cost is None or new_cost < self.best_cost:
            self.best_cost = new_cost
            self.best_plan = new_plan

            self.output_best()
            print('best cost so far:', self.best_cost)

    def output_best(self):
        self.output_best_as_permutation()
        # self.output_best_to_console()

    def output_best_as_permutation(self):
        all_visits_per_location = read_visits_cnt()
        all_visits_duplicated   = list(itertools.chain.from_iterable([[i] * v for i, v in enumerate(all_visits_per_location)]))

        correct_cnt_visits = sum(all_visits_per_location)

        all_tours_joined = []
        lens = []

        for tour in self.best_plan.tours:
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

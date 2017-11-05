import random

from MapsUrl import MapsUrl
from NatalityDataReader import NatalityDataReader
from mtsp_solvers.SA_MTSP_Solver import SA_MTSP_Solver


class ToursFinder:
    def __init__(self):
        pass

    def compute_tours(self, nr_iterations, cooling_rate):
        with open('data/times.txt', 'r') as f:
            times = eval(f.read())

        with open("data/lista_comune.txt") as villages_file:
            lines = villages_file.readlines()
            lines = [" ".join(line.split()[1:]) for line in lines]
            villages = lines

        hours_on_road_limit = 9
        tour_limit = 60 * 60 * hours_on_road_limit

        solver = SA_MTSP_Solver(100000, cooling_rate)

        all_tours = []

        for iteration in range(nr_iterations):
            sol, cost = solver.solve(times, 25, tour_limit=tour_limit)

            tours = sol.get_tours()
            tour_costs = [sum(times[x][y] for x, y in zip(tour[:-1], tour[1:])) for tour in tours]

            invalids = list(filter(lambda x: x > tour_limit, tour_costs))
            if len(invalids) > 0:
                print('Invalid solution!', invalids)

            tours_str = tours
            #
            # for tour, cost in zip(tours, tour_costs):
            #     if 0 < cost <= tour_limit:
            #         good_tours.append(tour)

            tours_str = [[villages[i] + ' IASI ROMANIA' for i in tour] for tour in tours_str if len(tour) > 2]
            print(tours_str[0])

            print(cost)
            print(MapsUrl().generate_from(tours_str[0]))

            with open('data/tours/tours_{}.txt'.format(cost), 'w') as f:
                for idx, tour in enumerate(tours_str):
                    f.write(str(tour) + '\n')
                    f.write(MapsUrl().generate_from(tour) + '\n')
                    node_times = [i[1] * 30 / 12 for i in NatalityDataReader().read()]
                    node_times [:5] = [0 for i in range(5)]
                    f.write('Timp in fiecare comuna (minute pe luna):\n' + '\n'.join([tour[ti] + ' : ' + str(node_times[i]) for ti, i in enumerate(tours[idx])]) + '\n')

                    f.write('\n\n')



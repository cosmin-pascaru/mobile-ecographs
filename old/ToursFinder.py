from src.concrete.sa_mtsp_solver import SaMtspSolver, SaMtspSolverParams


class ToursFinderParams(object):
    def __init__(self):
        self.min_cnt_tours   = None
        self.output_file     = None
        self.times_filename  = 'data/times.txt'
        self.places_filename = 'data/lista_comune.txt'


class ToursFinder:
    def __init__(self):
        pass

    def compute_tours(self,
                      tours_finder_params : ToursFinderParams,
                      mtsp_solver_params  : SaMtspSolverParams,):

        times_filename  = tours_finder_params.times_filename
        places_filename = tours_finder_params.places_filename
        min_cnt_tours   = tours_finder_params.min_cnt_tours

        with open(times_filename, 'r') as f:
            times = eval(f.read())

        # with open(places_filename, 'r') as places_file:
        #     lines = places_file.readlines()
        #     lines = [" ".join(line.split()[1:]) for line in lines]

        hours_on_road_limit = 8
        tour_limit = 60 * 60 * hours_on_road_limit

        solver = SaMtspSolver(mtsp_solver_params)

        all_tours = []

        while len(all_tours) < min_cnt_tours:
            sol, cost = solver.solve(times, 25, tour_limit=tour_limit)

            tours = sol.get_tours()
            tour_costs = [sum(times[x][y] for x, y in zip(tour[:-1], tour[1:])) for tour in tours]

            invalids = list(filter(lambda x: x > tour_limit, tour_costs))
            if len(invalids) > 0:
                print('Invalid solution!', invalids)

            tours = list(filter(lambda t: len(t[0]) > 2 and t[1] < tour_limit, zip(tours, tour_costs)))
            tours = [t[0] for t in tours]

            all_tours += tours

            print(cost)

            # print(MapsUrl().generate_from(tours_str[0]))

            with open('data/tours/good_tours.txt'.format(cost), 'a') as f:
                for tour in tours:
                    f.write(' '.join(map(str, tour)) + '\n')
                # for idx, tour in enumerate(tours_str):
                #     f.write(str(tour) + '\n')
                #     f.write(MapsUrl().generate_from(tour) + '\n')
                #     node_times = [i[1] * 30 / 12 for i in NatalityDataReader().read()]
                #     node_times [:5] = [0 for i in range(5)]
                #     f.write('Timp in fiecare comuna (minute pe luna):\n' + '\n'.join([tour[ti] + ' : ' + str(node_times[i]) for ti, i in enumerate(tours[idx])]) + '\n')
                #
                #     f.write('\n\n')



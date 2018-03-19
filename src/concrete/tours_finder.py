from src.abstract.mtsp_solver import IMtspSolver
from src.concrete.sa_mtsp_solver import CSaMtspSolver, CSaMtspSolverParams, CMtspSolverParams
from src.params.constants import MAX_TIME_ON_ROAD


class CToursFinderParams(object):
    def __init__(self):
        self.min_cnt_tours   = None
        self.distance_matrix = None
        self.debug           = False


class CToursFinder:
    def __init__(self):
        pass

    def compute_tours(self,
                      tours_finder_params : CToursFinderParams,
                      solver              : IMtspSolver       ,
                      solver_params                           ):

        distance_matrix = tours_finder_params.distance_matrix
        min_cnt_tours   = tours_finder_params.min_cnt_tours

        all_tours = []

        while len(all_tours) < min_cnt_tours:
            sol, cost = solver.run_mtsp(solver_params)

            tours        = sol.get_tours()
            tour_lengths = [sum(distance_matrix[x][y] for x, y in zip(tour[:-1], tour[1:])) for tour in tours]

            tours = self._filter_tours(tours, tour_lengths)

            all_tours += tours

            if tours_finder_params.debug:
                print("Generated MTSP solution, cost = {}".format(cost))

        return all_tours

    def _filter_tours(self, tours, tour_lengths):
        return list(t[0] for t in filter(lambda t: len(t[0]) > 2 and t[1] < MAX_TIME_ON_ROAD, zip(tours, tour_lengths)))


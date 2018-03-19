import copy
import random

from old.NatalityDataReader import NatalityDataReader
from src.abstract.mtsp_solver import IMtspSolver
from src.abstract.sa_solver import CSaParams, ISaSolver
from src.params.constants import MAX_TIME_ON_ROAD


class CMtspSolverParams(object):
    def __init__(self, distance_matrix=None, nr_mtsp_tours=None, tour_time_limit=None):
        self.distance_matrix = distance_matrix
        self.nr_mtsp_tours   = nr_mtsp_tours
        self.tour_time_limit = tour_time_limit


class CSaMtspSolverParams(object):
    def __init__(self, sa_params : CSaParams = CSaParams(), mtsp_params : CMtspSolverParams = CMtspSolverParams()):
        self.sa_params   = sa_params
        self.mtsp_params = mtsp_params


class CSolution(object):
    neighbourhood_functions = None

    def __init__(self, nr_nodes, nr_tours):
        self.nr_nodes = nr_nodes
        self.nr_tours = nr_tours

        self.permutation = None
        self.tour_ends = None

        self.cost = None

    def get_tours(self):
        return [[0] + self.permutation[start:end] + [0] for start, end in
                zip([0] + self.tour_ends[:-1], self.tour_ends)]

    def compute_cost(self, distance_matrix, tour_limit):
        cost = 0

        for tour_st, tour_end in zip([0] + self.tour_ends[:-1], self.tour_ends):
            circuit = [0] + self.permutation[tour_st:tour_end] + [0]

            circuit_cost = 0

            for node_st, node_end in zip(circuit[:-1], circuit[1:]):
                circuit_cost += distance_matrix[node_st][node_end]

            if circuit_cost > tour_limit:
                circuit_cost *= CSaMtspSolver.TOO_LONG_TOUR_PENALTY

            cost += circuit_cost
        return cost

    def get_random_neighbour_and_cost(self, distance_matrix, tour_limit):
        neighbour = copy.deepcopy(self)

        p = random.random()

        for neighbour_f in CSolution.neighbour_functions:
            if p < neighbour_f[1]:
                neighbour_f[0](neighbour)

        return neighbour, neighbour.compute_cost(distance_matrix, tour_limit)

    @staticmethod
    def generate_random(nr_nodes, nr_tours):
        s = CSolution(nr_nodes, nr_tours)

        permutation = list(range(nr_nodes))
        random.shuffle(permutation)

        tour_ends = random.sample(range(1, nr_nodes + 1), nr_tours)
        tour_ends.sort()
        tour_ends[-1] = nr_nodes

        s.permutation = permutation
        s.tour_ends = tour_ends

        return s

    def swap2(self):
        i, j = random.sample(range(0, self.nr_nodes), 2)
        self.permutation[i], self.permutation[j] = self.permutation[j], self.permutation[i]

    def swap2adj(self):
        i = random.randint(0, self.nr_nodes - 2)
        self.permutation[i], self.permutation[i + 1] = self.permutation[i + 1], self.permutation[i]

    def swap3(self):
        i, j, k = random.sample(range(0, self.nr_nodes), 3)
        self.permutation[i], \
        self.permutation[j], \
        self.permutation[k] \
            = \
            self.permutation[j], \
            self.permutation[k], \
            self.permutation[i]

    def change_lengths(self):
        if self.nr_tours < 2:
            return

        i = random.randint(0, self.nr_tours - 2)

        if i > 0:
            left = self.tour_ends[i - 1]
        else:
            left = 1

        if i < self.nr_tours - 1:
            right = self.tour_ends[i + 1]
        else:
            right = self.nr_nodes

        self.tour_ends[i] = random.randint(left, right)


CSolution.neighbour_functions = [(CSolution.swap2         , 0.0),
                                 (CSolution.swap2adj      , 0.6),
                                 (CSolution.swap3         , 0.7),
                                 (CSolution.change_lengths, 1.0)]


class CSaMtspSolver(IMtspSolver, ISaSolver):
    TOO_LONG_TOUR_PENALTY = 100

    def __init__(self):
        super(IMtspSolver, self).__init__()

        self.nr_nodes = None
        self.nr_tours = None
        self.distance_matrix = None
        self.tour_time_limit = None

    def run_mtsp(self, params: CSaMtspSolverParams):
        self.distance_matrix = params.mtsp_params.distance_matrix
        self.tour_time_limit = params.mtsp_params.tour_time_limit
        self.nr_tours = params.mtsp_params.nr_mtsp_tours
        self.nr_nodes = len(self.distance_matrix)

        if len(self.distance_matrix) != len(self.distance_matrix[0]):
            raise ValueError('Matrix must be square!')

        best_sol, best_cost = ISaSolver.run_sa(self, params.sa_params)

        return best_sol, best_cost

    def _get_initial_sol(self):
        sol = CSolution.generate_random(self.nr_nodes, self.nr_tours)
        cost = sol.compute_cost(self.distance_matrix, MAX_TIME_ON_ROAD)

        return sol, cost

    def _get_random_neighbour(self, sol: CSolution):
        return sol.get_random_neighbour_and_cost(self.distance_matrix, MAX_TIME_ON_ROAD)

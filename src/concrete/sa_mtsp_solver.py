import copy
import math
import random

from old.NatalityDataReader import NatalityDataReader
from src.abstract.mtsp_solver import IMtspSolver


class SSaMtspSolverParams(object):
    def __init__(self, initial_temperature=None, cooling_rate=None, debug=False):
        self.initial_temperature = initial_temperature
        self.cooling_rate        = cooling_rate
        self.debug               = debug


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

    def compute_cost(self, distance_matrix, tour_limit, bonuses):
        cost = 0

        for tour_st, tour_end in zip([0] + self.tour_ends[:-1], self.tour_ends):
            circuit = [0] + self.permutation[tour_st:tour_end] + [0]

            circuit_cost = 0
            # circuit_cost = sum(bonuses[i] for i in self.permutation[tour_st:tour_end] if i > 4)

            for node_st, node_end in zip(circuit[:-1], circuit[1:]):
                circuit_cost += distance_matrix[node_st][node_end]

            if circuit_cost > tour_limit:
                circuit_cost *= CSaMtspSolver.TOO_LONG_TOUR_PENALTY

            cost += circuit_cost
        return cost

    def get_random_neighbour_and_cost(self, distance_matrix, tour_limit, bonuses):
        neighbour = copy.deepcopy(self)

        p = random.random()

        for neighbour_f in CSolution.neighbour_functions:
            if p < neighbour_f[1]:
                neighbour_f[0](neighbour)

        return neighbour, neighbour.compute_cost(distance_matrix, tour_limit, bonuses)

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


CSolution.neighbour_functions = [(CSolution.swap2, 0.0),
                                 (CSolution.swap2adj, 0.6),
                                 (CSolution.swap3, 0.7),
                                 (CSolution.change_lengths, 1.0)]


class CSaMtspSolver(IMtspSolver): # TODO: inherit from sa solver
    TOO_LONG_TOUR_PENALTY = 100

    def __init__(self, params: SSaMtspSolverParams):
        super(IMtspSolver, self).__init__()

        self.nr_nodes = None
        self.nr_tours = None
        self.distance_matrix = None

        self.tour_limit = None

        self.initial_temperature = params.initial_temperature
        self.cooling_rate        = params.cooling_rate
        self.debug               = params.debug

        self.avg_time_per_nodes = None

    def solve(self, distance_matrix, nr_tours, time_limit=float('inf'), tour_limit=float('inf')):

        if len(distance_matrix) != len(distance_matrix[0]):
            raise ValueError('Matrix must be square!')

        self.avg_time_per_nodes = [i[1] * 30 * 60 / 12 for i in NatalityDataReader().read()]

        self.nr_nodes = len(distance_matrix)
        self.nr_tours = nr_tours
        self.distance_matrix = distance_matrix
        self.tour_limit = tour_limit

        best_solution = None
        best_cost = float('inf')

        current_solution = CSolution.generate_random(self.nr_nodes, self.nr_tours)
        current_cost = current_solution.compute_cost(self.distance_matrix, self.tour_limit, self.avg_time_per_nodes)

        iteration = 0

        temperature = self.initial_temperature
        while temperature > 1:

            neighbour, neighbour_cost = current_solution.get_random_neighbour_and_cost(self.distance_matrix,
                                                                                       self.tour_limit,
                                                                                       self.avg_time_per_nodes)

            if neighbour_cost < current_cost or math.exp(
                    (current_cost - neighbour_cost) / temperature) > random.random():

                current_solution, current_cost = neighbour, neighbour_cost

                if current_cost < best_cost:
                    best_solution, best_cost = current_solution, current_cost

            if iteration % 20000 == 0:
                print('Best cost so far: {}, temperature: {}'.format(best_cost, temperature))

            iteration += 1
            temperature *= 1 - self.cooling_rate

        if self.debug:
            print('Evaluated solutions: {}'.format(iteration))
            print('Best cost: {}'.format(best_cost))

        return best_solution, best_cost

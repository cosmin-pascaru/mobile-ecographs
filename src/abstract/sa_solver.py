import random
from abc import ABC, abstractmethod

import math


class SaSolver(ABC):
    MAX_TEMPERATURE = 1000000

    def __init__(self, print_progress_freq = 10000):
        self.temperature = None
        self.cooling_rate = None

        self.best_solution = None
        self.best_cost = None

        self.print_progress_freq = print_progress_freq

    def run_sa(self, cooling_rate):
        self.temperature = self.MAX_TEMPERATURE
        self.cooling_rate = cooling_rate

        self.best_solution = None
        self.best_cost = float('inf')

        iteration = 0

        current_sol, current_cost = self._get_random_sol()

        while self.temperature > 1:

            neighbour, neighbour_cost = self._get_random_neighbour(current_sol)

            if neighbour_cost < current_cost or \
                    math.exp((current_cost - neighbour_cost) / self.temperature) > random.random():

                current_sol, current_cost = neighbour, neighbour_cost

                if current_cost < self.best_cost:
                    self.best_solution, self.best_cost = current_sol, current_cost

            iteration += 1
            self.temperature *= 1 - self.cooling_rate

            if iteration % self.print_progress_freq == 0:
                print('Best cost so far: {}, temperature: {}'.format(self.best_cost, self.temperature))

        print('Evaluated solutions: {}'.format(iteration))
        print('Best cost: {}'.format(self.best_cost))

        return self.best_solution, self.best_cost

    @abstractmethod
    def _get_random_sol(self) -> tuple:
        pass

    @abstractmethod
    def _get_random_neighbour(self, sol) -> tuple:
        pass

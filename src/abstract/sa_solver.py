import random
from abc import ABC, abstractmethod

import math


class CSaSolver(ABC):
    MAX_TEMPERATURE = 1000000

    def __init__(self, print_progress_freq = 1):
        self.__temperature = None
        self.__cooling_rate = None

        self.__best_solution = None
        self.__best_cost = None

        self.__print_progress_freq = print_progress_freq

    def run_sa(self, cooling_rate):
        self.__temperature = self.MAX_TEMPERATURE
        self.__cooling_rate = cooling_rate

        self.__best_solution = None
        self.__best_cost = float('inf')

        iteration = 0

        current_sol, current_cost = self._get_random_sol()

        while self.__temperature > 1:

            neighbour, neighbour_cost = self._get_random_neighbour(current_sol)

            if neighbour_cost < current_cost or \
                    math.exp((current_cost - neighbour_cost) / self.__temperature) > random.random():

                current_sol, current_cost = neighbour, neighbour_cost

                if current_cost < self.__best_cost:
                    self.__best_solution, self.__best_cost = current_sol, current_cost

            iteration += 1
            self.__temperature *= 1 - self.__cooling_rate

            if iteration % self.__print_progress_freq == 0:
                print('Best cost so far: {}, temperature: {}'.format(self.__best_cost, self.__temperature))

        print('Evaluated solutions: {}'.format(iteration))
        print('Best cost: {}'.format(self.__best_cost))

        return self.__best_solution, self.__best_cost

    @abstractmethod
    def _get_random_sol(self) -> tuple:
        """Returns a tuple (sol, cost)"""
        pass

    @abstractmethod
    def _get_random_neighbour(self, sol) -> tuple:
        """Returns a tuple (sol, cost)"""
        pass

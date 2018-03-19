import random
from abc import ABC, abstractmethod

import math


class CSaParams(object):
    def __init__(self,
                 debug                = False,
                 cooling_rate         = None,
                 print_progress_freq  = None,
                 update_best_callback = None,
                 initial_temp         = 1000000):

        self.initial_temp         = initial_temp
        self.debug                = debug
        self.cooling_rate         = cooling_rate
        self.print_progress_freq  = print_progress_freq
        self.update_best_callback = update_best_callback


class ISaSolver(ABC):
    def __init__(self):
        pass

    def run_sa(self, params : CSaParams):
        temperature         = params.initial_temp
        cooling_rate        = params.cooling_rate
        print_progress_freq = params.print_progress_freq

        best_solution = None
        best_cost     = float('inf')

        iteration = 0

        current_sol, current_cost = self._get_initial_sol()

        while temperature > 1:
            neighbour, neighbour_cost = self._get_random_neighbour(current_sol)

            if neighbour_cost < current_cost or \
                    math.exp((current_cost - neighbour_cost) / temperature) > random.random():

                current_sol, current_cost = neighbour, neighbour_cost

                if current_cost < best_cost:
                    best_solution, best_cost = current_sol, current_cost

                    if params.update_best_callback:
                        params.update_best_callback(best_solution, best_cost)

            iteration   += 1
            temperature *= 1 - cooling_rate

            if params.debug and print_progress_freq and iteration % print_progress_freq == 0:
                print('Best cost so far: {}, temperature: {}'.format(best_cost, temperature))

        if params.debug:
            print('SA Evaluated solutions: {}'.format(iteration))
            print('SA Best cost: {}'.format(best_cost))

        return best_solution, best_cost

    @abstractmethod
    def _get_initial_sol(self) -> tuple:
        """Returns a tuple (sol, cost)"""
        pass

    @abstractmethod
    def _get_random_neighbour(self, sol) -> tuple:
        """Returns a tuple (sol, cost)"""
        pass

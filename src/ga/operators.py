import random

from src.common.constants import CONSULT_TIME, MAX_TIME_PER_DAY
from src.ga.individual import Individual
from src.ga.params import TOUR_COST, ON_ROAD_COST_FACTOR, TOO_LONG_TOUR_FACTOR
import src.ga.solver


def evaluate_tour(tour):
    home = 0

    tour_real_locations = [home] + [src.ga.solver.all_visits[i] for i in range(tour[0], tour[1])] + [home]
    total_on_road_time = sum(src.ga.solver.distance_matrix[i][j] for i, j in zip(tour_real_locations[:-1], tour_real_locations[1:]))
    total_on_visits_time = len(tour_real_locations) * CONSULT_TIME

    total_day_time = total_on_road_time + total_on_visits_time

    if total_day_time > MAX_TIME_PER_DAY:
        extra = (total_day_time - MAX_TIME_PER_DAY)
        too_long_tour_penalty = extra * extra * TOO_LONG_TOUR_FACTOR
    else:
        too_long_tour_penalty = 0

    return total_on_road_time * ON_ROAD_COST_FACTOR + too_long_tour_penalty


def evaluate(ind):
    tours = [(0, ind.ends[0])]
    for tour_start, tour_end in zip(ind.ends[:-1], ind.ends[1:]):
        tours.append((tour_start, tour_end))
    tours.append((ind.ends[-1], ind.len_perm))

    total_cost = 0
    total_cost += len(tours) * TOUR_COST
    total_cost += sum(evaluate_tour(t) for t in tours)

    return (total_cost, )


def crossover(ind1, ind2):
    return Individual.cx_perm(ind1, ind2)


mutations = [
    (Individual.mutate_rev         , 0.25),
    (Individual.mutate_swap2       , 0.25),
    (Individual.mutate_swap2_adj   , 0.05),
    (Individual.mutate_update_ends , 0.45)
]


def mutate(ind):
    total_p = 0
    p = random.random()
    for func, prob in mutations:
        total_p += prob
        if total_p <= p:
            return (func(ind), )

    return (mutations[-1][0](ind), )


def create_random_individual(ind_cls, nr_visits, nr_tours):
    return ind_cls(nr_visits, nr_tours, random=True)

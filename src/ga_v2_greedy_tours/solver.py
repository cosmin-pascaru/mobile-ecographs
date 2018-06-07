import random
import numpy as np
import itertools

import time
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from src.common.read_input import read_visits_cnt, read_distance_matrix
from src.ga_v2_greedy_tours.individual import init_individual
from src.ga_v2_greedy_tours.operators import evaluate, crossover, mutate
from src.ga_v2_greedy_tours.params import GA_POP_SIZE, GaType, GA_TYPE, GA_PROB_CROSSOVER, GA_PROB_MUTATION, \
    GA_NR_GENERATIONS, GA_MU, GA_LAMBDA

visits_cnt = read_visits_cnt()
all_visits = [[place_idx] * cnt_visits for place_idx, cnt_visits in enumerate(visits_cnt)]
all_visits = list(itertools.chain.from_iterable(all_visits))

distance_matrix = read_distance_matrix()

creator.create("Fitness", base.Fitness, weights=(-1,))
creator.create("Individual",
               np.ndarray,
               fitness=creator.Fitness,
               __eq__=(lambda self, other: ( np.ndarray.__eq__(self, other).all() )))

a = np.array([1])
b = np.array([1,2,3])

print((a==b).all())

np.ndarray(a)

# __eq__=lambda self, other: ( super(creator.Individual, self).__eq__(self, other).all() )

toolbox = base.Toolbox()

toolbox.register("individual" , init_individual, creator.Individual, len(all_visits))
toolbox.register("population" , tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate"   , evaluate)
toolbox.register("mate"       , crossover)
toolbox.register("mutate"     , mutate)
toolbox.register("select"     , tools.selTournament, tournsize=3)


def run():
    seed = 3458974
    random.seed(seed)
    np.random.seed(seed)

    stats = tools.Statistics(lambda ind: ind.fitness.values)

    stats.register( "min", np.min  )
    stats.register( "max", np.max  )
    stats.register( "avg", np.mean )
    stats.register( "std", np.std  )

    pop = toolbox.population(n=GA_POP_SIZE)
    hof = tools.HallOfFame(1)

    start_time = time.time()

    if GaType.GA_SIMPLE == GA_TYPE:
        pop, log = algorithms.eaSimple(population = pop               ,
                                       toolbox    = toolbox           ,
                                       cxpb       = GA_PROB_CROSSOVER ,
                                       mutpb      = GA_PROB_MUTATION  ,
                                       ngen       = GA_NR_GENERATIONS ,
                                       stats      = stats             ,
                                       halloffame = hof               ,
                                       verbose    = True              )

    elif GaType.GA_MU_LAMBDA == GA_TYPE:
        pop, log = algorithms.eaMuPlusLambda(population = pop               ,
                                             toolbox    = toolbox           ,
                                             cxpb       = GA_PROB_CROSSOVER ,
                                             mutpb      = GA_PROB_MUTATION  ,
                                             ngen       = GA_NR_GENERATIONS ,
                                             mu         = GA_MU             ,
                                             lambda_    = GA_LAMBDA         ,
                                             stats      = stats             ,
                                             halloffame = hof               ,
                                             verbose    = True              )
    else:
        raise RuntimeError("GA type not implemented")

    end_time = time.time()

    print("Time taken: {}".format(end_time - start_time))

__all__ = ["run", "all_visits", "distance_matrix"]

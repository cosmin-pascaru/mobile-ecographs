import random
import numpy as np
import itertools

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from src.common.read_input import read_visits_cnt, read_distance_matrix
from src.ga.individual import Individual
from src.ga.params import GA_POP_SIZE, GA_PROB_CROSSOVER, GA_PROB_MUTATION, GA_NR_GENERATIONS, NR_TOURS
from src.ga.operators import evaluate
from src.ga.operators import crossover
from src.ga.operators import mutate
from src.ga.operators import create_random_individual

visits_cnt = read_visits_cnt()
all_visits = [[place_idx] * cnt_visits for place_idx, cnt_visits in enumerate(visits_cnt)]
all_visits = list(itertools.chain.from_iterable(all_visits))

distance_matrix = read_distance_matrix()

creator.create("Fitness", base.Fitness, weights=(-1.0,))
creator.create("Individual", Individual, fitness=creator.Fitness)

toolbox = base.Toolbox()

toolbox.register("individual" , creator.Individual, nr_visits=len(all_visits), nr_tours=NR_TOURS)
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

    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop = toolbox.population(n=GA_POP_SIZE)
    hof   = tools.HallOfFame(1)

    pop, log = algorithms.eaSimple(population = pop               ,
                                   toolbox    = toolbox           ,
                                   cxpb       = GA_PROB_CROSSOVER ,
                                   mutpb      = GA_PROB_MUTATION  ,
                                   ngen       = GA_NR_GENERATIONS ,
                                   stats      = stats             ,
                                   halloffame = hof               ,
                                   verbose    = True              )

    print(pop)
    print(log)
    print(hof)

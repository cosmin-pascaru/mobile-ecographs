import random
import numpy as np
import itertools

import time
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from src.common.constants import SECONDS_PER_HOUR
from src.common.read_input import read_visits_cnt, read_distance_matrix
from src.ga_v2_greedy_tours.ea import eaMuPlusLambda
from src.ga_v2_greedy_tours.evaluation import evaluate_greedy_tour_selection_tuple
from src.ga_v2_greedy_tours.individual import init_individual
from src.ga_v2_greedy_tours.operators import evaluate, crossover, mutate
from src.ga_v2_greedy_tours.params import GA_POP_SIZE, GaType, GA_TYPE, GA_PROB_CROSSOVER, GA_PROB_MUTATION, \
    GA_NR_GENERATIONS, GA_MU, GA_LAMBDA, GA_POP_LOAD_TYPE, PopulationLoadType, GA_TIME_LIMIT

visits_cnt = read_visits_cnt()
all_visits = [[place_idx] * cnt_visits for place_idx, cnt_visits in enumerate(visits_cnt)]
all_visits = list(itertools.chain.from_iterable(all_visits))

distance_matrix = read_distance_matrix()

creator.create("Fitness", base.Fitness, weights=(-1,))
creator.create("Individual",
               np.ndarray,
               fitness = creator.Fitness,
               __eq__  = (lambda self, other: ( np.ndarray.__eq__(self, other).all() ))
               )

toolbox = base.Toolbox()

toolbox.register( "individual" , init_individual, creator.Individual, len(all_visits) )
toolbox.register( "population" , tools.initRepeat, list, toolbox.individual           )
toolbox.register( "evaluate"   , evaluate                                             )
toolbox.register( "mate"       , crossover                                            )
toolbox.register( "mutate"     , mutate                                               )
toolbox.register( "select"     , tools.selTournament, tournsize=3                     )

def load_population():
    if PopulationLoadType.POP_NEW == GA_POP_LOAD_TYPE:
        return toolbox.population(n = GA_POP_SIZE)

    elif PopulationLoadType.POP_LOAD_FILE == GA_POP_LOAD_TYPE:
        assert False


def save_population(pop):
    pass


def run_test_permutation_evaluation():
    perm = [321, 322, 323, 324, 325, 326, 199, 200, 201, 202, 203, 204, 205, 206, 212, 213, 214, 215, 216, 217, 218,
            219, 220, 221, 389, 390, 391, 392, 393, 100, 101, 102, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403,
            404, 405, 388, 526, 45, 46, 47, 48, 49, 370, 371, 372, 373, 543, 544, 545, 546, 7, 8, 9, 364, 365, 366, 367,
            368, 547, 548, 549, 550, 551, 552, 553, 554, 103, 104, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265,
            266, 387, 95, 96, 97, 98, 369, 527, 528, 529, 530, 179, 180, 181, 182, 183, 184, 99, 222, 223, 224, 225,
            226, 227, 228, 229, 230, 519, 520, 521, 522, 523, 524, 525, 267, 268, 269, 270, 271, 272, 273, 274, 165,
            166, 167, 168, 169, 253, 254, 255, 23, 80, 81, 82, 83, 84, 85, 86, 87, 88, 381, 382, 383, 384, 385, 386, 24,
            25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 376, 377, 378, 379, 380, 327, 328, 329,
            330, 331, 116, 117, 118, 105, 106, 5, 6, 557, 558, 559, 560, 561, 502, 503, 504, 505, 506, 507, 508, 191,
            192, 193, 194, 195, 196, 174, 175, 176, 177, 178, 170, 171, 172, 173, 62, 63, 64, 65, 66, 67, 68, 69, 110,
            111, 112, 113, 114, 115, 356, 357, 358, 359, 360, 361, 362, 363, 275, 276, 277, 278, 155, 156, 16, 17, 18,
            420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 298, 299, 300, 301, 19, 20, 21, 22, 431, 432, 433,
            434, 435, 436, 484, 485, 486, 487, 488, 489, 490, 491, 492, 496, 497, 498, 499, 500, 501, 131, 132, 133,
            134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 57, 58, 59, 60, 61, 207, 208, 279, 280, 281, 282,
            283, 374, 375, 231, 232, 233, 234, 235, 0, 1, 2, 3, 531, 532, 240, 241, 242, 243, 412, 413, 414, 149, 150,
            151, 152, 75, 76, 77, 78, 79, 148, 157, 158, 159, 160, 161, 162, 163, 164, 187, 188, 189, 190, 314, 315,
            316, 317, 415, 416, 417, 418, 419, 318, 319, 236, 237, 238, 239, 493, 494, 495, 320, 562, 563, 564, 565,
            566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 509, 510, 511, 512, 513, 514, 515, 516, 517,
            518, 209, 210, 211, 119, 120, 121, 122, 70, 71, 72, 308, 309, 310, 311, 312, 313, 437, 438, 439, 440, 441,
            145, 146, 147, 10, 11, 12, 123, 124, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297,
            406, 407, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 555, 556, 245, 246, 247, 248, 453, 454,
            455, 456, 457, 458, 459, 460, 461, 50, 51, 52, 53, 54, 55, 56, 302, 303, 304, 305, 306, 307, 4, 332, 333,
            334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 13, 14, 15, 462, 463, 464, 465, 466, 467, 468, 469,
            470, 471, 345, 346, 347, 348, 349, 350, 89, 90, 91, 92, 93, 94, 477, 478, 479, 480, 481, 482, 483, 533, 534,
            535, 536, 537, 538, 125, 126, 127, 128, 129, 130, 475, 476, 578, 579, 580, 581, 582, 42, 43, 44, 472, 473,
            474, 351, 352, 353, 354, 355, 73, 74, 249, 250, 251, 252, 539, 540, 541, 542, 185, 186, 197, 198, 107, 108,
            109, 153, 154, 244, 408, 409, 410, 411]

    score = evaluate(perm)

    print('SCORE IS... {}'.format(score))


def run():
    seed = random.randint(0, (1 << 30))
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

    if GA_TIME_LIMIT is not None:
        GA_NR_GENERATIONS = (1 << 30)

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

        pop, log = eaMuPlusLambda(population       = pop                  ,
                                  toolbox          = toolbox              ,
                                  cxpb             = GA_PROB_CROSSOVER    ,
                                  mutpb            = GA_PROB_MUTATION     ,
                                  ngen             = GA_NR_GENERATIONS    ,
                                  mu               = GA_MU                ,
                                  lambda_          = GA_LAMBDA            ,
                                  stats            = stats                ,
                                  halloffame       = hof                  ,
                                  verbose          = True                 ,
                                  time_limit       = GA_TIME_LIMIT        ,
                                  print_best_delay = 1000                 )
    else:
        raise RuntimeError("GA type not implemented")

    end_time = time.time()

    best = hof.items[0]
    score = evaluate_greedy_tour_selection_tuple(best)

    with open('data/runs_ga_{}_{}_{}'.format(GA_POP_SIZE, GA_PROB_CROSSOVER, GA_PROB_MUTATION), 'a') as f:
        f.write('{} {}\n'.format(*score))

    print("Time taken: {}".format(end_time - start_time))

__all__ = ["run", "all_visits", "distance_matrix"]

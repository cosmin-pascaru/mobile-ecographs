from enum import Enum, auto


class GaType(Enum):
    GA_SIMPLE    = auto()
    GA_MU_LAMBDA = auto()


class PopulationLoadType(Enum):
    POP_NEW       = auto()
    POP_LOAD_BEST = auto()
    POP_LOAD_FILE = auto()

#############################
GA_TYPE = GaType.GA_MU_LAMBDA
#############################

GA_POP_SAVE_FOLDER = 'data/ga/populations'
GA_POP_LOAD_FOLDER = GA_POP_SAVE_FOLDER
GA_POP_LOAD_TYPE   = PopulationLoadType.POP_LOAD_BEST
GA_POP_FILE        = None

GA_POP_BASENAME    = 'pop'
GA_POP_EXTENSION   = '.pkl'

GA_IND_SAVE_FOLDER = 'data/ga/best_individuals'

#############################

GA_POP_SIZE       = 150
GA_PROB_CROSSOVER = 0.6
GA_PROB_MUTATION  = 0.2
GA_NR_GENERATIONS = 10000

# Only used by GA_MU_LAMBDA
GA_MU     = GA_POP_SIZE
GA_LAMBDA = 2 * GA_MU
###########################

###########################
CX_UPMX_IND_PROB = 0.05
###########################

# Crossover distribution

CX_UPMX_PROB = 0.33
CX_PMX_PROB  = 0.33
CX_OX_PROB   = 0.34

# Mutation distribution

MUT_REV_SUBSEQ_PROB = 0.25
MUT_SWAP_2_PROB     = 0.75
MUT_SHUFFLE_PROB    = 0.00  # TODO: change, and observe results

###########################

TOUR_COST            = 10000000
ON_ROAD_COST_FACTOR  = 1
TOO_LONG_TOUR_FACTOR = 100


ASSERTS_ACTIVE = True

# RESULTS:
# 10000 generations - 1 hour - 63 tours
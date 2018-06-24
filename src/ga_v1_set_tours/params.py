from enum import Enum, auto


class GaType(Enum):
    GA_SIMPLE    = auto()
    GA_MU_LAMBDA = auto()


#############################
GA_TYPE = GaType.GA_MU_LAMBDA
#############################

GA_POP_SIZE       = 150
GA_PROB_CROSSOVER = 0.6
GA_PROB_MUTATION  = 0.2
GA_NR_GENERATIONS = 1500

# Only used by GA_MU_LAMBDA
GA_MU     = GA_POP_SIZE
GA_LAMBDA = 2 * GA_MU
###########################

NR_TOURS = 75

TOUR_COST            = 0
ON_ROAD_COST_FACTOR  = 1
TOO_LONG_TOUR_FACTOR = 100

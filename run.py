import math
import os
import random

import sys

from src.abstract.tour_selector import TourSelector
from src.concrete.greedy_planner import GreedyPlanner
from src.concrete.planning_manager import Manager
from src.concrete.planning_scorer_v1 import PlanningScorerV1
from src.concrete.sa_tour_selector import SaTourSelector
from src.input.planning_input import PlanningInput
from src.params.manager_params import ManagerParams
from src.params.planner_params import PlannerParams
from src.params.planning_scorer_params import PlanningScorerParams
from src.params.tour_selector_params import TourSelectorParams
from src.utils import SECONDS_PER_MINUTE
from src.utils import SECONDS_PER_HOUR

# seed = random.randint(0, (1 << 30))
seed = int(open('data/last_seed.txt', 'r').read().strip())
# seed = 475065778

random.seed(seed)
with open('data/last_seed.txt', 'w') as f:
    f.write(str(seed))

# Init struct
data = Manager.InitStruct()

# Tours
tours = list(map(lambda line: list(map(int, line.split())), open('data/tours/good_tours.txt', 'r').readlines()))
data.tours = tours

# Input
inp = PlanningInput()

places_names = tuple(map(lambda line: (' '.join(line.split()[1:])).title(), open('data/lista_comune.txt').readlines()))
places_suffix = ', Iasi, Romania'

inp.places_names = places_names
inp.places_suffix = places_suffix

inp.consult_time = 30 * SECONDS_PER_MINUTE
inp.max_time_per_day = 10 * SECONDS_PER_HOUR
inp.cnt_days = 21
inp.cnt_cars = 2

# Number of visits per place
visits_cnts = list(map(lambda line: math.ceil(int(line.split()[-1]) * 7 / 12), open('data/populatie_ajustata.txt', 'r').readlines()))
print('Total visits to do: {}'.format(sum(visits_cnts)))
inp.consults_per_node = visits_cnts

# Distance matrix
dm = eval(open('data/times.txt', 'r').read())
inp.distance_matrix = dm

# Set input
data.input = inp

# Tour selector
tour_sel_params = TourSelectorParams()
tour_sel_params.sa_cooling_rate = 0.01
tour_sel_params.debug = True

data.tour_selector_cls = SaTourSelector
data.tour_selector_params = tour_sel_params

# Planner
planner_params = PlannerParams()
planner_params.debug = False
planner_params.write_best_plan = True

data.planner_cls = GreedyPlanner
data.planner_params = planner_params

# Scorer
scorer_params = PlanningScorerParams()
scorer_params.debug = False

data.scorer_cls = PlanningScorerV1
data.scorer_params = scorer_params

# Manager params
manager_params = ManagerParams()
manager_params.debug = False
manager_params.maps_api_key = open('data/googleapi_key.txt', 'r').read().strip()
manager_params.tour_template_file = 'data/html/templates/tour_template.html'
manager_params.index_template_file = 'data/html/templates/index_template.html'

data.manager_params = manager_params

# Manager instantiation
manager = Manager(data)

manager.run()

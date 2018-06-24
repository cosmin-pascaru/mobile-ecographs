import math
import random

from src.alg.concrete.disabled_tour_selector import DisabledTourSelector
from src.alg.concrete.planning_manager import Manager, SManagerInput
from src.alg.concrete.sa_tour_selector import SaTourSelector
from src.alg.concrete.simple_planning_scorer import SimplePlanningScorer
from src.alg.params.manager_params import ManagerParams
from src.alg.params.planner_params import PlannerParams
from src.alg.params.tour_selector_params import DisabledTourSelectorParams, SaTourSelectorParams

from src.alg.concrete.greedy_planner import GreedyPlanner
from src.alg.input.planning_input import PlanningInput
from src.alg.params.planning_scorer_params import PlanningScorerParams
from src.common.read_input import read_visits_cnt, read_distance_matrix

seed = random.randint(0, (1 << 30))
# seed = int(open('data/last_seed.txt', 'r').read().strip())
# seed = 475065778

random.seed(seed)
with open('data/last_seed.txt', 'w') as f:
    f.write(str(seed))

# Init struct
data = SManagerInput()

# Tours
tours = list(map(lambda line: list(map(int, line.split())), open('data/tours/good_tours.txt', 'r').readlines()))
data.tours = tours

# Input
inp = PlanningInput()

places_names = tuple(map(lambda line: (' '.join(line.split()[1:])).title(), open('data/lista_comune.txt').readlines()))
places_suffix = ', Iasi, Romania'

inp.places_names = places_names
inp.places_suffix = places_suffix
inp.cnt_days = 21
inp.cnt_cars = 2

# Number of visits per place
visits_cnts = read_visits_cnt()
print('Total visits to do: {}'.format(sum(visits_cnts)))
inp.consults_per_node = visits_cnts

# Distance matrix
inp.distance_matrix = read_distance_matrix()

# Set input
data.input = inp

# Tour selector

USE_SA_TOUR_SELECTOR       = False
USE_DISABLED_TOUR_SELECTOR = not USE_SA_TOUR_SELECTOR

if USE_SA_TOUR_SELECTOR:
    tour_sel_params = SaTourSelectorParams()
    tour_sel_params.debug = True
    tour_sel_params.sa_params.cooling_rate = 0.01

    data.tour_selector_cls = SaTourSelector
    data.tour_selector_params = tour_sel_params

elif USE_DISABLED_TOUR_SELECTOR:
    tour_sel_params = DisabledTourSelectorParams()
    tour_sel_params.debug = True
    tour_sel_params.cnt_iterations = None
    tour_sel_params.max_time = 20

    data.tour_selector_cls = DisabledTourSelector
    data.tour_selector_params = tour_sel_params

# Planner
planner_params = PlannerParams()
planner_params.debug = False
planner_params.write_best_plan = True
planner_params.cnt_iterations = 1
planner_params.keep_percent = 0.2  # default used
# planner_params.keep_percent = 0.4  # large

data.planner_cls = GreedyPlanner
data.planner_params = planner_params

# Scorer
scorer_params = PlanningScorerParams()
scorer_params.debug = False

data.scorer_cls = SimplePlanningScorer
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

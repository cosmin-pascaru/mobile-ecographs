from src.concrete.tours_finder import CToursFinder, CToursFinderParams
from src.concrete.sa_mtsp_solver import CSaMtspSolverParams, CSaMtspSolver
from src.concrete.tours_writer import CToursWriter
from src.params.constants import MAX_TIME_ON_ROAD

with open('data/times.txt', 'r') as f:
    distance_matrix = eval(f.read())

tours_finder_params = CToursFinderParams()

tours_finder_params.distance_matrix = distance_matrix
tours_finder_params.min_cnt_tours = 20
tours_finder_params.debug = True

mtsp_solver        = CSaMtspSolver()
mtsp_solver_params = CSaMtspSolverParams()

mtsp_solver_params.mtsp_params.distance_matrix = distance_matrix
mtsp_solver_params.mtsp_params.tour_time_limit = MAX_TIME_ON_ROAD
mtsp_solver_params.mtsp_params.nr_mtsp_tours   = 5

mtsp_solver_params.sa_params.debug               = True
mtsp_solver_params.sa_params.print_progress_freq = None
mtsp_solver_params.sa_params.cooling_rate        = 0.001

tours = CToursFinder().compute_tours(tours_finder_params, mtsp_solver, mtsp_solver_params)

# CToursWriter().write_plain(tours, 'tmp.txt', 'a')


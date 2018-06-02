from src.concrete.sa_mtsp_solver import CSaMtspSolverParams, CSaMtspSolver, CMtspSolverParams

from src.alg.abstract import CSaParams
from src.alg.concrete.tours_finder import CToursFinder, CToursFinderParams
from src.common.constants import MAX_TIME_ON_ROAD

with open('data/times.txt', 'r') as f:
    distance_matrix = eval(f.read())

tours_finder_params = CToursFinderParams(distance_matrix, min_cnt_tours = 20, debug = True)
mtsp_params         = CMtspSolverParams(distance_matrix, nr_mtsp_tours = 5, tour_time_limit = MAX_TIME_ON_ROAD)
sa_params           = CSaParams(cooling_rate = 0.001, debug = True, print_progress_freq = None)

sa_mtsp_solver        = CSaMtspSolver()
sa_mtsp_solver_params = CSaMtspSolverParams(sa_params=sa_params, mtsp_params=mtsp_params)

tours = CToursFinder().compute_tours(tours_finder_params, sa_mtsp_solver, sa_mtsp_solver_params)

# CToursWriter().write_plain(tours, 'tmp.txt', 'a')


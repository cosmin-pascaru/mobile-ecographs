from NatalityDataReader import NatalityDataReader

from src.concrete.tours_finder import CToursFinder
from src.concrete.sa_mtsp_solver import CSaMtspSolverParams

print(NatalityDataReader().read())

mtsp_solver_params = CSaMtspSolverParams(100000, 0.000025)
CToursFinder().compute_tours(2, mtsp_solver_params)

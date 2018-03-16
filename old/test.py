from NatalityDataReader import NatalityDataReader

from src.concrete.sa_mtsp_solver import SSaMtspSolverParams
from old.ToursFinder import ToursFinder

print(NatalityDataReader().read())

mtsp_solver_params = SSaMtspSolverParams(100000, 0.000025)
ToursFinder().compute_tours(2, mtsp_solver_params)

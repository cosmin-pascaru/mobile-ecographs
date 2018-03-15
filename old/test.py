from NatalityDataReader import NatalityDataReader

from mtsp_solvers.SaMtspSolver import SaMtspSolverParams
from old.ToursFinder import ToursFinder

print(NatalityDataReader().read())

mtsp_solver_params = SaMtspSolverParams(100000, 0.000025)
ToursFinder().compute_tours(2, mtsp_solver_params)

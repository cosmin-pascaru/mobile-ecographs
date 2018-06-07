import numpy as np

from src.ga_v2_greedy_tours.params import ASSERTS_ACTIVE


def init_individual(cls, nr_visits):
    perm = np.random.permutation(nr_visits)

    ind = cls(perm)

    return ind


if ASSERTS_ACTIVE:
    def assert_valid(ind):
            sorted_ind = np.sort(ind)

            assert all(i == val for i, val in enumerate(sorted_ind))
else:
    def assert_valid(ind):
        pass


__all__ = ["assert_valid", "init_individual"]
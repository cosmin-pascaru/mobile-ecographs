import random

import numpy as np

from src.ga_v2_greedy_tours.params import ASSERTS_ACTIVE
import itertools


def init_individual(cls, visits_cnts):
    PROB_FULL_RANDOM = 0.0
    MAX_CNT = 15

    nr_visits = sum(visits_cnts)

    if random.random() < PROB_FULL_RANDOM:
        perm = np.random.permutation(nr_visits)
    else:
        all_visits = []
        for place_idx, cnt_visits in enumerate(visits_cnts):
            all_visits.extend(([place_idx] * MAX_CNT for _ in range(0, cnt_visits // MAX_CNT)))
            all_visits.append([place_idx] * (cnt_visits % MAX_CNT))

        all_visits_perm = []
        curr_total = 0
        for v in all_visits:
            all_visits_perm.append([curr_total + i for i in range(len(v))])
            curr_total += len(v)

        random.shuffle(all_visits_perm)

        perm = list(itertools.chain.from_iterable(all_visits_perm))

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
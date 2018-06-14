import random
import numpy as np


def _choose_2_rand_idx(ind):
    i = random.randrange(0, len(ind))
    j = random.randrange(0, len(ind))

    if (i > j):
        i, j = j, i

    return i, j


def shuffle(ind):
    i, j = _choose_2_rand_idx(ind)
    np.random.shuffle(ind[i:j])
    return ind


def reverse_subsequence(ind : np.ndarray):
    i, j = _choose_2_rand_idx(ind)
    ind[i:j] = np.flip(ind[i:j], 0)

    return ind


def swap2(ind):
    i, j = _choose_2_rand_idx(ind)
    ind[i], ind[j] = ind[j], ind[i]
    return ind



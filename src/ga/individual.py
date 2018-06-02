import random

import copy
import numpy as np


class Individual(object):
    def __init__(self, perm=None, ends=None, nr_visits=None, nr_tours=None):
        self.perm     = None
        self.ends     = None
        self.len_perm = None
        self.len_ends = None

        # Ends are exclusive:
        # len(ends) = number of tours - 1

        # ends = [e0, e1, e2, ..., ek-1]

        # t0: [0, 1, ..., e0 - 1]
        # t1: [e0, e0 + 1, ..., e2 - 1]
        # ...
        # tk-1: [ek-2, ek-2 + 1, ..., ek-1 - 1]
        # tk:  [ek-1, ek-1 + 1, ..., n - 1]
        # n = len(perm)

        if perm and ends:
            self.init_full(perm, ends)
        elif nr_visits and nr_tours:
            self.init_random(nr_visits, nr_tours)
        else:
            assert False

        self._assert_is_valid()



    def init_full(self, perm, ends):
        self.perm = perm
        self.ends = ends

        self.len_perm = len(self.perm)
        self.len_ends = len(self.ends)

        self._assert_is_valid()

    def init_random(self, nr_visits, nr_tours):
        self.perm = np.random.permutation(nr_visits)

        self.ends = np.random.randint(0, len(self.perm), nr_tours - 1, dtype=np.int32)
        self.ends . sort()

        self.len_perm = len(self.perm)
        self.len_ends = len(self.ends)

        self._assert_is_valid()

    def mutate_swap2(self):
        i, j = random.randrange(0, self.len_perm), random.randrange(0, self.len_perm)
        self.perm[i], self.perm[j] = self.perm[j], self.perm[i]

        self._assert_is_valid()

        return self

    def mutate_rev(self):
        i = random.randrange(0, self.len_perm)
        j = random.randrange(i, self.len_perm + 1)

        self.perm[i:j] = np.flip(self.perm[i:j], 0)

        self._assert_is_valid()

        return self

    def mutate_swap2_adj(self):
        i = random.randrange(0, self.len_perm - 1)
        self.perm[i], self.perm[i + 1] = self.perm[i + 1], self.perm[i]

        self._assert_is_valid()

        return self

    def mutate_update_ends(self):
        i = random.randrange(0, self.len_ends)

        left  = self.ends[i - 1]     if i > 0                 else 1
        right = self.ends[i + 1] + 1 if i < self.len_ends - 1 else self.len_perm

        self.ends[i] = random.randrange(left, right)

        self._assert_is_valid()

        return self

    @staticmethod
    def cx_perm(ind1, ind2):
        ind1._assert_is_valid()
        ind2._assert_is_valid()

        return Individual._cx_perm_single(ind1, ind2), \
               Individual._cx_perm_single(ind2, ind1)

    @staticmethod
    def _cx_perm_single(ind1, ind2):
        assert ind1.len_perm == ind2.len_perm

        ind1._assert_is_valid()
        ind2._assert_is_valid()

        len_perm = ind1.len_perm

        idx_left  = random.randrange(0,            ind1.len_perm    )
        idx_right = random.randrange(idx_left + 1, ind1.len_perm + 1)

        in_ind1 = np.zeros(len_perm, dtype=np.bool)

        for i in range(idx_left, idx_right):
            in_ind1[ind1.perm[i]] = True

        child_perm = np.repeat(-1, len_perm)
        child_ends = ind1.ends if random.random() < 0.5 else ind2.ends

        ind2_idx = 0

        for child_idx in range(0, idx_left):
            while in_ind1[ind2.perm[ind2_idx]]:
                ind2_idx += 1

            child_perm[child_idx] = ind2.perm[ind2_idx]
            ind2_idx += 1

        child_perm[idx_left : idx_right] = ind1.perm[idx_left : idx_right]

        for child_idx in range(idx_right, len_perm):
            while in_ind1[ind2.perm[ind2_idx]]:
                ind2_idx += 1
            child_perm[child_idx] = ind2.perm[ind2_idx]
            ind2_idx += 1

        child = copy.copy(ind1)

        child.perm = child_perm
        child.ends = child_ends
        child.len_perm = len(child.perm)
        child.len_ends = len(child.ends)

        child._assert_is_valid()

        return child

    def _assert_is_valid(self):

        # TODO: make this do nothing

        assert (self.len_perm == len(self.perm))
        assert (self.len_ends == len(self.ends))

        sorted_perm = np.sort(self.perm)

        assert (all(i == sorted_perm[i] for i in range(len(sorted_perm))))
        assert (all(prv <= nxt for prv, nxt in zip(self.ends[:-1], self.ends[1:])))





# a = np.array([1,2,3,4,5,6])
# a[1:5] = np.flip(a[1:5], 0)
# print(a)
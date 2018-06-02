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


    def init_full(self, perm, ends):
        self.perm = perm
        self.ends = ends

        self.len_perm = len(self.perm)
        self.len_ends = len(self.ends)

    def init_random(self, nr_visits, nr_tours):
        self.perm = np.random.permutation(nr_visits)
        self.ends = np.random.randint(0, len(self.perm), nr_tours - 1, dtype=np.int32)

        self.len_perm = len(self.perm)
        self.len_ends = len(self.ends)

    def mutate_swap2(self):
        i, j = random.randrange(0, self.len_perm), random.randrange(0, self.len_perm)
        self.perm[i], self.perm[j] = self.perm[j], self.perm[i]

        return self

    def mutate_rev(self):
        i = random.randrange(0, self.len_perm)
        j = random.randrange(i, self.len_perm + 1)

        self.perm[i:j] = np.flip(self.perm[i:j], 0)
        return self

    def mutate_swap2_adj(self):
        i = random.randrange(0, self.len_perm - 1)
        self.perm[i], self.perm[i + 1] = self.perm[i + 1], self.perm[i]
        return self

    def mutate_update_ends(self):
        i = random.randrange(0, self.len_ends)

        left  = self.ends[i - 1]     if i > 0                 else 1
        right = self.ends[i + 1] + 1 if i < self.len_ends - 1 else self.len_perm

        print(left, right)
        self.ends[i] = random.randrange(left, right)
        return self

    @staticmethod
    def cx_perm(ind1, ind2):
        return Individual._cx_perm_single(ind1, ind2), \
               Individual._cx_perm_single(ind2, ind1)

    @staticmethod
    def _cx_perm_single(ind1, ind2):
        assert ind1.len_perm == ind2.len_perm

        len_perm = ind1.len_perm

        idx_left  = random.randrange(0,            ind1.len_perm    )
        idx_right = random.randrange(idx_left + 1, ind1.len_perm + 1)

        in_ind1 = np.zeros(len_perm, dtype=np.bool)

        for i in range(idx_left, idx_right):
            in_ind1[ind1.perm[i]] = True

        child_perm = np.copy(ind1.perm)
        child_ends = ind1.ends if random.random() < 0.5 else ind2.ends

        ind2_idx = 0

        cnt_true  = sum(1 if i > 0  else 0 for i in in_ind1)
        cnt_false = sum(1 if i <= 0 else 0 for i in in_ind1)
        cnt       = len(in_ind1)

        print(cnt_true)
        print(cnt_false)
        print(cnt)
        print(cnt_true + cnt_false)
        print()

        print('lft', idx_left)
        print('rgt', idx_right)
        print("perm", len_perm)

        for child_idx in range(0, idx_left):
            try:
                while in_ind1[ind2.perm[ind2_idx]]:
                    ind2_idx += 1
            except Exception:
                print("ind2_idx", ind2_idx)
                raise

            child_perm[child_idx] = ind2.perm[ind2_idx]

        child_perm[idx_left : idx_right] = ind1.perm[idx_left : idx_right]

        for child_idx in range(idx_right, len_perm):
            while in_ind1[ind2.perm[ind2_idx]]:
                ind2_idx += 1
            child_perm[child_idx] = ind2.perm[ind2_idx]

        child = copy.copy(ind1)
        child.perm = child_perm
        child.ends = child_ends

        return child

# a = np.array([1,2,3,4,5,6])
# a[1:5] = np.flip(a[1:5], 0)
# print(a)
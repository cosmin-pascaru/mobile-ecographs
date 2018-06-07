import random

import functools

from src.ga_v2_greedy_tours.crossovers import cx_pmx, cx_ox, cx_upmx
import src.ga_v2_greedy_tours.evaluation
from src.ga_v2_greedy_tours.mutations import reverse_subsequence as mut_rev_subseq, swap2 as mut_swap2
from src.ga_v2_greedy_tours.params import CX_OX_PROB, CX_PMX_PROB, CX_UPMX_PROB, MUT_REV_SUBSEQ_PROB, MUT_SWAP_2_PROB

evaluate_greedy_tour_selection = src.ga_v2_greedy_tours.evaluation.evaluate_greedy_tour_selection


def evaluate(ind):
    return evaluate_greedy_tour_selection(ind)


def _to_tuple(f, *args, **kwargs):
    return (f(*args, **kwargs), )


def _apply_weighted_random_func(func_arr, *args):
    total_p = 0
    p = random.random()
    for func, prob in func_arr:
        total_p += prob
        if total_p <= p:
            return func(*args)

    func, prob = func_arr[-1]
    return func(*args)


mutations = [
    (mut_rev_subseq, MUT_REV_SUBSEQ_PROB),
    (mut_swap2,      MUT_SWAP_2_PROB)
]

crossovers = [
    (cx_ox,   CX_OX_PROB),
    (cx_pmx,  CX_PMX_PROB),
    (cx_upmx, CX_UPMX_PROB)
]

mutate    = functools.partial( _to_tuple , _apply_weighted_random_func , mutations  )
crossover = functools.partial(             _apply_weighted_random_func , crossovers )

__all__ = ["evaluate", "mutate", "crossover"]

import random
import functools

from deap.tools import cxPartialyMatched as deap_pmx
from deap.tools import cxUniformPartialyMatched as deap_upmx
from deap.tools import cxOrdered as deap_ox

import src.ga_v2_greedy_tours.individual
from src.ga_v2_greedy_tours.params import CX_UPMX_IND_PROB

assert_valid_individual = src.ga_v2_greedy_tours.individual.assert_valid


def _deap_cx_wrapper(cx_func, ind1, ind2):
    ind1, ind2 = cx_func(ind1, ind2)

    assert_valid_individual(ind1)
    assert_valid_individual(ind2)

    return ind1, ind2

deap_upmx_set_prob = functools.partial(deap_upmx, indpb = CX_UPMX_IND_PROB)

cx_pmx = functools.partial(_deap_cx_wrapper, deap_pmx)
cx_upmx = functools.partial(_deap_cx_wrapper, deap_upmx_set_prob)
cx_ox = functools.partial(_deap_cx_wrapper, deap_ox)

__all__ = ["cx_ox", "cx_pmx", "cx_upmx"]
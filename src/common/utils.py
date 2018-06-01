import datetime
import random

from src.alg.params.constants import SECONDS_PER_HOUR, SECONDS_PER_MINUTE


def ceil_div(a, b):
    return (a + b - 1) // b


def sec_to_str(seconds):
    h = seconds // SECONDS_PER_HOUR
    m = (seconds % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE

    h_str = '{} ore'.format(h) if h > 0 else ''
    si    = ' si ' if (h > 0) and (m > 0) else ''
    m_str = '{} minute'.format(m) if m > 0 or (m == 0 and h == 0) else ''

    return "{}{}{}".format(h_str, si, m_str)


def weighted_choice(choices):
    if not choices:
        return None

    total = sum(weight for choice, weight in choices)
    prob = random.uniform(0.0, total)
    partial_sum = 0.0
    for choice, weight in choices:
        if partial_sum + weight >= prob:
            return choice
        partial_sum += weight

    return choices[-1][0]


def list_sub(a, b):
    """Returns a list containing x - y, for every (x, y) in zip(a, b)"""
    return list(x - y for x, y in zip(a, b))


def today_as_str():
    months = ['',
              'Ianuarie',
              'Februarie',
              'Martie',
              'Aprilie',
              'Mai',
              'Iunie',
              'Iulie',
              'August',
              'Septembrie',
              'Octombrie',
              'Noiembrie',
              'Decembrie']

    today = datetime.datetime.today()
    return '{} {}'.format(today.day, months[today.month])

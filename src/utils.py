import random


SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR   = 60 * 60

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
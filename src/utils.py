import random


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
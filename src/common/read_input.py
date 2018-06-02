import math

def read_visits_cnt():
    return list(map(lambda line: math.ceil(int(line.split()[-1]) * 7 / 12),
                           open('data/populatie_ajustata.txt', 'r').readlines()))


def read_distance_matrix():
    return eval(open('data/times.txt', 'r').read())
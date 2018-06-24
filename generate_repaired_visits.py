import math

from src.common.constants import CONSULT_TIME

filename = "data/runs_ga_smart_100_0.6_0.3_300"
with open(filename, 'r') as f:
    lines = f.readlines()

    total_nr_tours = 0
    total_dist = 0

    for line in lines:
        nr_tours, dist = tuple(map(int, line.split()))
        total_nr_tours += nr_tours
        total_dist += dist

    n = len(lines)
    print(total_nr_tours / n, '&',  total_dist / n)

exit(0)

with open('data/populatie_ajustata_normalizata.txt', 'w') as g:
    with open('data/populatie_ajustata.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            split = line.split()

            text = " ".join(split[:-1])
            val  = math.ceil(int(split[-1]) * 7 / 12)

            g.write("{} {}\n".format(text, val))


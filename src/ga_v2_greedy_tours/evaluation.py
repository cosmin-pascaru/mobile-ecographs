from src.common.constants import CONSULT_TIME, MAX_TIME_PER_DAY
from src.ga_v2_greedy_tours.params import TOUR_COST
import src.ga_v2_greedy_tours
import src.ga_v2_greedy_tours.solver

def _compute_tours_greedy(ind):

    distance_matrix = src.ga_v2_greedy_tours.solver.distance_matrix
    all_visits      = src.ga_v2_greedy_tours.solver.all_visits

    all_tours = []
    home = 0

    curr_tour = [home]
    curr_dist = 0

    def reset_curr_tour():
        nonlocal curr_tour
        nonlocal curr_dist

        curr_tour = [home]
        curr_dist = 0

    def finish_curr_tour():
        nonlocal curr_tour
        nonlocal curr_dist

        curr_dist += distance_matrix[curr_tour[-1]][home]
        curr_tour.append(home)

    def add_to_curr_tour(new_location):
        nonlocal curr_tour
        nonlocal curr_dist

        curr_dist += distance_matrix[curr_tour[-1]][new_location] + CONSULT_TIME
        curr_tour.append(new_location)

    def can_add_to_curr_tour(new_location):
        nonlocal curr_tour
        nonlocal curr_dist

        return curr_dist + \
               distance_matrix[curr_tour[-1]][new_location] + \
               CONSULT_TIME + \
               distance_matrix[new_location][home] <= MAX_TIME_PER_DAY

    def add_curr_tour_to_all_tours():
        nonlocal curr_tour
        nonlocal curr_dist
        nonlocal all_tours

        all_tours.append((curr_tour, curr_dist))

    ##################################################

    for location_idx in ind:
        location = all_visits[location_idx]

        if can_add_to_curr_tour(location):
            add_to_curr_tour(location)
        else:
            finish_curr_tour()

            add_curr_tour_to_all_tours()

            reset_curr_tour()

    if curr_dist > 0:
        # curr tour is not empty
        finish_curr_tour()
        add_curr_tour_to_all_tours()

    return all_tours


least_tours_so_far = float('inf')

def evaluate_greedy_tour_selection(ind):
    all_tours = _compute_tours_greedy(ind)

    total_dist = sum(dist for _, dist in all_tours)
    tours_count_penalty = len(all_tours) * TOUR_COST

    total_cost = total_dist + tours_count_penalty

    global least_tours_so_far

    if len(all_tours) < least_tours_so_far:
        least_tours_so_far = len(all_tours)
        print("LEAST TOURS SO FAR: {}".format(least_tours_so_far))

    return (total_cost, )


def asdfasdf():
    pass
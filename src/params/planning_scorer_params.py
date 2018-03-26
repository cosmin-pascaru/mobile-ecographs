
class CPlanningScorerParams:
    def __init__(self, debug=False, tour_cost=5000, car_cost=10000, road_cost_factor=1):
        self.debug            = debug
        self.car_cost         = car_cost
        self.not_visited_cost = 100000
        self.road_cost_factor = road_cost_factor
        self.tour_cost        = tour_cost

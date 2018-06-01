
class CPlanningScorerParams:
    def __init__(self, debug=False, tour_cost=100000000, road_cost_factor=1, consult_time_factor=1):
        self.debug               = debug
        self.road_cost_factor    = road_cost_factor
        self.consult_time_factor = consult_time_factor
        self.tour_cost           = tour_cost

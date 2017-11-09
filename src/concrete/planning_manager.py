from src.concrete.maps_url import MapsUrl


class Manager:

    class InitStruct:
        def __init__(self):
            self.input = None

            self.manager_params = None

            self.tours = None

            self.tour_selector_cls = None
            self.tour_selector_params = None

            self.planner_cls = None
            self.planner_params = None

            self.scorer_cls = None
            self.scorer_params = None

    def __init__(self, init_struct : InitStruct):
        self.input = init_struct.input
        self.params = init_struct.manager_params

        self.scorer = init_struct.scorer_cls(manager=self,
                                             input=init_struct.input,
                                             params=init_struct.scorer_params)
        self.planner = init_struct.planner_cls(manager=self,
                                               input=init_struct.input,
                                               params=init_struct.planner_params,
                                               scorer=self.scorer)
        self.tour_selector = init_struct.tour_selector_cls(manager=self,
                                                           tours=init_struct.tours,
                                                           params=init_struct.tour_selector_params,
                                                           planner=self.planner)

    def run(self):
        self.tour_selector.run_sa(self.tour_selector.params.sa_cooling_rate)

        # self.set_output()

    def get_distance(self, x, y):
        return self.input.distance_matrix[x][y]

    def compute_tour_distance(self, tour, visits=None):
        if tour is None:
            return 0

        if visits is None:
            return sum(self.get_distance(tour[i - 1], tour[i]) for i in range(1, len(tour))) + self.get_distance(tour[-1], tour[0])

        actual_tour = [0] + [t for t, v in zip(tour, visits) if v > 0] + [0]

        return self.compute_tour_distance(actual_tour)

    def get_url(self, tour):
        return MapsUrl().generate_from(self.input.places_names[i] + self.input.places_suffix for i in tour)
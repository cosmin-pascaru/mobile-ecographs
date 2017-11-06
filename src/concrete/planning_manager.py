class Manager:

    class InitStruct:
        def __init__(self):
            self.input = None

            self.manager_params = None

            self.tour_selector_cls = None
            self.tour_selector_params = None

            self.planner_cls = None
            self.planner_params = None

            self.scorer_cls = None
            self.scorer_params = None

    def __init__(self, init_struct : InitStruct):
        self.input = init_struct.input
        self.params = init_struct.manager_params

        self.scorer = init_struct.scorer_cls(init_struct.input, init_struct.scorer_params)
        self.planner = init_struct.planner_cls(init_struct.planner_params, self.scorer)
        self.tour_selector = init_struct.tour_selector_cls(init_struct.tour_selector_params, self.planner)

    def run(self):
        self.tour_selector.run_sa()

        # self.set_output()


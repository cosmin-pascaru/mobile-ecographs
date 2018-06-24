from src.alg.abstract.sa_solver import SaParams


class TourSelectorParams(object):
    def __init__(self):
        # General params
        self.debug = False


class SaTourSelectorParams(object):
    def __init__(self):
        self.tour_sel_params = TourSelectorParams()
        self.sa_params       = SaParams()


class DisabledTourSelectorParams(TourSelectorParams):
    def __init__(self):
        super().__init__()
        self.cnt_iterations = None
        self.max_time = None


from src.alg.abstract.sa_solver import CSaParams


class CTourSelectorParams(object):
    def __init__(self):
        # General params
        self.debug = False


class CSaTourSelectorParams(object):
    def __init__(self):
        self.tour_sel_params = CTourSelectorParams()
        self.sa_params       = CSaParams()


class CDisabledTourSelectorParams(CTourSelectorParams):
    def __init__(self):
        super().__init__()
        self.cnt_iterations = None
        self.max_time = None


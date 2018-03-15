
class TourSelectorParams:
    def __init__(self):
        # General params
        self.debug = False


class SaTourSelectorParams(TourSelectorParams):
    def __init__(self):
        super().__init__()
        self.initial_temp    = None
        self.sa_cooling_rate = None


class DisabledTourSelectorParams(TourSelectorParams):
    def __init__(self):
        super().__init__()
        self.cnt_iterations = None



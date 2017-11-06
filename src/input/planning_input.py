class PlanningInput:
    def __init__(self):
        self.distance_matrix = None
        """Distances between all nodes, in seconds"""

        self.consults_per_node = None
        """List of numbers, how many consults to do at every node"""

        self.consult_time = None
        """Duration of a consult in seconds"""

        self.cnt_cars = None
        """Number of tours that can be done in a day"""

        self.cnt_days = None
        """Number of days for which a planning must be found"""



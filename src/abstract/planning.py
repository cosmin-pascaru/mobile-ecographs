
class Planning:
    class Day:
        def __init__(self):
            self.tours = None
            """A list of tours done in a day (Planning.Tour)"""

    class Tour:
        def __init__(self):
            self.tour = None
            """List of indexes of visited locations"""

            self.cnt_visits = None
            """List of number of visits done in every location of tour"""

    def __init__(self):
        self.data = None
        """A list of plannings per day (Planning.Day)"""

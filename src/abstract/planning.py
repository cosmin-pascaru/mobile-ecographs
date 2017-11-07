
class Planning:
    class Day:
        def __init__(self, tours_per_day):
            if tours_per_day is None:
                return

            self.tours = [None for _ in range(tours_per_day)]
            """A list of tours done in a day (Planning.Tour)"""

        def __len__(self):
            return len(self.tours)

        def __getitem__(self, index):
            return self.tours[index]

        def __setitem__(self, index, value):
            if len(self) <= index:
                self.tours += [None] * (index - len(self) + 1)
            self.tours[index] = value

    class Tour:
        def __init__(self, tour = None, cnt_visits = None):
            self.tour = tour
            """List of indexes of visited locations"""

            self.cnt_visits = cnt_visits
            """List of number of visits done in every location of tour"""

    def __init__(self, days, tours_per_day):
        if days is None or tours_per_day is None:
            return

        self.days = [Planning.Day(tours_per_day) for _ in range(days)]
        """A list of plannings per day (Planning.Day)"""

    def __len__(self):
        return len(self.days)

    def __getitem__(self, index):
        return self.days[index]

    def __setitem__(self, key, value):
        self.days[key] = value
from src.utils import SECONDS_PER_HOUR


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

    def write(self, tours_file, days_file, manager):
        places_names = manager.input.places_names

        with open(tours_file, 'w') as f:
            unique_tours = {}
            for day in self.days:
                if day is None:
                    continue

                for tour in day.tours:
                    if tour is None:
                        continue
                    if tour.tour is None:
                        continue
                    tuple_tour = tuple(tour.tour)
                    if unique_tours.get(tuple_tour, None) is None:
                        unique_tours[tuple_tour] = len(unique_tours)

            temp = list(unique_tours.items())
            temp.sort(key=lambda x: x[1])

            print(temp)
            f.write('\n'.join('Index {}: \n'.format(i) + '\tDurata: {} ore \n'.format(manager.compute_tour_distance(t) / SECONDS_PER_HOUR) + '\t' + str([places_names[place] for place in t]) + '\n\t' + manager.get_url(tuple(t)) for t, i in temp))

        with open(days_file, 'w') as f:
            for i, day in enumerate(self.days):
                f.write('Ziua {}:\n'.format(i))

                for tour in day.tours:
                    if tour is None:
                        continue
                    if tour.tour is None:
                        continue

                    tuple_tour = tuple(tour.tour)
                    tour_index = unique_tours[tuple_tour]

                    if sum(tour.cnt_visits) == 0:
                        continue

                    f.write('\tIndexul traseului: {}\n'.format(tour_index))

                    time_on_road = manager.compute_tour_distance(tuple_tour) / SECONDS_PER_HOUR
                    time_on_visits = sum(tour.cnt_visits) * 0.5 # hours

                    f.write('\tDurata drum: {} ore\n'.format(time_on_road))
                    f.write('\tDurata investigatii: {} ore\n'.format(time_on_visits))
                    f.write('\tDurata totala: {} ore\n'.format(time_on_road + time_on_visits))

                    f.write('\tComunele:\n')
                    for place_index, place in enumerate(tuple_tour):
                        cnt_visits = tour.cnt_visits[place_index]
                        if cnt_visits == 0:
                            continue
                        f.write('\t\t{} : {} vizite, {} minute\n'.format(places_names[place], cnt_visits, cnt_visits * 30))
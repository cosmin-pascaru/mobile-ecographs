from old.Singleton import Singleton
from src import utils
from src.utils import SECONDS_PER_HOUR, sec_to_str


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
        def __init__(self, tour=None, cnt_visits=None):
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

    class Writer(metaclass=Singleton):
        def __init__(self):
            pass

        def write_tours_html(self, planning, tours_html_file, manager):
            places_names = manager.input.places_names

            unique_tours = manager.compute_unique_tours(planning)
            unique_tours = sorted(unique_tours.items(), key=lambda x: x[1])

            tours_html = []
            for tour, index in unique_tours:
                embed_url = manager.get_embed_url(tour)

                tour_html = open(manager.params.tour_template_file, 'r').read()
                tour_html = tour_html.format(index=index + 1,
                                             tour=[places_names[place] for place in tour],
                                             duration=utils.sec_to_str(manager.compute_tour_distance(tour)),
                                             iframe_src=embed_url)
                tours_html.append(tour_html)

            tours_html = '\n'.join(tours_html)

            index_page_html = open(manager.params.index_template_file, 'r').read()
            index_page_html = index_page_html.format(date=utils.today_as_str(), tours=tours_html)

            with open(tours_html_file, 'w') as f:
                f.write(index_page_html)

        def write(self, planning, tours_file, days_file, manager):
            unique_tours = manager.compute_unique_tours(planning)

            self.write_tours(planning, tours_file, unique_tours, manager)
            self.write_days(planning, days_file, unique_tours, manager)

        def write_tours(self, planning, tours_file, unique_tours, manager):
            places_names = manager.input.places_names

            with open(tours_file, 'w') as f:
                temp = list(unique_tours.items())
                temp.sort(key=lambda x: x[1])

                # print(temp)
                for t, i in temp:
                    tour_time = sec_to_str(manager.compute_tour_distance(t))

                    f.write('Traseu {}:\n'.format(i + 1))
                    f.write('\tDurata: {}\n'.format(tour_time))
                    f.write('\t{}\n'.format([places_names[place] for place in t]))
                    f.write('\t{}\n'.format(manager.get_embed_url(t)))

        def write_days(self, planning, days_file, unique_tours, manager):
            places_names = manager.input.places_names

            with open(days_file, 'w') as f:
                for i, day in enumerate(planning.days):
                    f.write('Ziua {}:\n'.format(i + 1))

                    for tour in day.tours:
                        if tour is None:
                            continue
                        if tour.tour is None:
                            continue

                        tuple_tour = tuple(tour.tour)
                        cnt_visits = tour.cnt_visits
                        tour_index = unique_tours[tuple_tour]

                        if sum(tour.cnt_visits) == 0:
                            continue

                        f.write('\tTraseul {}\n'.format(tour_index + 1))

                        time_on_road = manager.compute_tour_distance(tuple_tour, cnt_visits)
                        time_on_visits = sum(tour.cnt_visits) * manager.input.consult_time

                        f.write('\tDurata drum: {}\n'.format(sec_to_str(time_on_road)))
                        f.write('\tDurata investigatii: {}\n'.format(sec_to_str(time_on_visits)))
                        f.write('\tDurata totala: {}\n'.format(sec_to_str(time_on_road + time_on_visits)))

                        f.write('\tComunele:\n')
                        for place_index, place in enumerate(tuple_tour):
                            cnt_visits = tour.cnt_visits[place_index]
                            if cnt_visits == 0:
                                continue
                            time_on_visits = cnt_visits * manager.input.consult_time
                            f.write('\t\t{}: {} vizite, {}\n'.format(places_names[place], cnt_visits,
                                                                     sec_to_str(time_on_visits)))

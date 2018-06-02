from old.Singleton import Singleton
from src.common import utils
from src.common.constants import CONSULT_TIME
from src.common.utils import sec_to_str, ceil_div


class CTour:
    def __init__(self, locations=None, visits_per_location=None):
        self.locations = locations
        self.visits_per_loc = visits_per_location


class CPlanning:
    def __init__(self):
        self.tours = []

    def to_full_planning(self, cnt_days : int = None, cnt_cars : int = None):
        """
        Generates the full planning corresponding to self.
        Only one of *cnt_days* or *cnt_cars* must be set to a natural number, depending on which should be used.
        """

        assert ((cnt_days is None) != (cnt_cars is None))

        if cnt_cars:
            cnt_days = ceil_div(len(self.tours), cnt_cars)

        cnt_tours_per_day = ceil_div(len(self.tours), cnt_days)
        data = [self.tours[i:i + cnt_tours_per_day] for i in range(0, len(self.tours), cnt_tours_per_day)]

        return CFullPlanning(data)


class CFullPlanning:
    def __init__(self, data=None):
        if data:
            self.days = data
        else:
            self.days = []

    def compute_unique_tours(self):
        unique_tours = {}
        for day in self.days:
            if not day:
                continue

            for tour in day:
                if not tour:
                    continue
                if not tour.locations:
                    continue

                tuple_tour = tuple(tour.locations)
                if unique_tours.get(tuple_tour, None) is None:
                    unique_tours[tuple_tour] = len(unique_tours)
        return unique_tours


class CWriter(metaclass=Singleton):
    def __init__(self):
        pass

    def write_tours_html(self, planning, tours_html_file, manager):
        places_names = manager.input.places_names

        unique_tours = planning.compute_unique_tours()
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
        unique_tours = planning.compute_unique_tours()

        # TODO: uncomment
        # self.write_tours(list(unique_tours.items()), tours_file, manager)
        # self.write_days(planning, days_file, unique_tours, manager)

    def write_tours(self, tours, tours_file, manager):
        places_names = manager.input.places_names

        with open(tours_file, 'w') as f:
            # temp = list(unique_tours.items())
            # temp.sort(key=lambda x: x[1])

            for t, i in tours:
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

                for tour in day:
                    if not tour:
                        continue
                    if not tour.locations:
                        continue

                    tuple_tour = tuple(tour.locations)
                    cnt_visits = tour.visits_per_loc
                    tour_index = unique_tours[tuple_tour]

                    if sum(tour.visits_per_loc) == 0:
                        continue

                    f.write('\tTraseul {}\n'.format(tour_index + 1))

                    time_on_road = manager.compute_tour_distance(tuple_tour, cnt_visits)
                    time_on_visits = sum(tour.visits_per_loc) * CONSULT_TIME

                    f.write('\tDurata drum: {}\n'.format(sec_to_str(time_on_road)))
                    f.write('\tDurata investigatii: {}\n'.format(sec_to_str(time_on_visits)))
                    f.write('\tDurata totala: {}\n'.format(sec_to_str(time_on_road + time_on_visits)))

                    f.write('\tComunele:\n')
                    for place_index, place in enumerate(tuple_tour):
                        cnt_visits = tour.cnt_visits[place_index]
                        if cnt_visits == 0:
                            continue
                        time_on_visits = cnt_visits * CONSULT_TIME
                        f.write('\t\t{}: {} vizite, {}\n'.format(places_names[place], cnt_visits,
                                                                 sec_to_str(time_on_visits)))

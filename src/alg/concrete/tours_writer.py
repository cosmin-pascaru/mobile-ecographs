
class ToursWriter(object):
    def __init__(self):
        pass

    def write_plain(self, tours, filename, mode):
        with open(filename, mode) as f:
            f.write('\n'.join(self._to_str_plain(tour) for tour in tours))

    def write_html(self, tours, filename):
        raise NotImplementedError()

    def _to_str_plain(self, tour):
        return ' '.join(map(str, tour))

    # with open(times_filename, 'r') as f:
    #     times = eval(f.read())

    # with open(places_filename, 'r') as places_file:
    #     lines = places_file.readlines()
    #     lines = [" ".join(line.split()[1:]) for line in lines]

    # hours_on_road_limit = 8
    # tour_limit = 60 * 60 * hours_on_road_limit

    # print(MapsUrl().generate_from(tours_str[0]))

    # with open('data/tours/good_tours.txt'.format(cost), 'a') as f:
    #     for tour in tours:
    #         f.write(' '.join(map(str, tour)) + '\n')
    #     for idx, tour in enumerate(tours_str):
    #         f.write(str(tour) + '\n')
    #         f.write(MapsUrl().generate_from(tour) + '\n')
    #         node_times = [i[1] * 30 / 12 for i in NatalityDataReader().read()]
    #         node_times [:5] = [0 for i in range(5)]
    #         f.write('Timp in fiecare comuna (minute pe luna):\n' + '\n'.join([tour[ti] + ' : ' + str(node_times[i]) for ti, i in enumerate(tours[idx])]) + '\n')
    #
    #         f.write('\n\n')
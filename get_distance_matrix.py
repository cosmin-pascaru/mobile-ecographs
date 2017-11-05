from MapsApi import MapsApi

with open("data/lista_comune.txt") as villages_file:
    lines = villages_file.readlines()
    lines = [" ".join(line.split()[1:]) for line in lines]
    villages = [line + ", Iasi, Romania" for line in lines]

api = MapsApi()
mat = api.get_dist_and_times_matrix(villages)

# distances = [[MapsApi.get_distance_from_element(elem) for elem in row] for row in mat]
# durations = [[MapsApi.get_duration_from_element(elem) for elem in row] for row in mat]
#
# with open('distances_only.txt', 'w') as f:
#     f.write(str(distances))
#
# with open('durations_only.txt', 'w') as f:
#     f.write(str(durations))
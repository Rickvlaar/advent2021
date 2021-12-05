from util import console, parse_file_as_list, get_runtime
import numpy as np

day_5_file = parse_file_as_list('input/day_5.txt')
test_file = parse_file_as_list('input/day_5_test.txt')


def convert_file_to_coords(file: list[str]):
    return np.array([[a.split(','), b.split(',')] for a, b in [line.split(' -> ') for line in file]], dtype=int)


def fill_lines(coords, include_diag=False):
    vent_map = np.zeros((coords.max() + 1, coords.max() + 1))
    for coord_a, coord_b in coords:
        determine_action(vent_map, coord_a, coord_b, include_diag)
    return vent_map


def determine_action(vent_map, coord_a, coord_b, include_diag=False):
    # 0 = x, 1 = y
    x_a = coord_a[0]
    x_b = coord_b[0]
    y_a = coord_a[1]
    y_b = coord_b[1]
    if x_a == x_b and y_a != y_b:
        fill_y_line(vent_map, coord_a, coord_b)
    elif x_a != x_b and y_a == y_b:
        fill_x_line(vent_map, coord_a, coord_b)
    elif include_diag:
        fill_diagonal(vent_map, coord_a, coord_b)


def fill_x_line(vent_map, coord_a, coord_b):
    x_min = min(coord_a[0], coord_b[0])
    x_max = max(coord_a[0], coord_b[0]) + 1

    # the y remains static
    y = coord_a[1]
    vent_map[y, x_min:x_max] += 1


def fill_y_line(vent_map, coord_a, coord_b):
    y_min = min(coord_a[1], coord_b[1])
    y_max = max(coord_a[1], coord_b[1]) + 1

    # the x remains static
    x = coord_a[0]
    vent_map[y_min:y_max, x] += 1


def fill_diagonal(vent_map, coord_a, coord_b):
    x_min = min(coord_a[0], coord_b[0])
    x_max = max(coord_a[0], coord_b[0]) + 1

    y_min = min(coord_a[1], coord_b[1])
    y_max = max(coord_a[1], coord_b[1]) + 1

    x_traversal = [x for x in range(x_min, x_max)]
    y_traversal = [y for y in range(y_min, y_max)]

    if coord_a[0] > coord_b[0]:
        x_traversal.reverse()
    if coord_a[1] > coord_b[1]:
        y_traversal.reverse()

    coords_to_update = zip(x_traversal, y_traversal)
    for coord in coords_to_update:
        vent_map[coord[1], coord[0]] += 1


def count_dangerous_coords(vent_map: np.array):
    filtered = np.where(vent_map > 1)
    return filtered[0].size


@get_runtime
def run(file, straight_only=False):
    coords = convert_file_to_coords(file)
    vent_map = fill_lines(coords, straight_only)
    return count_dangerous_coords(vent_map)


if __name__ == '__main__':
    test_a = run(test_file)
    test_b = run(test_file, True)
    day_5a = run(day_5_file)
    day_5b = run(day_5_file, True)

    console.print(f'test solution 5A: {test_a}')
    console.print(f'test solution 4B: {test_b}')
    console.print(f'solution 5A: {day_5a}')
    console.print(f'solution 5B: {day_5b}')

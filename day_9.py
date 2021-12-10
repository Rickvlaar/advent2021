from util import console, parse_file_as_list, get_runtime, convert_str_list_to_int_list
from math import prod
import numpy as np

day_file = parse_file_as_list('input/day_9.txt')
test_file = parse_file_as_list('input/day_9_test.txt')


class Point:

    def __init__(self, height: int, coord: (int, int)):
        self.height = height
        self.coord = coord
        self.neighbours: list[int]

        x = self.coord[0]
        y = self.coord[1]
        self.neigh_coords = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

@get_runtime
def smoke_a_ery_day(height_map: list[str]) -> int:
    height_map = np.array([list(line) for line in height_map], dtype=int)
    height_dict = create_dict_from_map(height_map)
    low_points = get_low_points_2(height_map, height_dict)
    return sum([point.height for point in low_points]) + len(low_points)


@get_runtime
def smoke_b_regularly(height_map: list[str]) -> int:
    height_map = np.array([list(line) for line in height_map], dtype=int)
    height_dict = create_dict_from_map(height_map)
    # basins = get_basins(height_map, low_points)
    low_points = get_low_points_2(height_map, height_dict)
    basins = get_basins2(height_dict, low_points)
    # top_3 = get_biggest(basins)
    # prod([basin[0] for basin in top_3])
    basins.sort(key=len)
    return prod([len(basin) for basin in basins[-3:]])


def create_dict_from_map(height_map: np.ndarray) -> dict:
    height_array = np.array([list(line) for line in height_map], dtype=int)
    height_dict = {}
    for y, x_line in enumerate(height_array):
        for x, height in enumerate(x_line):
            height_dict[(x, y)] = height
    return height_dict


def get_biggest(basins):
    basin_sizes = [len(basin) for basin in basins]
    return sorted(zip(basin_sizes, basins), reverse=True)[:3]


def get_basins(height_map, low_points):
    basins = []
    for point in low_points:
        basin = [point]
        basin_coords = {point[1]}
        keep_basin(point, height_map, basin, basin_coords)
        basins.append(basin)
    return basins


def keep_basin(point, height_map, basin: list[list[int], list[int]], basin_coords):
    height = point[0]
    x, y = point[1]
    neighbours = get_neighbours(height_map, x, y)
    for neigh_point in neighbours:
        if height < neigh_point[0] < 9 and neigh_point[1] not in basin_coords:
            basin_coords.add(neigh_point[1])
            basin.append(neigh_point)
            keep_basin(neigh_point, height_map, basin, basin_coords)


def get_low_points(height_map) -> list:
    low_points = []
    for y, x_line in enumerate(height_map):
        for x, point in enumerate(x_line):
            neighbours = get_neighbours(height_map, x, y)
            if point < min([neigh[0] for neigh in neighbours]):
                low_points.append([point, (x, y)])
    return low_points


def get_basins2(height_dict, low_points):
    basins = []
    for point in low_points:
        basin = [point]
        basin_coords = {point.coord}
        keep_basin2(height_dict, point, basin, basin_coords)
        basins.append(basin)
    return basins


def keep_basin2(height_dict, point: Point, basin, basin_coords):
    for neigh_coord in point.neigh_coords:
        if neigh_coord in height_dict and neigh_coord not in basin_coords:
            neigh_height = height_dict[neigh_coord]
            if point.height < neigh_height < 9:
                neigh_point = Point(neigh_height, neigh_coord)
                basin_coords.add(neigh_coord)
                basin.append(neigh_point)
                keep_basin2(height_dict, neigh_point, basin, basin_coords)


def get_low_points_2(height_map, height_dict) -> list:
    low_points = []
    for y, x_line in enumerate(height_map):
        for x, height in enumerate(x_line):
            if height == 9:
                continue
            point = Point(height, (x, y))
            get_neighbours_2(height_dict, point)
            if point.height < min(point.neighbours):
                low_points.append(point)
    return low_points


def get_neighbours_2(height_dict, point: Point):
    point.neighbours = [height_dict.get(coord, 10) for coord in point.neigh_coords]


def get_neighbours(height_map, x, y) -> list[list[int], list[int]]:
    neighbours = []
    if x > 0:
        neighbours.append([height_map[y, x - 1], (x - 1, y)])
    if x < len(height_map[0]) - 1:
        neighbours.append([height_map[y, x + 1], (x + 1, y)])
    if y > 0:
        neighbours.append([height_map[y - 1, x], (x, y - 1)])
    if y < len(height_map) - 1:
        neighbours.append([height_map[y + 1, x], (x, y + 1)])
    return neighbours


if __name__ == '__main__':
    nin_a = smoke_a_ery_day(day_file)
    nin_b = smoke_b_regularly(day_file)
    console.print(f'solution 9A: {nin_a}')
    console.print(f'solution 9B: {nin_b}')

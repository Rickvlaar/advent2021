from util import console, parse_file_as_list, get_runtime, convert_str_list_to_int_list
from math import prod
import numpy as np


day_file = parse_file_as_list('input/day_9.txt')
test_file = parse_file_as_list('input/day_9_test.txt')


@get_runtime
def smoke_a_ery_day(height_map: list[str]) -> int:
    height_map = np.array([list(line) for line in height_map], dtype=int)
    low_points = get_low_points(height_map)
    return sum([point for point, coord in low_points]) + len(low_points)


@get_runtime
def smoke_b_regularly(height_map: list[str]):
    height_map = np.array([list(line) for line in height_map], dtype=int)
    low_points = get_low_points(height_map)
    basins = get_basins(height_map, low_points)
    top_3 = get_biggest(basins)
    return prod([basin[0] for basin in top_3])


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


def get_neighbours(height_map, x, y) -> list[list[int], list[int]]:
    neighbours = []
    if x > 0:
        neighbours.append([height_map[y, x - 1], (x-1, y)])
    if x < len(height_map[0]) - 1:
        neighbours.append([height_map[y, x + 1], (x+1, y)])
    if y > 0:
        neighbours.append([height_map[y - 1, x], (x, y-1)])
    if y < len(height_map) - 1:
        neighbours.append([height_map[y + 1, x], (x, y+1)])
    return neighbours


if __name__ == '__main__':
    nin_a = smoke_a_ery_day(day_file)
    nin_b = smoke_b_regularly(day_file)
    console.print(f'solution 9A: {nin_a}')
    console.print(f'solution 9B: {nin_b}')


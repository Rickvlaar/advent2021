from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from itertools import product
import heapq
import numpy as np

day_file = parse_file_as_list('input/day_15.txt')
test_file = parse_file_as_list('input/day_15_test.txt')


def run_a(file):
    danger_map = np.array([list(line) for line in file], dtype=int)
    the_hood = get_the_hood_straight(danger_map)
    pathfinder = PathFinder(danger_map, the_hood)
    pathfinder.start_pathfinding(pathfinder.starting_point, [])


class PathFinder:
    def __init__(self, danger_map, hood):
        self.danger_map = danger_map
        self.hood = hood
        self.starting_point = (0, 0)
        self.target = (danger_map.shape[0] - 1, danger_map.shape[1] - 1)
        self.visited_points = set()
        self.paths = []
        self.possible_routes = []
        self.coord_step_dict = {}
        self.last_step = None

    @dataclass(order=True)
    class Step:
        danger_level: int
        origin: field(compare=False)
        coord: field(compare=False)
        # previous: field(compare=False)

    def start_pathfinding(self, start_coord, path):
        self.paths.append(path)
        self.visited_points.add(start_coord)
        neighbours = self.hood.get(start_coord)  # start neighbours

        paths = []
        for neigh in neighbours:
            heapq.heappush(paths, self.Step(self.danger_map[neigh], start_coord, neigh))

        while paths:
            most_close = heapq.heappop(paths)
            # console.print(most_close)
            # most_close.previous.add(most_close.coord)
            self.coord_step_dict[most_close.coord] = most_close

            danger_neigh_dict = self.get_neighbours_danger(most_close)

            if most_close.coord == self.target:
                console.print(most_close)
                self.last_step = most_close
                return

            for neigh_coord, danger_level in danger_neigh_dict.items():
                heapq.heappush(paths, self.Step(danger_level + most_close.danger_level, most_close.coord, neigh_coord))

    def get_neighbours_danger(self, step):
        danger_neigh_dict = {neigh: self.danger_map[neigh] for neigh in self.hood.get(step.coord) if neigh not in self.coord_step_dict.keys()}
        return danger_neigh_dict


def get_the_hood_straight(grid):
    max_y = grid.shape[0] - 1
    max_x = grid.shape[1] - 1
    the_hood = dict()
    for y, line in enumerate(grid):
        for x, num in enumerate(line):
            neighbs = []
            if x > 0:
                neighbs.append((y, x - 1))
            if x < max_x:
                neighbs.append((y, x + 1))
            if y > 0:
                neighbs.append((y - 1, x))
            if y < max_y:
                neighbs.append((y + 1, x))
            the_hood[(y, x)] = neighbs
    return the_hood


def get_the_hood_8(grid: np.array):
    max_y = grid.shape[0]
    max_x = grid.shape[1]
    the_hood = dict()
    for y, line in enumerate(grid):
        for x, num in enumerate(line):
            xs = [x_2 for x_2 in range(x - 1, x + 2) if 0 <= x_2 < max_x]
            ys = [y_2 for y_2 in range(y - 1, y + 2) if 0 <= y_2 < max_y]
            the_hood[(y, x)] = [coord for coord in product(ys, xs)]
    return the_hood


if __name__ == '__main__':
    run_a(day_file)
    answer_a = 'a'
    console.print(f'solution 14A: {answer_a}')

    answer_b = 'a'
    console.print(f'solution 14B: {answer_b}')

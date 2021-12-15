from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from itertools import product
import heapq
import numpy as np

day_file = parse_file_as_list('input/day_15.txt')
test_file = parse_file_as_list('input/day_15_test.txt')


class PathFinder:
    def __init__(self, danger_map, hood):
        self.danger_map = danger_map
        self.hood = hood
        self.starting_point = (0, 0)
        self.target = (danger_map.shape[0] - 1, danger_map.shape[1] - 1)
        self.coord_step_dict = {}
        self.last_step = None

    @dataclass(order=True)
    class Step:
        danger_level: int
        origin: field(compare=False)
        coord: field(compare=False)

    def start_pathfinding(self, start_coord, path):
        neighbours = self.hood.get(start_coord)  # start neighbours

        paths = []
        for neigh in neighbours:
            heapq.heappush(paths, self.Step(self.danger_map[neigh], start_coord, neigh))

        self.dijk_it(paths)

    def dijk_it(self, paths):
        while paths:
            most_close = heapq.heappop(paths)
            if most_close.coord in self.coord_step_dict:
                continue

            self.coord_step_dict[most_close.coord] = most_close

            if most_close.coord == self.target:
                console.print(most_close)
                self.last_step = most_close
                return

            for neighbour in self.hood.get(most_close.coord):
                if neighbour in self.coord_step_dict:
                    continue
                danger_level = self.danger_map[neighbour] + most_close.danger_level
                heapq.heappush(paths, self.Step(danger_level, most_close.coord, neighbour))


def transform_danger_map(danger_map):
    sub_lists = []
    for y in range(5):
        for x in range(5):
            z = danger_map + y + x
            f = np.vectorize(lambda x: x - 9 if x > 9 else x)
            sub_lists.append(f(z))

    final = []
    for v in range(5):
        final.append(np.hstack(sub_lists[v*5:v*5+5]))

    final = np.vstack(np.array(final))
    return final


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


@time_function()
def run_a(file):
    danger_map = np.array([list(line) for line in file], dtype=int)
    the_hood = get_the_hood_straight(danger_map)
    pathfinder = PathFinder(danger_map, the_hood)
    pathfinder.start_pathfinding(pathfinder.starting_point, [])
    return pathfinder.last_step.danger_level


@time_function()
def run_b(file):
    danger_map = np.array([list(line) for line in file], dtype=int)
    danger_map = transform_danger_map(danger_map)
    the_hood = get_the_hood_straight(danger_map)
    pathfinder = PathFinder(danger_map, the_hood)
    pathfinder.start_pathfinding(pathfinder.starting_point, [])
    return pathfinder.last_step.danger_level


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution 15A: {answer_a}')
    console.print(f'solution 15B: {answer_b}')

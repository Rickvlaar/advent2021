from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from collections import defaultdict
from itertools import product
import numpy as np

day_file = parse_file_as_list('input/day_25.txt')
test_file = parse_file_as_list('input/day_25_test.txt')

EAST = 1
SOUTH = 2


def parse_file(file: list[str]) -> np.array:
    cucum_map = np.array([list(line) for line in file])
    for y, line in enumerate(cucum_map):
        for x, cucum in enumerate(line):
            if cucum == '>':
                cucum_map[y, x] = EAST
            elif cucum == 'v':
                cucum_map[y, x] = SOUTH
            else:
                cucum_map[y, x] = 0
    return np.array(cucum_map, dtype=int)


def move_east(cucum_map: np.array):
    made_a_move = False
    new_cucum_map = np.copy(cucum_map)
    for y, line in enumerate(cucum_map):
        for x, cucum in enumerate(line):
            if cucum == EAST:
                moved = move_cucum_east(cucum_map, new_cucum_map, (y, x))
                if not made_a_move and moved:
                    made_a_move = True
    return new_cucum_map, made_a_move


def move_cucum_east(cucum_map: np.array, new_cucum_map: np.array, coord: tuple):
    target_x = coord[1] + 1
    if target_x == cucum_map.shape[1]:
        target_x = 0
    target_coord = coord[0], target_x
    if not cucum_map[target_coord]:
        new_cucum_map[coord] = 0
        new_cucum_map[target_coord] = EAST
        return True


def move_south(cucum_map: np.array):
    made_a_move = False
    new_cucum_map = np.copy(cucum_map)
    for y, line in enumerate(cucum_map):
        for x, cucum in enumerate(line):
            if cucum == SOUTH:
                moved = move_cucum_south(cucum_map, new_cucum_map, (y, x))
                if not made_a_move and moved:
                    made_a_move = True
    return new_cucum_map, made_a_move


def move_cucum_south(cucum_map: np.array, new_cucum_map: np.array, coord: tuple):
    target_y = coord[0] + 1
    if target_y == cucum_map.shape[0]:
        target_y = 0
    target_coord = target_y, coord[1]
    if not cucum_map[target_coord]:
        new_cucum_map[coord] = 0
        new_cucum_map[target_coord] = SOUTH
        return True


@time_function()
def run_a(file):
    cucum_map = parse_file(file)

    migration_count = 0
    moved_east = True
    moved_south = True
    while moved_east or moved_south:
        cucum_map, moved_east = move_east(cucum_map)
        cucum_map, moved_south = move_south(cucum_map)
        migration_count += 1
    console.print(cucum_map)
    console.print(migration_count)


@time_function()
def run_b(file):
    pass


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution 25A: {answer_a}')
    console.print(f'solution 25B: {answer_b}')

import itertools

from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from math import prod
import numpy as np

day_file = parse_file_as_list('input/day_17.txt')
test_file = parse_file_as_list('input/day_17_test.txt')


# target area: x=20..30, y=-10..-5
def parse_target(file: list[str]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    x_raw, y_raw = file[0].removeprefix('target area: ').split(', ')

    x_range_tuple = tuple([int(x) for x in x_raw.removeprefix('x=').split('..')])
    y_range_tuple = tuple([int(y) for y in y_raw.removeprefix('y=').split('..')])

    # answers = []
    # for bla in file[2:]:
    #     splitline = bla.split(' ')
    #     for val in splitline:
    #         answers.append(val.strip())
    #
    # answers.sort()
    # console.print(answers)

    return x_range_tuple, y_range_tuple


# 0 == x, 1 == y
def fire(velocity: np.array, position: np.array):
    # update position by velocity
    position += velocity

    # reduce x, y velocity by drag
    velocity -= 1

    if velocity[0] < 0:
        velocity[0] = 0

    return velocity, position


def hit_target(position, x_range_tuple, y_range_tuple):
    return x_range_tuple[0] <= position[0] <= x_range_tuple[1] and y_range_tuple[0] <= position[1] <= y_range_tuple[1]


def missed_target(position, velocity, x_range_tuple, y_range_tuple):
    undershoot = velocity[0] == 0 and position[0] > x_range_tuple[1]
    overshoot = velocity[0] == 0 and position[0] < x_range_tuple[0]
    passed_target = position[1] < y_range_tuple[0]

    misses = [undershoot, overshoot, passed_target]

    return any(misses)


def project_path(velocity, x_range_tuple, y_range_tuple):
    position = np.array([0, 0])
    max_y = 0

    while 1:
        velocity, position = fire(velocity, position)

        if position[1] > max_y:
            max_y = position[1]

        if hit_target(position, x_range_tuple, y_range_tuple):
            return max_y
        elif missed_target(position, velocity, x_range_tuple, y_range_tuple):
            return None


@time_function()
def run_a(file):
    x_range_tuple, y_range_tuple = parse_target(file)
    try_velocities = np.array([start_velocity for start_velocity in itertools.product(np.arange(-250, 250, dtype=int), repeat=2)])

    hits = []
    for velocity in try_velocities:
        hit = project_path(velocity, x_range_tuple, y_range_tuple)
        if hit is not None:
            hits.append(hit)

    hits.sort()
    return hits[-1], len(hits)

def run_b(file):
    pass


if __name__ == '__main__':
    answer_a, answer_b = run_a(day_file)

    console.print(f'solution 17A: {answer_a}')
    console.print(f'solution 17B: {answer_b}')

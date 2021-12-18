import itertools

from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from math import prod
from functools import reduce
import numpy as np

day_file = parse_file_as_list('input/day_17.txt')
test_file = parse_file_as_list('input/day_17_test.txt')


# target area: x=20..30, y=-10..-5
def parse_target(file: list[str]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    x_raw, y_raw = file[0].removeprefix('target area: ').split(', ')

    x_range_tuple = tuple([int(x) for x in x_raw.removeprefix('x=').split('..')])
    y_range_tuple = tuple([int(y) for y in y_raw.removeprefix('y=').split('..')])

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


def will_never_hit(velocity, x_range_tuple, y_range_tuple):
    backwards = velocity[0] < 1
    too_slow = (velocity[0] * (velocity[0] + 1)) // 2 < x_range_tuple[0]
    too_fast = velocity[0] > x_range_tuple[1] or velocity[1] < y_range_tuple[0]

    return any([backwards, too_slow, too_fast])


def missed_target(position, velocity, x_range_tuple, y_range_tuple):
    passed_target = position[1] < y_range_tuple[0]
    overshoot = position[0] > x_range_tuple[1]
    undershoot = velocity[0] == 0 and position[0] < x_range_tuple[0]

    return any([passed_target, undershoot, overshoot])


def project_path(velocity, x_range_tuple, y_range_tuple):
    veloc = tuple(velocity)
    position = np.array([0, 0])
    max_y = 0
    while 1:
        velocity, position = fire(velocity, position)

        if position[1] > max_y:
            max_y = position[1]

        if missed_target(position, velocity, x_range_tuple, y_range_tuple):
            return
        elif hit_target(position, x_range_tuple, y_range_tuple):
            return max_y, veloc


def reverse_engineer(x_range_tuple, y_range_tuple):
    coords = []
    for x in range(x_range_tuple[0], x_range_tuple[1]):
        for y in range(y_range_tuple[0], y_range_tuple[1]):
            coords.append((x, y))
    # (217, -69) -> (0, 0)
    # (

    console.print(len(coords))



@time_function(1)
def run(file):
    x_range_tuple, y_range_tuple = parse_target(file)
    try_velocities = np.array(
            [start_velocity for start_velocity in itertools.product(np.arange(-250, 250, dtype=int), repeat=2)])

    reverse_engineer(x_range_tuple, y_range_tuple)

    hits = []
    for velocity in try_velocities:
        if will_never_hit(velocity, x_range_tuple, y_range_tuple):
            continue

        hit = project_path(velocity, x_range_tuple, y_range_tuple)
        if hit is not None:
            hits.append(hit)

    hits.sort()
    return hits[-1], len(hits)


if __name__ == '__main__':
    answer_a, answer_b = run(day_file)

    console.print(f'solution 17A: {answer_a}')
    console.print(f'solution 17B: {answer_b}')

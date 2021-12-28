from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
import plotly.graph_objects as go
from random import randint

from itertools import product, combinations, permutations
import numpy as np

day_file = parse_file_as_list('input/day_22.txt')
test_file = parse_file_as_list('input/day_22_test.txt')


@dataclass
class Cuboid:
    action: int
    x_range_tuple: tuple
    y_range_tuple: tuple
    z_range_tuple: tuple
    x: list = field(init=False)
    y: list = field(init=False)
    z: list = field(init=False)
    on_count: int = field(init=False, default=0)
    overlap_cuboids: list = field(default_factory=list)
    overlap_dict: dict = field(default_factory=dict)
    shape: go.Isosurface = field(init=False)

    def get_volume(self) -> int:
        x_size = abs(self.x_range_tuple[1] - self.x_range_tuple[0]) + 1
        y_size = abs(self.y_range_tuple[1] - self.y_range_tuple[0]) + 1
        z_size = abs(self.z_range_tuple[1] - self.z_range_tuple[0]) + 1
        return x_size * y_size * z_size

    def overlaps(self, cuboid: 'Cuboid'):
        x_min, x_max = cuboid.x_range_tuple
        y_min, y_max = cuboid.y_range_tuple
        z_min, z_max = cuboid.z_range_tuple

        # -44 -> 5 :: -5 -> 47
        x_overlaps = x_min <= self.x_range_tuple[0] and x_max >= self.x_range_tuple[0] or \
                     x_min >= self.x_range_tuple[0] and x_min <= self.x_range_tuple[1]

        y_overlaps = y_min <= self.y_range_tuple[0] and y_max >= self.y_range_tuple[0] or \
                     y_min >= self.y_range_tuple[0] and y_min <= self.y_range_tuple[1]

        z_overlaps = z_min <= self.z_range_tuple[0] and z_max >= self.z_range_tuple[0] or \
                     z_min >= self.z_range_tuple[0] and z_min <= self.z_range_tuple[1]

        return x_overlaps and y_overlaps and z_overlaps

    def get_overlap_size(self, cuboid: 'Cuboid'):
        x_overlap = self.get_range_overlap_size(cuboid.x_range_tuple, self.x_range_tuple)
        y_overlap = self.get_range_overlap_size(cuboid.y_range_tuple, self.y_range_tuple)
        z_overlap = self.get_range_overlap_size(cuboid.z_range_tuple, self.z_range_tuple)
        return x_overlap * y_overlap * z_overlap

    def get_range_overlap_size(self, own_range, their_range):
        min, max = their_range
        overlap = 0
        # -50 -> 50 :: 20 - 30
        if min >= own_range[0] and max <= own_range[1]:
            overlap = max - min
        # -50 -> 50 :: 20 - 60
        elif min >= own_range[0] and max >= own_range[1]:
            overlap = own_range[1] - min
        # -50 -> 50 :: -100 -> 30
        elif min < own_range[0] and max <= own_range[1]:
            overlap = max - own_range[0]
        # -50 -> 50 :: -100 -> 100
        elif min < own_range[0] and max >= own_range[1]:
            overlap = own_range[1] - own_range[0]
        return overlap

    def get_overlap_range(self, own_range, their_range):
        min, max = their_range
        overlap_range = None
        # -50 -> 50 :: 20 - 30
        if min >= own_range[0] and max <= own_range[1]:
            overlap_range = (min, max)
        # -50 -> 50 :: 20 - 60
        elif min >= own_range[0] and max >= own_range[1]:
            overlap_range = (min, own_range[1])
        # -50 -> 50 :: -100 -> 30
        elif min < own_range[0] and max <= own_range[1]:
            overlap_range = (own_range[0], max)
        # -50 -> 50 :: -100 -> 100
        elif min < own_range[0] and max >= own_range[1]:
            overlap_range = own_range
        return overlap_range

    def get_overlap_cuboid(self, cuboid: 'Cuboid'):
        x_overlap_range = self.get_overlap_range(cuboid.x_range_tuple, self.x_range_tuple)
        y_overlap_range = self.get_overlap_range(cuboid.y_range_tuple, self.y_range_tuple)
        z_overlap_range = self.get_overlap_range(cuboid.z_range_tuple, self.z_range_tuple)
        return Cuboid(cuboid.action, x_overlap_range, y_overlap_range, z_overlap_range)

    def three_d(self):
        x_min, x_max = self.x_range_tuple
        y_min, y_max = self.y_range_tuple
        z_min, z_max = self.z_range_tuple

        # The
        # octants
        # are: | (+x, +y, +z) | (-x, +y, +z) | (+x, +y, -z) | (-x, +y, -z) | (+x, -y, +z) | (-x, -y, +z) | (
        # +x, -y, -z) | (-x, -y, -z) |

        self.x = [x_max, x_min, x_max, x_min, x_max, x_min, x_max, x_min]
        self.y = [y_max, y_max, y_max, y_max, y_min, y_min, y_min, y_min]
        self.z = [z_max, z_max, z_min, z_min, z_max, z_max, z_min, z_min]

        self.shape = go.Isosurface(
                x=self.x,
                y=self.y,
                z=self.z,
                value=[self.action for _ in range(len(self.x))],
                opacity=1,
                isomin=0)

    def split_cuboid(self, overlap: 'Cuboid'):
        splits = []

        z_min, z_max = self.z_range_tuple
        # Only create new cuboid is dimension does not dissapear in other cube
        if z_min < overlap.z_range_tuple[0] or z_max > overlap.z_range_tuple[1]:
            z_min = overlap.z_range_tuple[1] + 1 if overlap.z_range_tuple[1] < z_max else z_min
            z_max = overlap.z_range_tuple[0] - 1 if overlap.z_range_tuple[0] > z_min else z_max
            cub_z = Cuboid(1, overlap.x_range_tuple, overlap.y_range_tuple, (z_min, z_max))
            splits.append(cub_z)

        x_min, x_max = self.x_range_tuple
        if x_min < overlap.x_range_tuple[0] or x_max > overlap.x_range_tuple[1]:
            x_min = overlap.x_range_tuple[1] + 1 if overlap.x_range_tuple[1] < x_max else x_min
            x_max = overlap.x_range_tuple[0] - 1 if overlap.x_range_tuple[0] > x_min else x_max
            cub_x = Cuboid(1, (x_min, x_max), overlap.y_range_tuple, self.z_range_tuple)
            splits.append(cub_x)

        y_min, y_max = self.y_range_tuple
        if y_min < overlap.y_range_tuple[0] or y_max > overlap.y_range_tuple[1]:
            y_min = overlap.y_range_tuple[1] + 1 if overlap.y_range_tuple[1] < y_max else y_min
            y_max = overlap.y_range_tuple[0] - 1 if overlap.y_range_tuple[0] > y_min else y_max
            cub_y = Cuboid(1, self.x_range_tuple, (y_min, y_max), self.z_range_tuple)
            splits.append(cub_y)

        return splits

    def split_nested_cuboid(self, nested: 'Cuboid'):
        sub_x_range = self.x_range_tuple[0], nested.x_range_tuple[1]
        sub_y_range = self.y_range_tuple[0], nested.y_range_tuple[1]
        sub_z_range = self.z_range_tuple[0], nested.z_range_tuple[1]

        sub_cuboid = Cuboid(1, sub_x_range, sub_y_range, sub_z_range)
        outer_cubs = self.split_cuboid(sub_cuboid)
        inner_cubs = sub_cuboid.split_cuboid(nested)

        return outer_cubs + inner_cubs

    def is_nested_in(self, cuboid: 'Cuboid'):
        x_min, x_max = self.x_range_tuple
        y_min, y_max = self.y_range_tuple
        z_min, z_max = self.z_range_tuple

        nested_x = x_min >= cuboid.x_range_tuple[0] and x_max <= cuboid.x_range_tuple[1]
        nested_y = y_min >= cuboid.y_range_tuple[0] and y_max <= cuboid.y_range_tuple[1]
        nested_z = z_min >= cuboid.z_range_tuple[0] and z_max <= cuboid.z_range_tuple[1]

        return nested_x and nested_y and nested_z


def turn(self, cuboid: 'Cuboid'):
    for x in range(cuboid.x_range_tuple[0], cuboid.x_range_tuple[1] + 1):
        for y in range(cuboid.y_range_tuple[0], cuboid.y_range_tuple[1] + 1):
            for z in range(cuboid.z_range_tuple[0], cuboid.z_range_tuple[1] + 1):
                self.overlap_dict[(x, y, z)] = cuboid.action


def parse_target(file: list[str]):
    cuboids = []
    for line in file:
        action, coords = line.split(' ')

        action = 1 if action == 'on' else 0

        x_raw, y_raw, z_raw = coords.split(',')

        x_range_tuple = tuple([int(x) for x in x_raw.removeprefix('x=').split('..')])
        y_range_tuple = tuple([int(y) for y in y_raw.removeprefix('y=').split('..')])
        z_range_tuple = tuple([int(z) for z in z_raw.removeprefix('z=').split('..')])

        cub = Cuboid(action, x_range_tuple, y_range_tuple, z_range_tuple)
        cuboids.append(cub)

    return cuboids


def turn_m_on(cubs: list[Cuboid], target_cuboid: Cuboid):
    new_cubs = []
    while cubs:
        fresh_cub = cubs.pop(0)
        new_cubs = check_cube_overlap(fresh_cub, new_cubs)


    on_count = 0
    for cub in new_cubs:
        cub.three_d()
        on_count += cub.get_volume()

    data = [cub.shape for cub in new_cubs]
    fig = go.Figure(data=data)
    fig.show()

    return on_count


def check_cube_overlap(fresh_cube: Cuboid, existing_cubes: list[Cuboid]):
    new_existing_cubes = []
    for cuboid in existing_cubes:
        if cuboid.overlaps(fresh_cube):
            if cuboid.is_nested_in(fresh_cube) and cuboid.action:
                # Destroy the cuboid by skipping it
                continue
            else:
                overlap_cuboid = cuboid.get_overlap_cuboid(fresh_cube)
                splits = cuboid.split_nested_cuboid(overlap_cuboid)
                new_existing_cubes.extend(splits)

        # if no overlap and activation cube, just place the cube, otherwise ignore missed turn-off
        elif cuboid.action:
            new_existing_cubes.append(cuboid)

    if fresh_cube.action:
        new_existing_cubes.append(fresh_cube)
    return new_existing_cubes


@time_function()
def run_a(file):
    cubs = parse_target(file)
    target_cuboid = Cuboid(0, (-50, 50), (-50, 50), (-50, 50))
    return turn_m_on(cubs, target_cuboid)


@time_function()
def run_b(file):
    pass


if __name__ == '__main__':
    answer_a = run_a(test_file)
    answer_b = run_b(day_file)

    correct = 2758514936282235
    if answer_a != correct:
        console.print(f'Off by just {answer_a - correct}')
    else:
        console.print('CORRECTO!!!')

    console.print(f'solution 22A: {answer_a}')
    console.print(f'solution 22B: {answer_b}')

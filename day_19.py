from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from math import dist
from functools import reduce
from itertools import permutations
from collections import defaultdict
import numpy as np

day_file = parse_file_as_list('input/day_19.txt')
test_file = parse_file_as_list('input/day_19_test.txt')


@dataclass
class Scanner:
    number: int
    coords: np.array = field(init=False)
    beacon_matches: dict[int: list['BeaconMatch']] = field(init=False, default_factory=dict)
    beacon_rel_pos_dict: defaultdict[tuple: set] = field(init=False)
    relative_position: tuple = field(init=False)


@dataclass
class BeaconMatch:
    coord_1: np.array
    coord_2: np.array
    scanner_1: Scanner
    scanner_2: Scanner
    match_val: set[float]


def parse_file(file: list[str]):
    scanner_coords_dict = defaultdict(list)

    scanner_no = -1
    for line in file:
        if not line:
            continue
        elif line[0:3] == '---':
            scanner_no += 1
        else:
            scanner_coords_dict[scanner_no].append(line.split(','))

    scanner_dict = defaultdict(Scanner)
    for key, value in scanner_coords_dict.items():
        scanner = Scanner(key)
        scanner.coords = np.array(value, dtype=int)
        scanner_dict[key] = scanner

    return scanner_dict


def create_beacon_map(coord_list: np.array):
    beacon_map = np.zeros((1000, 1000, 1000), dtype=int)
    for x, y, z in coord_list:
        beacon_map[z, y, x] = 1
    return beacon_map


# at this point all maps are relative to the scanner itself
def get_scanner_coord_maps(scanner_dict):
    for scanner in scanner_dict:
        get_beacon_relative_positions(scanner_dict[scanner])

    find_overlapping_beacons(scanner_dict)

    determine_scanner_positions(scanner_dict)

    return scanner_dict


# how to center around the beacons instead of the scanner?
def get_beacon_relative_positions(scanner: Scanner):
    beacon_rel_pos_dict = defaultdict(set)
    scanner.beacon_rel_pos_dict = beacon_rel_pos_dict

    for coord in scanner.coords:
        for sub_coord in scanner.coords:
            abs_dist = dist(coord, sub_coord)

            if abs_dist == 0:
                continue

            scanner.beacon_rel_pos_dict[tuple(coord)].add(abs_dist)

    return scanner


def find_overlapping_beacons(scanner_dict: dict):
    for scanner_num, scanner in scanner_dict.items():
        for other_scanner__num, other_scanner in scanner_dict.items():
            if scanner_num == other_scanner__num:
                continue

            match_scanner_coords(scanner, other_scanner)


def match_scanner_coords(scanner_1: Scanner, scanner_2: Scanner):
    for beacon, rel_posses in scanner_1.beacon_rel_pos_dict.items():
        for other_beacon, other_rel_posses in scanner_2.beacon_rel_pos_dict.items():

            overlap = rel_posses.intersection(other_rel_posses)
            if len(overlap) > 1:
                if scanner_2.number not in scanner_1.beacon_matches:
                    scanner_1.beacon_matches[scanner_2.number] = []

                scanner_1.beacon_matches[scanner_2.number].append(BeaconMatch(np.array(beacon),
                                                                              np.array(other_beacon),
                                                                              scanner_1,
                                                                              scanner_2,
                                                                              overlap))


# use scanner 0 as baseline to map the rest against
# don't forget to factor in rotation
def determine_scanner_positions(scanner_dict: dict[int: Scanner]):
    scanner_dict[0].relative_position = (0, 0, 0)
    for scanner_number, scanner in scanner_dict.items():

        for match_scanner_num, matches in scanner.beacon_matches.items():
            #     reference_map = create_map_from_matches(matches)
            #     map_to_orientate = create_map_from_matches(scanner_dict[match_scanner_num].beacon_matches[scanner_number])
            determine_orientation(matches)
        #
        #     pass


def determine_orientation(matches: list[BeaconMatch], plane_angles: tuple = (0, 0, 0)):
    x_plane_angle = plane_angles[0]
    y_plane_angle = plane_angles[1]
    z_plane_angle = plane_angles[2]

    relative_position = matches[0].coord_1 - matches[0].coord_2
    for match in matches:
        reference = match.coord_1
        orientation = match.coord_2

        # mismatched orientation
        if relative_position and relative_position != reference - orientation:
            return determine_orientation(matches)

    # if they stay the same, orientation is good
    return plane_angles



def rotate_x(coordinate):
    x, y, z = coordinate
    if x > 0 and z > 0:
        coordinate = [x, y, -z]
    elif x < 0 and z > 0:
        coordinate = [-x, y, z]
    elif x < 0 and z < 0:
        coordinate = [x, y, -z]
    elif x > 0 and z < 0:
        coordinate = [-x, y, z]
    return coordinate


def rotate_y(coordinate):
    x, y, z = coordinate
    if x > 0 and y > 0:
        coordinate = [-x, y, z]
    elif x < 0 and y > 0:
        coordinate = [x, -y, z]
    elif x < 0 and y < 0:
        coordinate = [-x, y, z]
    elif x > 0 and y < 0:
        coordinate = [x, -y, z]
    return coordinate


def rotate_z(coordinate):
    x, y, z = coordinate
    if y > 0 and z > 0:
        coordinate = [x, -y, z]
    elif y < 0 and z > 0:
        coordinate = [x, y, -z]
    elif y < 0 and z < 0:
        coordinate = [x, -y, z]
    elif y > 0 and z < 0:
        coordinate = [x, y, -z]

    return coordinate


def create_map_from_matches(matches: list[BeaconMatch]):
    # use first point as 0,0,0 reference
    x_offset, y_offset, z_offset = np.array([0, 0, 0]) - np.array(matches[0].coord_1)
    beacon_map = np.zeros((1000, 1000, 1000), dtype=int)
    beacon_map[0, 0, 0] = 1

    # place the rest in the map with offset
    for match in matches[1:]:
        x_new = match.coord_1[0] - x_offset
        y_new = match.coord_1[1] - y_offset
        z_new = match.coord_1[2] - z_offset

        beacon_map[z_new, y_new, x_new] = 1

    return beacon_map


@time_function()
def run_a(file):
    # scanner_dict = parse_file(file)
    # scanner_dict = get_scanner_coord_maps(scanner_dict)

    x = np.array([-618, -824, -621])
    y = np.array([686, 422, 578])

    # # y = np.rot90(y, k=2, axes=(0, 2))
    # determine_orientation(x, y)
    # console.print(scanner_map_dict)


@time_function()
def run_b(file):
    pass


if __name__ == '__main__':
    answer_a = run_a(test_file)
    answer_b = run_b(test_file)

    console.print(f'solution 19A: {answer_a}')
    console.print(f'solution 19B: {answer_b}')

from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
import numpy as np

day_file = parse_file_as_list('input/day_23.txt')
test_file = parse_file_as_list('input/day_23_test.txt')


# Amber (A), Bronze (B), Copper (C), and Desert (D). They live in a burrow that consists of a hallway and four side rooms.
# Amphipods can move up, down, left, or right so long as they are moving into an unoccupied open space.
# THIS MEANS THEY CANNOT PASS EACH OTHER
# walls (#), and open space (.).
# #############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########

ENERGY_DICT = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000
}


def get_current_order(file: list[str]):
    return [[char for char in line if char in 'ABCD'] for line in file[2:4]]


@time_function()
def run_a(file):
    console.print(file)


    starting_positions = get_current_order(file)



@time_function()
def run_b(file):
    pass

if __name__ == '__main__':
    answer_a = run_a(test_file)
    answer_b = run_b(test_file)

    console.print(f'solution 23A: {answer_a}')
    console.print(f'solution 23B: {answer_b}')

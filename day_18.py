from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from math import ceil
from functools import reduce
from itertools import permutations

day_file = parse_file_as_list('input/day_18.txt')
test_file = parse_file_as_list('input/day_18_test.txt')

BOOM = 1337


def parse_file(file: list[str]) -> list:
    return [eval(line) for line in file]


def add_snails(snail_list: list) -> list:
    return reduce(snail_func, snail_list)


def snail_func(snail_1: list, snail_2: list):
    combined_snail = [snail_1, snail_2]

    explosions_made = True
    splits_made = True
    while explosions_made or splits_made:
        combined_snail, explosions_made = go_explode(combined_snail)
        splits_made = go_split(combined_snail)

    console.print(combined_snail)
    return combined_snail


def go_explode(snail: list):
    changes_made = False
    exploding = True
    while exploding:
        exploding = go_deeper(snail)
        if isinstance(exploding, tuple):
            snail = place_numbers(snail, exploding)
            changes_made = True
    return snail, changes_made


def place_numbers(snail, numbers):
    # place left
    snail = recursive_reversed(snail)
    place_number(snail, numbers[0])

    # place right
    snail = recursive_reversed(snail)
    place_number(snail, numbers[1])

    # clean up a little
    clean_boom(snail)
    return snail


def go_deeper(snail: list, deepness: int = 0):
    deepness += 1

    for index, snail_number in enumerate(snail):
        if isinstance(snail_number, list):
            if deepness >= 4 and all([isinstance(element, int) for element in snail[index]]):
                return explode(snail, index)
            else:
                outcome = go_deeper(snail_number, deepness)
                if outcome:
                    return outcome


def go_split(snail: list):
    for index, snail_number in enumerate(snail):
        if isinstance(snail_number, list):
            if go_split(snail_number):
                return True

        elif isinstance(snail_number, int) and snail_number >= 10:
            split(snail, index)
            return True


def place_number(snail: list, number: int, ready_to_place: bool = False):
    # find the boom first
    for index, snail_number in enumerate(snail):
        if snail_number == BOOM:
            ready_to_place = True
        elif ready_to_place and isinstance(snail_number, int):
            snail[index] += number
            return
        elif isinstance(snail_number, list):
            ready_to_place = place_number(snail_number, number, ready_to_place)
    return ready_to_place


def clean_boom(snail: list, delete_boom: bool = False):
    # find the boom first
    for index, snail_number in enumerate(snail):
        if snail_number == BOOM:
            snail[index] = 0
            return True
        if isinstance(snail_number, list):
            if clean_boom(snail_number, delete_boom):
                return


def recursive_reversed(items):
    if isinstance(items, list):
        return [recursive_reversed(item) for item in reversed(items)]
    return items


def explode(snail: list, explode_index: int):
    left, right = snail[explode_index]
    snail[explode_index] = BOOM
    return left, right


def split(snail: list, split_index: int):
    num_to_split = snail[split_index]
    a = num_to_split // 2
    b = ceil(num_to_split / 2)
    new_pair = [a, b]
    snail[split_index] = new_pair


def get_magnitude(snail):
    num_a = snail[0]
    num_b = snail[1]
    if isinstance(num_a, list):
        num_a = get_magnitude(num_a)
    if isinstance(num_b, list):
        num_b = get_magnitude(num_b)

    return 3 * num_a + 2 * num_b


@time_function()
def run_a(file):
    parsed_file = parse_file(file)
    final_snail = add_snails(parsed_file)
    return get_magnitude(final_snail)


@time_function()
def run_b(file):
    parsed_file = parse_file(file)

    # combolist = []
    # for a, b in permutations(parsed_file, 2):
    #     combo = [a, b]
    #     snailcombi = add_snails(combo)
    #     console.print(snailcombi)
    #
    #
    #     combolist.append(combo)
    #     break
    #
    #
    # for combo in combolist:
    #     console.print(combo)


    # snailcombi = add_snails()
    # magnitude = get_magnitude(snailcombi)
    #
    # magnitude_list = [get_magnitude(add_snails(list(combo))) for combo in permutations(parsed_file, 2)]
    #
    # bla = add_snails([[[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]], [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]])
    # console.print(bla)
    # console.print(get_magnitude(bla))
    # console.print(magnitude_list)
    # magnitude_list.sort()
    # return magnitude_list[-1]


if __name__ == '__main__':
    answer_a = run_a(test_file)
    answer_b = run_b(test_file)

    console.print(f'solution 18A: {answer_a}')
    console.print(f'solution 18B: {answer_b}')


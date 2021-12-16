from util import console, parse_file_as_list, time_function
from itertools import pairwise
from collections import Counter, defaultdict
from functools import reduce


day_file = parse_file_as_list('input/day_14.txt')
test_file = parse_file_as_list('input/day_14_test.txt')


def parse_file(file: list[str]) -> (str, dict[str: str]):
    polymer = file[0]
    rules = {rule: insert for rule, insert in [line.split(' -> ') for line in file[2:]]}
    return polymer, rules


def insert_polymers(polymer: str, rules: dict[str, str]):
    new_string = list(polymer)

    offset = 1
    for index, pair in enumerate(pairwise(polymer)):
        element_pair = ''.join(pair)
        if element_pair in rules:
            new_string.insert(index + offset, rules.get(element_pair))
            offset += 1
    return new_string


def recursive_pair_match(pair: str, rules: dict[str, str], max_iter: int, x: int):
    new_char = rules.get(pair)
    x += 1
    if max_iter == x:
        return new_char
    new_pair_1 = pair[0] + new_char
    new_pair_2 = new_char + pair[1]
    return recursive_pair_match(new_pair_1, rules, max_iter, x) + new_char + recursive_pair_match(new_pair_2, rules, max_iter, x)


@time_function()
def run(n: int):
    polymer, rules = parse_file(day_file)

    new_polymer = polymer[0]

    for y in range(7):
        new_polymer = polymer[0]
        for x in range(len(polymer) - 1):
            new_polymer += recursive_pair_match(polymer[x: x+2], rules, y+1, 0) + polymer[x+1]
        console.print(Counter(new_polymer).most_common())

    # repeats = recursive_pair_match(polymer[0: 2], rules, n, 0)
    # y = 1
    # while 1:
    #     if repeats[0: y] not in repeats[y:]:
    #         console.print(repeats)
    #         console.print('\n\n')
    #         console.print(repeats[0: y])
    #
    #         return
    #     y += 1

    most_common = Counter(new_polymer).most_common()
    return most_common[0][1] - most_common[-1][1]


if __name__ == '__main__':
    answer_a = run(1)
    console.print(f'solution 14A: {answer_a}')

    # answer_b = run(40)
    # console.print(f'solution 14B: {answer_b}')



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


def split_to_pairs(polymer: str) -> list[str]:
    return [polymer[pos:pos + 2] for pos in range(len(polymer) - 1)]


def create_pairs_dict(rules: dict):
    new_dict = dict()
    count_dict = dict()
    for pair, value in rules.items():
        new_char = rules.get(pair)
        new_dict[pair] = [pair[0] + new_char, new_char + pair[1]]
        count_dict[pair] = 0
    return new_dict, count_dict


def polymerize(rules, pairs_dict: dict[str: list[str]], pairs_count: dict[str: int], char_counter):
    new_count_dict = {pair: 0 for pair in pairs_count}
    for pair, count in pairs_count.items():
        char = rules.get(pair)
        char_counter[char] += count

        pairs = pairs_dict.get(pair)
        for subpair in pairs:
            new_count_dict[subpair] += count
    return new_count_dict


@time_function(100)
def run(n: int):
    polymer, rules = parse_file(day_file)
    pairs_dict, count_dict = create_pairs_dict(rules)

    pairs = split_to_pairs(polymer)
    for pair in pairs:
        count_dict[pair] += 1

    char_counter = defaultdict(int)
    for char in polymer:
        char_counter[char] += 1

    for _ in range(n):
        count_dict = polymerize(rules, pairs_dict, count_dict, char_counter)

    most_common = Counter(char_counter).most_common()

    return most_common[0][1] - most_common[-1][1]


if __name__ == '__main__':
    answer_a = run(10)
    answer_b = run(40)

    console.print(f'solution 14A: {answer_a}')
    console.print(f'solution 14B: {answer_b}')

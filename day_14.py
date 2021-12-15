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


def recursive_pair_match(pair: str, rules: dict[str, str], new_chars: list[str], max_iter: int, x: int):
    if max_iter == x:
        return

    new_char = rules.get(pair)
    new_chars.append(new_char)

    new_pair_1 = pair[0] + new_char
    new_pair_2 = new_char + pair[1]

    x += 1

    recursive_pair_match(new_pair_1, rules, new_chars, max_iter, x)
    recursive_pair_match(new_pair_2, rules, new_chars, max_iter, x)



@time_function()
def run(n: int):
    polymer, rules = parse_file(test_file)
    for _ in range(n):
        console.print(_)
        polymer = insert_polymers(polymer, rules)
        console.print(Counter(polymer).most_common())
    most_common = Counter(polymer).most_common()
    return most_common[0][1] - most_common[-1][1]


if __name__ == '__main__':
    answer_a = run(10)
    console.print(f'solution 14A: {answer_a}')

    answer_b = run(40)
    console.print(f'solution 14B: {answer_b}')



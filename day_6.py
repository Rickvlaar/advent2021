from collections import defaultdict
from util import console, parse_file_as_list, get_runtime
import numpy as np

day_6_file = parse_file_as_list('input/day_6.txt')
test_file = parse_file_as_list('input/day_6_test.txt')


def parse_list(file):
    return [int(char) for char in file[0].split(',')]


def parse_file_as_dict(file):
    fish_dic = defaultdict(int)
    for char in file[0].split(','):
        fish_dic[int(char)] += 1
    return fish_dic


# integers are immutable!
@get_runtime
def reproduce_fish(school: list[int], days: int) -> int:
    for _ in range(days):
        new_fish = []
        for index, fish in enumerate(school):
            if fish == 0:
                school[index] = 6
                new_fish.append(8)
            else:
                school[index] = fish - 1
        school.extend(new_fish)
    return len(school)


@get_runtime
def smart_reproduce_fish(school: dict[int, int], days: int) -> int:
    for _ in range(days):
        # move all the counts up day
        new_school = {fish_age: 0 for fish_age in range(9)}
        for fish_age, count in school.items():
            if fish_age == 0:
                new_school[8] += count
                new_school[6] += count
            else:
                new_school[fish_age - 1] += count
        school = new_school
    return sum(school.values())


if __name__ == '__main__':
    test_6a = parse_list(test_file)
    test_6a = reproduce_fish(test_6a, 80)
    test_6b = parse_file_as_dict(test_file)
    test_6b = smart_reproduce_fish(test_6b, 256)

    six_a = parse_list(day_6_file)
    six_a = reproduce_fish(six_a, 80)
    six_b = parse_file_as_dict(day_6_file)
    six_b = smart_reproduce_fish(six_b, 256)

    console.print(f'test solution 6A: {test_6a}')
    console.print(f'test solution 6B: {test_6b}')
    console.print(f'solution 6A: {six_a}')
    console.print(f'solution 6B: {six_b}')

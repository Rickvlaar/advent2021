import statistics
import math
from util import console, parse_file_as_list, get_runtime, convert_str_list_to_int_list

day_7_file = parse_file_as_list('input/day_7.txt')
test_file = parse_file_as_list('input/day_7_test.txt')


def prepare_file(file: list[str]) -> list[int]:
    return convert_str_list_to_int_list(file[0].split(','))


@get_runtime
def calc_crab_fuel_consumption_a(crabby_posses: list[int]):
    most_efficient = round(statistics.median(crabby_posses))
    return sum([abs(pos - most_efficient) for pos in crabby_posses])


@get_runtime
def calc_crab_fuel_consumption_b(crabby_posses: list[int]):
    most_efficient = round(statistics.mean(crabby_posses))
    fuel = 0
    # x = lambda a : a * b
    # fuel2 = map(x, crabby_posses)

    for pos in crabby_posses:
        diff = abs(pos - most_efficient)
        fuel += (diff * (diff + 1)) / 2
    return fuel


if __name__ == '__main__':
    crabby_posses = prepare_file(day_7_file)
    sev_a = calc_crab_fuel_consumption_a(crabby_posses)
    sev_b = calc_crab_fuel_consumption_b(crabby_posses)

# console.print(f'test solution 6A: {test_6a}')
    # console.print(f'test solution 6B: {test_6b}')
    console.print(f'solution 7A: {sev_a}')
    console.print(f'solution 7B: {sev_b}')
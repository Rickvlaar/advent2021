import statistics
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
    most_efficient = sum(crabby_posses) // len(crabby_posses)
    fuel = 0
    for pos in crabby_posses:
        diff = abs(pos - most_efficient)
        fuel += (diff * (diff + 1)) / 2
    return fuel


if __name__ == '__main__':
    crabby_posse = prepare_file(test_file)
    test_a = calc_crab_fuel_consumption_a(crabby_posse)
    test_b = calc_crab_fuel_consumption_b(crabby_posse)

    crabby_posses = prepare_file(day_7_file)
    sev_a = calc_crab_fuel_consumption_a(crabby_posses)
    sev_b = calc_crab_fuel_consumption_b(crabby_posses)

    console.print(f'solution 7A: {sev_a}')
    console.print(f'solution 7B: {sev_b}')

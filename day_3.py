import numpy as np
from typing import List, Callable
import util

day_3_diagnostics = util.parse_file_as_list('input/day_3.txt')

test_input = ['00100',
              '11110',
              '10110',
              '10111',
              '10101',
              '01111',
              '00111',
              '11100',
              '10000',
              '11001',
              '00010',
              '01010']


def reshape_array(report: List[any]) -> np.ndarray:
    reshaped = [list(line) for line in report]
    return np.transpose(reshaped)


def report_to_bin_array(report: List[any]) -> list[int]:
    reshaped = [list(line) for line in report]
    return [int(''.join(line), 2) for line in np.transpose(reshaped)]


@util.get_runtime
def get_power_rate(transposed_array: list[int], half_bit_length: int) -> int:
    gamma_rate = ''
    epsilon_rate = ''
    for line in transposed_array:
        gamma_rate += get_most_common_bit(line, half_bit_length)
        epsilon_rate += get_least_common_bit(line, half_bit_length)
    return int(gamma_rate, 2) * int(epsilon_rate, 2)


@util.get_runtime
def get_life_support_rate(report: List[str]) -> int:
    oxygen_rating = filter_array(report, get_most_common_bit)
    co2_rating = filter_array(report, get_least_common_bit)
    return oxygen_rating * co2_rating


def filter_array(report: List[str], filter_func: Callable) -> int:
    input_report = [list(line) for line in report]
    transposed_array = reshape_array(report)

    for bit_index in range(len(transposed_array)):
        line = transposed_array[bit_index]
        bits = int(''.join(line), 2)
        limit = int(round((len(line) / 2 + 0.1)))
        wanted_val = filter_func(bits, limit)
        lines_kept = [input_report[index] for index, val in enumerate(line) if val == wanted_val]
        transposed_array = reshape_array(lines_kept)
        input_report = lines_kept
        if len(lines_kept) == 1:
            break

    return int(''.join(input_report[0]), 2)


def get_most_common_bit(bits: int, limit: int) -> str:
    return '1' if bits.bit_count() >= limit else '0'


def get_least_common_bit(bits: int, limit: int) -> str:
    return '0' if bits.bit_count() >= limit else '1'


if __name__ == '__main__':
    test_half_bit_length = int(len(test_input) / 2)
    test_array = report_to_bin_array(test_input)
    test_power_rate = get_power_rate(test_array, test_half_bit_length)
    test_life_support_rate = get_life_support_rate(test_input)
    util.console.print(f'test solution 3A: {test_power_rate}')
    util.console.print(f'test solution 3B: {test_life_support_rate}\n')

    day3_half_bit_length = int(len(day_3_diagnostics) / 2)
    reshaped_array = report_to_bin_array(day_3_diagnostics)
    power_rate = get_power_rate(reshaped_array, day3_half_bit_length)
    life_support_rate  = get_life_support_rate(day_3_diagnostics)
    util.console.print(f'solution 3A: {power_rate}')
    util.console.print(f'solution 3B: {life_support_rate}\n')

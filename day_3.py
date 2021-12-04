from collections import Counter
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


@util.get_runtime
def get_power_rate(transposed_array: np.ndarray) -> int:
    # gamma_rate = ''.join([get_most_common_bit(line) for line in transposed_array])
    # epsilon_rate = ''.join([get_least_common_bit(line) for line in transposed_array])
    # print(Counter(transposed_array[0]).most_common()[0][0])

    # gamma_rate = ''.join([Counter(line).most_common()[0][0] for line in transposed_array])
    # epsilon_rate = ''.join([Counter(line).most_common()[1][0] for line in transposed_array])
    gamma_rate = ''
    epsilon_rate = ''
    for line in transposed_array:
        counter = Counter(line).most_common()
        gamma_rate += get_most_common_bit(counter)
        epsilon_rate += get_least_common_bit(counter)
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
        counter = Counter(line).most_common()
        wanted_val = filter_func(counter)
        lines_kept = [input_report[index] for index, val in enumerate(line) if val == wanted_val]
        transposed_array = reshape_array(lines_kept)
        input_report = lines_kept
        if len(lines_kept) == 1:
            break

    return int(''.join(input_report[0]), 2)


def get_most_common_bit(counter) -> str:
    return counter[0][0]


def get_least_common_bit(counter) -> str:
    return counter[-1][0]


if __name__ == '__main__':
    test_array = reshape_array(test_input)
    util.console.print(f'test solution 2A: {get_power_rate(test_array)}')
    util.console.print(f'test solution 2B: {get_life_support_rate(test_input)}\n')

    reshaped_array = reshape_array(day_3_diagnostics)
    util.console.print(f'solution 2A: {get_power_rate(reshaped_array)}')
    util.console.print(f'solution 2B: {get_life_support_rate(day_3_diagnostics)}\n')



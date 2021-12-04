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
    reshaped = [[int(char) for char in line] for line in report]
    return np.transpose(reshaped)


def report_to_bin_array(report: List[any]) -> list[int]:
    reshaped = [list(line) for line in report]
    return [int(''.join(line), 2) for line in np.transpose(reshaped)]


@util.get_runtime
def get_power_rate(transposed_array: list[int], half_bit_length: int) -> int:
    gamma_rate = []
    epsilon_rate = []
    for line in transposed_array:
        gamma_rate.append(get_most_common_bit(line, half_bit_length))
        epsilon_rate.append(get_least_common_bit(line, half_bit_length))

    gamma_rate = convert_bitlist_to_bit(gamma_rate)
    epsilon_rate = convert_bitlist_to_bit(epsilon_rate)

    return gamma_rate * epsilon_rate


def convert_bitlist_to_bit(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | int(bit)
    return int(out)


@util.get_runtime
def get_life_support_rate(transposed_array) -> int:
    oxygen_rating = filter_array(transposed_array, get_most_common_bit)
    co2_rating = filter_array(transposed_array, get_least_common_bit)
    return oxygen_rating * co2_rating


def filter_array(transposed_array, filter_func: Callable) -> int:
    ind = 0
    while 1:
        line = transposed_array[ind]
        bits = convert_bitlist_to_bit(line)
        limit = int(round((len(line) / 2) + .1))
        wanted_val = filter_func(bits, limit)
        delete_indeces = [index for index, val in enumerate(line) if val != wanted_val]
        transposed_array = np.delete(transposed_array, delete_indeces, 1)
        ind += 1
        if len(transposed_array[0]) == 1:
            break

    return convert_bitlist_to_bit(transposed_array.transpose().flatten())


def get_most_common_bit(bits: int, limit: int) -> int:
    return 1 if bits.bit_count() >= limit else 0


def get_least_common_bit(bits: int, limit: int) -> int:
    return 0 if bits.bit_count() >= limit else 1


if __name__ == '__main__':
    # test_half_bit_length = int(len(test_input) / 2)
    # test_array = report_to_bin_array(test_input)
    # test_power_rate = get_power_rate(test_array, test_half_bit_length)
    # test_life_support_rate = get_life_support_rate(test_input)
    # util.console.print(f'test solution 3A: {test_power_rate}')
    # util.console.print(f'test solution 3B: {test_life_support_rate}\n')

    day3_half_bit_length = int(len(day_3_diagnostics) / 2)
    reshaped_array = report_to_bin_array(day_3_diagnostics)
    power_rate = get_power_rate(reshaped_array, day3_half_bit_length)

    shaped = reshape_array(day_3_diagnostics)
    life_support_rate = get_life_support_rate(shaped)
    util.console.print(f'solution 3A: {power_rate}')
    util.console.print(f'solution 3B: {life_support_rate}\n')

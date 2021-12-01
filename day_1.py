import util

day_1_input = util.parse_file_as_list('input/day_1.txt')
test_input = [199,
              200,
              208,
              210,
              200,
              207,
              240,
              269,
              260,
              263]


@util.get_runtime
def count_increases(measurements: list[int], window_size: int = 1) -> int:
    no_o_increases = 0
    for index in range((window_size - 1), len(measurements)):
        meas_win = sum(measurements[index - window_size: index])
        prev_meas_win = sum(measurements[index - window_size - 1: index - 1])
        if meas_win > prev_meas_win:
            no_o_increases += 1
    return no_o_increases


if __name__ == '__main__':
    day_1_input = util.convert_str_list_to_int_list(day_1_input)
    print(count_increases(day_1_input))  # Day 1A
    print(count_increases(day_1_input, 3))  # Day 1B

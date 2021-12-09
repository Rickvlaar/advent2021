from util import console, parse_file_as_list, get_runtime, convert_str_list_to_int_list

day_file = parse_file_as_list('input/day_8.txt')
test_file = parse_file_as_list('input/day_8_test.txt')

num_letter_dict = {
        '0': {'a', 'b', 'c', 'e', 'f', 'g'},
        '1': {'c', 'f'},
        '2': {'a', 'c', 'd', 'e', 'g'},
        '3': {'a', 'c', 'd', 'f', 'g'},
        '4': {'b', 'c', 'd', 'f'},
        '5': {'a', 'b', 'd', 'f', 'g'},
        '6': {'a', 'b', 'd', 'e', 'f', 'g'},
        '7': {'a', 'c', 'f'},
        '8': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        '9': {'a', 'b', 'c', 'd', 'f', 'g'}
}


def parse_file(file: list[str]):
    signals_outputs = [[signals.split(' '), output.split(' ')] for signals, output in
                       [line.split(' | ') for line in file]]
    for signal_output in signals_outputs:
        signal_output[0] = [set(list(signal)) for signal in signal_output[0]]
        signal_output[1] = [set(list(output)) for output in signal_output[1]]
    return signals_outputs


# # count digits 1, 4, 7, 8
# def count_output_easiest(signals_outputs):
#     le_count = 0
#     tracked_num_lengths = {len(ONE), len(FOU), len(SEV), len(EIG)}
#     for signal_output in signals_outputs:
#         x = [output for output in signal_output[1] if len(output) in tracked_num_lengths]
#         le_count += len(x)
#     return le_count


def convert_outputs(signals_outputs):
    for signal_output in signals_outputs:
        determine_line_mapping(signal_output)


def determine_line_mapping(signal_output: list[list[set[str]]]):
    signals = signal_output[0]
    signals.sort(key=len)
    all_letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    # Use this dict to reduce
    signal_letter_dict = {letter: all_letters for letter in all_letters}
    for signal in signals:
        if len(signal) == 2:
            clear_impossible_values(signal_letter_dict, signal, num_letter_dict['1'])
        elif len(signal) == 3:
            clear_impossible_values(signal_letter_dict, signal, num_letter_dict['7'])
        elif len(signal) == 4:
            clear_impossible_values(signal_letter_dict, signal, num_letter_dict['4'])

    # reduce_further(signal_letter_dict)

    console.print(signal_letter_dict)
    console.print(signals)

    # each line has its own mapping!
    pass


def clear_impossible_values(signal_letter_dict: dict[str: set[str]], signal: set[str], match: set[str]):
    for key, values in signal_letter_dict.items():
        if key in match:
            signal_letter_dict[key] = values.intersection(signal)
        else:
            signal_letter_dict[key] = values.difference(signal)
    return signal_letter_dict


def reduce_further(signal_letter_dict: dict[str: set[str]]):
    for key, values in signal_letter_dict.items():
        if len(values) == 1:
            remove_value_from_dict(signal_letter_dict, key)
            break


def remove_value_from_dict(signal_letter_dict: dict[str: set[str]], skip_key):
    for key, values in signal_letter_dict.items():
        if key != skip_key and skip_key in values:
            signal_letter_dict[key] = values.difference(skip_key)


if __name__ == '__main__':
    console.print(f'solution 7A')
    file = parse_file(test_file)
    convert_outputs(file)

    # print(count_output_easiest(file))

    # console.print(f'solution 7A: {sev_a}')
    # console.print(f'solution 7B: {sev_b}')

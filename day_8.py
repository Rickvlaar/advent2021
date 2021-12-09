from util import console, parse_file_as_list, get_runtime, convert_str_list_to_int_list

day_file = parse_file_as_list('input/day_8.txt')
test_file = parse_file_as_list('input/day_8_test.txt')

num_letter_dict = {
        0: {'a', 'b', 'c', 'e', 'f', 'g'},
        1: {'c', 'f'},
        2: {'a', 'c', 'd', 'e', 'g'},
        3: {'a', 'c', 'd', 'f', 'g'},
        4: {'b', 'c', 'd', 'f'},
        5: {'a', 'b', 'd', 'f', 'g'},
        6: {'a', 'b', 'd', 'e', 'f', 'g'},
        7: {'a', 'c', 'f'},
        8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        9: {'a', 'b', 'c', 'd', 'f', 'g'}
}


def parse_file(file: list[str]):
    signals_outputs = [[signals.split(' '), output.split(' ')] for signals, output in
                       [line.split(' | ') for line in file]]
    for signal_output in signals_outputs:
        signal_output[0] = [set(list(signal)) for signal in signal_output[0]]
        signal_output[1] = [set(list(output)) for output in signal_output[1]]
    return signals_outputs


# count digits 1, 4, 7, 8
@get_runtime
def count_output_easiest(signals_outputs):
    le_count = 0
    tracked_num_lengths = {len(num_letter_dict[1]), len(num_letter_dict[4]), len(num_letter_dict[7]),
                           len(num_letter_dict[8])}
    for signal_output in signals_outputs:
        x = [output for output in signal_output[1] if len(output) in tracked_num_lengths]
        le_count += len(x)
    return le_count


@get_runtime
def convert_outputs(signals_outputs):
    segments_list = []

    for signal_output in signals_outputs:
        segments = []
        num_signal_dict = determine_line_mapping(signal_output[0])
        for output in signal_output[1]:
            for num, pattern in num_signal_dict.items():
                if output == pattern:
                    segments.append(num)

        segments = ''.join([str(char) for char in segments])
        segments_list.append(segments)
    return sum([int(output) for output in segments_list])


def determine_line_mapping(signal_output: list[list[set[str]]]):
    signal_output.sort(key=len)
    all_letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    # Use this dict to reduce
    signal_letter_dict = {letter: all_letters for letter in all_letters}
    num_signal_dict = {}
    for signal in signal_output:
        if len(signal) == 2:
            num_signal_dict[1] = signal
            # clear_impossible_values(signal_letter_dict, signal, num_letter_dict[1])
        elif len(signal) == 3:
            num_signal_dict[7] = signal
            # clear_impossible_values(signal_letter_dict, signal, num_letter_dict[7])
        elif len(signal) == 4:
            num_signal_dict[4] = signal
            # clear_impossible_values(signal_letter_dict, signal, num_letter_dict[4])
        elif len(signal) == 7:
            num_signal_dict[8] = signal

    deduce_1(num_signal_dict, signal_output)
    deduce_2(num_signal_dict, signal_output)

    return num_signal_dict


def deduce_1(signal_num_dict, signals):
    for sig in signals:
        if len(sig) == 5 and signal_num_dict[1] <= sig:
            signal_num_dict[3] = sig
        if len(sig) == 6 and not signal_num_dict[1] <= sig:
            signal_num_dict[6] = sig
        if len(sig) == 6 and not signal_num_dict[4] <= sig and signal_num_dict[1] <= sig:
            signal_num_dict[0] = sig


def deduce_2(signal_num_dict, signals):
    for sig in signals:
        if len(sig) == 6 and sig != signal_num_dict[6] and sig != signal_num_dict[0]:
            signal_num_dict[9] = sig
        if len(sig) == 5 and len(signal_num_dict[6] - sig) == 1:
            signal_num_dict[5] = sig
        if len(sig) == 5 and len(signal_num_dict[6] - sig) == 2 and sig != signal_num_dict[3]:
            signal_num_dict[2] = sig


def clear_impossible_values(signal_letter_dict: dict[str: set[str]], signal: set[str], match: set[str]):
    for key, values in signal_letter_dict.items():
        if key in match:
            signal_letter_dict[key] = values.intersection(signal)
        else:
            signal_letter_dict[key] = values.difference(signal)
    return signal_letter_dict


def remove_value_from_dict(signal_letter_dict: dict[str: set[str]], skip_key):
    for key, values in signal_letter_dict.items():
        if key != skip_key and skip_key in values:
            signal_letter_dict[key] = values.difference(skip_key)


if __name__ == '__main__':
    file = parse_file(day_file)

    a = count_output_easiest(file)
    b = convert_outputs(file)

    console.print(f'solution 8A: {a}')
    console.print(f'solution 8B: {b}')

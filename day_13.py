from util import console, parse_file_as_list, time_function
import numpy as np

day_file = parse_file_as_list('input/day_13.txt')
test_file = parse_file_as_list('input/day_13_test.txt')


def get_coords_and_instructions(file: list[str]):
    file_split = file.index('')

    coords = np.array([np.fromstring(line, sep=',', dtype=int) for line in file[:file_split]])

    instructions = []
    for line in file[file_split + 1:]:
        string, num = line.split('=')
        instructions.append([string[-1], num])

    return coords, instructions


def create_map_from_coords(coords: np.array):
    max_x = max([x for x, y in coords]) + 1
    max_y = max([y for x, y in coords]) + 1

    dot_map = np.zeros((max_y, max_x), dtype=bool)
    for x, y in coords:
        dot_map[y, x] = True
    return dot_map


def fold_dot_map(dot_map: np.array, direction, fold_at):
    fold_at = int(fold_at)
    if direction == 'y':
        dot_map = dot_map[:fold_at, ] + np.flipud(dot_map[fold_at + 1:, ])
    elif direction == 'x':
        dot_map = dot_map[:, :fold_at] + np.fliplr(dot_map[:, fold_at + 1:])
    return dot_map


@time_function(100)
def run_a(file):
    coords, fold_instructions = get_coords_and_instructions(file)
    dot_map = create_map_from_coords(coords)
    dot_map = fold_dot_map(dot_map, fold_instructions[0][0], fold_instructions[0][1])
    return len(dot_map[dot_map])


@time_function(100)
def run_b(file):
    coords, fold_instructions = get_coords_and_instructions(file)
    dot_map = create_map_from_coords(coords)
    for direction, fold_at in fold_instructions:
        dot_map = fold_dot_map(dot_map, direction, fold_at)
    return dot_map


if __name__ == '__main__':
    answer_a = run_a(day_file)
    dot_map = run_b(day_file)

    console.print(f'solution 13A: {answer_a}')
    console.print(f'solution 13B: \n\n')

    np.set_printoptions(linewidth=np.nan, formatter={'all': lambda x: '#' if x else ' '})
    console.print(dot_map)


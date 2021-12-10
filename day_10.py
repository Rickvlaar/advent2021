from util import console, parse_file_as_list, get_runtime, convert_str_list_to_int_list
import re

day_file = parse_file_as_list('input/day_10.txt')
test_file = parse_file_as_list('input/day_10_test.txt')

POINTS_DIC = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
}

OPEN_CLOSE_DIC = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
}

FINISH_DIC = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
}


@get_runtime
def check_for_corruption_a(file):
    score = 0
    for line in file:
        score += recurse_check(line)
    return score


def recurse_check(line: str) -> int:
    pattern = re.compile(pattern='[({[<]{1}[)}\]>]{1}')
    for mat in pattern.finditer(line):
        if mat[0][1] != OPEN_CLOSE_DIC[mat[0][0]]:
            return POINTS_DIC[mat[0][1]]

    line_sub_tuple = pattern.subn('', line)
    if line_sub_tuple[1] > 0:
        return recurse_check(line_sub_tuple[0])

    return 0


@get_runtime
def finish_the_lines_b(file):
    clean_file = banish_the_corrupted(file)
    scores = []
    for line in clean_file:
        scores.append(get_finish_points(line))
    scores.sort()
    return scores[round(len(scores) / 2)]


def banish_the_corrupted(file):
    keep_lines = []
    for index, line in enumerate(file):
        if recurse_check(line) == 0:
            keep_lines.append(index)
    return [recurse_clean(file[x]) for x in keep_lines]


def recurse_clean(line: str) -> str:
    pattern = re.compile(pattern='[({[<]{1}[)}\]>]{1}')

    line_sub_tuple = pattern.subn('', line)
    if line_sub_tuple[1] > 0:
        return recurse_clean(line_sub_tuple[0])

    return line_sub_tuple[0]


def get_finish_points(line: str) -> int:
    score = 0
    for char in reversed(line):
        score *= 5
        score += FINISH_DIC[OPEN_CLOSE_DIC[char]]
    return score


if __name__ == '__main__':
    ten_a = check_for_corruption_a(day_file)
    ten_b = finish_the_lines_b(day_file)
    console.print(f'solution 10A: {ten_a}')
    console.print(f'solution 10B: {ten_b}')

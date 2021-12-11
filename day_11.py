from util import console, parse_file_as_list, time_function
import numpy as np
from itertools import product

day_file = parse_file_as_list('input/day_11.txt')
test_file = parse_file_as_list('input/day_11_test.txt')


@time_function(10)
def octo_flash_a(file: list[str], iterations: int) -> int:
    octo_grid = np.array([list(line) for line in file], dtype=int)
    the_hood = get_the_hood(octo_grid)
    flash_count = 0
    for _ in range(iterations):
        octo_grid, flash_count = do_step(octo_grid, flash_count, the_hood)
    return flash_count


@time_function(10)
def octo_flash_b(file: list[str]) -> int:
    octo_grid = np.array([list(line) for line in file], dtype=int)
    the_hood = get_the_hood(octo_grid)
    flash_count = 0
    steps = 0
    while np.any(octo_grid):
        octo_grid, flash_count = do_step(octo_grid, flash_count, the_hood)
        steps += 1
    return steps


def do_step(octo_grid: np.array, flash_count: int, the_hood):
    octo_grid += 1
    flashed_octos = set()

    while octo_grid.max() > 9:
        for y, octo_line in enumerate(octo_grid):
            for x, octo in enumerate(octo_line):
                if octo > 9 and (y, x) not in flashed_octos:
                    octo_grid[y, x] = 0
                    flash_count += 1
                    flashed_octos.add((y, x))
                    up_the_neighbours(y, x, octo_grid, the_hood)

    return octo_grid, flash_count


def up_the_neighbours(y, x, octo_grid, the_hood):
    for coord in the_hood[(y, x)]:
        if coord == (y, x):
            continue
        val = octo_grid[coord]
        if val != 0:
            octo_grid[coord] += 1


def get_the_hood(octo_grid):
    the_hood = dict()
    for y, octo_line in enumerate(octo_grid):
        for x, octo in enumerate(octo_line):
            xs = [x_2 for x_2 in range(x - 1, x + 2) if 0 <= x_2 < 10]
            ys = [y_2 for y_2 in range(y - 1, y + 2) if 0 <= y_2 < 10]
            the_hood[(y, x)] = [coord for coord in product(ys, xs)]
    return the_hood


if __name__ == '__main__':
    elf_a = octo_flash_a(day_file, 100)
    elf_b = octo_flash_b(day_file)
    # ten_b = finish_the_lines_b(day_file)
    console.print(f'solution 11A: {elf_a}')
    console.print(f'solution 11B: {elf_b}')

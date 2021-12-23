from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from math import dist
from functools import reduce
from itertools import product
from collections import defaultdict
import numpy as np

day_file = parse_file_as_list('input/day_20.txt')
test_file = parse_file_as_list('input/day_20_test.txt')


def get_algo_and_image(file: list[str]) -> (np.array, np.array):
    algo = np.array([[char == '#' for char in line] for line in file[0]], dtype=int)
    image = np.array([[char == '#' for char in line] for line in file[2:]], dtype=int)
    return algo, image


def get_the_hood_8(grid: np.array) -> dict:
    max_y = grid.shape[0]
    max_x = grid.shape[1]
    the_hood = dict()
    for y, line in enumerate(grid):
        for x, num in enumerate(line):
            xs = [x_2 for x_2 in range(x - 1, x + 2) if 0 <= x_2 < max_x]
            ys = [y_2 for y_2 in range(y - 1, y + 2) if 0 <= y_2 < max_y]
            the_hood[(y, x)] = [coord for coord in product(ys, xs)]
    return the_hood


@dataclass
class ImageEnhancer:
    image: np.array
    algorithm: np.array
    the_hood: dict = field(init=False)

    def enhance(self):
        new_image = np.zeros(shape=self.image.shape, dtype=int)

        for y, line in enumerate(self.image):
            for x, pixel in enumerate(line):
                binary_str = ''.join([str(pixel) for pixel in self.image[y - 1:y + 2, x - 1:x + 2].flatten()]).zfill(9)
                decimal_val = int(binary_str, 2)
                pixel_val = self.algorithm[decimal_val]
                new_image[y, x] = pixel_val

        self.image = new_image[1:-1, 1:-1]

    def get_pixel_count(self):
        return np.count_nonzero(self.image)


@time_function()
def run_a(file, n):
    algo, image = get_algo_and_image(file)
    image = np.pad(image, n * 2, constant_values=0)
    enhancer = ImageEnhancer(image, algo)

    np.set_printoptions(linewidth=np.nan, formatter={'all': lambda x: '#' if x == 1 else '.'})

    for _ in range(n):
        enhancer.enhance()

    return enhancer.get_pixel_count()


if __name__ == '__main__':
    answer_a = run_a(day_file, 2)
    answer_b = run_a(day_file, 50)

    console.print(f'solution 20A: {answer_a}')
    console.print(f'solution 20B: {answer_b}')


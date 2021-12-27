from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
import numpy as np

day_file = parse_file_as_list('input/day_21.txt')
test_file = parse_file_as_list('input/day_22_test.txt')



@time_function()
def run_a(file):
   pass


@time_function()
def run_b(file):
    pass


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution 21A: {answer_a}')
    console.print(f'solution 21B: {answer_b}')

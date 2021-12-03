from typing import Callable
import time
from rich.console import Console

console = Console(color_system='truecolor')

def parse_file_as_list(file):
    return [num.rstrip('\n') for num in open(file=file, newline='\n')]


def convert_str_list_to_int_list(str_list: list[str]) -> list[int]:
    return [int(element) for element in str_list]


def get_runtime(function: Callable):
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = function(*args, **kwargs)
        end = time.perf_counter_ns()
        console.print(f'[bold blue]{function.__name__}[/bold blue]', '[red]ran for[/red]', (end-start)/1e6, '[red]ms[/red]')
        return result
    return wrapper


def time_function(iterations: int, function: Callable, *args, **kwargs):
    start = time.perf_counter_ns()
    for _ in range(iterations):
        function(*args, **kwargs)
    end = time.perf_counter_ns()
    console.print(f'[bold blue]{function.__name__}[/bold blue]', '[red]ran for[/red]', (end - start) / 1e6,'[red]ms[/red]')

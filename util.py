from typing import Callable
import time
from rich.console import Console

console = Console(color_system='truecolor')


def parse_file_as_list(file):
    return [num.rstrip('\n') for num in open(file=file, newline='\n')]


def convert_str_list_to_int_list(str_list: list[str]) -> list[int]:
    return [int(element) for element in str_list]


# Time function runtime in ms
def get_runtime(function: Callable):
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = function(*args, **kwargs)
        end = time.perf_counter_ns()
        console.print(f'[bold blue]{function.__name__}[/bold blue]',
                      '[red]ran for[/red]', (end - start) / 1e6,
                      '[red]ms[/red]')
        return result

    return wrapper


# Time function runtime for 'n' iterations in ms
def time_function(iterations: int = 100):
    def decorator(function: Callable):
        def wrapper(*args, **kwargs):
            start = time.perf_counter_ns()

            result = None
            for _ in range(iterations):
                result = function(*args, **kwargs)

            end = time.perf_counter_ns()

            # Total runtime
            console.print(f'[bold blue]{function.__name__}[/bold blue]',
                          f'[red]total runtime for[/red]',
                          f'{iterations}',
                          f'[red]iterations[/red]',
                          (end - start) / 1e6,
                          '[red]ms[/red]')

            # Average runtime
            console.print(f'[bold blue]{function.__name__}[/bold blue]',
                          f'[red]average runtime for[/red]',
                          f'{iterations}',
                          f'[red]iterations[/red]',
                          (end - start) / 1e6 / iterations,
                          '[red]ms[/red]')

            return result
        return wrapper
    return decorator

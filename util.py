import time
from rich import print


def parse_file_as_list(file):
    return [num.rstrip('\n') for num in open(file=file, newline='\n')]


def convert_str_list_to_int_list(str_list: list[str]) -> list[int]:
    return [int(element) for element in str_list]


def get_runtime(function):
    def wrapper(*args, **kwargs):
        start = time.time_ns()
        result = function(*args, **kwargs)
        end = time.time_ns()
        print(f'[bold blue]{function.__name__}[/bold blue]', '[red]ran for[/red]', (end-start)/1e6, '[red]ms[/red]')
        return result
    return wrapper

def parse_file_as_list(file):
    return [num.rstrip('\n') for num in open(file=file, newline='\n')]


def convert_str_list_to_int_list(str_list: list[str]) -> list[int]:
    return [int(element) for element in str_list]

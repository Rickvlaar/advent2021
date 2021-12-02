from rich import print
import util

day_2_directions = util.parse_file_as_list('input/day_2.txt')
test_directions = ['forward 5',
                   'down 5',
                   'forward 8',
                   'up 3',
                   'down 8',
                   'forward 2']


class Submarine:
    def __init__(self, directions: list[list[str, int]], manual_version: str):
        self.depth = 0
        self.horizontal_pos = 0
        self.aim = 0
        self.directions = directions
        self.manual_version = manual_version

    @util.get_runtime
    def process_directions(self):
        for direction, val in self.directions:
            self.get_direction_handler(direction)(val)

    def get_direction_handler(self, direction: str):
        match direction:
            case 'forward':
                return self.forwards_a if self.manual_version == 'a' else self.forwards_b
            case 'up':
                return self.up if self.manual_version == 'a' else self.up_aim
            case 'down':
                return self.down if self.manual_version == 'a' else self.down_aim

    def forwards_a(self, val: int):
        self.horizontal_pos += val

    def forwards_b(self, val: int):
        self.horizontal_pos += val
        self.depth += (val * self.aim)

    def down(self, val: int):
        self.depth += val

    def up(self, val: int):
        self.depth -= val

    def down_aim(self, val: int):
        self.aim += val

    def up_aim(self, val: int):
        self.aim -= val


def split_command_and_value(list_str: list[str]) -> list[list[str, int]]:
    return [[a, int(b)] for a, b in [line.split(' ') for line in list_str]]


# moved this out so I can properly measure runtime
def prepare_input(filename):
    return split_command_and_value(filename)


@util.get_runtime
def get_solutions(command_value_list):
    sub_a = Submarine(directions=command_value_list, manual_version='a')
    sub_b = Submarine(directions=command_value_list, manual_version='b')

    sub_a.process_directions()
    sub_b.process_directions()

    print(f'solution 2A: {sub_a.depth * sub_a.horizontal_pos}')
    print(f'solution 2B: {sub_b.depth * sub_b.horizontal_pos}')


if __name__ == '__main__':
    get_solutions(prepare_input(test_directions))
    get_solutions(prepare_input(day_2_directions))

from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from math import prod

day_file = parse_file_as_list('input/day_16.txt')
test_file = parse_file_as_list('input/day_16_test.txt')


@dataclass
class Command:
    version: int
    command_type: int
    length_type: int = field(init=False, default=int)
    length: int = field(init=False, default=6)
    sub_packets_string: str = field(init=False, default=str)
    value: int = field(init=False, default=0)
    sub_packets: list['Command'] = field(default_factory=list, init=False)

    def is_literal(self):
        return self.command_type == 4

    def sum(self):
        self.value = sum([command.value for command in self.sub_packets])

    def product(self):
        self.value = prod([command.value for command in self.sub_packets])

    def min(self):
        self.value = min([command.value for command in self.sub_packets])

    def max(self):
        self.value = max([command.value for command in self.sub_packets])

    def greater_than(self):
        self.value = 1 if self.sub_packets[0].value > self.sub_packets[1].value else 0

    def less_than(self):
        self.value = 1 if self.sub_packets[0].value < self.sub_packets[1].value else 0

    def equals(self):
        self.value = 1 if self.sub_packets[0].value == self.sub_packets[1].value else 0

    def perform_command_function(self):
        if self.command_type == 0:
            self.sum()
        elif self.command_type == 1:
            self.product()
        elif self.command_type == 2:
            self.min()
        elif self.command_type == 3:
            self.max()
        elif self.command_type == 5:
            self.greater_than()
        elif self.command_type == 6:
            self.less_than()
        elif self.command_type == 7:
            self.equals()
    

@dataclass
class BinParser:
    bin_string: str
    commands: list[Command] = field(default_factory=list, init=False)

    def run(self):
        while len(self.bin_string) and int(self.bin_string):
            self.commands.append(self.parse_command())

    def parse_command(self) -> Command:
        command = Command(
                version=self.get_version(),
                command_type=self.get_type()
        )

        if command.is_literal():
            self.parse_literal_command(command)
        else:
            self.parse_operator_command(command)
            
        command.perform_command_function()
        return command

    def parse_literal_command(self, command: Command):
        command = self.read_sub_packets(command)
        zeroes_to_delete = len(command.sub_packets_string) % 4
        if zeroes_to_delete:
            self.reduce_bin_string(4 - zeroes_to_delete)

    def parse_operator_command(self, command: Command):
        command.length += 1
        command.length_type = self.get_length_type()

        if command.length_type == 0:
            self.parse_subs_by_length(command)
        else:
            self.parse_subs_by_packet_count(command)

    def parse_subs_by_length(self, command):
        # FIXME: this count
        bla = self.bin_string[0:16]
        total_length_of_bits_subpackets = int(self.bin_string[0:15], 2)
        command.length += 15
        self.reduce_bin_string(15)

        x = 0

        # steps of four in chars leads to trailing zeroes
        while x < total_length_of_bits_subpackets:
            sub_command = self.parse_command()
            command.sub_packets.append(sub_command)
            command.length += sub_command.length
            x += sub_command.length

        # remove trailing 0
        self.reduce_bin_string(total_length_of_bits_subpackets - x)

    def parse_subs_by_packet_count(self, command: Command):
        sub_packet_count = int(self.bin_string[0:11], 2)
        command.length += 11
        self.reduce_bin_string(11)

        for _ in range(sub_packet_count):
            sub_command = self.parse_command()
            command.length += sub_command.length
            command.sub_packets.append(sub_command)

    def read_sub_packets(self, command: Command) -> Command:
        has_more = 1

        command.sub_packets_string = ''
        while has_more:
            command.sub_packets_string += self.bin_string[1:5]
            has_more = int(self.bin_string[0])
            self.reduce_bin_string(5)
            command.length += 5
        command.value = int(command.sub_packets_string, 2)
        return command

    def get_length_type(self) -> int:
        length_type = int(self.bin_string[0], 2)
        self.reduce_bin_string(1)
        return length_type

    def get_version(self) -> int:
        version = int(self.bin_string[0:3], 2)
        self.reduce_bin_string(3)
        return version

    def get_type(self) -> int:
        command_type = int(self.bin_string[0:3], 2)
        self.reduce_bin_string(3)
        return command_type

    def reduce_bin_string(self, by: int):
        self.bin_string = self.bin_string[by:]


def get_prefix_zeroes(first_char):
    prexif_zeroes = ''

    if first_char == '0':
        prexif_zeroes = '0000'
    elif first_char == '1':
        prexif_zeroes = '000'
    elif first_char in '23':
        prexif_zeroes = '00'
    elif first_char in '4567':
        prexif_zeroes = '0'

    return prexif_zeroes


def sum_versions(command: Command, version_sum: int):
    version_sum += command.version
    for sub_command in command.sub_packets:
        version_sum = sum_versions(sub_command, version_sum)
    return version_sum


@time_function()
def run_a(file) -> int:
    bin_string = get_prefix_zeroes(file[0][0]) + bin(int(file[0], 16))[2:]  # remove the 0b prefix

    bin_parser = BinParser(bin_string)
    bin_parser.run()

    return sum_versions(bin_parser.commands[0], 0)


@time_function()
def run_b(file):
    bin_string = get_prefix_zeroes(file[0][0]) + bin(int(file[0], 16))[2:]  # remove the 0b prefix

    bin_parser = BinParser(bin_string)
    bin_parser.run()
    return bin_parser.commands[0].value


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution 16A: {answer_a}')
    console.print(f'solution 16B: {answer_b}')

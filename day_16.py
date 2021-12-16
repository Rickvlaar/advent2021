from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
import numpy as np

day_file = parse_file_as_list('input/day_16.txt')
test_file = parse_file_as_list('input/day_16_test.txt')


# The three bits labeled V (110) are the packet version, 6.
# The three bits labeled T (100) are the packet type ID, 4, which means the packet is a literal value.
# The five bits labeled A (10111) start with a 1 (not the last group, keep reading) and contain the first four bits of the number, 0111.
# The five bits labeled B (11110) start with a 1 (not the last group, keep reading) and contain four more bits of the number, 1110.
# The five bits labeled C (00101) start with a 0 (last group, end of packet) and contain the last four bits of the number, 0101.
# The three unlabeled 0 bits at the end are extra due to the hexadecimal representation and should be ignored.

# T4
# 3   3   5     5     5
# VVV TTT AAAAA BBBBB CCCCC

# T1 & T6
#   3   3 1 15              11          16
# VVV TTT I LLLLLLLLLLLLLLL AAAAAAAAAAA BBBBBBBBBBBBBBBB


@dataclass
class Command:
    version: int
    command_type: int
    length_type: int = field(init=False, default=int)
    length: int = field(init=False, default=6)
    sub_packets_string: str = field(init=False, default=str)
    value: int = field(init=False, default=int)
    sub_packets: list['Command'] = field(default_factory=list, init=False)

    def is_literal(self):
        return self.command_type == 4


@dataclass
class BinParser:
    bin_string: str
    commands: list[Command] = field(default_factory=list, init=False)

    def run(self):
        while len(self.bin_string) and int(self.bin_string):
            self.parse_command()

    def parse_command(self) -> Command:
        command = Command(
                version=self.get_version(),
                command_type=self.get_type()
        )
        self.commands.append(command)

        if command.is_literal():
            self.parse_literal_command(command)
        else:
            self.parse_operator_command(command)

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


def run_a(file) -> int:
    # remove the 0b prefix
    prexif_zeroes = ''

    # first_char = int(file[0][0], 16)
    # if  first_char == '0':
    #     prexif_zeroes.zfill(4)
    # elif first_char == '1':
    #     prexif_zeroes.zfill(3)
    # elif first_char

    bin_string = '00' + bin(int(file[0], 16))[2:]
    bin_parser = BinParser(bin_string)
    bin_parser.run()


    return sum([command.version for command in bin_parser.commands])




def run_b(file):
    pass


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution 16A: {answer_a}')
    console.print(f'solution 16B: {answer_b}')

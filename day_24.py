from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from collections import defaultdict
from itertools import product
import numpy as np

day_file = parse_file_as_list('input/day_24.txt')
test_file = parse_file_as_list('input/day_24_test.txt')


@dataclass
class ALU:
    commands: list[list[str]]
    model_no: list[int] = field(init=False)
    at_inp: int = field(default=0)
    programs: dict[int: list[list[str]]] = field(init=False)
    vars: defaultdict = field(default_factory=defaultdict)

    def split_programs(self):
        self.programs = dict()
        no = 1
        commands_in_program = []
        for command in self.commands:
            if command[0] == 'inp':
                commands_in_program = [command]
                self.programs[no] = commands_in_program
                no += 1
            else:
                commands_in_program.append(command)

    def run_program(self):
        for command in self.commands:
            if command[0] == 'inp':
                # self.vars['w'] = inp_no
                self.inp(command)
            elif command[0] == 'add':
                self.add(command)
            elif command[0] == 'mul':
                self.mul(command)
            elif command[0] == 'div':
                self.div(command)
            elif command[0] == 'mod':
                self.mod(command)
            elif command[0] == 'eql':
                self.eql(command)

    def inp(self, command):
        command, store_at = command
        self.vars[store_at] = self.model_no[self.at_inp]
        self.at_inp += 1
        console.print(self.vars)

    def add(self, command):
        command, store_at, do_with = command
        if do_with.lstrip('-').isnumeric():
            self.vars[store_at] += int(do_with)
        else:
            self.vars[store_at] += self.vars[do_with]

    def mul(self, command):
        command, store_at, do_with = command
        if do_with.lstrip('-').isnumeric():
            self.vars[store_at] *= int(do_with)
        else:
            self.vars[store_at] *= self.vars[do_with]

    def div(self, command):
        command, store_at, do_with = command
        if do_with.lstrip('-').isnumeric():
            do_with = int(do_with)
            if do_with == 0 or self.vars[store_at] == 0:
                return
            self.vars[store_at] //= do_with
        else:
            self.vars[store_at] //= self.vars[do_with]

    def mod(self, command):
        command, store_at, do_with = command
        if do_with.lstrip('-').isnumeric():
            do_with = int(do_with)
            if do_with <= 0 or self.vars[store_at] < 0:
                return
            self.vars[store_at] = self.vars[store_at] % do_with
        else:
            self.vars[store_at] = self.vars[store_at] % self.vars[store_at]

    def eql(self, command):
        command, store_at, do_with = command
        if do_with.lstrip('-').isnumeric():
            self.vars[store_at] = 1 if int(do_with) == self.vars[store_at] else 0
        else:
            self.vars[store_at] = 1 if self.vars[do_with] == self.vars[store_at] else 0


def creat_alu_from_file(file: list[str]):
    parsed_file = [line.split(' ') for line in file]
    alu = ALU(commands=parsed_file)
    alu.vars = defaultdict(int)
    return alu


def split_programs(commands: list[list[str]]):
    programs = dict()
    no = 1
    commands_in_program = []
    for command in commands:
        if command[0] == 'inp':
            commands_in_program = [command]
            programs[no] = commands_in_program
            no += 1
        else:
            commands_in_program.append(command)
    return programs


@dataclass
class Program:
    no: int
    x_modifier: int
    y_modifier: int
    z_divider: int

    def run(self, w, z):

        if self.is_positive():
            # y = w + self.y_modifier
            z = (z * 26) + w + self.y_modifier

        else:
            x = 0 if (z % 26) + self.x_modifier == w else 1

            if x == 0:
                z //= 26
            else:
                # y = w + self.y_modifier
                z += w + self.y_modifier
        # z % 26 should always be equal to w - xmodifier
        return z

    def rev_run(self, w, target_z):
        if self.is_positive():
            z = (target_z / 26) - (w + self.y_modifier)
        else:
            z = (target_z * 26) + (w - self.x_modifier)
        return z

    def is_negative(self):
        return self.x_modifier < 0

    def is_positive(self):
        return self.x_modifier > 0


def get_program(program, no):
    x_modifier = int(program[5][2])
    y_modifier = int(program[15][2])
    z_divider = int(program[4][2])
    return Program(no, x_modifier, y_modifier, z_divider)


def get_modifiers(programs_dict: dict):
    program_modifiers = defaultdict(Program)
    for progno, program in programs_dict.items():
        program_modifiers[progno] = get_program(program, progno)
    return program_modifiers


@time_function()
def run_a(file):
    parsed_file = [line.split(' ') for line in file]
    programs_dict = split_programs(parsed_file)
    simple_programs_dict = get_modifiers(programs_dict)

    # the final Z should be 0

    version_no = int(1e7)
    version = [9 for _ in range(14)]
    looking = 1
    while looking:
        version, version_no = change_version_no(version_no, version, simple_programs_dict)
        looking = check_version(simple_programs_dict, version)

    console.print(version)


def check_version(simple_programs_dict, version):
    z = 0
    for index, no in enumerate(version):
        program = simple_programs_dict[index + 1]
        w = 9

        if program.is_negative():
            w = (z % 26) + program.x_modifier

            if w > 9 or w < 1:
                if version[0] < 2:
                    console.print('prog', program.no, program)
                    console.print(w)
                    console.print(version)
                # console.print('ali illegali')
                return 1

        z = program.run(w, z)
        console.print(z)
        # console.print(version)
    return 0


def change_version_no(version_no: int, version, simple_programs_dict):
    version_no -= 1
    version_str = str(version_no)
    while '0' in version_str:
        version_no -= 1
        version_str = str(version_no)

    pos = 0
    for index, val in enumerate(version):
        if simple_programs_dict[index + 1].is_positive():
            version[index] = int(version_str[pos])
            pos += 1
    return version, version_no


def go_looking(program: Program, target_z: int, simple_programs_dict: dict[int: Program], possibilities: dict,
               path_str: str = '', ):
    for w in range(9, 0, -1):
        new_target_z = program.run(w, target_z)

        if program.no >= 8:
            # all we need is the path and last z
            possibilities[new_target_z] = path_str
            return

        sub_program = simple_programs_dict[program.no + 1]
        go_looking(sub_program, new_target_z, simple_programs_dict, possibilities, path_str + str(w))


def go_looking_back(program: Program, target_z: int, simple_programs_dict: dict[int: Program], possibilities: dict,
                    path_str: str = '', ):
    for w in range(9, 0, -1):
        new_target_z = program.rev_run(w, target_z)

        if program.no <= 7:
            # all we need is the path and last z
            possibilities[new_target_z] = path_str
            return
        else:
            sub_program = simple_programs_dict[program.no - 1]
            go_looking_back(sub_program, new_target_z, simple_programs_dict, possibilities, str(w) + path_str)


def match_target(program: Program, target_z: int):
    subpossibles = dict()
    for w in range(9, 0, -1):
        z = program.rev_run(w, target_z)

        console.print(z)
    return subpossibles


@time_function()
def run_b(file):
    pass


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution 24A: {answer_a}')
    console.print(f'solution 24B: {answer_b}')

# def really(z, w):
# x always starts as 0
# y always starts as 0
# z can be any int

# inp w
# mul x 0 == 0
# add x z == any int x == z
# mod x 26 == 0 - 25
# div z 26/1 == any int
# add x -4 == (0-25) - 4
# eql x w == 0 or 1
# eql x 0 == 0 or 1

# what it do?
#   if (z % 26) + modifier == w: x = 0

# mul y 0 == 0
# add y 25 == 25
# mul y x == 25 or 0
# add y 1 == 26 or 1

# what it do?
#   if x == 1: y == 26
#   if x == 0: y == 1

# if y == 1, z stays the same
# mul z y == any int

# mul y 0 == always 0
# add y w == 1-9
# add y 12 == 1-9 + 12 (13 - 21)
# mul y x == 0 or (1-9 + 12)

# if y == 0, z stays the same
# z = z / 26 * (1 or 26) + (w + modifier or 0)

# add z y == any int

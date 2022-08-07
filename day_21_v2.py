from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from math import prod
from itertools import cycle, product, combinations_with_replacement
from copy import copy, deepcopy

day_file = parse_file_as_list('input/day_21.txt')
test_file = parse_file_as_list('input/day_21_test.txt')


@dataclass
class Turn:
    throw: int
    one_score: int
    one_pos: int
    two_score: int
    two_pos: int
    winner: int = None
    # next_turns: list['Turn'] = field(default_factory=list)


won_games_1 = 0
won_games_2 = 0
universes_won_1 = 0
universes_won_2 = 0
all_possible_throws = [throw for throw in product([1, 2, 3], repeat=3)]
throw_values = [sum(throw) for throw in all_possible_throws]
throw_value_frequency = Counter(throw_values)  # ranges from 3-9


def play_dirac():
    first_turn = Turn(throw=0,
                      one_score=0,
                      one_pos=3,
                      two_score=0,
                      two_pos=4)

    play_rounds(turn=first_turn, who_turn=1, universes_created=1)

    console.print(
        f'games finished: {won_games_1 + won_games_2:,}, player 1: {universes_won_1:,}, player 2: {universes_won_2:,}')


def play_rounds(turn: Turn, who_turn: int, universes_created: int) -> None:
    for throw in range(3, 10):
        new_turn = Turn(throw=throw,
                        one_pos=turn.one_pos,
                        one_score=turn.one_score,
                        two_pos=turn.two_pos,
                        two_score=turn.two_score)
        new_universes_created = universes_created * throw_value_frequency[throw]

        is_game_won = do_turn(new_turn, throw_value=throw, who_turn=who_turn)

        if is_game_won:
            if who_turn == 1:
                global universes_won_1
                universes_won_1 += new_universes_created
            else:
                global universes_won_2
                universes_won_2 += new_universes_created
        else:
            new_who_turn = 2 if who_turn == 1 else 1
            play_rounds(turn=new_turn, who_turn=new_who_turn, universes_created=new_universes_created)


def do_turn(turn: Turn, throw_value: int, who_turn: int) -> bool:
    if who_turn == 1:
        new_pos = (turn.one_pos + throw_value) % 10
        if not new_pos:
            new_pos = 10

        turn.one_pos = new_pos
        turn.one_score += turn.one_pos

        if turn.one_score >= 21:
            # global won_games_1
            # won_games_1 += 1
            turn.winner = 1
            return True

    elif who_turn == 2:
        new_pos = (turn.two_pos + throw_value) % 10
        if not new_pos:
            new_pos = 10

        turn.two_pos = new_pos
        turn.two_score += turn.two_pos

        if turn.two_score >= 21:
            # global won_games_2
            # won_games_2 += 1
            turn.winner = 2
            return True

    else:
        return False


def run_a(file):
    play_dirac()

    return 1


if __name__ == '__main__':
    answer_a = run_a(day_file)
    # answer_b = run_b(test_file)

    console.print(f'solution 21A: {answer_a}')

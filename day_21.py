from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from math import prod
from itertools import cycle, product, permutations
from copy import copy

day_file = parse_file_as_list('input/day_21.txt')
test_file = parse_file_as_list('input/day_21_test.txt')


@dataclass
class Player:
    number: int
    position: int
    score: int = field(default=0)
    rolls: list[int] = field(default_factory=list)


# moving clockwise on spaces in order of increasing value, wrapping back around to 1 after 10
def deterministic(players: list[Player]):
    total_roll_count = 0
    roll_values = 0
    for x in cycle(range(1, 101)):
        total_roll_count += 1
        roll_values += x

        if total_roll_count % 3 == 0:
            player = players.pop(0)
            # mod 10 goes awry when hitting exactly 20,30 etc
            new_pos = (player.position + roll_values) % 10
            if not new_pos:
                new_pos = 10

            player.position = new_pos

            player.score += player.position
            players.append(player)
            roll_values = 0

            if player.score >= 1000:
                return players, total_roll_count


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


def play_dirac(players: list[Player]):
    first_turn = Turn(throw=0,
                      one_score=0,
                      one_pos=players[0].position,
                      two_score=0,
                      two_pos=players[1].position)

    # play_rounds(turn=first_turn, who_turn=1, universes_created=1)
    play_rounds_2(one_pos=first_turn.one_pos,
                  one_score=first_turn.one_score,
                  two_pos=first_turn.two_pos,
                  two_score=first_turn.two_score,
                  who_turn=1,
                  universes_created=1)

    console.print(
            f'games finished: {won_games_1 + won_games_2:,}, player 1: {universes_won_1:,}, player 2: {universes_won_2:,}')

    return universes_won_1 if universes_won_1 > universes_won_2 else universes_won_2


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


def play_rounds_2(one_pos: int, one_score: int, two_pos: int, two_score: int, who_turn: int,
                  universes_created: int) -> None:

    for throw in range(3, 10):
        new_universes_created = universes_created * throw_value_frequency[throw]

        if who_turn == 1:
            new_score, new_pos = do_turn_2(pos=one_pos, score=one_score, throw_value=throw)
        else:
            new_score, new_pos = do_turn_2(pos=two_pos, score=two_score, throw_value=throw)

        if new_score >= 21:
            if who_turn == 1:
                global universes_won_1
                universes_won_1 += new_universes_created
            else:
                global universes_won_2
                universes_won_2 += new_universes_created
        else:
            new_who_turn = 2 if who_turn == 1 else 1
            if who_turn == 1:
                play_rounds_2(one_pos=new_pos,
                              one_score=new_score,
                              two_pos=two_pos,
                              two_score=two_score,
                              who_turn=new_who_turn,
                              universes_created=new_universes_created)
            else:
                play_rounds_2(one_pos=one_pos,
                              one_score=one_score,
                              two_pos=new_pos,
                              two_score=new_score,
                              who_turn=new_who_turn,
                              universes_created=new_universes_created)


def do_turn_2(pos: int, score: int, throw_value: int) -> (int, int):
    new_pos = (pos + throw_value) % 10
    if not new_pos:
        new_pos = 10

    pos = new_pos
    score += pos

    return score, pos


def do_turn(turn: Turn, throw_value: int, who_turn: int) -> bool:
    if who_turn == 1:
        new_pos = (turn.one_pos + throw_value) % 10
        if not new_pos:
            new_pos = 10

        turn.one_pos = new_pos
        turn.one_score += turn.one_pos

        if turn.one_score >= 21:
            turn.winner = 1
            return True

    elif who_turn == 2:
        new_pos = (turn.two_pos + throw_value) % 10
        if not new_pos:
            new_pos = 10

        turn.two_pos = new_pos
        turn.two_score += turn.two_pos

        if turn.two_score >= 21:
            turn.winner = 2
            return True

    else:
        return False


def parse_file(file: list[str]):
    player_1_pos = file[0].removeprefix('Player 1 starting position: ')
    player_2_pos = file[1].removeprefix('Player 2 starting position: ')
    return [Player(1, int(player_1_pos)), Player(2, int(player_2_pos))]


@time_function()
def run_a(file):
    players = parse_file(file)
    players, total_roll_count = deterministic(players)
    return min([player.score * total_roll_count for player in players])


@time_function()
def run_b(file):
    players = parse_file(file)
    return play_dirac(players)


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution 21A: {answer_a}')
    console.print(f'solution 21B: {answer_b}')

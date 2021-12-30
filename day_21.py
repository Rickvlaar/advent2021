from util import console, parse_file_as_list, time_function
from dataclasses import dataclass, field
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
            # mod 10 goes awry when hitting exactyl 20,30 etc
            new_pos = (player.position + roll_values) % 10
            if not new_pos:
                new_pos = 10

            player.position = new_pos

            player.score += player.position
            players.append(player)
            roll_values = 0

            if player.score >= 1000:
                return players, total_roll_count


def dirac(players: list[Player]):
    # die_score will always be 3-9 -> 7 possibilities per player, per round after 3 dice rolls
    # every round has 2 players
    # that means 7**2 possibilities per round == 49
    # longest possible game is 21 rounds or 63 throws
    # winning score >= 21
    # see what player wins for throw sequence, then calculate universes from that

    # These are the example values (Looping is not an option)
    # 444356092776315 + 341960390180808 = 786316482957123
    # 26982324785360601
    # 786,316,482,957,123 games played

    # check_winning_turn((0, 8), rolls=tuple(), roll_turn_dict=winner_dict)
    # recurshit((0,4), (0,8), tuple(), winner_dict)

    player_1 = get_winning_turns_dict((0, 4))
    player_2 = get_winning_turns_dict((0, 8))
    console.print(max(len(x) for x in player_1))
    console.print(max(len(x) for x in player_2))

    # current code returns about factor 70 too high
    winners = sum([27**turn for turn in player_1.values()])
    winners2 = sum([27**turn for turn in player_2.values()])

    console.print(winners, winners2)
    return winners


def get_winning_turns_dict(player: tuple):
    winner_dict = dict()
    check_winning_turn(player, rolls=tuple(), roll_turn_dict=winner_dict)
    return winner_dict


def check_winning_turn(player, rolls, roll_turn_dict, turn_count=1):
    possible_turn_rolls = range(3, 10)
    for roll in possible_turn_rolls:
        new_rolls = rolls + (roll,)
        new_player = update_players_score(roll, player)
        if new_player[0] >= 21:
            roll_turn_dict[new_rolls] = turn_count
        else:
            check_winning_turn(new_player, new_rolls, roll_turn_dict, turn_count + 1)
/

def update_players_score(roll: int, player: tuple[int, int]):
    new_pos = (player[1] + roll) % 10
    if not new_pos:
        new_pos = 10
    return player[0] + new_pos, new_pos


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
    players = dirac(players)
    console.print(players)


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution 21A: {answer_a}')
    console.print(f'solution 21B: {answer_b}')

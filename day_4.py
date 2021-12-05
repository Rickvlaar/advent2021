from util import console, parse_file_as_list, get_runtime
import numpy as np

day_4_file = parse_file_as_list('input/day_4.txt')
test_file = parse_file_as_list('input/day_4_test.txt')


class Bingo:
    def __init__(self):
        self.draw_order: list[int] = list()
        self.all_possible_bingos: set[tuple] = set()
        self.drawn_numbers: list[int] = list()
        self.bingo_cards: list[BingoCard] = list()
        self.winner_count: int = 0

    def setup_bingo_from_file(self, file: list[str]) -> None:
        self.draw_order = [int(num) for num in file[0].split(',')]

        numbers = list()
        for line in file[2:]:
            if line:
                numbers.append([int(char.strip()) for char in line.split(' ') if char])
            else:
                self.bingo_cards.append(BingoCard().create_card_from_list(input_matrix=numbers))
                numbers = []
        self.bingo_cards.append(BingoCard().create_card_from_list(input_matrix=numbers))

    def play(self, play_till_end: bool = False) -> int:
        for num in self.draw_order:
            self.drawn_numbers.append(num)
            for card in self.bingo_cards:
                if not card.bingo:
                    card.new_num_draw(num)
                    if card.bingo:
                        self.winner_count += 1
                        if not play_till_end or len(self.bingo_cards) == self.winner_count:
                            return self.get_score(num, card)

    def get_score(self, num, card) -> int:
        unmarked_no_sum = sum(card.card_numbers.difference(self.drawn_numbers))
        final_score = num * unmarked_no_sum
        return final_score


class BingoCard:

    def __init__(self):
        self.number_dict: dict[int: BingoCard.Number] = dict()
        self.card_numbers: set[int] = set()
        self.bingo: bool = False

    def create_card_from_list(self, input_matrix: list[list[int]]) -> 'BingoCard':
        numbers_matrix = np.array(input_matrix)
        transposed_matrix = numbers_matrix.transpose()

        for number_list in numbers_matrix:
            self.card_numbers.update(number_list)
            self.number_dict.update({num: self.Number(set(number_list)) for num in number_list})

        for number_list in transposed_matrix:
            for num in number_list:
                self.number_dict.get(num).inline_number_sets.append(set(number_list))

        return self

    def new_num_draw(self, num: int) -> None:
        if num in self.number_dict:
            card_number = self.number_dict.get(num)
            card_number.drawn = True
            if self.is_bingo(card_number):
                self.bingo = True

    def is_bingo(self, card_number) -> bool:
        for number_set in card_number.inline_number_sets:
            if all([self.number_dict.get(num).drawn for num in number_set]):
                return True

    class Number:

        def __init__(self, number_set: set[int]):
            self.drawn: bool = False
            self.inline_number_sets: list[set] = [number_set]


@get_runtime
def run_a():
    bingo_a = Bingo()
    bingo_a.setup_bingo_from_file(day_4_file)
    return bingo_a.play()


@get_runtime
def run_b():
    bingo_b = Bingo()
    bingo_b.setup_bingo_from_file(day_4_file)
    return bingo_b.play(True)

# only straight lines will win
if __name__ == '__main__':
    a = run_a()
    b = run_b()
    console.print(f'solution 4A: {a}')
    console.print(f'solution 4B: {b}')

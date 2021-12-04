from util import console, parse_file_as_list, get_runtime
from itertools import permutations
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

    def setup_bingo_from_file(self, file: list[str]):
        self.draw_order = [int(num) for num in file[0].split(',')]

        numbers = list()
        for line in file[2:]:
            if line:
                numbers.append([int(char.strip()) for char in line.split(' ') if char])
            else:
                self.bingo_cards.append(BingoCard().create_card_from_list(input_matrix=numbers))
                numbers = []
        self.bingo_cards.append(BingoCard().create_card_from_list(input_matrix=numbers))

    @get_runtime
    def play_2(self):
        for num in self.draw_order:
            console.print(num)
            self.drawn_numbers.append(num)
            for card in self.bingo_cards:
                if not card.bingo:
                    card.new_num_draw(num)
                    if card.bingo:
                        numbersum = sum(card.card_numbers.difference(self.drawn_numbers))
                        console.print(f'Unmarked number sum: {numbersum}')
                        console.print(f'Last number: {num}')
                        console.print(f'Solution 4A: {num}')
                        self.winner_count += 1
                        if self.winner_count == len(self.bingo_cards):
                            return


    # @get_runtime
    # def play(self):
    #     # Start with first 5 numbers, because bingo needs 5
    #     self.drawn_numbers.extend(self.draw_order[:5])
    #     self.all_possible_bingos = set(permutations(self.drawn_numbers))
    #
    #     for num in self.draw_order[4:]:
    #         console.print(num)
    #         self.drawn_numbers.append(num)
    #         self.all_possible_bingos = set(permutations(self.drawn_numbers, 5))
    #         if self.we_have_a_winner():
    #             console.print(f'Last number: {num}')
    #             console.print(f'Solution 4A: {num}')
    #             self.winner_count += 1
    #             if self.winner_count == len(self.bingo_cards):
    #                 return
    #
    # def we_have_a_winner(self):
    #     for card in self.bingo_cards:
    #         if not card.bingo:
    #             if not card.bingo_numbers.isdisjoint(self.all_possible_bingos):
    #                 card.bingo = True
    #                 self.winner_count += 1
    #                 the_winner = card.bingo_numbers.intersection(self.all_possible_bingos)
    #                 # console.print(f'The winner is: {the_winner}')
    #                 numbersum = sum(card.card_numbers.difference(self.drawn_numbers))
    #                 console.print(f'Unmarked number sum: {numbersum}')
    #                 return the_winner


class BingoCard:

    def __init__(self):
        self.bingo_numbers: set[tuple[int]] = set()
        self.number_dict: dict[int: BingoCard.Number] = dict()
        self.card_numbers: set[int] = set()
        self.bingo: bool = False

    def create_card_from_list(self, input_matrix: list[list[int]]):
        numbers_matrix = np.array(input_matrix)
        transposed_matrix = numbers_matrix.transpose()

        for number_list in numbers_matrix:
            self.card_numbers.update(number_list)
            self.number_dict.update({num: self.Number(set(number_list)) for num in number_list})

        for number_list in transposed_matrix:
            for num in number_list:
                self.number_dict.get(num).inline_number_sets.append(set(number_list))

        return self

    def new_num_draw(self, num: int):
        if num in self.number_dict:
            card_number = self.number_dict.get(num)
            card_number.drawn = True
            if self.is_bingo(card_number):
                self.bingo = True
                console.print('BINGO!')

    def is_bingo(self, card_number) -> bool:
        for number_set in card_number.inline_number_sets:
            if all([self.number_dict.get(num).drawn for num in number_set]):
                return True

    class Number:

        def __init__(self, number_set: set[int]):
            self.drawn: bool = False
            self.inline_number_sets: list[set] = [number_set]


# only straight lines will win
if __name__ == '__main__':
    bingo = Bingo()
    bingo.setup_bingo_from_file(day_4_file)
    bingo.play_2()

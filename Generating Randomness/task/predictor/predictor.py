from itertools import product
from random import choice


class Predictor:
    def __init__(self):
        self.prompt = 'Print a random string containing 0 or 1:\n'
        self.data_string = ''
        # an array of all possible permutations of 0 and  1
        self.triplets = [''.join(el) for el in product(('0', '1'), repeat=3)]
        self.pattern = {}
        self.test_string = ''
        self.capital = 1000
        self.start_game = True

    def get_input(self):
        print('Please give AI some data to learn...')
        while True:
            length = len(self.data_string)
            if length < 100:
                print(f'Current data length is {length}, {100 - length} symbols left')
                print(self.prompt)
                line_in = input()
                self.process_input(line_in)
            else:
                print(f'Final data string:')
                print(self.data_string)
                print()
                self.find_triplets(self.data_string)
                self.display_triplets()
                break

    def get_test_string(self):
        while True:
            print(self.prompt)
            self.test_string = input()
            if self.test_string.isdecimal() and '1' in self.test_string and '0' in self.test_string:
                break
            elif self.test_string == 'enough':
                print('Game over!')
                exit(0)
            else:
                self.test_string = ''

    def play_game(self):
        if self.start_game:
            print(f"""You have ${self.capital}. Every time the system successfully predicts your next press, you lose $1.\nOtherwise, you earn 
$1. Print "enough" to leave the game. Let's go!""")
            self.start_game = False
        self.get_test_string()
        self.predict_string()
        # update pattern
        self.find_triplets(self.test_string)
        print(f'Your capital is now ${self.capital}')

    def predict_string(self):
        predicted_string = choice(self.triplets)
        correct = 0
        for i in range(3, len(self.test_string)):
            end_triplet = self.test_string[i - 3:i]
            if self.pattern[end_triplet][0] == self.pattern[end_triplet][1]:
                next_letter = choice(['0', '1'])
            elif self.pattern[end_triplet][0] > self.pattern[end_triplet][1]:
                next_letter = '0'
            else:
                next_letter = '1'
            predicted_string += next_letter
            if next_letter == self.test_string[i]:
                correct += 1
        print('prediction:')
        print(predicted_string)
        correct_percent = round(correct / (len(self.test_string) - 3) * 100, 2)
        print(f'Computer guessed right {correct} out of {len(self.test_string) - 3} symbols ({correct_percent} %)')
        self.capital += len(self.test_string) - 3 - correct * 2

    def process_input(self, line_in):
        for i in line_in:
            if i == '0' or i == '1':
                self.data_string += i

    def find_triplets(self, data_string):
        for triplet in self.triplets:
            zeros = 0
            ones = 0
            for i in range(len(data_string)):
                if data_string[i:i+4] == (triplet + '1'):
                    ones += 1
                elif data_string[i:i+4] == (triplet + '0'):
                    zeros += 1
            self.pattern[triplet] = (zeros, ones)

    def display_triplets(self):
        for triplet in self.pattern:
            zeros = self.pattern[triplet][0]
            ones = self.pattern[triplet][1]
            print(f'{triplet}: {zeros},{ones}')


if __name__ == "__main__":
    pred = Predictor()
    pred.get_input()
    while True:
        pred.play_game()

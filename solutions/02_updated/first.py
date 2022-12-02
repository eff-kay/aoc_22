import pytest
import argparse
import os.path


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    # define the possible shapes and the corresponding scores
    SHAPES = {'A': 'Rock', 'B': 'Paper', 'C': 'Scissors'}
    SCORES = {'X': 1, 'Y': 2, 'Z': 3}
    b_map = {'A':'X', "B":'Y', "C":"Z"}

    # define the function to determine the outcome of a round
    def determine_outcome(player1, player2):
        if player2 == b_map[player1]:
            return 3 # a draw
        elif (player1 == 'C' and player2 == 'Y') or (player1 == 'B' and player2 == 'X') or (player1 == 'A' and player2 == 'Z'):
            return 0 # player1 wins
        else:
            return 6 # player1 loses

    # parse the input and calculate the total score
    total_score = 0
    for line in data.splitlines():
        # split the input into opponent's choice and player's choice
        opponent, player = line.split(' ')
        
        # determine the outcome of the round
        outcome = determine_outcome(opponent, player)
        
        # update the total score
        total_score += SCORES[player] + outcome
        
    # print the total score
    return total_score

INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))
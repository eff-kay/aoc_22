import pytest
import argparse
import os.path


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    a = {'A':'B', 'B':'C', 'C':'A'}
    a_map = {'X':'A', 'Y':'B', 'Z':'C'}
    b = {'X':'Y', 'Y':'Z', 'Z':'X'}
    b_map = {'A':'X', 'B':'Y', 'C':'Z'}

    b_score = {'X': 1, 'Y':2, 'Z':3} 

    inp = data.split("\n")
    inp = [x.split(' ') for x in inp]

    total_score = 0
    for first, sec in inp[:-1]:
        if a[first] == a_map[sec]:
            total_score += 6
        elif b[sec] == b_map[first]:
            total_score += 0
        elif b_map[first] == sec:
            total_score += 3
        else:
            raise Exception(msg='this should not happen')
    
        total_score+=b_score[sec]

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
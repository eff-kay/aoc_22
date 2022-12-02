import pandas as pd
import pytest
import argparse
import os.path

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):

    a = {'A':'B', 'B':'C', 'C':'A'}
    a_rev = {v:k for k,v in a.items()}

    b_map = {'A':'X', 'B':'Y', 'C':'Z'}
    b_score = {'X': 1, 'Y':2, 'Z':3} 

    inp = data.split("\n")[:-1]
    inp = [x.split(' ') for x in inp]


    st = {'X':'loose', 'Y':'draw', 'Z':'win'}

    total_score = 0
    for first, sec in inp[:-1]:

        if st[sec]=='loose':
            sv = b_map[a_rev[first]]
            sv = b_score[sv]
            total_score+=0
        elif st[sec] == 'win':
            sv = b_map[a[first]]
            sv = b_score[sv]
            total_score+=6
        elif st[sec] == 'draw':
            sv = b_map[first]
            sv = b_score[sv]
            total_score+=3
        else:
            raise Exception(msg='this should not happen')
    
        total_score+=sv

    return total_score


INPUT_S = '''A Y
B X
C Z
'''
EXPECTED = 12

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

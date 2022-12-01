import pandas as pd
import pytest
import argparse
import os.path

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split("\n\n")
    inp = [x.rstrip().split('\n') for x in inp]
    inp  = sum(sorted([sum(list(map(int, x))) for x in inp], reverse=True)[:3])
    return inp


INPUT_S = '''\
'''
EXPECTED = -1

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

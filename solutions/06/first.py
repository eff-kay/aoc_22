import pytest
import argparse
import os.path
import re

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(data):
    inp = data

    for i, ch in enumerate(inp[4:], 4):
        print('i',i)
        block = inp[i-4:i]

        if len(set(block)) !=len(block):
            continue
        else:
            return i


INPUT_S = '''\
bvwbjplbgvbhsrlpgdmjqwftvncz
'''
EXPECTED = 5


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        ('nppdvjthqldpwncqszvftbrmjlhg', 6),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11),
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
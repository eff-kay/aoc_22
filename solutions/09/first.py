import pytest
import argparse
import os.path
import re


# increase the recursion depth in python
import sys
sys.setrecursionlimit(10000)

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(data):
    inp = data.splitlines()
    instructions = [[x.split(' ')[0], int(x.split(' ')[1])] for x in inp]

    # simulate the steps
    grid = [['.' for i in range(10)] for j in range(10)]
    start = (0, 0)
    DR = {'L': 0, 'R': 0, 'U': -1, 'D': 1}
    DC = {'L': -1, 'R': 1, 'U': 0, 'D': 0}

    head_position = start
    tail_position = start

    tail_visits = set()

    for i, (di, steps) in enumerate(instructions):

        for _ in range(steps):
            tail_visits.add(tail_position)
            head_position = (head_position[0] + DR[di], head_position[1]+DC[di])

            diff_r = (head_position[0] - tail_position[0])
            dff_c = (head_position[1] - tail_position[1])

            if abs(diff_r)<=1 and abs(dff_c)<=1:
                pass

            elif abs(diff_r)>=2 and abs(dff_c)>=2:
                tail_position = (head_position[0]-1 if tail_position[0]<head_position[0] else head_position[0]+1,
                     head_position[1]-1 if tail_position[1]<head_position[1] else head_position[1]+1)
            elif abs(diff_r)>=2:
                tail_position = (head_position[0]-1 if tail_position[0]<head_position[0] else head_position[0]+1, head_position[1])

            elif abs(dff_c)>=2:
                    tail_position = (head_position[0], head_position[1]-1 if tail_position[1]<head_position[1] else head_position[1]+1)

    return len(tail_visits)

INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
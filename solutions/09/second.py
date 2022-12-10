import pytest
import argparse
import os.path

# increase the recursion depth in python

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.splitlines()
    instructions = [[x.split(' ')[0], int(x.split(' ')[1])] for x in inp]

    # simulate the steps
    start = (0, 0)
    DR = {'L': 0, 'R': 0, 'U': -1, 'D': 1}
    DC = {'L': -1, 'R': 1, 'U': 0, 'D': 0}

    head_position = start

    tails = [(0, 0) for _ in range(9)]
    tail_visits = set()

    def move_tail(head_position, tail_position):

        diff_r = (head_position[0] - tail_position[0])
        diff_c = (head_position[1] - tail_position[1])

        if abs(diff_r)<=1 and abs(diff_c)<=1:
            pass

        elif abs(diff_r)>=2 and abs(diff_c)>=2:
            tail_position = (head_position[0]-1 if tail_position[0]<head_position[0] else head_position[0]+1,
                head_position[1]-1 if tail_position[1]<head_position[1] else head_position[1]+1)
        elif abs(diff_r)>=2:
            tail_position = (head_position[0]-1 if tail_position[0]<head_position[0] else head_position[0]+1, head_position[1])

        elif abs(diff_c)>=2:
                tail_position = (head_position[0], head_position[1]-1 if tail_position[1]<head_position[1] else head_position[1]+1)
        
        return tail_position

    for i, (di, steps) in enumerate(instructions):

        for _ in range(steps):
            head_position = (head_position[0] + DR[di], head_position[1]+DC[di])
            tails[0] = move_tail(head_position, tails[0])
            for ti in range(1,9):
                tails[ti] = move_tail(tails[ti-1], tails[ti])
            tail_visits.add(tails[8])

    return len(tail_visits)

INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


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
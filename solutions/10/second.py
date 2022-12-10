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
    x = 0
    in_progress = True
    cycle_count = 0
    total = 0
    ins = ''
    result = []
    row = ''
    while in_progress:
        # print('cycle count', row, x, ins)
        ins = inp.pop(0)
        if ins == 'noop':
            for _ in range(1):
                if cycle_count%40 in [x, x+1, x+2]:
                    row+='#'
                    print(cycle_count, 'for #', x)
                    if len(row)==40:
                        result.append(row)
                        row = ''
                else:
                    row+='.'
                    print(cycle_count, 'for .', x)
                    if len(row)==40:
                        result.append(row)
                        row = ''
                cycle_count+=1
        else:
            value = int(ins.split(' ')[1])
            for _ in range(2):
                if cycle_count%40 in [x, x+1, x+2]:
                    row+='#'
                    if len(row)==40:
                        result.append(row)
                        row = ''
                else:
                    row+='.'
                    if len(row)==40:
                        result.append(row)
                        row = ''
                cycle_count+=1
            x+=value

        if len(inp) ==0:
            in_progress = False
        

    print('start ---->')
    for j in result:
        print(''.join(j))
    
    print()

    return result

INPUT_S = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''
EXPECTED = '''##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....'''


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
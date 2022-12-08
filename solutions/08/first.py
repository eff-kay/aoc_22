import pytest
import argparse
import os.path
import re


# increase the recursion depth in python
import sys
sys.setrecursionlimit(10000)

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(data):
    grid = data.splitlines()

    grid = [list(map(int,list(row))) for row in grid]

    def is_visible(row, col):
        is_visible = True

        if row == 0 or row == len(grid) - 1 or col == 0 or col == len(grid[row]) - 1:
            is_visible = True
        else:
            is_visible = False
            if not is_visible:
                for i in range(col - 1, -1, -1): 
                    if int(grid[row][i]) >= int(grid[row][col]):
                        is_visible = False
                        break
                    else:
                        is_visible = True
            
            if not is_visible:
                for i in range(col + 1, len(grid[row])):
                    if int(grid[row][i]) >= int(grid[row][col]):
                        is_visible = False
                        break
                    else:
                        is_visible = True
            
            if not is_visible:
                for i in range(row - 1, -1, -1):
                    if int(grid[i][col]) >= int(grid[row][col]):
                        is_visible = False
                        break
                    else:
                        is_visible = True
            
            if not is_visible:
                for i in range(row + 1, len(grid)):
                    if int(grid[i][col]) >= int(grid[row][col]):
                        is_visible = False
                        break
                    else:
                        is_visible = True

        return is_visible

    def traverse_grid(row, col, count):

        if row >= len(grid):
            return count

        if col >= len(grid[row]):
            return traverse_grid(row + 1, 0, count)

        if col < len(grid[row]):
            if is_visible(row, col):
                count += 1
            return traverse_grid(row, col + 1, count)
    

    return traverse_grid(0, 0, 0)

INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
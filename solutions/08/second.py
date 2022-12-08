import pandas as pd
import pytest
import argparse
import os.path
import re
import sys
sys.setrecursionlimit(10000)

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):

    grid = data.splitlines()
    grid = [list(map(int,list(row))) for row in grid]
    
    # compare with max_so_far
    def update_max_so_far(row, col, max_so_far):
        count_up = 0
        for i in range(row - 1, -1, -1):
            print(i, col, grid[i][col] , grid[row][col])
            if grid[i][col] >= grid[row][col]:
                count_up+=1
                break
            count_up += 1

        count_down = 0
        for i in range(row + 1, len(grid)):
            if grid[i][col] >= grid[row][col]:
                count_down+=1
                break
            count_down += 1


        count_left = 0
        for i in range(col - 1, -1, -1):
            if grid[row][i] >= grid[row][col]:
                count_left+=1
                break
            count_left += 1
        
        count_right = 0
        for i in range(col + 1, len(grid[row])):
            if grid[row][i] >= grid[row][col]:
                count_right+=1
                break
            count_right += 1


        total_count = count_up * count_down * count_left * count_right
        return max(max_so_far, total_count)


    def traverse_grid(row, col, max_so_far):
        if row >= len(grid):
            return max_so_far

        if col >= len(grid[row]):
            return traverse_grid(row + 1, 0, max_so_far)

        if col < len(grid[row]):
            max_so_far = update_max_so_far(row, col, max_so_far)
            return traverse_grid(row, col + 1, max_so_far)
    

    return traverse_grid(0, 0, 0)

INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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

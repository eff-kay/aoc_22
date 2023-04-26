import pytest
import argparse
import os.path
import re


# increase the recursion depth in python
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import namedtuple
from dataclasses import dataclass

# TODO: more ground in every direction
def compute(data):
    total = 0

    inp = data.splitlines()
    inp = ['.'*1000+x+'.'*1000 for x in inp]
    inp = ['.'*len(inp[0])]*1000 + inp + ['.'*(len(inp[0]))]*1000
    print(len(inp), len(inp[0]))
    di_data = {}

    north = [(-1,0), (-1, +1), (-1, -1)]
    south = [(+1,0), (+1, +1), (+1, -1)]
    west = [(0, -1), (-1, -1), (+1, -1)]
    east = [(0, +1), (-1, +1), (+1, +1)]


    di_order = [north, south, west, east]
    
    for row in range(len(inp)):
        for col in range(len(inp[0])):
            di_data[(row, col)] =  inp[row][col]

    round = 1
    while round:
        print("ROUNG ", round)
        print()
        elf_positions = {k:v for k,v in di_data.items() if v!='.'}
        # first half: consider the 8 positions adjancent

        proposals = []
        from_map = {}

        for k, v in elf_positions.items():
            move = False
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    row_check = k[0]+i
                    col_check = k[1]+j
                    if (i,j)!=(0,0) and di_data[(row_check, col_check)] == '#' :
                        move=True
                        break
            
            if move:
                # iterate through the 4 directions
                proposed = False
                for dir in di_order:
                    sub_elf_exists = False
                    if not proposed:
                        for i,j in dir:
                            # iterate through the possible checks
                            row_check = k[0]+i
                            col_check = k[1]+j

                            if di_data[(row_check, col_check)]=='#':
                                # if we find somone break, and look at the other direction
                                sub_elf_exists = True
                                break
                        
                        if not sub_elf_exists:
                            # if the end happens because we looked everwhere then we have found the next direction
                            proposed=True
                            next_row = k[0]+dir[0][0]
                            next_col = k[1]+dir[0][1]
                            proposals.append((next_row, next_col))
                            # we will never consider the same next, so it doesn't matter if we override it
                            from_map[(next_row, next_col)] = (k[0], k[1])

                    else:
                        break
            
        # second half
        from collections import Counter
        co = Counter(proposals)
        co = [x for x,y in co.items() if y==1]

        for item in co:
            di_data[item] = '#'
            di_data[from_map[item]] = '.'
            not_moved = False
    
        # rotate the order
        di_order = di_order[1:] + [di_order[0]]
        round+=1

        if round==11:
            break

    total=0

    # find a better way for this bounding box method
    # start with outer, go innter, and remove the rows
    def find_enclosing_rect(di_data, inp):
        result = []

        p_str=''
        for ind, val in di_data.items():
            p_str+=val
            if ind[1]==len(inp[0])-1:
                result.append(p_str)
                p_str = ''
        
        while True:
            if len(set(result[0]))>1:
                break
            else:
                result = result[1:]
        
        while True:
            if len(set(result[-1]))>1:
                break
            else:
                result = result[:-1]

        invert_result = list(zip(*result))

        while True:
            if len(set(invert_result[0]))>1:
                break
            else:
                invert_result = invert_result[1:]

        while True:
            if len(set(invert_result[-1]))>1:
                break
            else:
                invert_result = invert_result[:-1]

        result = list(zip(*invert_result))
        
        return result

    def find_enclosing_rect_efficient(di_data, inp):
        elf_positions = {k:v for k,v in di_data.items() if v!='.'}

        min_row = min([k[0] for k,v in elf_positions.items()])
        max_row = max([k[0] for k,v in elf_positions.items()])
        min_col = min([k[1] for k,v in elf_positions.items()])
        max_col = max([k[1] for k,v in elf_positions.items()])

        result = []

        p_str=''
        for ind, val in di_data.items():
            p_str+=val
            if ind[1]==len(inp[0])-1:
                result.append(p_str)
                p_str = ''

        result = result[min_row:max_row+1] 
        result = [x[min_col:max_col+1] for x in result]

        return result

    # result = find_enclosing_rect(di_data, inp)
    result = find_enclosing_rect_efficient(di_data, inp)

    total = 0
    for row in result:
        for v in row:
            if v =='.':
                total+=1
    return total

INPUT_S = '''.....
..##.
..#..
.....
..##.
.....
'''
EXPECTED = 64

INPUT_S_1 = '''..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............
'''

EXPECTED_1 = 110


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
        # ("1,1,1\n2,1,1", 10),

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
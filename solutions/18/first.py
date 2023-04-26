import pytest
import argparse
import os.path
import re


# increase the recursion depth in python
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import namedtuple
from dataclasses import dataclass

def compute(data):

    @dataclass
    class Side:
        axes:list
        covered:bool

    @dataclass
    class Cube:
        sides:list[Side]
    
    inp = data.splitlines()
    cubes = [list(map(int, x.split(','))) for x in inp]

    form_cubes = []

    for x,y,z in cubes:

        # draw the cube at the location, assuming that it is the top,front,right corner
        front_face = [(x,0,0),(x,y,0), (x,y,z), (x,0,z)]
        back_face = [(x-1,0,0), (x-1, y,0), (x-1,y,z), (x-1,0,z)]

        right_face = [(x,y,0), (0,y,0), (0,y,z), (x,y,z)]
        left_face = [(x,y-1,0), (0,y-1,0), (0,y-1,z), (x,y-1,z)]

        top_face = [(x,0,z), (x,y,z), (0,y,z), (0,0,z)]
        bottom_face = [(x,0,z-1), (x,y,z-1), (0,y,z-1), (0,0,z-1)]
        cube = Cube([Side(front_face, False), Side(back_face, False), Side(right_face, False), Side(left_face, False), Side(top_face, False), Side(bottom_face, False)])

        form_cubes.append(cube)
    
    for i in range(len(form_cubes)):
        for side in form_cubes[i].sides:
            # see if the sides match or not
            for j in range(i+1, len(form_cubes)):
                compare_cube = form_cubes[j]
                
                for compare_side in compare_cube.sides:
                    if set(side.axes)==set(compare_side.axes):
                        side.covered = True
                        compare_side.covered = True
    
    total = 0
    for cube in form_cubes:
        for side in cube.sides:
            if not side.covered:
                total+=1

    return total

INPUT_S = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 64


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
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
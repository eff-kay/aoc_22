import pytest
import argparse
import os.path
import re


# increase the recursion depth in python
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import namedtuple, deque
from functools import lru_cache
from dataclasses import dataclass

def compute(data):
    inp = data.splitlines()
    cubes = set(tuple(map(int, x.split(','))) for x in inp)

    SURFACE = set()
    INNER = set()

    @lru_cache
    def surface_bfs(x,y,z):
        if (x,y,z) in SURFACE:
            return True

        if (x,y,z) in INNER:
            return False

        SEEN = set()
        Q = deque([(x,y,z)])

        while Q:
            x,y,z = Q.popleft()

            # if it exits in cubes then its an adjoining surface
            if (x,y,z) in cubes:
                continue

            if (x,y,z) in SEEN:
                continue

            SEEN.add((x,y,z))

            # if we go infinite then its a surface point
            if len(SEEN)>5000:
                for p in SEEN:
                    SURFACE.add(p)
                return True
            
            # append neighbours
            for d in (-1, +1):
                Q.append((x+d, y, z))
                Q.append((x, y+d, z))
                Q.append((x, y, z+d))
                
            # this will be overridden by out
            for p in SEEN:
                INNER.add(p)

    total =0

    print(cubes)
    for (x,y,z) in cubes:
        for d in (-1, +1):
            if surface_bfs(x+d, y, z):
                total+=1

            if surface_bfs(x, y+d, z):
                total+=1
            if surface_bfs(x, y, z+d):
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
EXPECTED = 58


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
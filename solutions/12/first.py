import pytest
import argparse
import os.path
import re


# increase the recursion depth in python
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import namedtuple

def compute(data):
    inp = data.splitlines()


    # we can use a namedtuple to store the position and the distance
    pos_dis = namedtuple('pos_dis', ['pos', 'dis']) 

    # we can use a set to store the visited nodes
    visited = set()

    # we can use a list to store the nodes to visit
    to_visit = [pos_dis((0,0), 0)]
    # start travering from 0,0 and go all way till we reach E.
    distance = 0
    while to_visit:
        # implement the djiakstra algorithm to find the shortest path to E
        # we the neighbour function is only fetching the neighbours whose ord value is greater or equal to the current node

        # pop the first element from the list
        pos, dis = to_visit.pop(0)
        print('tryhing', pos, inp[pos[0]][pos[1]], dis)

        if pos in visited:
            continue
            

        distance = dis

        # check if we have reached E
        if inp[pos[0]][pos[1]] == 'E':
            print('dis', dis)
            distance = dis+1
            break

        # add the adjacent nodes to the list
        if pos[0] > 0:
            # top
            next_pos = (pos[0]-1, pos[1])
            if next_pos not in visited and pos[0]-1 >= 0 and (ord(inp[pos[0]-1][pos[1]]) - ord(inp[pos[0]][pos[1]])) in (1, 0):
                # only append if distance is less than the current distance
                if not to_visit or to_visit[0].dis > dis+1:
                    print('appending top', next_pos)
                    to_visit.insert(0, pos_dis(next_pos, dis+1))

                
        if pos[0] < len(inp)-1:
            # bottom
            next_pos = (pos[0]+1, pos[1])
            if next_pos not in visited and pos[0]+1 < len(inp) and (ord(inp[pos[0]+1][pos[1]]) - ord(inp[pos[0]][pos[1]])) in (0, 1):
                print('appending bottom', next_pos)
                to_visit.append(pos_dis(next_pos, dis+1))
            
            elif inp[pos[0]][pos[1]] == 'S':
                to_visit.insert(0, pos_dis(next_pos, dis+1))
            
        if pos[1] > 0:
            # left
            next_pos = (pos[0], pos[1]-1)
            if next_pos not in visited and pos[1]-1 >= 0 and (ord(inp[pos[0]][pos[1]-1]) - ord(inp[pos[0]][pos[1]])) in (0,1 ):
                print('appending left', next_pos)
                to_visit.append(pos_dis(next_pos, dis+1))

        if pos[1] < len(inp[0])-1:
            # right
            next_pos = (pos[0], pos[1]+1)
            if next_pos not in visited and pos[1]+1 < len(inp[0]) and (ord(inp[pos[0]][pos[1]+1])-ord(inp[pos[0]][pos[1]])) in (0,1 ):
                print('appending right', next_pos)
                to_visit.append(pos_dis(next_pos, dis+1))
            
            elif inp[pos[0]][pos[1]] == 'S':
                to_visit.insert(0, pos_dis(next_pos, dis+1))
        
        visited.add(pos)

    print(visited)
    return distance+1


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


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
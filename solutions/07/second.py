import pandas as pd
import pytest
import argparse
import os.path
import re

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.splitlines()

    from collections import defaultdict
    size = defaultdict(int)
    current_path = []

    for row in inp:
        if row.startswith('$'):
            cmd = row.split(' ')
            if cmd[1]=='cd':
                # handle cd
                if cmd[2]=='..':
                    # handle backtrack
                    current_path.pop()
                else:
                    dir = cmd[2]
                    current_path.append(dir)

            elif cmd[1]=='ls':
                # handle ls
                pass
        else:
            output = row.split(' ')
            if output[0] == 'dir':
                pass
            else:
                local_size = int(output[0])
                for i in range(len(current_path)+1):
                    # all parent paths
                    parent_path = '/'.join(current_path[:i])
                    size[parent_path]+=local_size
        
    del size['']
    ans = float('inf')
    for k,v in size.items():
        if v>=size['/'] - (70000000-30000000):
            ans = min(ans, v)
    return ans

INPUT_S = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 24933642

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

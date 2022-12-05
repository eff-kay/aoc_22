import pytest
import argparse
import os.path
import re

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(data):
    inp = data.split('\n\n')
    crates, ins = inp
    cr_ind, cr_cols = crates.splitlines()[:-1], crates.splitlines()[-1]

    di_crates = {k:[] for k in map(int, cr_cols.strip().split())}
    split_crates = [cr.split(" ") for cr in cr_ind]

    for sc in split_crates:
        i = 0
        di_ind = 1
        while i<len(sc):
            print(di_ind, i, sc[i], sc)
            if sc[i]=='':
                joined = ''.join(sc[i:i+4])

                if joined=='':
                    i = i+4
                    di_ind+=1
            else:
                di_crates[di_ind].append(sc[i])
                di_ind += 1
                i+=1

    di_crates = {k: list(reversed(v)) for k,v in di_crates.items()}
    print(di_crates)

    for row in ins.splitlines():
        numbers = re.findall("move ([0-9]+) from ([0-9]+) to ([0-9]+)", row)
        nu, src, dest = map(int, numbers[0])

        for i in range(nu):
            print(nu-i, di_crates[src])
            top = di_crates[src].pop()
            di_crates[dest].append(top)

    
    
    res = []

    for k,v in di_crates.items():
        res.append(v.pop())

    return ''.join(re.findall("([A-Z])", ''.join(res)))


INPUT_S = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'CMZ'

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
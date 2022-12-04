import pytest
import argparse
import os.path

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    pairs = 0
    inp = data.splitlines()

    for row in inp:
        fir, sec = row.split(',')

        fir_st = int(fir.split('-')[0])
        fir_end = int(fir.split('-')[1])
        fir = set(range(fir_st, fir_end+1))

        sec_st = int(sec.split('-')[0])
        sec_end = int(sec.split('-')[1])
        sec = set(range(sec_st, sec_end+1))

        if len(fir - sec)==0 or len(sec-fir)==0:
            pairs+=1

    return pairs

INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 2

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
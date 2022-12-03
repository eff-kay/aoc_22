import pytest
import argparse
import os.path

from string import ascii_lowercase, ascii_uppercase

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split("\n")[:-1]
    map_lower = {k:v  for k,v in zip(ascii_lowercase, range(1, 27))}
    map_upper = {k:v  for k,v in zip(ascii_uppercase, range(27, 53))}

    score=0
    for x in inp:
        fi, se = x[:int(len(x)/2)], x[int(len(x)/2):]

        for y in fi:
            if y in se:
                if y in ascii_lowercase:
                    score+=map_lower[y]
                elif y in ascii_uppercase:
                    score+=map_upper[y]
                break

    return score

INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 157

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
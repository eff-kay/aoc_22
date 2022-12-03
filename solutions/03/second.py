import pandas as pd
import pytest
import argparse
import os.path

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
from string import ascii_lowercase, ascii_uppercase

def compute(data):
    inp = data.split("\n")[:-1]
    map_lower = {k:v  for k,v in zip(ascii_lowercase, range(1, 27))}
    map_upper = {k:v  for k,v in zip(ascii_uppercase, range(27, 53))}

    # print(len(first), first[0], first[-1], len(second), second[0], second[-1])

    score = 0
    def exists_in(list_of_lists, list_ind, ch, exists):
        if list_ind == len(list_of_lists):
            return exists

        exists = False
        if ch in list_of_lists[list_ind]:
            exists = True
            return exists and exists_in(list_of_lists, list_ind+1, ch, exists)
        
        return exists

    for x in range(0,len(inp), 3):
        first = inp[x:x+3]
        for ch in first[0]:
            exists = False
            exists = exists_in(first, 1, ch, exists)
            if exists==True:
                if ch in ascii_lowercase:
                    score+=map_lower[ch]
                elif ch in ascii_uppercase:
                    score+=map_upper[ch]
                break

    # print('score', score)
    # for ch in second[0]:
    #     exists = False
    #     exists = exists_in(second, 1, ch, exists)
    #     if exists==True:
    #         if ch in ascii_lowercase:
    #             score+=map_lower[ch]
    #         elif ch in ascii_uppercase:
    #             sore+=map_upper[ch]
    #         break

    return score


INPUT_S = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 122

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

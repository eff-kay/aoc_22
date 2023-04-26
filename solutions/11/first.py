import pytest
import argparse
import os.path
import re


# increase the recursion depth in python
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import namedtuple

def compute(data):
    inp = data.split('\n\n')

    m_contains = {}

    # turns
    for setting in inp:
        ins = setting.splitlines()
        m = int(ins[0].strip().split(' ')[1][0])

        m_structure = {'objects':[], 'operations':[], 'test': -1, 'true_condition':-1, 'false_condition':-1, 'inspected':0}

        st = [int(x) for x in ins[1].strip().split(':')[1].strip().split(', ')]

        m_structure['objects'] = st

        op = ins[2].strip().split(':')[1].strip()

        m_structure['operations'] = re.sub('new = ', '', op).replace('old', 'o')


        test = ins[3].strip().split(':')[1].strip()
        test = int(re.match(r'divisible by (\d+)', test)[1])
        m_structure['test'] = test

        true_condition = int(re.match(r'If true: throw to monkey (\d+)', ins[4].strip())[1])

        m_structure['true_condition'] = true_condition

        false_condition = int(re.match(r'If false: throw to monkey (\d+)', ins[5].strip())[1])

        m_structure['false_condition'] = false_condition

        m_contains[m] = m_structure



    print(m_contains)
    in_progress = True
    round = 1
    from pprint import pprint
    while in_progress:
        for m in m_contains:
            if len(m_contains[m]['objects']) == 0:
                continue

            for _ in range(len(m_contains[m]['objects'])):
                m_contains[m]['inspected']+=1
                o = m_contains[m]['objects'].pop(0)
                print('tyring', m_contains[m]['operations'])
                o = eval(m_contains[m]['operations'])
                print(o)
                # if m_contains[m]['operations'] == 'new = old * 19':
                #     o = o*19
                # elif m_contains[m]['operations'] == 'new = old + 6':
                #     o = o+6
                # elif m_contains[m]['operations'] == 'new = old * old':
                #     o = o*o
                # elif m_contains[m]['operations'] == 'new = old + 3':
                #     o = o+3

                o = o//3
                if o % m_contains[m]['test'] == 0:
                    m_contains[m_contains[m]['true_condition']]['objects'].append(o)
                else:
                    m_contains[m_contains[m]['false_condition']]['objects'].append(o)
            
        round+=1
        if round == 21:
            in_progress = False
            

    pprint(m_contains)
    from functools import reduce
    most_active = sorted([x['inspected'] for x in m_contains.values()], reverse=True)[:2]
    print(most_active)
    total = reduce(lambda x,y: x*y, most_active)
    return total

        

INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 10605


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
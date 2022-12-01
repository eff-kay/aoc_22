import pandas as pd


def first():
    inp = open('1.txt').read().split("\n\n")

    inp = [x.rstrip().split('\n') for x in inp]

    inp  = max([sum(list(map(int, x))) for x in inp])

    print(inp)
    # return gamma*eps

if __name__=="__main__":
    print(first())

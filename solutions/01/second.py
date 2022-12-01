import pandas as pd

def second():
    inp = open('1.txt').read().split("\n\n")
    inp = [x.rstrip().split('\n') for x in inp]
    inp  = sum(sorted([sum(list(map(int, x))) for x in inp], reverse=True)[:3])
    print(inp)

if __name__=="__main__":
    print(second())

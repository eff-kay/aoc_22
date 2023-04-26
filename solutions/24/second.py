import pytest
import argparse
import os.path
import re


# increase the recursion depth in python
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import namedtuple, defaultdict, deque
from dataclasses import dataclass

# differentiate between old and new values, maybe we do need to return a new board

# TODO: more ground in every direction
def compute(data):
    inp = data.splitlines()

    def print_board(board):
        print()
        for row in board:
            print(''.join(row))
        print()
    
    def print_board_dict(board):
        # board = sorted(board.items(), key=lambda x: x[0])
        # print(board)

        print()
        p_str = ''
        min_i =  min([k[0] for k, v in board.items()])
        max_i =  max([k[0] for k, v in board.items()])

        min_j =  min([k[1] for k, v in board.items()])
        max_j =  max([k[1] for k, v in board.items()])

        for x in range(min_i, max_i+1):
            p_str = ''
            for y in range(min_j, max_j+1):
                if len(board[(x,y)])==1:
                    p_str+=board[(x,y)][0]
                else:
                    p_str+= str(len(board[(x,y)]))
            print(''.join(p_str))
        
        print()

    print("START")
    # print_board(inp)


    di_data = {}
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            di_data[(i,j)] = [inp[i][j]]

    dir_map = {'^':(-1, 0), 'v':(1,0), '>':(0,1), '<':(0, -1)}

    print_board_dict(di_data)

    def put_dot(board, loc):
        if len(board[loc])>=1 and board[loc]!='.':
            return board
        elif len(board[loc])==0:
            board[loc] = ['.']
            # print('putting dot in', loc, board[loc])
            return board
    
    def fetch_opposite(curr_loc, dir):
        diff = dir_map[dir]
        op_row, op_col = diff[0], diff[1]

        if op_row == -1:
            op_row= len(inp)-2
            op_col = curr_loc[1]
        elif op_col == -1:
            op_col = len(inp[0])-2
            op_row = curr_loc[0]
        elif op_row == 1:
            op_col = curr_loc[1]
        elif op_col == 1:
            op_row = curr_loc[0]
        
        # print('opposite fetched', op_row, op_col, curr_loc)
        return op_row, op_col
        
    def move_direction(board, loc, dir):
        xi,xj = dir_map[dir]
        i,j = loc

        if di_data[(i+xi, j+xj)][0]=='#':
            I, J = fetch_opposite((i,j), dir)
            if len(board[(I,J)])==1 and board[(I, J)][0] == '.':
                board[(I,J)][0] = dir
            else:
                board[(I, J)].append(dir)
        else:
            if len(board[(i+xi,j+xj)])==1 and board[(i+xi, j+xj)][0] == '.':
                board[(i+xi, j+xj)][0] = dir
            else:
                board[(i+xi, j+xj)].append(dir)

        board = put_dot(board, (i,j))  
        return board
    
    def update_path_e(board, path_e):
        e_loc = path_e[-1]
        i, j = e_loc

        def print_ne(board, loc):
            x,y = loc
            print('fetching ni for ', loc)
            print(board[(x, y+1)], board[(x+1, y)], board[(x-1, y)], board[(x, y-1)])

        # check right
        if len(board[(i,j+1)])>0 and board[(i,j+1)][0]=='.':
            path_e.append((i,j+1))
        # check down
        elif len(board[(i+1,j)])>0 and board[(i+1,j)][0]=='.':
            path_e.append((i+1, j))
        # check up
        elif len(board[(i-1,j)])>0 and board[(i-1,j)][0]=='.':
            path_e.append((i-1, j))
        # check left
        elif len(board[(i,j-1)])>0 and board[(i,j-1)][0]=='.':
            path_e.append((i, j-1))
        else:
            # wait
            path_e.append((i,j))
        
        print_ne(board, (i,j))
        print('move to ', path_e[-1])
        if path_e[-1]==(0,1):
            path_e.pop()
        return path_e

    minute = 1
    path_E = [(0,1)]
    end_i, end_j = len(inp)-1, len(inp[0])-2

    # while True:
    #     print("MINUTE ", minute)
    #     new_board = defaultdict(list)
    #     for loc, v in di_data.items():
    #         i, j = loc
    #         # print(i,j, v)
    #         if len(v)==1 and (v[0]=='#' or v[0]=='.'):
    #             # check the new board
    #             if len(new_board[(i,j)])>0:
    #                 continue
    #             new_board[(i,j)].append(v[0])
    #             continue
                
    #         elif len(v)==1 and v[0]==">":
    #             new_board = move_direction(new_board, (i,j), ">")
    #         elif len(v)==1 and v[0]=='<':
    #             new_board = move_direction(new_board, (i,j), '<')
    #         elif len(v)==1 and v[0]=='^':
    #             new_board = move_direction(new_board, (i,j), '^')
    #         elif len(v)==1 and v[0]=='v':
    #             new_board = move_direction(new_board, (i,j), "v")

    #         elif len(v)>1:
    #             for sym in v:
    #                 new_board = move_direction(new_board, (i,j), sym)
    #     path_E = update_path_e(new_board, path_E)
    #     di_data = {k:v for k,v in new_board.items()}
    #     print(len(inp), len(inp[0]))
    #     if path_E[-1] == (end_i, end_j):
    #         break
    #     minute+=1

    # return minute



    lines = [x for x in data.split('\n')]
    print(lines)
    G = lines
    R = len(G)
    C = len(G[0])
    # print(R, C)

    r = 0
    c = 0

    while G[r][c] =='#':
        c+=1
    
    BAD_CELLS = {}

    for t in range((R-2)*(C-2)*3):
        BAD = set()

        for rr in range(R):
            for cc in range(C):
                if G[rr][cc] == '>':
                    BAD.add((rr, 1+(cc-1+t)%(C-2)))
                
                elif G[rr][cc] == 'v':
                    BAD.add((1+(rr-1+t)%(R-2), cc))

                elif G[rr][cc] == '<':
                    BAD.add((rr, 1+((cc-1-t)%(C-2))))

                elif G[rr][cc] == '^':
                    BAD.add((1+((rr-1-t)%(R-2)),  cc))

        BAD_CELLS[t] = BAD                

    p1 = False
    SEEN = set()
    start = (r, c, 0, False, False)
    Q = deque([start])
    while Q:
        (r, c, t, got_end, got_start ) = Q.popleft()
        if not (0<=r<R and 0<=c<C and G[r][c]!='#'):
            continue
        if r==R-1 and got_end and got_start:
            # print('result', t)
            return t

        if r == R-1:
            print('j1', t)
            got_end = True
        
        if r==0 and got_end:
            print('j2', t)
            got_start = True

        if (r, c, t, got_start, got_end) in SEEN:
            continue

        SEEN.add((r,c ,t, got_start, got_end))
        BAD  = BAD_CELLS[t+1]

        if (r,c ) not in BAD:
            Q.append((r, c, t+1, got_end, got_start))

        if (r+1,c ) not in BAD:
            Q.append((r+1, c, t+1, got_end, got_start))

        if (r-1,c ) not in BAD:
            Q.append((r-1, c, t+1, got_end, got_start))

        if (r,c+1 ) not in BAD:
            Q.append((r, c+1, t+1, got_end, got_start))

        if (r,c-1 ) not in BAD:
            Q.append((r, c-1, t+1, got_end, got_start))

    return 0

INPUT_S = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''
EXPECTED = 54


INPUT_S_1 = '''#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        # ("1,1,1\n2,1,1", 10),

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
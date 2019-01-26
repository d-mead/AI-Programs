BLANK = "??????????.......??.......??.......??.......??.......??.......???????????"
from collections import deque
# from graphics import *
# from PIL import *


def main():
    display(BLANK)
    board = BLANK
    board = drop(board, 0, '@')
    board = drop(board, 1, 'o')
    board = drop(board, 2, '@')
    board = drop(board, 3, '@')
    display(board)
    print(get_valid_cols(board))
    print(check_win(board))


def check_win(board):
    directions = [1, -1, 8, -8, 9, -9, 10, -10]
    spots = [x for x in range(10, 62) if (board[x] != '.' and board[x] != '?')]
    for spot in spots:
        o_spot = spot  # preserve original value
        token = board[spot]  # which type?
        for dir in directions:
            count = 1
            new_spot = o_spot + dir
            while board[new_spot] == token:
                new_spot += dir
                count += 1
            if count == 4:
                return token
    return False


def get_valid_cols(board):
    valids = []
    for col in range(10, 17):
        if board[col] == ".":
            valids.append(col-10)
    return valids


def drop(board, col, token):
    for row in range(7, 0, -1):
        if board[row*9+col+1] == '.':
            board = place(board, row*9+col+1, token)
            break
    return board


def place(board, spot, token):
    new_board = board[:spot] + token + board[spot+1:]
    return new_board


def display(board):
    for row in range(1, 7):
        print(" ".join(board[x] for x in range(row*9+1, row*9+8)) + "\t" + str(list(range(row*9+1, row*9+8))))
    print()

if __name__ == "__main__":
    main()
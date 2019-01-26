BLANK = "??????????.......??.......??.......??.......??.......??.......???????????"

import time
import tkinter as tk
from PIL import ImageTk
import random

def main():
    global master
    blank_window()
    time.sleep(1)
    # display(BLANK)

    random_game()

    master.mainloop()


def random_game():
    board = BLANK
    token = '@'
    swap = {'@':'o', 'o':'@'}

    while not check_win(board):
        valid_columns = get_valid_cols(board)
        if len(valid_columns) == 0:
            break
        col = valid_columns[random.randint(0, len(valid_columns)-1)]
        board = drop(board, col, token)
        token = swap[token]
        display(board)

    statement = {"@": "black wins!", 'o': 'red wins!', '.': 'tie game'}
    print(statement[check_win(board)])

    display_winner(check_win(board))


def display_winner(token):
    statement = {"@": "black wins!", 'o': 'red wins!', '.': 'tie game'}
    colors = {'@': 'black', 'o': 'red', '.': 'grey'}
    w.create_text(350, 50, fill=colors[token], font="Helvetica 40 italic bold", text=statement[token])


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
            animate_drop(board, col+10, row*9+col+1, token)
            board = place(board, row * 9 + col + 1, token)
            break
    return board


def animate_drop(board, start, stop, token):
    global index_to_cord

    colors = {'@': 'black', 'o': 'red'}

    color = colors[token]

    x = index_to_cord[start][0]
    start_y = index_to_cord[start][1]
    end_y = index_to_cord[stop][1]

    for y in range(start_y, end_y, 40):
        wipe_window()
        w.create_circle(x, y, 40, outline='', fill=color)
        display_window(board)
        time.sleep(.008)
    wipe_window()
    display_window(board)


def place(board, spot, token):
    new_board = board[:spot] + token + board[spot+1:]
    return new_board


def display(board):
    for row in range(1, 7):
        print(" ".join(board[x] for x in range(row*9+1, row*9+8)) + "\t" + str(list(range(row*9+1, row*9+8))))
    print()
    display_window(board)


def display_window(board):

    w.create_image(353, 401, image=photoimage)

    colors = {'@': 'black', 'o': 'red'}
    spots = [x for x in range(10, 62) if (board[x] != '.' and board[x] != '?')]
    for spot in spots:
        token = board[spot]
        color = colors[token]
        cord = index_to_cord[spot]
        w.create_circle(cord[0], cord[1], 40, outline='', fill=color)

    master.update_idletasks()
    master.update()


def wipe_window():
    w.delete('all')

    for index in index_to_cord.values():
        w.create_circle(index[0], index[1], 40, outline='', fill='SteelBlue3')


def blank_window():
    global master
    master = tk.Tk()

    global photoimage
    photoimage = ImageTk.PhotoImage(file="yellows.png")

    global w
    w = tk.Canvas(master, width=700, height=700)
    w.pack()

    w.create_image(353, 401, image=photoimage)


    global index_to_cord
    index_to_cord = dict()

    for row_i, row in zip(range(10, 56, 9), range(0, 7)):
        for col_i, col in zip(range(row_i, row_i + 7), range(0, 8)):
            index_to_cord[col_i] = (50 + 100 * col, 150 + 100 * row)

    for index in index_to_cord.values():
        w.create_circle(index[0], index[1], 40, outline='', fill='SteelBlue3')

    master.update_idletasks()
    master.update()


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

tk.Canvas.create_circle = _create_circle


if __name__ == "__main__":
    main()
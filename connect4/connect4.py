import time
import tkinter as tk
from PIL import ImageTk
import random
import sys

BLANK = "??????????.......??.......??.......??.......??.......??.......???????????"

x = 0
y = 0
xo = 0
yo = 0


animate = True


def main():
    global maxing, mining
    opposite = {'@': 'o', 'o': '@'}
    maxing = 'o'#input(':')
    mining = opposite[maxing]
    global master
    if animate:
        blank_window()
        time.sleep(1)
        print('\33[32mINSTRUCTIONS: \033[0m ')
        print('\033[32mclick anywhere along the column to drop a disk when its your turn\033[0m ')
    else:
        print('\33[32mINSTRUCTIONS: \033[0m ')
        print('\33[32mtype the column number you want to drop a disk in when its your turn \033[0m ')

    line = sys.argv[1]

    if line == "RANDOM":
        smart_game_random()
    elif line == "PLAYER":
        smart_game()

    if animate:
        master.mainloop()


def human_move(board, token):
    if animate:
        xo = x
        yo = y

        while xo == x and yo == y:
            w.update()
            time.sleep(.1)

        spot = int(x/100)
    else:
        spot = int(input("choose a column: "))

    new_board = drop_a(board, spot, token)
    return new_board


# PLAYERGAME
def smart_game():
    board = BLANK
    token = '@'
    swap = {'@':'o', 'o':'@'}

    if maxing == 'o':
        display_turn(token)
        display(board)
        board = human_move(board, token)  # input asked/waited for in this method
        token = swap[token]

    while check_win(board) == '.':
        display_turn(token)
        display(board)
        display_turn(token)
        board = smart_move(board, token)
        token = swap[token]
        if check_win(board) != '.':
            break

        display_turn(token)
        display(board)
        display_turn(token)
        board = human_move(board, token)  # input asked/waited for in this method
        token = swap[token]
        if check_win(board) != '.':
            break

    display(board)

    statement = {"@": "black (player) wins!", 'o': 'red (ai) wins!', '.': 'tie game', False: 'uh oh'}
    print(statement[check_win(board)])

    display_winner(check_win(board))

    display(board)


# RANDOMGAME
def smart_game_random():
    board = BLANK
    token = '@'
    swap = {'@':'o', 'o':'@'}

    if maxing == 'o':
        display_turn(token)
        display(board)
        display_turn(token)
        board = random_move(board, token)
        token = swap[token]

    while check_win(board) == '.':
        display_turn(token)
        display(board)
        display_turn(token)
        board = smart_move(board, token)
        token = swap[token]
        if check_win(board) != '.':
            break

        display_turn(token)
        display(board)
        display_turn(token)
        board = random_move(board, token)
        token = swap[token]
        if check_win(board) != '.':
            break

    display(board)

    statement = {"@": "black (random) wins!", 'o': 'red (ai) wins!', '.': 'tie game', False: 'uh oh'}
    print(statement[check_win(board)])

    display_winner(check_win(board))

    display(board)


def smart_move(board, token):

    valid_cols = get_valid_cols(board)

    if len(valid_cols) != 0:
        best_spot, value = maxmin_ab_2(board, token, 6, -9999, 9999)
        print(token, "chosen move:", best_spot)
        new_board = drop_a(board, best_spot, token)
        return new_board
    else:
        return -1


def random_move(board, token):
    display_turn(token)
    valid_cols = get_valid_cols(board)

    if len(valid_cols) != 0:
        spot = valid_cols[random.randint(0, len(valid_cols)-1)]
        print(token, "chosen move:", spot)
        new_board = drop_a(board, spot, token)
        return new_board
    else:
        return -1


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


def maxmin_ab_2(board, player, depth, a, b):
    global cou, maxing, mining
    opponent = {'o':'@', '@': 'o'}[player]
    best = {mining: min, maxing: max}
    if depth == 0:  # if we've reached the desired depth
        return None, score_board(board)  # return the score

    possible_moves = []  # empty list of possible moves

    if player == maxing:
        value = -999999999999
        for spot in get_valid_cols(board):
            mov = drop(board, spot, player)
            next_players_moves = get_valid_cols(mov)
            if check_win(mov) == '.':
                next_player = opponent
            else:
                next_player = '?'
            if next_player == '?':
                if check_win(mov) == maxing:
                    possible_moves.append((spot, 1000000))
                    break
                else:
                    possible_moves.append((spot, -1000000))
            else:
                this_val = maxmin_ab_2(mov, next_player, depth-1, a, b)[1]
                value = max(value, this_val)
                a = max(a, value)
                possible_moves.append((spot, this_val))
                if a >= b:
                    break

    else:
        value = 999999999999
        for spot in get_valid_cols(board):
            mov = drop(board, spot, player)
            if check_win(mov) == '.':
                next_player = opponent
            else:
                next_player = '?'
            if next_player == '?':
                if check_win(mov) == maxing:
                    possible_moves.append((spot, 1000000))
                    break
                else:
                    possible_moves.append((spot, -1000000))
            else:
                this_val = maxmin_ab_2(mov, next_player, depth - 1, a, b)[1]
                value = min(value, this_val)
                b = min(b, value)
                possible_moves.append((spot, this_val))
                if a >= b:
                    break

    if len(possible_moves) > 0:
        return best[player](possible_moves, key=lambda x: x[1])

    else:
        if check_win(board) == maxing:
            return None, 100000
        else:
            return None, -100000


def score_board(board):
    score = 0
    score += max_connected(board, maxing) - max_connected(board, mining) + random.random()
    return score


def max_connected(board, token):
    max_count = 0
    directions = [1, -1, 8, -8, 9, -9, 10, -10]
    spots = [x for x in range(10, 62) if (board[x] == token)]
    for spot in spots:
        o_spot = spot  # preserve original value
        token = board[spot]  # which type?
        for dir in directions:
            count = 1
            new_spot = o_spot + dir
            while board[new_spot] == token:
                new_spot += dir
                count += 1
            if count > max_count:
                max_count = count
    return max_count


def display_winner(token):
    if animate:
        if sys.argv[1] == 'RANDOM':
            statement = {"@": "black (random) wins!", 'o': 'red (ai) wins!', '.': 'tie game'}
        else:
            statement = {"@": "black (player) wins!", 'o': 'red (ai) wins!', '.': 'tie game'}
        colors = {'@': 'black', 'o': 'red', '.': 'grey'}
        w.create_text(350, 50, fill=colors[token], font="Helvetica 40 italic bold", text=statement[token], width=700)


def display_turn(token):
    if animate:
        if sys.argv[1] == 'RANDOM':
            statement = {'@': "black\'s (random\'s) turn...", 'o': 'red\'s (ai) turn...'}
        else:
            statement = {'@': "black\'s (your) turn...", 'o': 'red\'s (ai) turn...'}
        colors = {'@': 'black', 'o': 'red', '.': 'grey'}
        w.create_text(350, 50, fill=colors[token], font="Helvetica 30 bold", text=statement[token], width=900)


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
    return '.'


def get_valid_cols(board):
    valids = []
    for col in range(10, 17):
        if board[col] == ".":
            valids.append(col-10)
    return valids


def drop_a(board, col, token):
    for row in range(7, 0, -1):
        if board[row*9+col+1] == '.':
            if animate:
                animate_drop(board, col+10, row*9+col+1, token)
            board = place(board, row * 9 + col + 1, token)
            break
    return board


def drop(board, col, token):
    for row in range(7, 0, -1):
        if board[row*9+col+1] == '.':
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
        display_turn(token)
        display_window(board)

        time.sleep(.008)
    wipe_window()
    # display_turn(token)
    display_window(board)


def place(board, spot, token):
    new_board = board[:spot] + token + board[spot+1:]
    return new_board


def display(board):
    print("0 1 2 3 4 5 6")
    for row in range(1, 7):
        print(" ".join(board[x] for x in range(row*9+1, row*9+8)))# + "\t" + str(list(range(row*9+1, row*9+8))))
    print()
    print()
    if animate:
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

    # start_window = w.create_window(500, 40, anchor=NW, window=OptionMenu(master, d, *list(range(1, 10))))

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

    # global d

    # d = StringVar(w, value=6)
    #
    # start_window = w.create_window(500, 40, anchor=NW, window=OptionMenu(master, d, *list(range(1, 10))))

    w.bind("<Button-1>", callback)

    master.update_idletasks()
    master.update()


def callback(event):
    global x, y
    # print("clicked at", event.x, event.y)
    x = event.x
    y = event.y


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tk.Canvas.create_circle = _create_circle


if __name__ == "__main__":
    main()
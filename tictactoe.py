import sys
from collections import deque
import os


def main():
    # global comp

    state = sys.argv[1]#
    play(state)


def play(state):
    global human, comp
    if state.count(".") == 9:
        human = input("X or O: ").lower()  # if empty board, ask if they are x or o
        if human == 'x':
            comp = 'o'
            display(state)
            state = human_move(state)
        else:
            comp = 'x'
    else:
        if state.count('o') >= state.count('x'):
            human = 'o'
            comp = 'x'
        else:
            human = 'x'
            comp = 'o'

    print("you are %s's" % human)
    print()

    while end_test(state) == '.':
        display(state)
        moves = comp_move(state)
        state = best_move(moves, state)
        display(state)

        if end_test(state) != '.':
            break

        state = human_move(state)

    print()
    end = end_test(state)
    print(("X Wins" if end == 'x' else "O Wins" if end == 'o' else 'Draw') + "!")


def best_move(d, state):
    global comp
    moves = list(sorted(d.items(), key=lambda kv: kv[1], reverse=True))
    dot = moves[0][0]
    return state[:dot] + comp + state[dot+1:]


def comp_move(state):
    global human, comp

    dots = get_empty(state)
    moves = dict()

    for dot in dots:
        move = state[:dot] + comp + state[dot+1:]
        moves[dot] = minimax(move, comp, False)#evaluate(move, comp, True)##mini(state, human)##

    for dot, eval in moves.items():
        print("%s:\t%s" % (dot, "W" if eval == 1 else "T" if eval == 0 else "L"))
    print()

    return moves


def minimax(state, player, maxing):
    global comp, human
    end = end_test(state)
    if end != ".":
        if end == comp:
            return 1
        elif end == 'd':
            return 0
        else:
            return -1

    dots = get_empty(state)
    boards = boards_from(state, dots, opposite(player))

    if maxing:
        value = -1000
        for move in boards:
            value = max(value, minimax(move, comp, not maxing))
        return value
    else:
        value = 1000
        for move in boards:
            value = min(value, minimax(move, human, not maxing))
        return value


def boards_from(state, dots, player):
    boards = []
    for dot in dots:
        boards.append(fill(state, dot, player))
    return boards


def fill(state, dot, val):
    return state[:dot] + val + state[dot + 1:]


def get_empty(state):
    return [i for i, var in enumerate(state) if var == "."]


def opposite(val):
    if val == 'x':
        return 'o'
    return 'x'


def evaluate(state, val, maxing):
    global human, comp
    value = 0
    end = end_test(state)
    if end != ".":
        if end == comp:
            return 1
        elif end == 'd':
            return 0
        else:  # end == 'o'
            return -1

    best_eval = 0
    best_move = ""

    dots = [i for i, var in enumerate(state) if var == "."]
    for dot in dots:
        move = state[:dot]+val+state[dot+1:]
        eval = evaluate(move, opposite(val), not maxing)
        value += eval
        if maxing:
            if eval < best_eval:
                best_eval = eval
                # best_move = move
        else:
            if eval > best_eval:
                best_eval = eval
                # best_move = move

    return value


def minimax(state, player, maxing):
    global comp
    end = end_test(state)
    if end != ".":
        if end == comp:
            return 1
        elif end == 'd':
            return 0
        else:
            return -1

    dots = get_empty(state)

    if maxing:
        value = -100000
        for dot in dots:
            move = state[:dot] + player + state[dot + 1:]
            value = max(value, minimax(move, opposite(player), not maxing))
        return value
    else:
        value = 100000
        dots = [i for i, var in enumerate(state) if var == "."]
        for dot in dots:
            move = state[:dot] + player + state[dot + 1:]
            value = min(value, minimax(move, opposite(player), not maxing))
        return value


def human_move(state):
    global human, comp
    i = int(input("your turn: "))
    if state[i] != ".":
        print("ERROR")
    else:
        state = state[:i] + human + state[i+1:]

    return state




# def minimax(state, val):
#     global human, comp
#
#     best_move = -1
#     result = 'L'
#
#     dots = [i for i, var in enumerate(state) if var == "."]
#     for dot in dots:
#         move = state[:dot]+val+state[dot+1:]
#         end = end_test(move)
#         if end != '.':
#             if end_test == comp:
#                 best_move = move
#                 return move, 'W'
#             elif end_test == 'd':
#                 best_move = move
#                 result = "T"
#             else:
#                 if best_move == -1:
#                     best_move = move
#             return best_move, result
#         else:
#             if val == 'x':
#                 return minimax(move, 'o')
#             else:
#                 return minimax(move, 'x')


def mini(state, val):
    min_rate = 10000000
    min_dot = -1
    dots = [i for i, var in enumerate(state) if var == "."]
    for dot in dots:
        move = state[:dot]+val+state[dot+1:]
        end = end_test(move)
        rate = 0
        if end != '.':
            if end == val:
                rate = 2
            elif end == 'd':
                rate = 1
            else:
                rate = 0
        else:
            if val == 'x':
                rate += maxi(move, 'o')
            else:
                rate += maxi(move, 'x')

        if rate < min_rate:
            min_rate = rate
            min_dot = dot

    return min_rate


def maxi(state, val):
    max_rate = 0
    max_dot = -1
    dots = [i for i, var in enumerate(state) if var == "."]
    for dot in dots:
        move = state[:dot] + val + state[dot + 1:]
        end = end_test(move)
        rate = 0
        if end != '.':
            if end == val:
                rate = 2
            elif end == 'd':
                rate = 1
            else:
                rate = 0
        else:
            if val == 'x':
                rate += mini(move, 'o')
            else:
                rate += mini(move, 'x')

        if rate > max_rate:
            max_rate = rate
            max_dot = dot

    return max_rate




    # return value


def all_possible(state, val):
    endings = []
    x_wins = set()
    o_wins = set()
    draws = set()
    queue = deque()
    queue.append((state, val))

    while len(queue) > 0:
        temp, va = queue.pop()

        end = end_test(temp)
        if end != ".":
            if end == "x":
                x_wins.add(temp)
            elif end == "o":
                o_wins.add(temp)
            elif end == "d":
                draws.add(temp)
            endings.append(temp)
        else:
            dots = [i for i, var in enumerate(temp) if var == "."]
            for dot in dots:
                move = temp[:dot] + va + temp[dot+1:]
                if va == "x":
                    queue.append((move, 'o'))
                else:
                    queue.append((move, 'x'))

    display(state)
    print()
    print("Endings:\t%s" % len(endings))
    print("X Wins: \t%s" % len(x_wins))
    print("O Wins: \t%s" % len(o_wins))
    print("Draws:  \t%s" % len(draws))


# X Win: x, O Win: o, Full: d, Not Done: .
def end_test(state):
    l = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
         [0, 3, 6], [1, 4, 7], [2, 5, 8],
         [0, 4, 8], [2, 4, 6]]

    for li in l:
        if state[li[0]] == state[li[1]] == state[li[2]]:
            if state[li[0]] == 'x' or state[li[0]] == 'o':
                return state[li[0]]

    if state.count(".") == 0:
        return "d"

    return "."


def display(state):
    for row in range(0, 3):
        print(" ".join(state[row * 3 : (row + 1) * 3]) + "\t" + " ".join([str(row*3), str(row*3+1), str(row*3+2)]))
    print()


if __name__ == "__main__":
    main()
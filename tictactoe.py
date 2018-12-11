import sys
from collections import deque
import os

def main():
    sys.setrecursionlimit(500000)
    global comp

    state = sys.argv[1]#'.........'

    play(state)

# 255,168 total games: 131,184 x wins, 77,904 o wins, 46,080 ties


def play(state):
    global human, comp
    if state.count(".") == 9:
        human = input("X or O: ").lower() # if empty board, ask if they are x or o
        if human == 'x':
            comp = 'o'
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

    if human == 'x':
        display(state)
        state = human_move(state)
        # display(state)

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
    print("computer's turn...")
    print()
    dots = [i for i, var in enumerate(state) if var == "."]
    moves = dict()

    for dot in dots:
        move = state[:dot] + comp + state[dot+1:]
        moves[dot] = evaluate(move, human)

    for dot, eval in moves.items():
        print("%s:\t%s" % (dot, ('W' if eval > 0 else "L" if eval < 0 else "T")))
    print()

    return moves


def human_move(state):
    global human, comp
    i = int(input("your turn: "))
    if state[i] != ".":
        print("ERROR")
    else:
        state = state[:i] + human + state[i+1:]

    return state


def evaluate(state, val):
    global human, comp
    value = 0
    end = end_test(state)
    if end != ".":
        if end == comp:
            return 1
        elif end == 'd':
            return 0
        else: # end == 'o'
            return -1

    dots = [i for i, var in enumerate(state) if var == "."]
    for dot in dots:
        if val == 'x':
            value += evaluate(state[:dot]+val+state[dot+1:], 'o')
        else:
            value += evaluate(state[:dot] + val + state[dot + 1:], 'x')
    return value


def all_possible(state, val):
    endings = []
    x_wins = set()
    o_wins = set()
    draws = set()
    queue = deque()
    queue.append((state, val))
    count = 0

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
            if temp in queue:
                print("A")
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


def rand_place(state, val):
    for i, var in state:
        if var == ".":
            state[i] = val
    return state


def display(state):
    # print(state)
    for row in range(0, 3):
        print(" ".join(state[row * 3 : (row + 1) * 3]))
    print()


if __name__ == "__main__":
    main()
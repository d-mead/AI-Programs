import sys


def main():

    state = sys.argv[1]

    play(state)

    # all_possible(state, 'x')


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
        state = comp_move(state)
        display(state)

        if end_test(state) != '.':
            break

        state = human_move(state)

    end = end_test(state)
    print(("I Win" if end == comp else "You Win" if end == human else 'Draw') + "!")
    print()


def comp_move(state):
    global human, comp

    print("my turn")
    print()

    dots = get_empty(state)
    moves = dict()

    for dot in dots:
        move = state[:dot] + comp + state[dot+1:]
        moves[dot] = minimax(move, comp, False)

    for dot, eval in moves.items():
        print("%s:\t%s" % (dot, "Win" if eval == 1 else "Tie" if eval == 0 else "Loss"))
    print()

    moves = list(sorted(moves.items(), key=lambda kv: kv[1], reverse=True))

    dot = moves[0][0]

    print("i'll choose %s" % dot)
    print()

    return fill(state, dot, comp)#state[:dot] + comp + state[dot+1:]


def human_move(state):
    global human, comp
    print("your turn")
    print("your options are " + ", ".join([str(x) for x in get_empty(state)]))
    i = int(input("your move: "))
    print()
    while i not in get_empty(state):
        print("Not a valid space")
        print("your options are " + ", ".join([str(x) for x in get_empty(state)]))
        i = int(input("your move: "))

    state = state[:i] + human + state[i+1:]

    return state


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


def all_possible(state, val):
    from collections import deque

    endings = []
    x_wins = {5: 0, 7: 0, 9: 0}
    o_wins = {6: 0, 8: 0}
    draws = set()
    visited = set()
    visited.add(state)
    queue = deque()
    queue.append((state, val, 0))

    while len(queue) > 0:
        temp, va, depth = queue.pop()

        end = end_test(temp)
        if end != ".":
            if temp not in visited:
                if end == "x":
                    x_wins[depth] += 1
                elif end == "o":
                    o_wins[depth] += 1
                elif end == "d":
                    draws.add(temp)
            endings.append(temp)
            visited.add(temp)
        else:
            dots = [i for i, var in enumerate(temp) if var == "."]
            for dot in dots:
                move = temp[:dot] + va + temp[dot+1:]
                if va == "x":
                    queue.append((move, 'o', depth+1))
                else:
                    queue.append((move, 'x', depth+1))

    display(state)
    print()
    print("Endings:\t%s" % len(endings))
    print("X Wins: \t%s" % x_wins)
    print("O Wins: \t%s" % o_wins)
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
    print("current board:")
    print()
    for row in range(0, 3):
        print(" ".join(state[row * 3 : (row + 1) * 3]) + "\t" + " ".join([str(row*3), str(row*3+1), str(row*3+2)]))
    print()


if __name__ == "__main__":
    main()
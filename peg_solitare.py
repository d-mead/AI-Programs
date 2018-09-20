import sys
from collections import deque
import time


def main():
    start = "0xxxxxxxxxxxxxx"
    goal = "x00000000000000"
    size = 5

    # state = "xxxxxxxxxx0xxxx"
    # index = 10
    # display(state)
    # print()
    # display(diag_right_up(state, index))
    # print()
    # for child in get_children(state):
    #     display(child)
    #     print()
    path = find_path(start)
    if path != -1:
        for state in path:
            display(state)
            print()
    else:
        print('heck')


def find_path(start):
    fringe = deque()
    visited = {start, }
    starting_path = deque()
    starting_path.append(start)
    fringe.append(Board(start, starting_path))

    while len(fringe) is not 0:
        board = fringe.popleft()
        if goal_check(board.get_state()):
            return board.get_path()
        children = get_children(board.get_state())
        for child in children:
            if child not in visited:
                path = deque(board.get_path())
                path.append(child)
                fringe.append(Board(child, path))
                visited.add(child)
    if len(fringe) == 0:
        return -1


def get_children(state):
    index = 0
    children_set = set()
    for char in state:
        if char == "0":
            if diag_left(state, index) != -1:
                children_set.add(diag_left(state, index))
            if diag_right(state, index) != -1:
                children_set.add(diag_right(state, index))
            if left(state, index) != -1:
                children_set.add(left(state, index))
            if right(state, index) != -1:
                children_set.add(right(state, index))
            if diag_left_up(state, index) != -1:
                children_set.add(diag_left_up(state, index))
            if diag_right_up(state, index) != -1:
                children_set.add(diag_right_up(state, index))
        index += 1
    return children_set


def diag_left(state, index):
    row = get_row(index)
    if row < 4:
        if state[index+row] == "x" and state[index+row+row+1] == "x":
            return swaps(state, index, index+row, index+row+row+1)
    return -1


def diag_right(state, index):
    row = get_row(index)
    if row < 4:
        if state[index+row+1] == "x" and state[index + row + 1 + row + 1 + 1] == "x":
            return swaps(state, index, index+row+1, index + row + 1 + row + 1 + 1)
    return -1


def diag_left_up(state, index):
    row = get_row(index)
    if row > 2:
        if index == 5 or index == 8 or index == 9 or index == 12 or index == 13 or index == 14:
            if state[index - row] == "x" and state[index - row - (row - 1)] == "x":
                return swaps_up(state, index - row - (row - 1), index - row, index)
                # return state[:index - row - (row - 1)] + "0" + state[index - row - (row - 1) + 1: index-row] + "0" + state[index-row+1:index] + "x" + state[index+1:]
    return -1


def diag_right_up(state, index):
    row = get_row(index)
    if row > 2:
        if index == 3 or index == 6 or index == 7 or index == 10 or index == 11 or index == 12:
            if state[index - row + 1] == "x" and state[index - row + 1 - row + 2] == "x":
                return swaps_up(state, index - row + 1 - row + 2, index - row + 1, index)
                # return state[:index - row + 1 - row + 2] + "0" + state[index - row + 1 - row + 2 + 1: index - row + 1] + "0" + state[index - row + 1 + 1:index] + "x" + state[index+1:]
    return -1

def left(state, index):
    row = get_row(index)
    if row > 2:
        if index != 3 and index != 4 and index != 6 and index != 7 and index != 10 and index != 11:
            if state[index-1] == "x" and state[index-2] == "x":
                return state[:index-2] + "00x" + state[index+1:]
    return -1


def right(state, index):
    row = get_row(index)
    if row > 2:
        if index != 4 and index != 5 and index != 8 and index != 9 and index != 13 and index != 14:
            if state[index + 1] == "x" and state[index + 2] == "x":
                return state[:index] + "x00" + state[index + 2 + 1:]
    return -1


def get_row(index):
    if index == 0:
        return 1
    elif index < 3:
        return 2
    elif index < 6:
        return 3
    elif index < 10:
        return 4
    else:
        return 5


def swaps(state, one, two, three):
    return state[:one] + "x" + state[one+1:two] + "0" + state[two+1:three] + "0" + state[three + 1:]


def swaps_up(state, one, two, three):
    return state[:one] + "0" + state[one+1:two] + "x" + state[two+1:three] + "x" + state[three + 1:]


class Board:

    def __init__(self, s, p):
        self.state = s  # state
        self.path = p  # path traveled to that state so far

    def get_path(self):
        # returns the path so far
        return self.path

    def get_state(self):
        # returns the state
        return self.state


def display(state):
    print("    " + state[0])
    print("   " + " ".join(state[1:3]))
    print("  " + " ".join(state[3:6]))
    print(" " + " ".join(state[6:10]))
    print(" ".join(state[10:]))


def goal_check(state):
    if state == "x00000000000000":
        return True
    else:
        return False


if __name__ == "__main__":
    main()
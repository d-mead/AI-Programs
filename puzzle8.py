import sys
import random
from collections import deque


def main():
    global size
    size = 3
    rand = randomsolvable()
    print(rand)
    path = solveFrom(rand)
    print(len(path))
    show_sequence(rand, path)


# 4

def solveFrom(state):
    startState = state
    start = Puzzle(state, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState, }
    paths = []

    while len(fringe) is not 0:
        v = fringe.popleft()
        if v.getState == "012345678":
            print("arrived", len(v.getPath()))
        if goal_test(v.getState()):
            return(v.getPath())
        children = getChildren(v.getState())
        for child in children.keys():
            if child not in visited:
                child_path = children.get(child, 0)
                puz = Puzzle(child, v.getPath()+child_path)
                fringe.append(puz)
                visited.add(child)
    if len(fringe) is 0:
        return("no path exists")


def show_sequence(start, path):
    print_puzzle(start)
    state = start
    for move in path:       # up: 1, right: 2, down: 3, left: 4
        if move == "1":
            state = moveUp(state)
        elif move == "2":
            state = moveRight(state)
        elif move == "3":
            state = moveDown(state)
        else:
            state = moveLeft(state)
        print_puzzle(state)


class Puzzle():

    def __init__(self, s, p):
        self.state = s
        self.path = p

    def addMove(self, move):
        self.path = self.path + move

    def getPath(self):
        return self.path

    def getState(self):
        return self.state


# 2


def getAllWinnable():
    start = "012345678"
    fringe = deque()
    fringe.append(start)
    visited = {start, }

    while len(fringe) is not 0:
        v = fringe.pop()
        for child in getChildren(v):
            if child not in visited:
                fringe.append(child)
                visited.add(child)
    print(len(visited))


def getChildren(state):
    children = {moveUp(state): "1", moveRight(state): "2", moveDown(state): "3", moveLeft(state): "4"}
    return children
# up: 1, right: 2, down: 3, left: 4

# 3

def randomstate():
    return(''.join(random.sample("012345678", 9)))


def randomsolvable():
    state = "012345678"
    for x in range (random.randint(20, 30), 300):
        r = random.randint(1, 4)
        if r is 1:
            state = moveLeft(state)
        elif r is 2:
            state = moveRight(state)
        elif r is 3:
            state = moveUp(state)
        else:
            state = moveDown(state)
    return state


# MARK: MOVE FUNCS


def moveLeft(state):
    i = state.index("0")
    x, y = coord(state)
    if x is not 0:
        newState = state[:i-1] + state[i] + state[i-1] + state[i+1:]
        #display(newState)
        return(newState)
    else:
        return(state)


def moveRight(state):
    i = state.index("0")
    x, y = coord(state)
    if x is not size-1:
        newState = state[:i] + state[i+1] + state[i] + state[i+2:]
        #display(newState)
        return(newState)
    else:
        return(state)


def moveUp(state):
    i = state.index("0")
    x, y = coord(state)
    if y is not 0:
        if(i-size > 0):
            newState = state[:max(0, i-size)] + state[i] + state[max(0, i-size)+1:i] + state[max(0, i-size)] + state[i+1:]
        else:
            newState =  state[i] + state[max(0, i - size) + 1:i] + state[max(0, i - size)] + state[i + 1:]
        #display(newState)
        return(newState)
    else:
        return(state)


def moveDown(state):
    i = state.index("0")
    x, y = coord(state)
    if y is not size-1:
        if(i+size+1<=size*size-1):
            newState = state[:i] + state[i+size] + state[i+1:i+size] + state[i] + state[i+size+1:]
        else:
            newState = state[:i] + state[i + size] + state[i + 1:i + size] + state[i]
        #display(newState)
        return(newState)
    else:
        return(state)


# MARK: REQUIRED FUNCS


def get_children(state):
    return getChildren(state)


def goal_test(state):
    if state == '012345678':
        return True


def print_puzzle(state):
    display(state)


# MARK: MISC FUNCS


def coord(state):
    i = state.index("0")
    x = i % size
    y = int(i/size)
    return (x, y)


def display(state):
    for x in range(0, size):
        print(" ".join(state[x*size:(x+1)*size]))
    print("")


def getStartState():
    print("start state: " + sys.argv[1])
    print("size: " + sys.argv[2])

    return(sys.argv[1], int(sys.argv[2]))


main()
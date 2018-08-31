import sys
from collections import deque
import math

def main():
    global size
    size = 2
    getAllWinnable()
    # start, size = getStartState()
    # display(start)
    # start = moveLeft(start)
    # start = moveRight(start)
    # start = moveUp(start)
    # start = moveDown(start)


def getAllWinnable():
    start = "0123"
    fringe = deque()
    fringe.append(start)
    visited = {start, }

    while not len(fringe) is 0:
        v = fringe.pop()
        for child in getChildren(v):
            if not child in visited:
                fringe.append(child)
                visited.add(child)
    print(len(visited))



def getChildren(state):
    children = {moveLeft(state), moveDown(state), moveRight(state), moveUp(state)}
    return children


#MARK: MOVE FUNCS

def moveLeft(state):
    i = state.index("0")
    if i % size is not 0:
        newState = state[:i-1] + state[i] + state[i-1] + state[i+1:]
        display(newState)
        return(newState)
    else:
        #print("can't move left here")
        return(state)

def moveRight(state):
    #print(state)
    i = state.index("0")
    #print(i)
    #print((i-size+1) % size)
    if (i-size+1) % size is not 0:
        newState = state[:i] + state[i+1] + state[i] + state[i+2:]
        display(newState)
        return(newState)
    else:
        #print("can't move right here")
        return(state)

def moveUp(state):
    i = state.index("0")
    if i > size-1:
        newState = state[:i-size] + state[i] + state[i-size-1:i] + state[i-size] + state[i+1:]
        display(newState)
        return(newState)
    else:
        #print("can't move up here")
        return(state)

def moveDown(state):
    i = state.index("0")
    if i < size*(size-1):
        newState = state[:i] + state[i+size] + state[i+1:i+size] + state[i] + state[i+size+1:]
        display(newState)
        return(newState)
    else:
        #print("can't move down here")
        return(state)


#MARK: REQUIRED FUNCS
def get_children(state):
    print("hello world")

def goal_test(state):
    print("hello world")


def print_puzzle(state):
    display(state)


#MARK: MISC FUNCS

def display(state):
    for x in range(0, size):
        print(" ".join(state[x*size:(x+1)*size]))
    print("")

def getStartState():
    print("start state: " + sys.argv[1])
    print("size: " + sys.argv[2])

    return(sys.argv[1], int(sys.argv[2]))


main()
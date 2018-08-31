import sys
import math

def main():
    start, size = getStartState()
    display(start, size)
    start = moveLeft(start, size)
    start = moveRight(start, size)
    start = moveUp(start, size)
    start = moveDown(start, size)







#MARK: MOVE FUNCS

def moveLeft(state, size):
    i = state.index("0")
    if i % size is not 0:
        newState = state[:i-1] + state[i] + state[i-1] + state[i+1:]
        display(newState, size)
        return(newState)
    else:
        print("can't move left here")
        return(state)

def moveRight(state, size):
    i = state.index("0")
    if i-size % size is not 0:
        newState = state[:i] + state[i+1] + state[i] + state[i+2:]
        display(newState, size)
        return(newState)
    else:
        print("can't move right here")
        return(state)

def moveUp(state, size):
    i = state.index("0")
    if i > size-1:
        newState = state[:i-size] + state[i] + state[i-2:i] + state[i-size] + state[i+1:]
        display(newState, size)
        return(newState)
    else:
        print("can't move up here")
        return(state)

def moveDown(state, size):
    i = state.index("0")
    if i < size*(size-1):
        newState = state[:i] + state[i+size] + state[i+1:i+size] + state[i] + state[i+size+1:]
        display(newState, size)
        return(newState)
    else:
        print("can't move down here")
        return(state)


#MARK: MISC FUNCS

def display(state, size):
    for x in range(0, size):
        print(" ".join(state[x*size:(x+1)*size]))
    print()

def getStartState():
    print("start state: " + sys.argv[1])
    print("size: " + sys.argv[2])

    return(sys.argv[1], int(sys.argv[2]))


main()
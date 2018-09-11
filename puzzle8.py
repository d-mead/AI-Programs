import sys
import random
from collections import deque
import time


def main():
    global size
    size = 3

    # 9

    graph()

    # 7
    # start = time.process_time()
    #
    # rand = randomsolvable()
    # print(rand)
    # path = solve_bfs(rand)
    # if path == -1:
    #     print("no path found")
    # else:
    #     print(len(path))
    #     print(path)
    #     show_sequence(rand, path)
    #
    #
    # end = time.process_time()
    # print("seconds to run: %s" % (end - start))
    #
    #
    # start = time.process_time()
    #
    # print(rand)
    # path = solve_dfs(rand)
    # if path == -1:
    #     print("no path found")
    # else:
    #     print(len(path))
    #     print(path)
    #     show_sequence(rand, path)
    # end = time.process_time()
    # print(len(path))
    # print(path)
    # print("seconds to run: %s" % (end - start))


    # 4 /////////
    # rand = randomsolvable()
    # print(rand)
    # path = solve_bfs(rand)
    # if path == -1:
    #     print("no path found")
    # else:
    #     print(len(path))
    #     show_sequence(rand, path)
    # ///////

    #5
    # fract, avg, long = test_many()
    # print("fraction solvable:   " + str(round(fract, 3)))
    # print("average length:      " + str(avg))
    # print("longest path length: " + str(long))

    #6
    # stat, length, path = get_longest_path()
    # print("hardest state:  " + str(stat))
    # print("moves required: " + str(length))
    # print("solution: ")
    # print("")
    # show_sequence_reverse(stat, path[::-1])

# 9

def graph():
    start = "012345678"
    fringe = deque()
    fringe.append(start)
    next_fringe = deque()
    visited = {start, }
    dict = {}
    done = False
    count = 1

    while not done:
        while len(fringe) is not 0:
            v = fringe.pop()
            for child in getChildren(v):
                if child not in visited:
                    next_fringe.append(child)
                    visited.add(child)
        if len(next_fringe) is 0:
            done = True
        else:
            dict[count] = len(next_fringe)
            count += 1
            while len(next_fringe) is not 0:
                fringe.append(next_fringe.popleft())

    print(dict)

    # visited = {"012345678", }
    # current_visited = set()
    # current_unchecked = deque()
    # next_unchecked = deque()
    # start = "012345678"
    # current_unchecked.append(start)
    # dict = {}
    # for x in range(1, 32):
    #     print(x)
    #     while len(current_unchecked) is not 0:
    #         cur = current_unchecked.popleft()
    #         children = getChildren(cur)
    #         current_visited = current_visited.union(children.keys())
    #         current_visited = current_visited.difference(visited)
    #         for child in children.keys():
    #             next_unchecked.append(child)
    #         dict[x] = set(current_visited)
    #     visited = visited | current_visited
    #     while len(next_unchecked) is not 0:
    #         current_unchecked.append(next_unchecked.popleft())
    #     current_visited.clear()
    #     print(x)
    # print(dict)



# 7

def solve_dfs(state):
    startState = state
    start = Puzzle(state, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState, }

    while len(fringe) is not 0:
        v = fringe.pop()
        visited.add(v.getState())
        if goal_test(v.getState()):
            print("goal hit")
            return v.getPath()
        children = getChildren(v.getState())
        for child in children.keys():
            if child not in visited:
                puz = Puzzle(child, v.getPath()+children.get(child, 0))
                fringe.append(puz)
    if len(fringe) is 0:
        return -1


def hardest_length():
    startState = "012345678"
    start = Puzzle(startState, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState, }
    longest = 0

    while len(fringe) is not 0:
        v = fringe.popleft()
        children = getChildren(v.getState())
        for child in children.keys():
            if child not in visited:
                path = v.getPath() + children.get(child, 0)
                fringe.append(Puzzle(child, path))
                if len(path) > longest:
                    longest = len(path)
                visited.add(child)
    return longest

# 6


def get_longest_path():
    startState = "012345678"
    start = Puzzle(startState, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState, }
    longest = 0
    longest_state = ""
    longest_path = ""

    while len(fringe) is not 0:
        v = fringe.popleft()
        children = getChildren(v.getState())
        for child in children.keys():
            if child not in visited:
                path = v.getPath()+children.get(child, 0)
                fringe.append(Puzzle(child, path))
                if len(path) > longest:
                    longest = len(path)
                    longest_path = path
                    longest_state = v.getState()
                visited.add(child)
    return longest_state, longest, longest_path


def show_sequence_reverse(start, path):
    print_puzzle(start)
    state = start
    for move in path:       # up: 1, right: 2, down: 3, left: 4
        if move == "1":
            state = moveDown(state)
        elif move == "2":
            state = moveLeft(state)
        elif move == "3":
            state = moveUp(state)
        else:
            state = moveRight(state)
        print_puzzle(state)


# 5

def test_many():
    global fraction_solvable, average_length
    total = 50 #random.randint(100, 1000)
    num_solvable = 0
    total_length = 0
    longest_length = 0
    for x in range(1, total+1):
        path = solve_bfs(randomstate())
        if path != -1:
            print("#" + str(x) + " of " + str(total) + ": " + path)
            num_solvable += 1
            total_length += len(path)
            if len(path) > longest_length:
                longest_length = len(path)
        else:
            print("#" + str(x) + " of " + str(total) + ": no path found")
    average_length = int(total_length/total)
    fraction_solvable = num_solvable/total
    return fraction_solvable, average_length, longest_length

# //////


# 4

def solve_bfs(state):
    startState = state
    start = Puzzle(state, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState, }
    paths = []
    max_length = 31

    while len(fringe) is not 0:
        v = fringe.popleft()
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
        return(-1)


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


# 3 //////

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

# //////

# 2 //////


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
    children.pop(state, None)
    return children
# up: 1, right: 2, down: 3, left: 4

# //////

# 1 //////

    # move funcs

def moveLeft(state):
    i = state.index("0")
    if i % size is not 0:
        newState = state[:i-1] + state[i] + state[i-1] + state[i+1:]
        #print_puzzle(newState)
        return(newState)
    else:
        return(state)


def moveRight(state):
    i = state.index("0")
    if i % size is not size-1:
        newState = state[:i] + state[i+1] + state[i] + state[i+2:]
        #print_puzzle(newState)
        return(newState)
    else:
        return(state)


def moveUp(state):
    i = state.index("0")
    if int(i/size) is not 0:
        if(i-size > 0):
            newState = state[:max(0, i-size)] + state[i] + state[max(0, i-size)+1:i] + state[max(0, i-size)] + state[i+1:]
        else:
            newState =  state[i] + state[max(0, i - size) + 1:i] + state[max(0, i - size)] + state[i + 1:]
        #print_puzzle(newState)
        return(newState)
    else:
        return(state)


def moveDown(state):
    i = state.index("0")
    if int(i/size) is not size-1:
        if(i+size+1<=size*size-1):
            newState = state[:i] + state[i+size] + state[i+1:i+size] + state[i] + state[i+size+1:]
        else:
            newState = state[:i] + state[i + size] + state[i + 1:i + size] + state[i]
        #print_puzzle(newState)
        return(newState)
    else:
        return(state)

    # //////


def get_children(state):
    return getChildren(state)


def goal_test(state):
    if state == '012345678':
        return True


def print_puzzle(state):
    for x in range(0, size):
        print(" ".join(state[x*size:(x+1)*size]))
    print("")


# def coord(state):
#     i = state.index("0")
#     x = i % size
#     y = int(i/size)
#     return (x, y)


# def display(state):
#     for x in range(0, size):
#         print(" ".join(state[x*size:(x+1)*size]))
#     print("")


# def getStartState():
#     print("start state: " + sys.argv[1])
#     print("size: " + sys.argv[2])
#
#     return(sys.argv[1], int(sys.argv[2]))

# //////

main()
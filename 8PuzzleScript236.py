import sys
import random
#import xlsxwriter
from collections import deque
import time
import pickle
from heapq import heappush, heappop


def main():
    global size
    global goal

    goal = "012345678"
    size = 3
    #
    # test_many()

    # hundred = make_list(100)
    #
    # with open("100.pkl", "wb") as outfile:
    #     pickle.dump(hundred, outfile)

    with open("1000.pkl", "rb") as infile:
        thousand = pickle.load(infile)

    start = time.process_time()

    fract, avg, long = test_many(thousand)

    end = time.process_time()

    print("fraction solvable:   " + str(round(fract, 3)))
    print("average length:      " + str(avg))
    print("longest path length: " + str(long))

    print("seconds to run: %s" % (end - start))


    # filename = "16puzzle.txt"
    # file = open(filename, "r")
    # lines = file.readlines()
    # file.close()
    # goal = "0ABCDEFGHIJKLMNO"
    # sum_time = 0
    #
    # for line in lines:
    #     sep = line.split(" ")
    #     size = 4
    #     state = sep[0].replace("\n", "")
    #     start = time.process_time()
    #     path = solve_bfs(state)
    #     end = time.process_time()
    #     sum_time = sum_time + (end-start)
    #     if path == -1:
    #         print("No solution %s" % (end - start))
    #     else:
    #         print(str(len(path)) + " " + str((end - start)))





    # state = "025187436"
    #
    # start = time.process_time()
    # print(len(solve_bfs(state)))
    # end = time.process_time()
    # print("time to solve: " + str((end - start)))
    #
    # start = time.process_time()
    # print(len(solve_bfs_original(state)))
    # end = time.process_time()
    # print("time to solve: " + str((end - start)))



    # number 2:
    # getAllWinnable()


    # number 3:
    # print(randomstate())
    # print(randomsolvable())


    # number 7:
    # start = time.clock()
    # rand = randomstate()
    # print(rand)
    # path = solve_bfs(rand)
    # if path == -1:
    #     print("no path found")
    # else:
    #     print(len(path))
    #     print(path)
    #     show_sequence(rand, path)
    # end = time.clock()
    # print("seconds to run: %s" % (end - start))
    #
    # start = time.clock()
    # print(rand)
    # path = solve_dfs(rand)
    # if path == -1:
    #     print("no path found")
    # else:
    #     print(len(path))
    #     print(path)
    #     show_sequence(rand, path)
    # end = time.clock()
    # if path != -1:
    #     print(len(path))
    #     print(path)
    # print("seconds to run: %s" % (end - start))


    # number 9:
    # graph("012345678")


# functions for problem number: 11

# 4

def solve_bfs(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    startState = state
    start = Puzzle(state, "")
    fringe_top = deque()
    fringe_top.append((state, ""), )
    fringe_bottom = deque()
    end = Puzzle(goal, "")
    fringe_bottom.append((goal, ""), )
    visited_top = {startState, }
    visited_bottom = {goal, }
    fringe_t = {state, }

    if parityCheck(state) == 1:   #
        return -1                 # if parity determines its not solveable

    while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
        vt = fringe_top.popleft()                                     # your standard BFS algorithm
        vb = fringe_bottom.popleft()
        if vb[0] in visited_top:
            #for state in fringe_top:
            state = fringe_top[vb[0].index(fringe_t)]
                # if state[0] == vb[0]:
            return state[1] + vb[1]
        if goal_test(vt[0]):
            return vt[1]
        children = getChildren(vt[0])
        for child in children.keys():
            if child not in visited_top:
                fringe_top.append((child, vb[1]+children.get(child, 0)))
                visited_top.add(child)
        children = getChildren(vb[0])
        for child in children.keys():
            if child not in visited_bottom:
                fringe_bottom.append((child, vb[1]+children.get(child, 0)))
                visited_bottom.add(child)
    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return -2


def solve_bfs_zoom(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    fringe_top = deque()
    fringe_top.append((state, 0), )
    fringe_bottom = deque()
    fringe_bottom.append((goal, 0), )
    visited_top = {state, }
    visited_bottom = {goal, }

    if parityCheck(state) == 1:   #
        return -1                 # if parity determines its not solveable

    while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
        vt = fringe_top.pop()                                     # your standard BFS algorithm
        vb = fringe_bottom.pop()
        if vb[0] in visited_top:
            for state in fringe_top:
                if state[0] == vb[0]:
                    return state[1] + vb[1]
        if goal_test(vt[0]):
            return vt[1]
        children = getChildren(vt[0])
        for child in children.keys():
            if child not in visited_top:
                fringe_top.appendleft((child, vb[1]+1))
                visited_top.add(child)
        children = getChildren(vb[0])
        for child in children.keys():
            if child not in visited_bottom:
                fringe_bottom.appendleft((child, vb[1]+1))
                visited_bottom.add(child)
    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return -2

def solve_bfs_zoom_heap(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    start_state = state
    fringe_top = [(taxicab_dist(state, goal), state, 0), ]
    fringe_bottom = [(taxicab_dist(goal, state), goal, 0), ]
    visited_top = {state, }
    visited_bottom = {goal, }
    fringe_t = {state, }

    if parityCheck(state) == 1:   #
        return -1                 # if parity determines its not solveable

    while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm
        vb = heappop(fringe_bottom)
        if vb[1] in visited_top:
            for s in fringe_top:
                if s[1] == vb[1]:
                    return s[2] + vb[2]
        if goal_test(vt[1]):
            return vt[2]
        children = get_children(vt[1])
        for child in children.keys():
            if child not in visited_top:
                if isinstance(goal, tuple):
                    x=5
                heappush(fringe_top, (taxicab_dist(child, goal), child, vb[2]+1))
                visited_top.add(child)
        children = get_children(vb[1])
        for child in children.keys():
            if child not in visited_bottom:
                if isinstance(state, tuple):
                    x=5
                heappush(fringe_bottom, (taxicab_dist(child, state), child, vb[2] + 1))
                # fringe_bottom.appendleft((child, vb[1]+1))
                visited_bottom.add(child)
    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return -2


def taxicab_dist(state, aim):
    summ = 0
    for char in state:
        y_goal = int(aim.index(char) / size)
        x_goal = int(aim.index(char) % size)
        y_cur = int(state.index(char) / size)
        x_cur = int(state.index(char) % size)
        summ += abs(y_goal-y_cur) + abs(x_goal-x_cur)
    return summ


def solve_bfs_original(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    startState = state
    start = Puzzle(state, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState, }

    if parityCheck(state) == 1:   #
        return -1                 # if parity determines its not solveable

    while len(fringe) is not 0:                                  #
        v = fringe.popleft()                                     # your standard BFS algorithm
        if goal_test(v.getState()):                              #
            return v.getPath()                                   #
        children = getChildren(v.getState())                     #
        for child in children.keys():                            #
            if child not in visited:                             #
                child_path = children.get(child, 0)              #
                puz = Puzzle(child, v.getPath()+child_path)      #
                fringe.append(puz)                               #
                visited.add(child)                               #
    if len(fringe) is 0:
        return -1

# 5

def make_list(x):
    list = []
    for i in range(0, x):
        list.append(randomstate())
    return list


def test_many(list):
    # generates 100 to 1000 boards, attempts to solve them, and prints % solvable, avg path length, and longest path
    global fraction_solvable, average_length
    # dict = getAllWinnableDict()            # makes a dictionary of all the states and their paths to goal
    # total = random.randint(100, 1000)      # random number of states from 100 to 1000
    total = len(list)
    num_solvable = 0
    total_length = len(list)
    # print(total)
    longest_length = 0
    x = 0
    for rand in list:
        x += 1
        # rand = randomstate()            # makes a random state
        path = solve_bfs_zoom_heap(rand)
        if path == -1:
            print("#" + str(x) + " of " + str(total) + ": no path found")
        else:
            print("#" + str(x) + " of " + str(total) + ": " + str(path)) # prints update
            num_solvable += 1                  #
            total_length += path         # updates the tracking variables
            if path > longest_length:     #
                longest_length = path     #
    average_length = int(total_length/total)
    fraction_solvable = num_solvable/total
    return fraction_solvable, average_length, longest_length


def parityCheck(state):

    i = state.index("0")
    # state = state.replace("0", "")  # removes the 0 from the state string

    # print(parityCount(state))
    if goal == "012345678" :
        count = parityCount(state)
    else:
        count = abs(parityCount(goal) - parityCount(state))

    if size % 2 == 1:       # if size is odd
        if count % 2 == 1:  # if count is even
            return 1        # its solvable
        else:
            return 0
    else:                         # if size if even
        if (i // size) % 2 == 1:  # if the 0 was in an odd row
            if count % 2 == 0:    # if the count is even
                return 1          # not solvable
            else:
                return 0
        else:                     # if the 0 was in an even row
            if count % 2 == 1:    # if the count is odd
                return 1          # not solvable
            else:
                return 0


def parityCount(state):
    count = 0  # variable to count the number of out of order pairs
    i = state.index("0")
    state = state.replace("0", "")  # removes the 0 from the state string
    for char in state:
        for check in state[state.index(char):]:
            if char > check:
                count = count + 1  # iterates through all characters in the state,
                #  adding to the count varible if the character is out of order
    return count

# 9


def graph(goal_state):
    # takes in a goal and returns the distribution of the path lengths to get to the goal from every winnable state
    start = goal_state
    fringe = deque()           # fringe queue
    fringe.append(start)
    next_fringe = deque()      # fringe for the next layer (allows me to work by layer to separate by path length)
    visited = {start, }
    dict = {}               # [length from goal: number of paths this length]
    done = False
    count = 1               # tracks how far away from the goal we are

    while not done:                                   # while the length of the next fringe isn't 0 (do-while loop)
        while len(fringe) is not 0:                   # while current fringe isn't 0
            v = fringe.pop()                          #
            for child in getChildren(v):              #
                if child not in visited:              #
                    next_fringe.append(child)         # this child will be looked at in the next layer
                    visited.add(child)                #
        if len(next_fringe) is 0:                     # if theres no more nodes for the next layer
            done = True                               # end it
        else:                                         #
            dict[count] = len(next_fringe)            # number of paths this length = number of nodes in next layer
            count += 1                                # adds to the layer number counter
            while len(next_fringe) is not 0:          #
                fringe.append(next_fringe.popleft())  # adds next_fringe nodes to fringe

    print(dict)

    # workbook = xlsxwriter.Workbook('Spreadsheet2.xlsx')  #
    # worksheet = workbook.add_worksheet()                 #
    #                                                      #
    # for r in range(1, 32):                               # this was for when I added to to the excel sheet
    #     worksheet.write(r, 0, dict.get(r-1))             #
    #                                                      #
    # workbook.close()                                     #

# 7


def solve_dfs(state):
    # finds A path to the goal from the start state "state" using a depth first search
    startState = state
    start = Puzzle(state, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState, }

    if parityCheck(state) == 1:  # if we already know there's no solution
        return -1

    while len(fringe) is not 0:                                           # standard DFS algorithm
        v = fringe.pop()                                                  #
        visited.add(v.getState())                                         #
        if goal_test(v.getState()):                                       #
            print(len(v.getPath()))                                       #
            return 5                                                      #
        children = getChildren(v.getState())                              #
        for child in children.keys():                                     #
            if child not in visited:                                      #
                puz = Puzzle(child, v.getPath()+children.get(child, 0))   # puzzle holds a state and path to that state
                fringe.append(puz)                                        #
    if len(fringe) is 0:                                                  #
        return -1                                                         #

# 6


def get_longest_path():
    # returns the state, length, and path of the state furthest from the goal state
    startState = "012345678"
    start = Puzzle(startState, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState, }
    longest = 0
    longest_state = ""
    longest_path = ""

    while len(fringe) is not 0:                            # essentially just a BFS starting at the goal state that
        v = fringe.popleft()                               # goes as deep as it can, recording the state and path when
        children = getChildren(v.getState())               # its previous max is beat
        for child in children.keys():                      #
            if child not in visited:                       #
                path = v.getPath()+children.get(child, 0)  #
                fringe.append(Puzzle(child, path))         #
                if len(path) > longest:                    #
                    longest = len(path)                    #
                    longest_path = path                    #
                    longest_state = v.getState()           #
                visited.add(child)                         #
    return longest_state, longest, longest_path            # state, length, path


def show_sequence_reverse(start, path):
    # prints out the sequence of boards given a flipped path (left move is marked as right move, etc)
    print_puzzle(start)
    state = start
    combo = ""
    for move in path:       # up: 1, right: 2, down: 3, left: 4
        if move == "1":
            state = moveDown(state)
            combo += "D, "
        elif move == "2":
            combo += "L, "
            state = moveLeft(state)
        elif move == "3":
            combo += "U, "
            state = moveUp(state)
        else:
            combo += "R, "
            state = moveRight(state)
        print_puzzle(state)
    print(combo[:len(combo)-2])


def getAllWinnableDict():
    # creates a dictionary of all states and their path to the goal
    startState = "012345678"
    start = Puzzle(startState, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState: 0, }                                             #
                                                                            #
    while len(fringe) is not 0:                                             #
        v = fringe.popleft()                                                # iterates through all nodes in the graph
        children = getChildren(v.getState())                                #
        for child in children.keys():                                       #
            if child not in visited.keys():                                 #
                puz = Puzzle(child, v.getPath() + children.get(child, 0))   #
                fringe.append(puz)                                          #
                visited[child] = len(puz.getPath())                          #
    return visited


def show_sequence(start, path):
    # itterates through the path, makes the moves on the state, and prints the board after each move
    print_puzzle(start)
    state = start
    for move in path:    # up: 1, right: 2, down: 3, left: 4
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
    # class puzzle to make life easier

    def __init__(self, s, p):
        self.state = s  # state
        self.path = p   # path traveled to that state so far

    def addMove(self, move):
        # adds a move to the path so far
        self.path = self.path + move

    def getPath(self):
        # returns the path so far
        return self.path

    def getState(self):
        # returns the state
        return self.state


# 3

def randomstate():
    # generates a random state by shuffling the string "012345678"
    return(''.join(random.sample("012345678", 9)))


def randomsolvable():
    # generates a random but solvable state
    state = randomstate()   # random state
    while (parityCheck(state)) is 1:   # while it's not solvable
        state = randomstate()          # shuffle again
    # for x in range (random.randint(20, 30), 300): # makes at least 20 but at most 300 random moves on the board
    #     r = random.randint(1, 4)                  # essentially shuffling it from the goal state as a human would
    #     if r is 1:                                #
    #         state = moveLeft(state)               #
    #     elif r is 2:                              #
    #         state = moveRight(state)              #
    #     elif r is 3:                              #
    #         state = moveUp(state)                 #
    #     else:                                     #
    #         state = moveDown(state)               #

    # while the continuous shuffling method technically has an infinite O(n), it will on average run faster than the
    # "hand shuffling" method I previously had

    return state

# 2


def getAllWinnable():
    # iterates through the entire graph of solvable states and returns the total number of them
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
    # returns a dictionary of the children from a state, each child's value being the move direction used to get there
    children = {moveUp(state): "1", moveRight(state): "2", moveDown(state): "3", moveLeft(state): "4"}
    # children.pop(state, None)  # removes states that are the same as the original (i.e. if "moved up" from top row)
    return children

# up: 1, right: 2, down: 3, left: 4


# 1

    # move methods

def moveLeft(state):
    # moves space left
    i = state.index("0")
    if i % size is not 0:
        newState = state[:i-1] + state[i] + state[i-1] + state[i+1:]
        #print_puzzle(newState)
        return(newState)
    else:
        return(state)


def moveRight(state):
    # moves space right
    i = state.index("0")
    if i % size is not size-1:
        newState = state[:i] + state[i+1] + state[i] + state[i+2:]
        #print_puzzle(newState)
        return(newState)
    else:
        return(state)


def moveUp(state):
    # moves space up
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
    # moves space down
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
    # realized we needed method get_children after writing getChildren()
    return getChildren(state)


def goal_test(state):
    # if a state is at the goal state
    if state == goal:
        return True


def print_puzzle(state):
    # prints the puzzle in a more user friendly way
    for x in range(0, size):
        print(" ".join(state[x*size:(x+1)*size]))
    print("")

if __name__ == "__main__":
    # main func!
    main()


# code for doing the tasks for each problem


# 11
    # rand = randomstate()
    # print(rand)
    # print(parityCheck(rand))

    # 9

    # graph()

    # 7
    # start = time.clock()
    #
    # rand = randomstate()
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
    # end = time.clock()
    # print("seconds to run: %s" % (end - start))
    #
    #
    # start = time.clock()
    #
    # print(rand)
    # path = solve_dfs(rand)
    # if path == -1:
    #     print("no path found")
    # else:
    #     print(len(path))
    #     print(path)
    #     show_sequence(rand, path)
    # end = time.clock()
    # if path != -1:
    #     print(len(path))
    #     print(path)
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
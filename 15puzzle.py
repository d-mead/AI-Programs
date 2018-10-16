import sys
import random
# import xlsxwriter
from collections import deque
import time
from heapq import heappush, heappop
# heappush(list, item)
# heappop(list)
# import graph_tool
# from graph_tool.all import *
# import pandas as pd
# import numpy as np #######
# import networkx as nx ########
# import matplotlib.pyplot as plt

# sys.path.append('/Users/JackMead/Desktop/CompSci/PycharmProjects/AIPrograms/venv/lib/python3.7/site-packages/graph-tool-2.27/src')
# from graph_tool import *


def main():
    global size
    global goal

    goal = "0ABCDEFGHIJKLMNO"
    size = 4

    action = sys.argv[1]
    state = sys.argv[2]


    if action == "B":
        try:
            start = time.perf_counter()
            path = solve_bfs_original(state)
            end = time.perf_counter()
            print("%s BFS %s" % (len(path), end - start))
        except MemoryError:
            print("BFS Memory Error")
    elif action == "I":
        try:
            start = time.perf_counter()
            path = id_dfs(state, taxicab_dist(state, goal))
            end = time.perf_counter()
            print("%s ID DFS %s" % (len(path), end - start))
        except MemoryError:
            print("ID DFS Memory Error")
    elif action == "2":
        try:
            start = time.perf_counter()
            path = solve_bfs_zoom(state)
            end = time.perf_counter()
            print("%s BI BFS %s" % (path, end - start))
        except MemoryError:
            print("A* Memory Error")
    elif action == "A":
        try:
            start = time.perf_counter()
            path = a_star_taxi(state)
            end = time.perf_counter()
            print("%s A* %s" % (path, end - start))
        except MemoryError:
            print("A* Memory Error")
    elif action == "7":
        try:
            start = time.perf_counter()
            path = a_star_multiplier(state, .7)
            end = time.perf_counter()
            print("%s A* MULTI %s" % (path, end - start))
        except MemoryError:
            print("A* MULTI Memory Error")
        try:
            start = time.perf_counter()
            path = a_star_multiplier(state, .7)
            end = time.perf_counter()
            print("%s A* MULTI %s" % (path, end - start))
        except MemoryError:
            print("A* MULTI Memory Error")
        try:
            start = time.perf_counter()
            path = a_star_multiplier(state, .7)
            end = time.perf_counter()
            print("%s A* MULTI %s" % (path, end - start))
        except MemoryError:
            print("A* MULTI Memory Error")
    elif action == "!":
        try:
            start = time.perf_counter()
            path = solve_bfs_original(state)
            end = time.perf_counter()
            print("%s BFS %s" % (len(path), end - start))
        except MemoryError:
            print("BFS Memory Error")

        try:
            start = time.perf_counter()
            path = id_dfs(state, taxicab_dist(state, goal))
            end = time.perf_counter()
            print("%s ID DFS %s" % (len(path), end - start))
        except MemoryError:
            print("ID DFS Memory Error")

        try:
            start = time.perf_counter()
            path = solve_bfs_zoom(state)
            end = time.perf_counter()
            print("%s BI BFS %s" % (path, end - start))
        except MemoryError:
            print("A* Memory Error")

        try:
            start = time.perf_counter()
            path = a_star_taxi(state)
            end = time.perf_counter()
            print("%s A* %s" % (path, end - start))
        except MemoryError:
            print("A* Memory Error")

        try:
            start = time.perf_counter()
            path = a_star_multiplier(state, .7)
            end = time.perf_counter()
            print("%s A* MULTI %s" % (path, end - start))
        except MemoryError:
            print("A* MULTI Memory Error")
        try:
            start = time.perf_counter()
            path = a_star_multiplier(state, .7)
            end = time.perf_counter()
            print("%s A* MULTI %s" % (path, end - start))
        except MemoryError:
            print("A* MULTI Memory Error")
        try:
            start = time.perf_counter()
            path = a_star_multiplier(state, .7)
            end = time.perf_counter()
            print("%s A* MULTI %s" % (path, end - start))
        except MemoryError:
            print("A* MULTI Memory Error")


# original basic a star search
def a_star(state):
    fringe_top = [(taxicab_dist(state, goal)+0, state, 0)]
    visited_top = set()

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if vt[1] not in visited_top:
            visited_top.add(vt[1])
        else:
            continue

        if goal_test(vt[1]):
            return vt[2]

        children = get_children(vt[1])
        for child in children.keys():
            if child not in visited_top:
                heappush(fringe_top, ((vt[2]+1+taxicab_dist(child, goal)), child, vt[2]+1))
        # visited_top.add(vt[1])

    if len(fringe_top) is 0:
        return -2


# a_star using the special more efficient taxi cab distance calculator
def a_star_taxi(state):
    fringe_top = [(taxicab_dist(state, goal)+0, state, 0, taxicab_dist(state, goal))]
    visited_top = set()

    # if parity_check(state) == 1:
    #     return -1

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if vt[1] not in visited_top:
            visited_top.add(vt[1])
        else:
            continue

        if goal_test(vt[1]):
            return vt[2]

        children = get_children_taxi(vt[1])
        for child in children.keys():
            if child not in visited_top:
                # a = (vt[2]+1+taxicab_dist(child, goal))
                # b = (1+vt[0]+children.get(child))
                taxi = vt[3] + children.get(child)
                heappush(fringe_top, ((vt[2]+1+taxi), child, vt[2]+1, taxi))
        # visited_top.add(vt[1])

    if len(fringe_top) is 0:
        return -2


# a star using a random value as the second thing in the tuple
def a_star_random(state):
    fringe_top = [(taxicab_dist(state, goal) + 0, random.randint(1, 1000), state, 0, taxicab_dist(state, goal)), ]
    visited_top = set()

    # if parity_check(state) == 1:
    #     return -1

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if vt[2] not in visited_top:
            visited_top.add(vt[2])
        else:
            continue

        if goal_test(vt[2]):
            return vt[3]
        children = get_children_taxi(vt[2])
        for child in children.keys():
            if child not in visited_top:
                taxi = vt[4] + children.get(child)
                heappush(fringe_top, ((vt[3]+1+taxi), random.randint(1, 1000), child, vt[3] + 1, taxi))
        visited_top.add(vt[2])

    if len(fringe_top) is 0:
        return -2


# a star using taxi cab distance, random second value, and a multiplier value on the depth
def a_star_multiplier(state, multiplier):
    fringe_top = [(taxicab_dist(state, goal) + 0, random.randint(1, 1000), state, 0, taxicab_dist(state, goal)), ]
    visited_top = set()

    # if parity_check(state) == 1:
    #     return -1

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if vt[2] not in visited_top:
            visited_top.add(vt[2])
        else:
            continue

        if goal_test(vt[2]):
            return vt[3]
        children = get_children_taxi(vt[2])
        for child in children.keys():
            if child not in visited_top:
                taxi = vt[4] + children.get(child)
                heappush(fringe_top, ((multiplier * (vt[3] + 1) + taxi), random.randint(1, 1000), child, vt[3] + 1, taxi))
        visited_top.add(vt[2])

    if len(fringe_top) is 0:
        return -2


# a star search used to keep track of nodes per second
def a_star_nps(state):
    fringe_top = [(taxicab_dist(state, goal) + 0, state, 0, taxicab_dist(state, goal))]
    visited_top = set()

    # if parity_check(state) == 1:
    #     return -1

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if vt[1] not in visited_top:
            visited_top.add(vt[1])
        else:
            continue

        if goal_test(vt[1]):
            return (vt[2], len(visited_top))

        children = get_children_taxi(vt[1])
        for child in children.keys():
            if child not in visited_top:
                # a = (vt[2]+1+taxicab_dist(child, goal))
                # b = (1+vt[0]+children.get(child))
                taxi = vt[3] + children.get(child)
                heappush(fringe_top, ((vt[2] + 1 + taxi), child, vt[2] + 1, taxi))
        # visited_top.add(vt[1])

    if len(fringe_top) is 0:
        return -2


# standard ID DFS
def id_dfs(start, max):
    for k in range(taxicab_dist(start, goal), max+3):
        sol = solve_kdfs(start, k)
        if sol is not None:
            return sol
    return None


# standard KDFS
def solve_kdfs(start, k):
    fringe = deque()
    fringe.append((start, 0, {start, }, ""))
    while len(fringe) is not 0:
        v = fringe.pop()
        if goal_test(v[0]):
            return v[3]
        if v[1] <= k:
            children = get_children(v[0])
            for child in children:
                if child not in v[2]:
                    a = set(v[2])
                    a.add(child)
                    fringe.append((child, v[1] + 1, a, v[3] + children.get(child)))
    return None


# ID DFS used for keeping track of nodes per second
def id_dfs_nps(start, max):
    for k in range(taxicab_dist(start, goal), max+3):
        sol, nodes = solve_kdfs_nps(start, k)
        if sol is not None:
            return sol, nodes
    return None


# KDFS used for keeping track of nodes per second
def solve_kdfs_nps(start, k):
    fringe = deque()
    fringe.append((start, 0, {start, }, ""))
    nodes = 0
    while len(fringe) is not 0:
        v = fringe.pop()
        if goal_test(v[0]):
            return v[3], nodes
        if v[1] <= k:
            children = get_children(v[0])
            for child in children:
                if child not in v[2]:
                    a = set(v[2])
                    a.add(child)
                    fringe.append((child, v[1] + 1, a, v[3] + children.get(child)))
                    nodes += 1
    return None, None


# regular BFS search
def solve_bfs_original(state):
    startState = state
    start = (state, "")
    fringe = deque()
    fringe.append(start)
    visited = {state, }

    if parity_check(state) == 1:   #
        return -1                 # if parity determines its not solveable

    while len(fringe) is not 0:
        v = fringe.popleft()
        if goal_test(v[0]):
            return str(v[1])
        children = get_children(v[0])
        for child in children.keys():
            if child not in visited:
                fringe.append((child, v[1]+children.get(child, 0)))
                visited.add(child)
    if len(fringe) is 0:
        return -1


# regular BFS search for tracking nodes per second
def solve_bfs_original_nps(state):
    startState = state
    start = (state, "")
    fringe = deque()
    fringe.append(start)
    visited = {state, }

    while len(fringe) is not 0:
        v = fringe.popleft()
        if goal_test(v[0]):
            return str(v[1]), len(visited)
        children = get_children(v[0])
        for child in children.keys():
            if child not in visited:
                fringe.append((child, v[1] + children.get(child, 0)))
                visited.add(child)
    if len(fringe) is 0:
        return -1


# standard bidirectional BFS
def solve_bfs_zoom(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    start_state = state
    fringe_top = deque()
    fringe_top.append((state, 0), )
    fringe_bottom = deque()
    fringe_bottom.append((goal, 0), )
    visited_top = {state, }
    visited_bottom = {goal, }
    fringe_t = {state, }

    if parity_check(state) == 1:   #
        return -1                 # if parity determines its not solveable

    while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
        vt = fringe_top.pop()  # your standard BFS algorithm
        vb = fringe_bottom.pop()
        if vb[0] in visited_top:
            for state in fringe_top:
                if state[0] == vb[0]:
                    return state[1] + vb[1]
        if vt[0] in visited_bottom:
            for state in fringe_bottom:
                if state[0] == vt[0]:
                    return state[1] + vt[1]
        if goal_test(vt[0]):
            return vt[1]
        if vb[0] == state:
            return vb[1]
        children = get_children(vt[0])
        for child in children.keys():
            if child not in visited_top:
                fringe_top.appendleft((child, vt[1]+1))
                visited_top.add(child)
        children = get_children(vb[0])
        for child in children.keys():
            if child not in visited_bottom:
                fringe_bottom.appendleft((child, vb[1]+1))
                visited_bottom.add(child)
    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return -2


# bidirectional BFS for tracking nodes per second
def solve_bfs_zoom_nps(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    start_state = state
    fringe_top = deque()
    fringe_top.append((state, 0), )
    fringe_bottom = deque()
    fringe_bottom.append((goal, 0), )
    visited_top = {state, }
    visited_bottom = {goal, }
    fringe_t = {state, }

    if parity_check(state) == 1:  #
        return -1  # if parity determines its not solveable

    while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
        vt = fringe_top.pop()  # your standard BFS algorithm
        vb = fringe_bottom.pop()
        if vb[0] in visited_top:
            for state in fringe_top:
                if state[0] == vb[0]:
                    return state[1] + vb[1], len(visited_top) + len(visited_bottom)
        if goal_test(vt[0]):
            return vt[1], len(visited_top) + len(visited_bottom)
        children = get_children(vt[0])
        for child in children.keys():
            if child not in visited_top:
                fringe_top.appendleft((child, vb[1] + 1))
                visited_top.add(child)
        children = get_children(vb[0])
        for child in children.keys():
            if child not in visited_bottom:
                fringe_bottom.appendleft((child, vb[1] + 1))
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

    if parity_check(state) == 1:   #
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
                heappush(fringe_top, (taxicab_dist(child, goal), child, vt[2]+1))
                visited_top.add(child)
        children = get_children(vb[1])
        for child in children.keys():
            if child not in visited_bottom:
                heappush(fringe_bottom, (taxicab_dist(child, state), child, vb[2] + 1))
                # fringe_bottom.appendleft((child, vb[1]+1))
                visited_bottom.add(child)
    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return -2


def parity_check(state):
    i = state.index("0")
    # state = state.replace("0", "")  # removes the 0 from the state string

    # print(parityCount(state))
    if goal == "012345678":
        count = parity_count(state)
    else:
        count = abs(parity_count(goal) - parity_count(state))

    if size % 2 == 1:  # if size is odd
        if count % 2 == 1:  # if count is even
            return 1  # its solvable
        else:
            return 0
    else:  # if size if even
        if (i // size) % 2 == 1:  # if the 0 was in an odd row
            if count % 2 == 0:  # if the count is even
                return 1  # not solvable
            else:
                return 0
        else:  # if the 0 was in an even row
            if count % 2 == 1:  # if the count is odd
                return 1  # not solvable
            else:
                return 0


def parity_count(state):
    count = 0  # variable to count the number of out of order pairs
    i = state.index("0")
    state = state.replace("0", "")  # removes the 0 from the state string
    for char in state:
        for check in state[state.index(char):]:
            if char > check:
                count = count + 1  # iterates through all characters in the state,
                #  adding to the count varible if the character is out of order
    return count


def taxicab_dist(state, aim):
    summ = 0
    for char in state:
        if char is not "0":
            ai = aim.index(char)
            ci = state.index(char)
            y_goal = int(ai / size)
            x_goal = int(ai % size)
            y_cur = int(ci / size)
            x_cur = int(ci % size)
            summ += abs(y_goal-y_cur) + abs(x_goal-x_cur)
    return summ


def random_state():
    # generates a random state by shuffling the string "012345678"
    return ''.join(random.sample("012345678", 9))


def random_solvable():
    # generates a random but solvable state
    state = random_state()   # random state
    while (parity_check(state)) is 1:   # while it's not solvable
        state = random_state()          # shuffle again
    return state


def get_children(state):
    # returns a dictionary of the children from a state, each child's value being the move direction used to get there
    # children = {up(state): "1", right(state): "2", down(state): "3", left(state): "4"}
    children = {up(state): "1", right(state): "2", down(state): "3", left(state): "4"}
    # children.pop(state, None)  # removes states that are the same as the original (i.e. if "moved up" from top row)
    return children


def get_children_taxi(state):

    children = dict()
    o = state.index("0")

    left_state = left(state)
    left_taxi = 0
    if left_state != state:
        left_taxi = taxi_char(state[o - 1], left_state, goal)-taxi_char(state[o - 1], state, goal)
    children[left_state] = left_taxi

    right_state = right(state)
    right_taxi = 0
    if right_state != state:
        right_taxi = taxi_char(state[o + 1], right_state, goal) - taxi_char(state[o + 1], state, goal)
    children[right_state] = right_taxi

    up_state = up(state)
    up_taxi = 0
    if up_state != state:
        up_taxi = taxi_char(state[o - size], up_state, goal) - taxi_char(state[o - size], state, goal)
    children[up_state] = up_taxi

    down_state = down(state)
    down_taxi = 0
    if down_state != state:
        down_taxi = taxi_char(state[o + size], down_state, goal) - taxi_char(state[o + size], state, goal)
    children[down_state] = down_taxi

    return children

# up: 1, right: 2, down: 3, left: 4


def taxi_char(char, state, aim):
    summ = 0
    if char is not "0":
        ai = aim.index(char)
        ci = state.index(char)
        y_goal = int(ai / size)
        x_goal = int(ai % size)
        y_cur = int(ci / size)
        x_cur = int(ci % size)
        summ += abs(y_goal - y_cur) + abs(x_goal - x_cur)
    return summ


def left(state):
    # moves space left
    i = state.index("0")
    if i % size is not 0:
        newState = state[:i-1] + state[i] + state[i-1] + state[i+1:]
        #print_puzzle(newState)
        return(newState)
    else:
        return(state)


def right(state):
    # moves space right
    i = state.index("0")
    if i % size is not size-1:
        newState = state[:i] + state[i+1] + state[i] + state[i+2:]
        # print_puzzle(newState)
        return(newState)
    else:
        return(state)


def up(state):
    # moves space up
    i = state.index("0")
    if int(i/size) is not 0:
        if(i-size > 0):
            newState = state[:max(0, i-size)] + state[i] + state[max(0, i-size)+1:i] + state[max(0, i-size)] + state[i+1:]
        else:
            newState =  state[i] + state[max(0, i - size) + 1:i] + state[max(0, i - size)] + state[i + 1:]
        # print_puzzle(newState)
        return(newState)
    else:
        return(state)


def down(state):
    # moves space down
    i = state.index("0")
    if int(i/size) is not size-1:
        if(i+size+1<=size*size-1):
            newState = state[:i] + state[i+size] + state[i+1:i+size] + state[i] + state[i+size+1:]
        else:
            newState = state[:i] + state[i + size] + state[i + 1:i + size] + state[i]
        # print_puzzle(newState)
        return(newState)
    else:
        return(state)


def goal_test(state):
    # if a state is at the goal state
    if state == goal:
        return True


def print_puzzle(state):
    # prints the puzzle in a more user friendly way
    for x in range(0, size):
        print(" ".join(state[x*size:(x+1)*size]))
    print("")


# method I messed with to get the estimate on the korf100
def korf(m):
    filename = "korf100.txt"
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    global goal
    goal = "0ABCDEFGHIJKLMNO"
    sum_time = 0
    count = 0
    global size
    size = 4


    workbook = xlsxwriter.Workbook('Multiplier3.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(count, 0, "depth")
    worksheet.write(count, 1, "2.5")
    worksheet.write(count, 2, "3")
    worksheet.write(count, 3, "4")
    worksheet.write(count, 4, "5")
    worksheet.write(count, 5, "6")

    for line in lines[:10]:
        sep = line.split(" ")
        size = 4
        state = sep[0].replace("\n", "")

        print("%s: (%s)" % (state, count))

        worksheet.write(count+1, 0, count)

        for x in range(1, 11):
            try:
                # start = time.process_time()
                start = time.clock()
                path = a_star_multiplier(state, m)  ###
                # end = time.process_time()
                end = time.clock()
                sum_time = sum_time + (end - start)
                worksheet.write(count+1, x, path)  ###
                print("\tA-STAR %s\t%s \t%s" % (x, path, round(end - start, 5)))
            except MemoryError:
                print("\tA Star")

        count += 1

    print("Total Time: %s" % round(sum_time, 5))
    workbook.close()


# method I used to put the A Start multiplier results in an excel sheet
def multiplier_excel_1():
    workbook = xlsxwriter.Workbook('Multiplier3.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(count, 0, "depth")
    worksheet.write(count, 1, "2")
    worksheet.write(count, 1, "4")
    worksheet.write(count, 1, "8")
    worksheet.write(count, 1, "16")
    worksheet.write(count, 1, "32")
    worksheet.write(count, 1, "64")
    worksheet.write(count, 1, "128")

    for line in lines:
        sep = line.split(" ")
        size = 4
        state = sep[0].replace("\n", "")

        print("%s: (%s)" % (state, count))

        worksheet.write(count, 0, count)

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_multiplier(state, 2)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count, 1, path)  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_multiplier(state, 4)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count, 2, path)  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_multiplier(state, 8)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count, 3, path)  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_multiplier(state, 16)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count, 4, path)  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_multiplier(state, 32)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count, 5, path)  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_multiplier(state, 64)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count, 6, path)  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_multiplier(state, 128)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count, 7, path)  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        count += 1

    print("Total Time: %s" % round(sum_time, 5))
    workbook.close()


def req_1():
    filename = "16puzzle.txt"
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    goal = "0ABCDEFGHIJKLMNO"
    sum_time = 0
    count = 35
    size = 4

    workbook = xlsxwriter.Workbook('Random2.xlsx')
    worksheet = workbook.add_worksheet()

    for line in lines[35:41]:

        sep = line.split(" ")
        size = 4
        state = sep[0].replace("\n", "")

        print("%s: (%s)" % (state, count))

        worksheet.write(count-35, 0, count)

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_random(state)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count-35, 1, round(end - start, 5))  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_random(state)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count-35, 2, round(end - start, 5))  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        try:
            # start = time.process_time()
            start = time.clock()
            path = a_star_random(state)  ###
            # end = time.process_time()
            end = time.clock()
            sum_time = sum_time + (end - start)
            worksheet.write(count-35, 3, round(end - start, 5))  ###
            print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        count += 1

    print("Total Time: %s" % round(sum_time, 5))
    workbook.close()

# method for the nps exploration
def nps():
    state = "DACGEIFBHK0OLJMN"

    filename = "16puzzle.txt"
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    goal = "0ABCDEFGHIJKLMNO"
    sum_time = 0
    count = 0
    size = 4

    bfs = "AFICDB0GEHJOLMKN"
    iddfs = "ABKCHDG0IFEJLMNO"
    astar = "KDEB0AJFLIGNMHCO"
    bibfs = "FIEBDA0CONKGHLMJ"

    # start = time.process_time()
    start = time.clock()
    path, nodes = solve_bfs_original_nps(bfs)
    # end = time.process_time()
    end = time.clock()
    print("\tBFS \t%s \t%s \t%s" % (len(path), round(end - start, 5), nodes / round(end - start, 5)))

    # start = time.process_time()
    start = time.clock()
    path, nodes = id_dfs_nps(iddfs, 20)
    # end = time.process_time()
    end = time.clock()
    print("\tID DFS \t%s \t%s \t%s" % (len(path), round(end - start, 5), nodes / round(end - start, 5)))

    # start = time.process_time()
    start = time.clock()
    path, nodes = a_star_nps(astar)
    # end = time.process_time()
    end = time.clock()
    print("\tA-STAR \t%s \t%s \t%s" % (path, round(end - start, 5), nodes/round(end - start, 5)))

    # start = time.process_time()
    start = time.clock()
    path, nodes = solve_bfs_zoom_nps(bibfs)
    # end = time.process_time()
    end = time.clock()
    print("\tBI BFS \t%s \t%s \t%s" % (path, round(end - start, 5), nodes / round(end - start, 5)))


# visualiszes one of the searches
def visualize():
    g = Graph(directed = False)
    a_star_visialize(g)
    g.graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=10, output_size = (500, 500), output = "graph1.png")


def a_star_visualize(state):
    fringe_top = [(taxicab_dist(state, goal) + 0, state, 0, taxicab_dist(state, goal), [])]
    visited_top = set()

    g = nx.Graph()

    # if parity_check(state) == 1:
    #     return -1

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if vt[1] not in visited_top:
            visited_top.add(vt[1])
        else:
            continue

        if goal_test(vt[1]):
            return g, vt[4]

        children = get_children_taxi(vt[1])
        for child in children.keys():
            if child not in visited_top:
                # a = (vt[2]+1+taxicab_dist(child, goal))
                # b = (1+vt[0]+children.get(child))
                taxi = vt[3] + children.get(child)
                ancestors = list(vt[4])
                ancestors.append(vt[1])
                heappush(fringe_top, ((vt[2] + 1 + taxi), child, vt[2] + 1, taxi, ancestors))
                g.add_edge(child, vt[1])


def bi_bfs_visualize(state):
    fringe_top = deque()
    fringe_top.append((state, 0, [state, ]), )
    fringe_bottom = deque()
    fringe_bottom.append((goal, 0, [goal, ]), )
    visited_top = {state, }
    visited_bottom = {goal, }

    g = nx.Graph()

    while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
        vt = fringe_top.pop()  # your standard BFS algorithm
        vb = fringe_bottom.pop()

        if vb[0] in visited_top:
            for state in fringe_top:
                if state[0] == vb[0]:
                    g.add_edge(vb[2][0], state[2][len(state[2])-1])
                    return g, (state[2] + vb[2])

        if vt[0] in visited_bottom:
            for state in fringe_bottom:
                if state[0] == vt[0]:
                    g.add_edge(vt[2][0], state[2][len(state[2])-1])
                    return g, (vt[2] + state[2])

        if goal_test(vt[0]):
            return g, vt[2]

        if vb[0] == state:
            return g, vb[2]

        children = get_children(vt[0])
        for child in children.keys():
            if child not in visited_top:
                ancestors = list(vt[2])
                ancestors.append(vt[0])
                fringe_top.appendleft((child, vt[1]+1, ancestors))
                visited_top.add(child)
                g.add_edge(child, vt[0])

        children = get_children(vb[0])
        for child in children.keys():
            if child not in visited_bottom:
                ancestors = list(vb[2])
                ancestors.insert(0, vb[0])
                fringe_bottom.appendleft((child, vb[1]+1, ancestors))
                visited_bottom.add(child)
                g.add_edge(vb[0], child)


def solve_kdfs_visualize(start, k):
    g = nx.Graph()
    fringe = deque()
    fringe.append((start, 0, [start, ], ""))
    while len(fringe) is not 0:
        v = fringe.pop()
        if goal_test(v[0]):
            return v[3], v[2], g
        if v[1] <= k:
            children = get_children(v[0])
            for child in children:
                if child not in v[2]:
                    a = list(v[2])
                    a.append(child)
                    g.add_edge(v[0], child)
                    fringe.append((child, v[1] + 1, a, v[3] + children.get(child)))
    return None, None, None


def id_dfs_visualize(start, max):
    for k in range(taxicab_dist(start, goal), max+3):
        sol, l, g = solve_kdfs_visualize(start, k)
        if sol is not None:
            return g, l
    return None


def bfs_visualize(state):
    g = nx.Graph()
    start = (state, "", [state])
    fringe = deque()
    fringe.append(start)
    visited = {state, }

    while len(fringe) is not 0:
        v = fringe.popleft()
        if goal_test(v[0]):
            return g, v[2]
        children = get_children(v[0])
        for child in children.keys():
            if child not in visited:
                a = list(v[2])
                a.append(child)
                fringe.append((child, v[1] + children.get(child, 0), a))
                visited.add(child)
                g.add_edge(v[0], child)

    if len(fringe) is 0:
        return -1, -1


def visualize2():
    filename = "16puzzle.txt"
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    length = 7

    state = lines[length+1].split(" ")[0].replace("\n", "")

    plt.figure().suptitle("Search Algorithm Graphs for Path Length " + str(length))

    g, l = a_star_visualize(state)
    draw_graph(g, l, 221, state, "A-Star")

    plt.legend(('state', 'move'), loc='best', prop={'size': 6})

    g, l = bi_bfs_visualize(state)
    draw_graph(g, l, 222, state, "Bi-BFS")

    g, l = id_dfs_visualize(state, 12)
    draw_graph(g, l, 223, state, "ID-DFS")

    g, l = bfs_visualize(state)
    draw_graph(g, l, 224, state, "BFS")

    plt.show()


def draw_graph(g, l, subplot, state, title):
    edge_l = []
    color_list = [".6"] * len(g.edges())
    l.append(goal)
    prev = l[0]
    for node in l:
        edge_l.append((prev, node))
        if (prev, node) in list(g.edges()):
            index = list(g.edges()).index((prev, node))
            color_list[index] = "red"
        elif (node, prev) in list(g.edges()):
            index = list(g.edges()).index((node, prev))
            color_list[index] = 'red'
        prev = node

    plt.subplot(subplot)

    plt.title(title, loc='center', size = 'medium')

    nx.draw(g, with_labels=True, labels={state: "start", goal: "finish"}, font_size=7, node_color='darkblue',
            node_size=10, edge_color=color_list, width=2.0,
            edge_cmap=plt.cm.Blues, font_weight="bold", font_color="black")


def make_8puzzles():
    startState = "0ABCDEFGH"
    goal = "0ABCDEFGH"
    size = 3
    start = (startState, "")
    fringe = deque()
    fringe.append(start)
    visited = {startState: 0, }
    h = {0: startState, }

    while len(fringe) is not 0:
        v = fringe.popleft()
        children = get_children(v[0])
        for child in children.keys():
            if child not in visited.keys():
                puz = (child, v[1] + children.get(child, 0))
                fringe.append(puz)
                visited[child] = len(puz[1])
                if len(puz[1]) in h.keys():
                    if random.randint(0, 100) < 5:
                        h[len(puz[1])] = child
                else:
                    h[len(puz[1])] = child
    file = open("8puzzles.txt", "w")
    for thing in h.values():
        file.write(thing+"\n")
    return visited


def run_all(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    goal = lines[0].split()[0].replace("\n", "")
    sum_time = 0
    count = 0
    size = 3

    for line in lines:
        sep = line.split(" ")
        state = sep[0].replace("\n", "")

        print("%s: (%s)" % (state, count))

        try:
            start = time.process_time()
            path = solve_bfs_original(state) ###
            end = time.process_time()
            sum_time = sum_time + (end - start)
            print("\tBFS\t\t%s \t%s" % (len(path), round(end - start, 5)))
        except MemoryError:
            print("\tBFS")

        try:
            start = time.process_time()
            path = id_dfs(state, count) ###
            end = time.process_time()
            sum_time = sum_time + (end - start)
            print("\tID DFS\t%s \t%s" % (len(path), round(end - start, 5)))
        except MemoryError:
            print("\ID DFS")

        try:
            start = time.process_time()
            path = a_star_taxi(state) ###
            end = time.process_time()
            sum_time = sum_time + (end - start)
            print("\tA-STAR\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")

        try:
            start = time.process_time()
            path = solve_bfs_zoom(state) ###
            end = time.process_time()
            sum_time = sum_time + (end - start)
            print("\tBI BFS\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tBI BFS")

        count += 1

    print("Total Time: %s" % round(sum_time, 5))


if __name__ == "__main__":
    # main func!
    main()


# the discarded method graveyard

# Mostly stuff I thought would be cool in 1st pd (math) and then implemented in Ai the next
#  period and soon realized my flawed thinking. Kept in case I want to copy from them later.

#                ______
#          _____/      \\_____
#         |  _     ___   _   ||
#         | | \     |   | \  ||
#         | |  |    |   |  | ||
#         | |_/     |   |_/  ||
#         | | \     |   |    ||
#         | |  \    |   |    ||
#         | |   \. _|_. | .  ||
#         |                  ||
#         |   misc. methods  ||
#         |                  ||
# *       | *   **    * **   |**      **
#  \))ejm97/.,(//,,..,,\||(,,.,\\,.((//


def solve_kdfs_heap(start, k):
    fringe = [(taxicab_dist(start, goal), start, 0, {start, }, ""), ]
    while len(fringe) is not 0:
        v = heappop(fringe)
        if goal_test(v[1]):
            return v
        if v[2] < k:
            children = get_children(v[1])
            for child in children:
                if child not in v[3]:
                    a = set(v[3])
                    a.add(child)
                    heappush(fringe, (taxicab_dist(child, goal), child, v[2] + 1, a, v[4]+children.get(child)))
    return None


def id_dfs_heap(start, max):
    for k in range(1, max):
        sol = solve_kdfs_heap(start, k)
        if sol is not None:
            return sol
    return None


def solve_kbfs_cab(state, k):
    start_state = state
    fringe_top = [(taxicab_dist(state, goal), state, 0), ]
    visited_top = {state, }
    fringe_top_next = []
    fringe_t = {state, }
    done = False
    count = 0

    if parity_check(state) == 1:  #
        return -1  # if parity determines its not solveable

    while not done:
        while len(fringe_top) is not 0:
            vt = heappop(fringe_top)  # your standard BFS algorithm
            if goal_test(vt[1]):
                return vt[2]
            children = get_children(vt[1])
            for child in children.keys():
                if child not in visited_top:
                    # fringe_top.append((taxicab_dist(child, goal), child, vb[2]+1))
                    heappush(fringe_top_next, (taxicab_dist(child, goal), child, vt[2] + 1))
                    visited_top.add(child)
        if count >= k:
            done = True
        else:
            count += 1
            fringe_top = list(fringe_top_next)

    if len(fringe_top) is 0:
        return None


def id_bfs(start, max):
    for k in range(taxicab_dist(start, goal), max):
        sol = solve_kbfs_zoom_cab(start, k)
        if sol is not None:
            return sol
    if max == 0:
        return ""
    return None


def solve_kbfs_zoom_cab(state, k):
    start_state = state
    fringe_top = [(taxicab_dist(state, goal), state, 0), ]
    fringe_bottom = [(taxicab_dist(goal, state), goal, 0), ]
    visited_top = {state, }
    visited_bottom = {goal, }
    fringe_top_next = []
    fringe_bottom_next = []
    fringe_t = {state, }
    done = False
    count = -1

    if parity_check(state) == 1:  #
        return -1  # if parity determines its not solveable

    while not done:
        while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
            vt = heappop(fringe_top)  # your standard BFS algorithm
            vb = heappop(fringe_bottom)
            if vb[1] in visited_top:
                for s in fringe_top:
                    if s[1] == vb[1]:
                        #if s[2] + vb[2] < k:
                        return s[2] + vb[2]
            if goal_test(vt[1]):
                return vt[2]
            children = get_children(vt[1])
            for child in children.keys():
                if child not in visited_top:
                    # fringe_top.append((taxicab_dist(child, goal), child, vb[2]+1))
                    heappush(fringe_top_next, (taxicab_dist(child, goal), child, vt[2] + 1))
                    visited_top.add(child)
            children = get_children(vb[1])
            for child in children.keys():
                if child not in visited_bottom:
                    # fringe_bottom.append((taxicab_dist(child, state), child, vb[2] + 1))
                    heappush(fringe_bottom_next, (taxicab_dist(child, state), child, vb[2] + 1))
                    visited_bottom.add(child)
        if count >= k:
            done = True
        else:
            count += 1
            fringe_bottom = list(fringe_bottom_next)
            fringe_top = list(fringe_top_next)

    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return None


def solve_bfs_zoom_heap(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    start_state = state
    fringe_top = [(taxicab_dist(state, goal), state, 0), ]
    fringe_bottom = [(taxicab_dist(goal, state), goal, 0), ]
    visited_top = {state, }
    visited_bottom = {goal, }
    fringe_t = {state, }

    if parity_check(state) == 1:   #
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
                heappush(fringe_top, (taxicab_dist(child, goal), child, vt[2]+1))
                visited_top.add(child)
        children = get_children(vb[1])
        for child in children.keys():
            if child not in visited_bottom:
                heappush(fringe_bottom, (taxicab_dist(child, state), child, vb[2] + 1))
                # fringe_bottom.appendleft((child, vb[1]+1))
                visited_bottom.add(child)
    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return -2
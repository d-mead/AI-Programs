import sys
import random
#import xlsxwriter
from collections import deque
import time
import pickle
from heapq import heappush, heappop
# heappush(list, item)
# heappop(list)
#import graph_tool
# from graph_tool.all import *
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#sys.path.append('/Users/JackMead/Desktop/CompSci/PycharmProjects/AIPrograms/venv/lib/python3.7/site-packages/graph-tool-2.27/src')
#from graph_tool import *


def main():
    global size
    global goal
    global memory
    global memorylist
    global g

    memory = set()
    memorylist = []

    goal = "0ABCDEFGHIJKLMNO"
    size = 4

    visualize2()

    # filename = "16puzzle.txt"
    # file = open(filename, "r")
    # lines = file.readlines()
    # file.close()
    # goal = "0ABCDEFGHIJKLMNO"
    # sum_time = 0
    # count = 0
    # size = 4
    #
    #
    # for line in lines:
    #
    #     sep = line.split(" ")
    #     size = 4
    #     state = sep[0].replace("\n", "")
    #
    #     print("%s: (%s)" % (state, count))
    #
    #     #worksheet.write(count, 0, count)
    #
    #     try:
    #         # start = time.process_time()
    #         start = time.clock()
    #         path = a_star_multiplier(state, .6) ###
    #         # end = time.process_time()
    #         end = time.clock()
    #         sum_time = sum_time + (end - start)
    #         #worksheet.write(count, 1, path) ###
    #         print("\tA-STAR 2\t%s \t%s" % (path, round(end - start, 5)))
    #     except MemoryError:
    #         print("\tA Star")
    #
    #     count += 1
    #
    # print("Total Time: %s" % round(sum_time, 5))
    #workbook.close()


def a_star(state):
    fringe_top = [(taxicab_dist(state, goal)+0, state, 0)]
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

        children = get_children(vt[1])
        for child in children.keys():
            if child not in visited_top:
                heappush(fringe_top, ((vt[2]+1+taxicab_dist(child, goal)), child, vt[2]+1))
        # visited_top.add(vt[1])

    if len(fringe_top) is 0:
        return -2


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


def id_dfs(start, max):
    for k in range(taxicab_dist(start, goal), max+3):
        sol = solve_kdfs(start, k)
        if sol is not None:
            return sol
    return None


def id_dfs_nps(start, max):
    for k in range(taxicab_dist(start, goal), max+3):
        sol, nodes = solve_kdfs_nps(start, k)
        if sol is not None:
            return sol, nodes
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


def solve_bfs_original_nps(state):
    startState = state
    start = (state, "")
    fringe = deque()
    fringe.append(start)
    visited = {state, }

    if parity_check(state) == 1:  #
        return -1  # if parity determines its not solveable

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
        if goal_test(vt[0]):
            return vt[1]
        children = get_children(vt[0])
        for child in children.keys():
            if child not in visited_top:
                fringe_top.appendleft((child, vb[1]+1))
                visited_top.add(child)
        children = get_children(vb[0])
        for child in children.keys():
            if child not in visited_bottom:
                fringe_bottom.appendleft((child, vb[1]+1))
                visited_bottom.add(child)
    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return -2


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
    # returns a dictionary of the children from a state, each child's value being the move direction used to get there
    # find the one it swaps with
    # calculate how far it should be from that

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


def visualize():
    g = Graph(directed = False)
    a_star_visialize(g)
    g.graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=10, output_size = (500, 500), output = "graph1.png")


def a_star_visialize(state):
    fringe_top = [(taxicab_dist(state, goal) + 0, state, 0, taxicab_dist(state, goal), [state, ])]
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


def visualize2():

    state = "AFICDB0GEHJOLMKN"
    # Build a dataframe with 4 connections
    from_list = []
    to_list = []


    g, l = a_star_visialize(state)

    edge_l = []
    color_list = [".6"]*len(g.edges())
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

    # for e in range(0, len(g.edges())):
    #     if e < len(color_list):
    #         if color_list[e] != ".1":
    #             color_list[e] = ".5"
    #     else:
    #         color_list.append(".5")


    #print(g.edges())
    #print(vt[4])
    ##print(edge_l)

    # plt.subplot(121)
    #
    # nx.draw(g, with_labels=True, font_weight='bold')
    plt.subplot(111)


    nx.draw(g, labels = {state: "start", goal:"finish"}, with_labels=True, font_size = 10, node_color='darkblue', node_size=10, edge_color=color_list, width=2.0,
            edge_cmap=plt.cm.Blues, font_weight = "bold", font_color = "black", label = "Graph of all nodes proccesed and the correct path for A* search from " + state + " to " + goal+"." )


    #nx.draw_shell(g, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    options = {
    'node_color': 'black',
    'node_size': 10,
    'width': 2,

    }
    plt.show()


if __name__ == "__main__":
    # main func!
    main()









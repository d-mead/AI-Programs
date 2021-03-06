import sys
import random
from collections import deque
import time
from heapq import heappush, heappop
# import pickle
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from colour import Color

# sys.path.append('/Users/JackMead/Desktop/CompSci/PycharmProjects/AIPrograms/venv/lib/python3.7/site-packages/graph-tool-2.27/src')
# from graph_tool import *


def main():
            #  0      1       2        3       4
            #(name, size, direction, start, indexes)
    # cars = create_cars_list()

    # cars_0 = (("@", 2, 0, (2, 3), []),
    #           ("A", 2, 0, (1, 1), []),
    #           ("B", 3, 1, (1, 2), []),
    #           ("C", 2, 1, (1, 5), []),
    #           ("D", 3, 1, (4, 2), []),
    #           ("E", 3, 0, (3, 6), []),
    #           ("F", 2, 0, (5, 5), []),
    #           ("O", 3, 1, (6, 1), [])
    #         )


    # cars_0 = (("@", 2, 0, (2, 3), []),
    #           ("A", 2, 1, (3, 4), []),
    #           ("B", 2, 1, (6, 5), []),
    #           ("R", 3, 0, (3, 6), []),
    #           ("P", 3, 1, (4, 1), []),
    #           # ("O", 3, 1, (1, 1), []),
    #           ("Q", 3, 0, (4, 4), []),
    #           )

    # cars_0 = (("@", 2, 0, (3, 3), []),
    #           ("A", 3, 1, (1, 1), []),
    #           ("B", 3, 1, (2, 1), []),
    #           ("C", 3, 0, (3, 1), []),
    #           ("D", 2, 1, (6, 1), []),
    #           ("E", 2, 0, (3, 2), []),
    #           ("F", 3, 1, (5, 2), []),
    #           ("G", 2, 1, (6, 3), []),
    #           ("H", 2, 0, (1, 4), []),
    #           ("I", 2, 1, (3, 4), []),
    #           ("J", 2, 0, (4, 5), []),
    #           ("K", 2, 0, (2, 6), []),
    #           ("L", 2, 0, (4, 6), []),
    #           )

    # cars_0 = (("@", 2, 0, (3, 3), []),
    #           ("A", 3, 0, (1, 1), []),
    #           ("B", 2, 1, (4, 1), []),
    #           ("C", 3, 1, (5, 1), []),
    #           ("D", 3, 1, (6, 1), []), # row 1
    #           ("E", 2, 1, (1, 2), []),
    #           ("F", 2, 0, (2, 2), []), # 14
    #           ("G", 2, 0, (1, 4), []),
    #           ("H", 2, 1, (3, 4), []),
    #           ("I", 2, 1, (2, 5), []),
    #           ("J", 2, 0, (3, 6), []),
    #           ("K", 2, 0, (5, 6), []),
    #           ("L", 2, 0, (5, 5), []),
    #           )

    # cars_0 = (("@", 2, 0, (4, 3), []),
    #           ("A", 3, 1, (3, 1), []),
    #           ("B", 2, 0, (4, 1), []),
    #           ("C", 3, 1, (6, 1), []),
    #           ("D", 3, 1, (4, 4), []),  # row 1
    #           ("E", 2, 0, (5, 4), []),
    #           ("F", 2, 1, (1, 5), []),  # 14
    #           ("G", 2, 0, (2, 5), []),
    #           ("H", 2, 0, (5, 6), []),
    #           )

    # cars_0 = (("@", 2, 0, (3, 3), []),
    #           ("B", 3, 0, (1, 1), []),
    #           ("C", 2, 1, (4, 1), []),
    #           ("D", 3, 1, (5, 1), []),
    #           ("E", 3, 1, (6, 1), []),
    #           ("F", 2, 1, (1, 2), []),
    #           ("G", 2, 0, (2, 2), []),
    #           ("H", 2, 0, (1, 4), []),
    #           ("I", 2, 1, (3, 4), []),
    #           ("J", 2, 1, (2, 5), []),
    #           ("K", 2, 0, (5, 5), []),
    #           ("L", 2, 0, (3, 6), []),
    #           ("M", 2, 0, (5, 6), []),
    #           )

    cars_0 = (("@", 2, 0, (1, 3), []),
              ("A", 2, 1, (2, 1), []),
              ("B", 2, 0, (3, 1), []),
              ("C", 2, 0, (3, 2), []),
              ("D", 2, 1, (6, 2), []),
              ("E", 3, 1, (3, 3), []),
              ("F", 2, 1, (4, 3), []),
              ("G", 2, 0, (5, 4), []),
              ("H", 2, 1, (1, 5), []),
              ("I", 2, 0, (4, 5), []),
              ("J", 2, 1, (6, 5), []),
              ("K", 3, 0, (2, 6), []),
              )

    cars = list()

    for car in cars_0:
        cars.append((car[0], car[1], car[2], car[3], calculate_indexes(car[3], car[1], car[2])))

    blocked = list()
    for car in cars:
        blocked.extend(car[4])

    moves = set()

    states = list()

    state = tuple((cars, blocked, moves, states))

    state[3].append(display_state_string(state))

    # for s in get_children(state):
    #     display_state(s)

    # states = read_file("jams.txt")

    # for state in states:

    display_state(state)

    start = time.perf_counter()
    start = time.perf_counter()
    # bfs(state)
    a_star_taxi(state)
    end = time.perf_counter()
    print(round(end - start, 5))
    #
    #     print()
    #     print()


def read_file(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    states = list()

    count = 1

    reset_count = 0

    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"]

    for x in range(0, 40):
        reset_count = 0
        count +=1
        cars = list()
        car = lines[count].replace("\n", "").split(" ")
        cars.append(("@", int(car[3]), int(car[2]), (int(car[0])+1, int(car[1])+1), calculate_indexes((int(car[0])+1, int(car[1])+1), int(car[3]), int(car[2]))))
        count += 1
        while "." not in lines[count]:
            car = lines[count].split(" ")
            cars.append((letters[reset_count], int(car[3]), int(car[2]), (int(car[0])+1, int(car[1])+1), calculate_indexes((int(car[0])+1, int(car[1])+1), int(car[3]), int(car[2]))))
            count +=1
            reset_count += 1
        blocked = list()
        for car in cars:
            blocked.extend(car[4])

        state = tuple((cars, blocked, set(), list()))

        state[3].append(display_state_string(state))

        states.append(state)
        count += 2

    return states


def create_cars_list():
    cars = list()
    num_cars = input("Number of cars: ")
    for x in range(0, int(num_cars)):
        name = input("Name (A-Z): ")
        size = input("Size (2 or 3): ")
        direction = input("Direction (horizontal = 0, vertical = 1): ")
        starting_y = input("Starting row: ")
        starting_x = input("Starting column: ")
        starting_index = (int(starting_x), int(starting_y))
        index_list = calculate_indexes(starting_index, int(size), int(direction))
        cars.append((name, int(size), int(direction), starting_index, index_list))
    return cars


def calculate_indexes(start, size, direction):
    indexes = list()
    if direction == 0:
        for x in range(0, size):
            indexes.append((start[0]+x, start[1]))
    else:
        for y in range(0, size):
            indexes.append((start[0], start[1]+y))
    return indexes


def heuristic(state):
    count = 0
    red_car = 0
    for car in state[0]:
        if car[0] == "@":
            red_car = car

    # red_car = heappop(list(state[0]))

    for x in range(red_car[3][0]+2, 7):
        if (x, 3) in state[1]:
            count += 1
    return count


def a_star_taxi(state):
    fringe_top = [(heuristic(state)+0, state, 0, heuristic(state))]
    visited_top = set()

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if display_state_string_2(vt[1]) not in visited_top:
            visited_top.add(display_state_string_2(vt[1]))
        else:
            continue

        if goal_test(vt[1]):
            return vt[2]

        children = get_children(vt[1])
        for child in children:
            if display_state_string_2(child) not in visited_top:
                # a = (vt[2]+1+taxicab_dist(child, goal))
                # b = (1+vt[0]+children.get(child))
                heur = vt[3] + heuristic(state)
                heappush(fringe_top, ((vt[2]+1+heur), child, vt[2]+1, heur))
                visited_top.add(display_state_string_2(vt[1]))

    if len(fringe_top) is 0:
        return -2


def bfs(state):
    fringe = deque()
    fringe.append(state)
    visited = [state[1], ]

    while len(fringe) is not 0:
        s = fringe.popleft()
        if goal_test(s): # if the state is won
            return s[2] # return the moves

        children = get_children(s)
        for child in children:
            if child[1] not in visited:
                fringe.append(child)
                visited.append(child)

    if len(fringe) is 0:
        return -1


def display_state(state):
    board = [['·']*6 for i in range(6)]
    for car in state[0]:
        for cord in car[4]:
            try:
                board[cord[1]-1][cord[0]-1] = car[0]
            except IndexError:
                a = 5
    for x in range(0, 6):
        row = board[x]
        if x == 2:
            print(' '.join(row)+ ' →')
        else:
            print(' '.join(row))
    print(" ")
    a=5


def display_state_string(state):
    # print("d")
    # string = ""
    # board = [['·']*6 for i in range(6)]
    # for car in state[0]:
    #     for cord in car[4]:
    #         try:
    #             board[cord[1]-1][cord[0]-1] = car[0]
    #         except IndexError:
    #             a = 5
    #             print("ITS OVER ANAKIN")
    #
    # for x in range(0, 6):
    #     row = board[x]
    #     if x == 2:
    #         string += (' '.join(row)+ ' →\n')
    #     else:
    #         string += (' '.join(row)+ "\n")
    # return string
    return state


def display_state_string_2(state):
    string = ""
    board = [['·']*6 for i in range(6)]
    for car in state[0]:
        for cord in car[4]:
            try:
                board[cord[1]-1][cord[0]-1] = car[0]
            except IndexError:
                a = 5
                print("ITS OVER ANAKIN")

    for x in range(0, 6):
        row = board[x]
        if x == 2:
            string += (' '.join(row)+ ' →\n')
        else:
            string += (' '.join(row)+ "\n")
    return string


def get_children(state):
    children = list()
    for car in state[0]: # looping through all the cars
        a=5
        for car_move in get_car_moves(car, state):

            new_cars = list(state[0])
            new_cars.remove(car)
            new_cars.append(car_move[0])

            # new_blocked = list(state[1])
            # for index in state[1]:
            #     if index in car[4]:
            #         new_blocked.remove(index)

            # new_blocked = [x for x in list(state[1]) if x not in list(car[4])]

            new_blocked = list(set(state[1])-set(car[4])) # opted

            new_blocked.extend(car_move[0][4])

            new_moves = list(state[2])
            new_moves.append(car_move[1])

            new_states = list(state[3])

            new_state = (new_cars, new_blocked, new_moves, new_states)

            new_state[3].append(display_state_string(new_state)) # opted

            children.append(new_state)

    return children


def get_car_moves(car, state):
    car_moves = list()
    shift = 0
    
    blocked = list(state[1])
    for cord in car[4]:
        blocked.remove(cord)
    
    if car[2] == 0: # hor
        for x in range(car[3][0]+car[1], 7):
            if (x, car[3][1]) not in blocked: # if its not blocked
                shift = x-(car[3][0]+car[1])+1
                if car[4][car[1]-1][0]+shift < 7:
                    if not any(i in blocked for i in move_car(car, x-(car[3][0]+car[1])+1)[4]):
                        car_moves.append((move_car(car, x-(car[3][0]+car[1])+1), car[0]+"R"+str(shift)))
            else:
                break  # no more searching this line
        for x in range(car[3][0]-1, 0, -1): # from row 1 to just before the car back
            if (x, car[3][1]) not in blocked: # if its not blocked
                shift = x-car[3][0]
                if car[4][0][0]-shift > 0:
                    if not any(i in blocked for i in move_car(car, x-car[3][0])[4]):
                        car_moves.append((move_car(car, x-car[3][0]), car[0]+"L"+str(abs(shift))))
            else:
                break  # no more searching this line
    elif car[2] == 1:
        if car[0] == "O":
            a = 5
        for y in range(car[3][1]+car[1], 7):
            if (car[3][0], y) not in blocked:  # if its not blocked
                shift = y-(car[3][1]+car[1])+1
                if car[4][car[1]-1][1]+shift < 7:
                    if not any(i in blocked for i in move_car(car, y-(car[3][1]+car[1])+1)[4]):
                        car_moves.append((move_car(car, y-(car[3][1]+car[1])+1), car[0]+"D"+str(shift)))
            else:
                break  # no more searching this line
        for y in range(car[3][1]-1, 0, -1):  # from row 1 to just before the car back
            if (car[3][0], y) not in blocked:  # if its not blocked
                shift = y-car[3][1]
                if car[4][0][1] - shift > 0:
                    if not any(i in blocked for i in move_car(car, y-car[3][1])[4]):
                        car_moves.append((move_car(car, y-car[3][1]), car[0]+"U"+str(abs(shift))))
            else:
                break # no more searching this line
    return car_moves


def move_car(car, x):
    if car[2] == 0 : #hor
        if car[1] == 2:
            return car[0],car[1],car[2],(car[3][0]+x,car[3][1]),[(car[4][0][0]+x,car[4][0][1]),
                                                                (car[4][1][0]+x, car[4][1][1])]
        else:
            return car[0], car[1], car[2], (car[3][0] + x, car[3][1]), [(car[4][0][0] + x, car[4][0][1]),
                                                                        (car[4][1][0] + x, car[4][1][1]),
                                                                        (car[4][2][0] + x, car[4][2][1])]
    else:
        if car[1] == 2:
            return car[0], car[1], car[2], (car[3][0], car[3][1]+x), [(car[4][0][0], car[4][0][1]+x),
                                                                      (car[4][1][0], car[4][1][1]+x)]
        else:
            return car[0], car[1], car[2], (car[3][0], car[3][1]+x), [(car[4][0][0], car[4][0][1]+x),
                                                                      (car[4][1][0], car[4][1][1]+x),
                                                                      (car[4][2][0], car[4][2][1]+x)]


def finish(state):
    red_car = 0
    for car in state[0]:
        if car[0] == "@":
            red_car = car
    distance = 5-red_car[3][0]

    new_car = move_car(red_car, distance)

    new_cars = list(state[0])
    new_cars.remove(red_car)
    new_cars.insert(state[0].index(red_car), new_car)

    new_blocked = list(state[1])
    for index in state[1]:
        if index in red_car[4]:
            new_blocked.remove(index)
    new_blocked.extend(new_car[4])

    new_moves = list(state[2])
    new_moves.append("XR"+str(distance))

    new_states = list(state[3])

    new_state = (new_cars, new_blocked, new_moves, new_states)

    new_state[3].append(display_state_string(new_state))

    return new_state


def display_all(s, moves):
    for state in s:
        print(display_state(state))
    print(", ".join(moves))
    print(len(moves))


def goal_test(state):
    red_car = 0
    for car in state[0]:
        if car[0] == "@":
            red_car = car
    for x in range(red_car[3][0]+2, 7): # from the end of the red car to the exit
        if (x, 3) in state[1]: # if one of those indexes is blocked
            return False # its not a winning state
    state = finish(state)
    display_all(state[3], state[2])
    return True


def a_star_visualize(state):
    fringe_top = [(heuristic(state) + 0, state, 0, heuristic(state), [])]
    visited_top = set()

    g = nx.Graph()

    # if parity_check(state) == 1:
    #     return -1

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if display_state_string_2(vt[1]) not in visited_top:
            visited_top.add(display_state_string_2(vt[1]))
        else:
            continue

        if goal_test(vt[1]):
            return g, vt[4]

        children = get_children(vt[1])
        for child in children():
            if display_state_string_2(child) not in visited_top:
                # a = (vt[2]+1+taxicab_dist(child, goal))
                # b = (1+vt[0]+children.get(child))
                heur = vt[3] + heuristic(state)
                ancestors = list(vt[4])
                ancestors.append(vt[1])
                visited_top.add(display_state_string_2(vt[1]))
                heappush(fringe_top, ((vt[2] + 1 + heur), child, vt[2] + 1, heur, ancestors))
                g.add_edge(child, vt[1])


def visualize(state):

    plt.figure().suptitle("Search Algorithm Graphs for Path Length " + str(length+1))

    g, l = a_star_visualize(state)
    draw_graph(g, l, 221, state, "A-Star")

    plt.legend(('state', 'move'), loc='best', prop={'size': 6})

    plt.show()


def draw_graph(g, l, subplot, state, title):
    edge_l = []
    color_list = [".6"] * len(g.edges())
    l.append(goal)
    prev = l[0]

    red = Color("lightgrey")
    colors = list(red.range_to(Color("black"), len(g.edges())))

    print(str(colors[10]))

    for x in range(0, len(g.edges())):
        if str(colors[x])[0] == '#':
            if len(str(colors[x])) == 4:
                # print(str(str(colors[x])+str(colors[x])[1:]))
                color_list[x] = (str(colors[x])+str(colors[x])[1:])[:5]+"FF"

            else:
                # print(str(colors[x]))
                color_list[x] = str(colors[x])[:5]+"FF"

    count = 0

    for node in l:
        edge_l.append((prev, node))
        if (prev, node) in list(g.edges()):
            index = list(g.edges()).index((prev, node))
            color_list[index] = "red"
        elif (node, prev) in list(g.edges()):
            index = list(g.edges()).index((node, prev))
            color_list[index] = 'red'
        count += 1
        prev = node

    plt.subplot(subplot)

    plt.title(title, loc='center', size = 'medium')

    nx.draw(g, with_labels=True, labels={state: "start", goal: "finish"}, font_size=7, node_color='blue',
            node_size=5, edge_color=color_list, width=1.5, font_weight="bold", font_color="black")

if __name__ == "__main__":
    # main func!
    main()

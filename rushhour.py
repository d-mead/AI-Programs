import sys
import random
from collections import deque
import time
# from heapq import heappush, heappop
# import pickle

# sys.path.append('/Users/JackMead/Desktop/CompSci/PycharmProjects/AIPrograms/venv/lib/python3.7/site-packages/graph-tool-2.27/src')
# from graph_tool import *


def main():
            #  0      1       2        3       4
            #(name, size, direction, start, indexes)
    # cars = create_cars_list()

    cars_0 = (("X", 2, 0, (2, 3), []),
              ("A", 2, 0, (1, 1), []),
              ("B", 3, 1, (1, 2), []),
              ("C", 2, 1, (2, 5), []),
              ("D", 3, 1, (4, 2), []),
              ("E", 3, 0, (3, 6), []),
              ("F", 2, 0, (5, 5), []),
            )

    # cars_0 = (("X", 2, 0, (2, 3), []),
    #           ("A", 2, 0, (2, 4), []),
    #           ("B", 2, 1, (2, 5), []),
    #           ("C", 2, 0, (3, 6), []),
    #           ("O", 3, 1, (4, 3), []),
    #           ("P", 3, 1, (6, 4), []),
    #          )
    #
    # cars_0 = (("X", 2, 0, (2, 3), []),
    #           ("A", 2, 1, (3, 4), []),
    #           ("B", 2, 1, (6, 5), []),
    #           ("R", 3, 0, (3, 6), []),
    #           ("P", 3, 1, (4, 1), []),
    #           ("O", 3, 1, (1, 1), []),
    #           ("Q", 3, 0, (4, 4), [])
    #           )

    cars = list()

    for car in cars_0:
        cars.append((car[0], car[1], car[2], car[3], calculate_indexes(car[3], car[1], car[2])))

    blocked = list()
    for car in cars:
        blocked.extend(car[4])

    moves = list()

    states = list()

    state = tuple((cars, blocked, moves, states))

    state[3].append(display_state_string(state))

    display_state(state)

    # for s in get_children(state):
    #     display_state(s)

    start = time.perf_counter()
    bfs(state)
    end = time.perf_counter()
    print(round(end - start, 5))


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
    print()


def display_state_string(state):
    string = ""
    board = [['·']*6 for i in range(6)]
    for car in state[0]:
        for cord in car[4]:
            try:
                board[cord[1]-1][cord[0]-1] = car[0]
            except IndexError:
                a = 5
                # print("ITS OVER ANAKIN")

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
        for car_move in get_car_moves(car, state):

            new_cars = list(state[0])
            new_cars.remove(car)
            new_cars.insert(state[0].index(car), car_move[0])

            new_blocked = list(state[1])
            for index in state[1]:
                if index in car[4]:
                    new_blocked.remove(index)
            new_blocked.extend(car_move[0][4])

            new_moves = list(state[2])
            new_moves.append(car_move[1])

            new_states = list(state[3])

            new_state = (new_cars, new_blocked, new_moves, new_states)

            new_state[3].append(display_state_string(new_state))

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
                break # no more searching this line
        for x in range(car[3][0]-1, 0, -1): # from row 1 to just before the car back
            # if car[0] == "E":
            #     a = 5
            if (x, car[3][1]) not in blocked: # if its not blocked
                shift = x-car[3][0]
                if car[4][0][0]-shift > 0:
                    # if car[0]+"L"+str(abs(shift)) == "EL2":
                    #     a = 5
                    if not any(i in blocked for i in move_car(car, x-car[3][0])[4]):
                        car_moves.append((move_car(car, x-car[3][0]), car[0]+"L"+str(abs(shift))))
            else:
                break # no more searching this line
    elif car[2] == 1:
        if car[0] == "C":
            a = 5
        for y in range(car[3][1]+car[1], 7):
            if (car[3][0], y) not in blocked: # if its not blocked
                shift = y-(car[3][1]+car[1])+1
                if car[4][car[1]-1][0]+shift < 7:
                    if not any(i in blocked for i in move_car(car, y-(car[3][1]+car[1])+1)[4]):
                        car_moves.append((move_car(car, y-(car[3][1]+car[1])+1), car[0]+"D"+str(shift)))
            else:
                break # no more searching this line
        for y in range(car[3][1]-1, 0, -1): # from row 1 to just before the car back
            if (car[3][0], y) not in blocked: # if its not blocked
                shift = y-car[3][1]
                if car[4][0][1] - shift > 0:
                    if not any(i in blocked for i in move_car(car, y-car[3][1])[4]):
                        car_moves.append((move_car(car, y-car[3][1]), car[0]+"U"+str(abs(shift))))
            else:
                break # no more searching this line
    return car_moves


def move_car(car, x):
    if car[2] == 0 :# hor
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
        if car[0] == "X":
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


def display_all(s):
    for state in s[3][1:]:
        print(state)
    print(", ".join(s[2]))


def goal_test(state):
    red_index = state[0][0][3]
    for x in range(red_index[0]+2, 7): # from the end of the red car to the exit
        if (x, 3) in state[1]: # if one of those indexes is blocked
            return False # its not a winning state
    state = finish(state)
    display_all(state)
    return True


if __name__ == "__main__":
    # main func!
    main()

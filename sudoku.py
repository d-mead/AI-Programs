import sys
import time
import random
import math
import xlsxwriter
import datetime
from collections import deque
import copy
from random import shuffle


def main():
    sys.setrecursionlimit(500000)
    global sets, neighbors, visited
    visited = 0
    states = read_file("sudoku_puzzles_1.txt")
    # state = states[54]
    # solve(state)
    # solve_one(state)
    a = time.perf_counter()
    solve_file("sudoku_puzzles_1.txt")
    b = time.perf_counter()
    print("total time: %s" % round(b - a, 5))
    # record()


def solve_file(filename):
    global visited
    count = 0
    for state in read_file(filename):
        print("Board Number: %s" % count)
        start = time.perf_counter()
        solve_2(state)
        end = time.perf_counter()
        print("Time: %s \t Calls: %s" % (round(end - start, 5), visited))
        print()
        visited = 0
        count += 1


def solve_one(state):
    global visited
    start = time.perf_counter()
    solve_2(state)
    end = time.perf_counter()
    print("Time: %s \t Calls: %s" % (round(end - start, 5), visited))
    print()
    visited = 0


def record():
    global visited
    workbook = xlsxwriter.Workbook(str(datetime.datetime.now()) + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "number")
    worksheet.write(0, 1, "runtime")
    worksheet.write(0, 2, "visited")
    count = 0
    for state in read_file("sudoku_puzzles_1.txt"):
        print(count)
        start = time.perf_counter()
        solve_2(state)
        end = time.perf_counter()
        print("Time: %s \t Calls: %s" % (round(end - start, 5), visited))
        print()
        worksheet.write(count, 0, str(count))
        worksheet.write(count, 1, round(end-start, 5))
        worksheet.write(count, 2, visited)
        # print(round(end - start, 5))
        # print(visited)
        visited = 0
        count += 1

    workbook.close()


def make_list(state):
    global visited
    visited += 1
    options = dict()
    for i, char in enumerate(state):
        if char != ".":
            options[i] = char
        else:
            options[i] = available(state, i)
    sorted_options = dict(sorted(options.items(), key=lambda kv: (len(kv[1]), kv[0])))
    return sorted_options


def available(state, i):
    global neighbors
    neighs = []
    symbols = "123456789abcdefghijklmnopqrstuvwxyz"
    options = symbols[:int(math.sqrt(len(state)))]
    char = state[i]
    # for n in neighbors:
    #     if i in n:
    #         neighs.extend(list(n))
    for n in neighbors[i]:
        c = state[n]
        if c != ".":
            options = options.replace(c, "")
    return options


def propagate(state):
    global visited, neighbors
    visited += 1
    solved = deque()
    s = state.copy()
    for i, options in s.items():
        if len(options) == 1:
            solved.append(i)
            # print(i)
        # else:
        #     break
    i = 0
    while len(solved) != 0:
        i = solved.pop()
    # for i in solved:
        for n in neighbors[i]:
            if s[i] in s[n]:
                if len(s[n]) == 1:
                    # print(".", end="")
                    return None
                s[n] = s[n].replace(s[i], "")
                if len(s[n]) == 1:
                    # if n not in solved:
                    solved.append(n)
    



    # s = dict(sorted(s.items(), key=lambda kv: (len(kv[1]), kv[0])))

    # if len(solved) != len(state):
    #     sn = propagate(state)
    #     if sn:
    #         return sn
    return s


def csp_2(state):  # state is just the dict of available locations
    global visited

    if state is None:
        return None

    # vals = list(state.values())

    # if goal_test_string(dict_to_string_initial(state)):#len(vals[len(vals)-1]) == 1:
    #     return state

    var = -1#vals[0]
    # varis = []
    for index, options in state.items():
        if len(options) > 1:
            var = index
            # varis.append(index)
            break

    if var == -1:
        return state

    # var = varis[random.randint(0, len(varis)-1)]

    options = list(state[var])
    # shuffle(options)
    for val in options:
        # new_options = state.copy
        new_state = state.copy()
        new_state[var] = val
        result = csp_2(propagate(new_state))
        if result is not None:
            return result


def solve_2(state):
    global sets, neighbors, visited
    sets = constrained_sets(state)
    neighbors = make_neighbors(state)
    count = count_symbols(state)

    l = make_list(state[4])

    state = l

    solution = csp_2(state)

    display_s_string(dict_to_string_initial(solution))


def dict_to_string(s_dict):
    s_list = [""]*len(list(s_dict.keys()))
    for var, val in s_dict.items():
        s_list[var] = val

    s_string = "".join(s_list)

    return s_string


def dict_to_string_initial(s_dict):
    s_list = [""]*len(list(s_dict.keys()))
    for var, val in s_dict.items():
        if len(val) == 1:
            s_list[var] = val
        else:
            s_list[var] = "."

    s_string = "".join(s_list)

    return s_string


def solve(state):
    global sets, neighbors, visited
    # display(state)
    sets = constrained_sets(state)
    neighbors = make_neighbors(state)
    count = count_symbols(state)

    start = time.perf_counter()
    solution = csp(state)
    end = time.perf_counter()
    if solution:
        display(solution)
    print(round(end-start, 5))
    print(visited)


def csp(state):
    n = state[0]
    height = state[1]
    width = state[2]
    symbol_set = state[3]
    puzzle = state[4]

    global visited

    if goal_test(state):
        return state

    var = get_next_unassigned_var(state)

    visited += 1

    for val in get_sorted_values(state, var):
        s = list(state[4])
        s[var] = val
        new_puz = "".join(s)
        # new_puz = state[4].replace(state[4][var], str(val))
        new_state = (state[0], state[1], state[2], state[3], new_puz)
        result = csp(new_state)
        if result is not None:
            return result

    return None


def get_next_unassigned_var(state):
    n = state[0]
    height = state[1]
    width = state[2]
    symbol_set = state[3]
    puzzle = state[4]
    for i in range(0, n*n):
        if puzzle[i] == ".":
            return i
    return -1


def get_sorted_values(state, var):
    global neighbors
    n = state[0]
    height = state[1]
    width = state[2]
    symbol_set = state[3]
    puzzle = state[4]

    vals = []

    if var == -1:
        return vals

    n_symbols = []
    for n in neighbors[var]:
        n_symbols.append(puzzle[n])

    for val in symbol_set:
        if val not in n_symbols:
            vals.append(val)

    return vals


def read_file(filename):
    file = open(filename, "r")
    lines = [x.replace("\n", "") for x in file.readlines()]
    file.close()

    symbols = "123456789abcdefghijklmnopqrstuvwxyz"

    states = []

    for line in lines:
        n = int(math.sqrt(len(line)))

        subblock_height = 0
        subblock_width = 0

        if math.sqrt(n) % 1 == 0:
            subblock_height = int(math.sqrt(n))
            subblock_width = int(math.sqrt(n))
        else:
            for x in range(int(math.sqrt(n)), 0, -1):
                if n % x == 0:
                    subblock_height = x
                    break
            for x in range(int(math.sqrt(n))+1, n):
                if n % x == 0:
                    subblock_width = x
                    break

        symbol_set = symbols[:n]

        states.append((n, subblock_height, subblock_width, symbol_set, line))

    return states


def constrained_sets(state):
    n = state[0]
    height = state[1]
    width = state[2]
    puzzle = state[4]

    sets = []
    for x in range(0, n):
        sets.append(list(range(x*n, (x+1)*n)))
    for y in range(0, n):
        sets.append(list(range(y, n*n, n)))

    for a in range(0, n, width):
        for b in range(0, n, height):
            set = []
            for c in range(a, a+width):
                for d in range(b, b+height):
                    set.append(n*(d-1)+c+n)
            sets.append(set)

    return sets


def make_neighbors(state):
    global sets
    n = state[0]
    height = state[1]
    width = state[2]
    puzzle = state[4]

    l = []

    for i in range(0, n*n):
        neighbors = set()
        for s in sets:
            if i in s:
                for neighbor in s:
                    neighbors.add(neighbor)
        neighbors.remove(i)
        l.append(list(neighbors))

    return l


def count_symbols(state):
    n = state[0]
    height = state[1]
    width = state[2]
    symbol_set = state[3]
    puzzle = state[4]

    counts = dict()

    for symbol in symbol_set:
        counts[symbol] = puzzle.count(symbol)

    return counts


def display(state):
    n = state[0]
    puzzle = state[4]
    count = 0
    for x in range(0, n):
        for y in range(0, n):
            print(puzzle[count], end=" ")
            count += 1
        print()
    print()


def display_s_string(state):
    n = int(math.sqrt(len(state)))
    puzzle = state
    count = 0
    for x in range(0, n):
        for y in range(0, n):
            print(puzzle[count], end=" ")
            count += 1
        print()
    # print()


def display_nums(n):
    count = 0
    for x in range(0, n):
        for y in range(0, n):
            print(count, end="".join([" "]*int(2/len(str(count)))))
            count += 1
        print()


def display_cool(state):
    n = state[0]
    puzzle = state[4]
    height= state[1]
    width= state[2]
    count = 0
    for x in range(0, n):
        for y in range(0, n):
            if (y+1) % width == 0:
                print(puzzle[count], end="  !  ")
            else:
                print(puzzle[count], end="   ")
            count += 1
        if (x+1) % height == 0:
            print()
            print("".join(["_"]*n))
            print()
        else:
            print()
            print()


def goal_test(state):
    n = state[0]
    height = state[1]
    width = state[2]
    symbol_set = state[3]
    puzzle = state[4]

    for symbol in symbol_set:
        if puzzle.count(symbol) != n:
            return False
    return True

    # for s in sets:
    #     for symbol in symbol_set:
    #         check_set =
    #         if s.count(symbol_set) != 1:
    #             return False
    # return True


def goal_test_string(state):
    n = int(math.sqrt(len(state)))
    symbol_set = "123456789abcdefghijklmnopqrstuvwxyz"[:n]
    puzzle = state

    for symbol in symbol_set:
        if puzzle.count(symbol) != n:
            return False
    return True


if __name__ == "__main__":
    # main func!
    main()
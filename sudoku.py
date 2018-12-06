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
    global sets, neighbors, visited, symbol_set, sum_time, sum_visited
    sum_time = 0
    sum_visited = 0
    visited = 0

    # states = read_file("sudoku_puzzles_2_hard.txt")
    # state = states[54]
    # solve(state)
    # solve_one(state)

    a = time.perf_counter()
    solve_file("sudoku_puzzles_1.txt")
    b = time.perf_counter()
    print("total time: %s\t\ttotal calls: %s" % (round(sum_time, 5), sum_visited))

    # record("sudoku_puzzles_1.txt")


def solve_file(filename):
    global visited, sum_time, sum_visited
    count = 0
    for state in read_file(filename)[:]:
        make_symbols(int(math.sqrt(len(state[4]))))
        print("Board Number: %s" % count)
        start = time.perf_counter()
        s, t = solve_2(state)
        end = time.perf_counter()
        # print("Time: %s \t Calls: %s" % (t, visited))
        sum_time += t
        sum_visited += visited
        # print(goal_test_string(dict_to_string_initial(s)))
        print()
        visited = 0
        count += 1
    # print(sum_time)


def make_symbols(n):
    global symbol_set
    symbols = "123456789abcdefghijklmnopqrstuvwxyz"
    symbol_set = symbols[:n]


def solve_one(state):
    global visited
    start = time.perf_counter()
    solve_2(state)
    end = time.perf_counter()
    print("Time: %s \t Calls: %s" % (round(end - start, 5), visited))
    print()
    visited = 0


def record(filename):
    global visited
    workbook = xlsxwriter.Workbook(str(datetime.datetime.now()) + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "number")
    worksheet.write(0, 1, "runtime")
    worksheet.write(0, 2, "visited")
    count = 0
    for state in read_file(filename)[:]:
        make_symbols(int(math.sqrt(len(state[4]))))
        # print("Board Number: %s" % count)

        sol, t = solve_2(state)

        # print("Time: %s \t Calls: %s" % (t, visited))
        # print()
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
    # visited += 1
    options = dict()
    for i, char in enumerate(state):
        if char != ".":
            options[i] = char
        else:
            options[i] = available(state, i)
    sorted_options = options#dict(sorted(options.items(), key=lambda kv: (len(kv[1]), kv[0])))
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


def propagate(state, solved):
    global visited, neighbors, sets, symbol_set, changed

    changed = False

    if state is None:
        return None

    s = state.copy()

    while len(solved) != 0:
        i = solved.pop()
        c = s[i]
        for n in neighbors[i]:
            c2 = s[n]
            if c in c2:
                s[n] = s[n].replace(c, "")
                if len(s[n]) == 0:
                    return None
                if len(s[n]) == 1:
                    solved.append(n)
            changed = True
        if goal_test_dict(s):
            return s

    return s


def propagate_2(state):
    global sets, visited, neighbors, symbol_set, changed

    changed = False

    if not state:
        return None

    solved = deque()

    s = state.copy()
    for group in sets:
        for symbol in symbol_set:
            i_found = -1
            for i in group:
                c = s[i]
                if symbol in c:
                    if i_found == -1:
                        i_found = i
                    elif i_found > -1:
                        i_found = -2
                        # break
            if i_found > -1:
                if len(s[i_found]) > 1:
                    s[i_found] = symbol
                    changed = True
                    solved.append(i_found)
                    s = propagate(s, [i_found])
                    if s is None:
                        return None
                    # if goal_test_dict(s):
                    #     return s

    # r = propagate(s, solved)

    return s


def prop_2(state):
    global sets, visited, neighbors, symbol_set

    if not state:
        return None

    if goal_test_dict(state):
        return state

    s = state.copy()

    solved = []

    for group in sets: # count the number of each possible symbols
        options = dict()
        for i in group:
            syms = s[i]
            al = [s[x] for x in group]
            if len(syms) != 1:
                if group == [3, 12, 21, 30, 39, 48, 57, 66, 75]:
                    a = 5
                for char in syms:
                    if char not in al:
                        if char not in options:
                            options[char] = 1
                        else:
                            options[char] = options[char] + 1

        singles = []
        for i, val in options.items():
            if val == 1:
                singles.append(i)

        for single in singles:
            for i in group:
                if single in s[i]:
                    x = s[i]
                    s[i] = single
                    solved.append(i)
                    r = propagate(s, [i])
                    if r is None:
                        return None
                    s = r
                    # break

    # s = propagate(s, solved)

    if not s:
        return None

    return s


def propagate_3(state):
    global sets, visited, neighbors, symbol_set

    if not state:
        return None

    if goal_test_dict(state):
        # print("D")
        return state

    solved = deque()

    s = state.copy()

    for group in sets:

        vals = [s[x] for x in list(group)]

        dups = [x for x in vals if vals.count(x) > 1]

        for d in dups:
            if dups.count(d) == len(d):
                for i in group:
                    if s[i] != d:
                        for char in d:
                            if char in s[i]:
                                s[i] = s[i].replace(char, "")
                                if len(s[i]) == 1:
                                    solved.append(i)

    s = propagate(s, solved)

    return s


def strintersect(a, b):
    out = ""
    for c in a:
        if c in b:
            out += c
        if len(out) > 2:
            return "-"

    return out


def csp_2(state):  # state is just the dict of available locations
    global visited, sol

    if not state:
        return None

    if goal_test_dict(state):
        return state

    var = -1

    visited += 1

    options = []

    for index, options in state.items():
        if len(options) > 1:
            var = index
            options = list(options)
            break

    if var == -1:
        return state

    for val in options:
        new_state = state.copy()
        new_state[var] = val

        result = csp_2(propagate_3(propagate_2(propagate(new_state, [var]))))

        if result is not None:
            return result

    return None


def solve_2(state):
    global sets, neighbors, visited, changed
    changed = True
    sets = constrained_sets(state)
    neighbors = make_neighbors(state)
    count = count_symbols(state)

    l = make_list(state[4])

    state = l

    solved = []

    start = time.perf_counter()

    for i, val in state.items():
        if len(val) == 1:
            solved.append(i)

    state = propagate(state, solved)

    while changed:
        state = propagate_2(state)

    solution = csp_2(state)

    end = time.perf_counter()

    # print(dict_to_string_initial(solution))

    # display_s_string(dict_to_string_initial(solution))

    print("%s\t%s\t%s\t%s" % (int(math.sqrt(len(state))), dict_to_string_initial(solution), round(end-start, 5), visited))

    return solution, round(end-start, 5)


def goal_test_dict(s_dict):
    for options in list(s_dict.values()):
        if len(options) != 1:
            return False
    return True


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
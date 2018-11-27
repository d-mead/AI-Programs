import sys
import time
import random
import math
import xlsxwriter
import datetime


def main():
    sys.setrecursionlimit(500000)
    global sets, neighbors, visited
    visited = 0
    # states = read_file("sudoku_puzzles_1.txt")
    # state = states[61]
    # solve(state)
    record()


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
        solve(state)
        end = time.perf_counter()
        worksheet.write(count, 0, str(count))
        worksheet.write(count, 1, round(end-start, 5))
        worksheet.write(count, 2, visited)
        # print(round(end - start, 5))
        # print(visited)
        visited = 0
        count += 1

    workbook.close()


def make_list(state):
    options = []
    for char in state:
        if char != ".":
            options.append(char)
        else:


def avalable(state, i):
    global neighbors
    neighs = []
    symbols = "123456789abcdefghijklmnopqrstuvwxyz"
    options = symbols[:math.sqrt(len(state))]
    char = state[i]
    for n in neighbors:
        if i in n:
            neighs.extend(list(n))
    for n in neighs:
        c = state[n]
        if c != ".":
            options.replace(c, "")

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


if __name__ == "__main__":
    # main func!
    main()
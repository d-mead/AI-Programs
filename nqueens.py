import sys
import time
from collections import deque
import math
from heapq import heappush, heappop
import random
import matplotlib.pyplot as plt
import datetime


def main():
    sys.setrecursionlimit(500000)

    global size, visited, very_visited, times, nodes, depths, fig, twos

    very_visited = 0
    visited = 0
    size = 8

    times = []
    nodes = []
    depths = []
    twos = []

    # print(make_state(9))
    # print(display(make_state(8)))
    # print(is_valid(rotate(make_state(9))))

    # for n in range(16, 17):
    #     size = n
    #     print(n)
    #     print(display(make_state(n)))
    #     print()

    try_one_3_2(12)

    # test_code()

    # s = time.perf_counter()
    # n = int(sys.argv[1])
    # max = int(sys.argv[2])
    #
    # # try_one_3(n)
    #
    # # plot()
    #
    # deeper_update_skip(n, max)
    #
    # print(twos)
    #
    # # update()
    #
    # # try_many_3(n, 120)
    #
    # e = time.perf_counter()
    #
    # # plot()
    # # plt.savefig(str(datetime.datetime.now()) + ".png")
    # # plt.show()
    # # print("yep")


def test_code():
    print(climb_3(make_state(int(sys.argv[1]))))
    solve_time = 0
    size = int(sys.argv[1])#8
    while solve_time < 2:
        start = time.perf_counter()
        state = climb_3(make_state(size))
        end = time.perf_counter()
        solve_time = end - start
        print("%s: %s" % (size, solve_time))
        size += 1
    print("For size %s, the time was %s" % (size-1, solve_time))


def plot():
    global times, nodes, depths, fig, host, par1, color1, color2
    fig = plt.figure(figsize=(13, 7))
    host = fig.add_subplot(111)

    plt.grid(True, alpha=.5)
    # plt.ion()

    par1 = host.twinx()

    # host.set_xlim(0, 2)
    # host.set_ylim(0, 2)
    # par1.set_ylim(0, 4)

    color1 = "red"
    color2 = "blue"

    # host.set_xlabel("Size")
    host.set_ylabel("Time")
    par1.set_ylabel("States Processed")

    # p2, = par1.plot(depths, nodes, color=color2, label="States", picker=5)
    p1, = host.plot(depths, times, color=color1, label="Time", picker=5)


    lns = [p1]#, p2]
    host.legend(handles=lns, loc='best')

    host.yaxis.label.set_color(p1.get_color())
    # par1.yaxis.label.set_color(p2.get_color())

    fig.canvas.mpl_connect('pick_event', onpick)

    plt.draw()
    plt.pause(.00001)


def update():
    global fig, depths, times, nodes, host, par1, color1, color2

    # par1.plot(depths, nodes, color=color2, label="States", picker=5, linewidth=.7)
    host.plot(depths, times, color=color1, label="Time", picker=5, linewidth=.7)


    plt.draw()
    plt.pause(.00001)


def onpick(event):
    global times, depths, nodes
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind[0]
    print("Size: %s\nTime: %s\nStates: %s\n" % (depths[ind], times[ind], nodes[ind]))


def try_many(min, max):
    global size, depths
    depths = range(min, max+1)
    for n in range(min, max+1):
        try_one(n)


def try_many_times(n, r):
    global visited, very_visited, size
    visited = 0
    size = n
    print(n)
    state = [-1] * n
    total_time = 0
    for n in range(0, r+1):
        # state = [-1] * n

        start = time.perf_counter()

        solution, depth = csp(state, 0)

        end = time.perf_counter()
        # print(solution)
        # print(display(solution))
        print("%s \t%s \t%s" % (round(end - start, 6), visited, is_valid(solution)))
        # print(visited)
        # print(is_valid(solution))
        # print(depth)
        very_visited += visited
        times.append(round(end - start, 5))
        total_time += round(end - start, 5)
        nodes.append(visited)
        visited = 0
    print(total_time/r)
    print()


def try_one(n):
    global size, visited, very_visited, times, nodes
    visited = 0
    print(n)
    start = time.perf_counter()
    size = n

    solution, depth = csp([-1]*n, 0)

    # print(solution)

    end = time.perf_counter()
    print(round(end - start, 5))
    # print(display(solution))
    print(visited)
    print(is_valid(solution))
    print(depth)
    very_visited += visited
    times.append(round(end - start, 5))
    nodes.append(visited)
    visited = 0
    print()


def try_one_new(n):
    global size
    global visited, very_visited, times, nodes
    visited = 0
    state = random_state(n)
    print(n)
    start = time.perf_counter()
    size = n

    solution = climb_2(state)

    end = time.perf_counter()
    print(solution)
    print(display(solution))
    print(round(end - start, 5))
    print(visited)
    print(is_valid(solution))
    very_visited += visited
    times.append(round(end - start, 5))
    nodes.append(visited)
    visited = 0
    print()


def try_one_3(n):
    global size
    global visited, very_visited, times, nodes, twos
    visited = 0
    state = make_state(n)#random_state(n)#[int(n/2)]*n#
    print(n, end = ": ")
    start = time.perf_counter()
    size = n

    solution = climb_3(state)

    end = time.perf_counter()
    # print(solution)

    print("%s \t%s \t%s" % (round(end - start, 6), visited, is_valid(solution)))

    very_visited += visited
    times.append(round(end - start, 5))
    if round(end - start, 5) > 2:
        twos.append(n)
    nodes.append(visited)
    visited = 0

    print()


def try_one_3_2(n):
    global size
    global visited, very_visited, times, nodes, twos
    visited = 0
    state = make_state(n)#random_state(n)#[int(n/2)]*n#
    print(n)
    start = time.perf_counter()
    size = n

    solution, h = csp_2(state, full_invalids(state))

    end = time.perf_counter()
    # print(solution)

    print(display(solution))

    print("%s \t%s \t%s" % (round(end - start, 6), visited, is_valid(solution)))

    very_visited += visited
    times.append(round(end - start, 5))
    if round(end - start, 5) > 2:
        twos.append(n)
    nodes.append(visited)
    visited = 0

    print()


def deeper_update(min, max):
    global size, depths
    # depths = range(min, max + 1)
    for n in range(min, max + 1):
        try_one_3(n)
        depths.append(n)
        update()
        # if n > min + 5:
     #     update()


def deeper_update_skip(min, max):
    global size, depths
    # depths = range(min, max + 1)
    for n in range(min, max + 1):
        if n % 6 == 5 or n % 6 == 1:
            try_one_3(n)
            # depths.append(n)
            # update()
        # if n > min + 5:
        #     update()


def deeper(min, max):
    global size, depths
    depths = range(min, max + 1)
    for n in range(min, max + 1):
        try_one_3(n)


def csp(state, depth):
    global visited

    if goal_test(state):
        return state, depth

    var = get_next_unassigned_var(state, depth)

    visited += 1

    for val in get_sorted_values(state, var, depth):
        new_state = state[:]
        new_state[var] = val
        result = csp(new_state, depth+1)
        if result is not None:
            return result

    return None


def get_sorted_values(state, var, depth):
    if var is None:
        return set()
    global size
    safe = []

    for col in range(0, size):
        if is_valid_move(state, var, col):
            # safe.append(col)
            safe.append((col, rating(state, var, col, depth)))
            # heappush(safe, (1/(rating(state, var, col, depth)+1), col))
            # safe.append((col, random.randint(0, 100)))

    safe.sort(key=lambda x: x[1], reverse=False)

    # return safe

    return [i[0] for i in safe]

    # return safe.sort(key=lambda x: x.count, reverse=True)


def rating(state, var, col, depth):
    count = invalids(state, var, col)
    return count #random.random()


def is_valid_move(state, i, val):
    # coords = set()
    # for row, col in enumerate(state):
    #     coords.add((row, col))

    # if (i, val) in coords:
    #     return False

    for row, col in enumerate(state):
        if row != i and col != -1:
            if col == val:
                return False

            if abs(i - row) == abs(val - col):
                return False

    return True


def invalids(state, i, val):
    count = 0
    for row, col in enumerate(state):
        if row != i and col != -1:
            if col == val:
                count += 1
            elif abs(i - row) == abs(val - col):
                count += 1
    return count


def full_invalids(state):
    count = 0
    for x, y in enumerate(state):
        for row, col in enumerate(state):
            if row != x and col != -1:
                if col == y:
                    count += 1
                # if type(x) == list or type(row) == list or type(y) == list or type(col) == list:
                #     a = 5
                if abs(x - row) == abs(y - col):
                    count += 1
    return count/2


def full_invalids_max(state, max):
    count = 0
    for x, y in enumerate(state):
        for row, col in enumerate(state):
            if row != x and col != -1:
                if col == y:
                    count += 1
                # if type(x) == list or type(row) == list or type(y) == list or type(col) == list:
                #     a = 5
                if abs(x - row) == abs(y - col):
                    count += 1
            if count >= max:
                if max != 0:
                    return -1
    return count


def is_valid(state):
    # coords = set()
    #
    # for row, col in enumerate(state):
    #     coords.add((row, col))

    for i, val in enumerate(state):
        for row, col in enumerate(state):
            if row != i and col != -1:
                if abs(i - row) == abs(val - col):
                    return False
                if col == val:
                    return False

    return True


def get_next_unassigned_var(state, depth):
    vars = []
    for var in range(0, size):
        if state[var] == -1:
            # return var
            # r = get_next_rating(state, var)
            # if r < m:
            #     m = r
            #     max_v = var
            vars.append((var, get_next_rating(state, var, depth)))
    return sorted(vars, key=lambda x: x[1], reverse=False)[0][0]


def get_next_rating(state, var, depth):
    return 1/(count_valid_vals(state, var)+1)#count_valids_in_row(state, var)#*random.randint(depth, size)


def count_valid_vals(state, var):
    count = 0
    for col in range(0, size):
        if is_valid_move(state, var, col):
            count += 1

    return count


def count_invalids_in_row(state, var):
    count = 0

    col = state[var]

    # coords = set()
    # for row, col in enumerate(state):
    #     coords.add((row, col))

    for i, val in enumerate(state):
        if i != i and val != -1:
            if abs(i - var) == abs(val - col):
                count += 1

            if col == val:
                count += 1

    return count


def count_valids_in_row(state, var):
    count = 0
    for col in range(0, size):
        if is_valid_move(state, var, col):
            count += 1
    return count


def do_thang(state):
    global visited, tried
    tried = set()

    peak = full_invalids(state)

    max = len(state)*5

    for x in range(0, max):
    # while not is_valid(state):
        if is_valid(state):
            # print("yep")
            # print(state)
            break
        visited += 1
        print(visited)
        var = next_var(state)
        # new_state = state[:]

        # h, n = get_next_val(state, var)

        state[var] = get_next_val(state, var)
        # s = "".join(str(x) for x in new_state)
        # if s not in tried:
        # state = new_state
        #     tried.add(s)
    if visited > max-2:
        print(visited)
        visited = 0
        return do_thang(random.sample(state, len(state)))

    return state

    # return None


def next_var(state):
    # vars = []
    # for var in range(0, size):
    #     vars.append((var, get_next_val(state, var)))
    # return sorted(vars, key=lambda x: x[1], reverse=False)[0][0]

    var = random.randint(0, size-1)
    return var


def get_next_val(state, var):
    vars = []
    for col in range(0, size):
        vars.append((col, score_invalidity(state, var, col))) #math.sqrt(random.random()+10)*
    return sorted(vars, key=lambda x: x[1], reverse=False)[0][0]


def next_vals(state, var):
    vars = []
    for col in range(0, size):
        vars.append((col, score_invalidity(state, var, col)))
    vars.sort(key=lambda x: x[1], reverse=False)
    return [i[0] for i in vars]


def random_state(n):
    state = []
    for x in range(0, n):
        state.append(x)
    random.shuffle(state)
    return state


def score_invalidity(state, i, val):
    # coords = set()
    # for row, col in enumerate(state):
    #     coords.add((row, col))

    count = 0

    for row, col in enumerate(state):
        if row != i and col != -1:
            if abs(i - row) == abs(val - col):
                count += 1

            elif col == val:
                count += 1

    return count


def climb(state):
    global visited
    peak = full_invalids(state)
    for x in range(10000000):
        # state, h = climb(state)
        # if h == 0:
        #     break
        visited += 1
        n, h = climb_step(state)
        if h == 0:
            break
        if h < peak:
            peak = h
            state = n
            print(h)
        # else:
        #     break
    return state


def climb_step(state):
    next_move, h = climb_next_var(state)

    if next_move:
        state[next_move[0]] = next_move[1]

    return state, h


def climb_next_var(state):
    moves = dict()

    now = full_invalids(state)

    for col in range(len(state)):
        for row in range(len(state)):
            if state[row] == col:
                # We don't need to evaluate the current
                # position, we already know the h-value
                continue

            state_copy = list(state)
            # Move the queen to the new row
            state_copy[col] = row
            if now < 3:
                m = full_invalids_max(state_copy, 3)
                if m != -1:
                    moves[(col, row)] = m
                    now = m
            #     if is_valid(state):
            #         print("yurp")
            #         a = 5
            else:
                m = full_invalids_max(state_copy, now)
                if m != -1:
                    moves[(col, row)] = m
                    now = m

    # moves = sorted(moves, key=lambda x: x[1], reverse=False)
    # top = [0][0]
    # best_moves = []
    # last = top
    # count = 1
    # for h, c in enumerate(moves):
    # # while moves[count] >= top:
    #     if h == top:
    #         best_moves.append(c)

    bests = []
    top_s = 0
    top = full_invalids(state)
    for k, v in moves.items():
        if v < top:
            top = v
            top_s = k

    for k, v in moves.items():
        if v == top:
            bests.append(k)

    # if len(bests) == 0:
    #     return None, top

    return bests[random.randint(0, len(bests)-1)], top


def climb_2(state):
    top = full_invalids(state)
    h = top
    global visited
    while not is_valid(state):#sh > -10:
        next_state, h = next_move(state, top)
        if h < top:
            state[next_state[0]] = next_state[1]
            top = h#full_invalids(state)
            # print(h)# print(top)
        # else:
        #     a=5
        visited += 1

        # if visited > len(state)*5:
        #     break
    # if visited > len(state)*5-1:
    #     visited = 0
    #     return climb_2(random.sample(state, len(state)))

    return state


def next_move(state, h):
    row = random.randint(0, size-1)
    c = causes(state, row, state[row])
    moves = dict()
    min = h
    for col in range(0, size):
        nh = h-(c-causes(state, row, col))
        if nh < min:
            moves[(row, col)] = nh
            # min = nh

    bests = []
    for s, ch in moves.items():
        if ch == min:
            bests.append(s)
    if len(bests) == 0:
        return -1, min
    return bests[random.randint(0, len(bests)-1)], min


def causes(state, row, col):
    count = 0
    count += state.count(col)
    if state[row] == col:
        count += -1
    for var, val in enumerate(state):
        if abs(row-var) == abs(val-col):
            if row != var:
                count += 1
    return count


def csp_2(state, h):
    global visited

    if h < 1:
        return state, h

    var = next_row(state)

    visited += 1

    for nh, val in min_conflicts_list(state, var, h):
        new_state = state[:]
        new_state[var] = val
        result = csp_2(new_state, nh)
        if result is not None:
            return result

    return None


def climb_3(state):
    global size, visited
    size = len(state)
    count = 0
    current = state#full_invalids(state)
    best = full_invalids(current)+random.random()
    max = 10000000000
    for i in range(0, max):
        if best < 1:
            return current
        var = next_row(current)#random.randint(0, size-1)
        visited += 1
        value, h = min_conflicts(current, var, best)
        if int(h) < best:
            best = h
            current[var] = value
            # print(best)
        # else:
        #     return climb_3(state)

        if visited > size*5:#math.sqrt(size):
            # print("r: %s, %s" % (best, visited))
            visited = 0
            return climb_3(random_state(len(state)))
    return -1


def min_conflicts(state, var, h):
    global size
    var_h = conflicts(state, var, state[var])
    best_h = int(h)-(var_h-conflicts(state, var, 0))+random.random()
    best_val = 0
    # best_hs = deque()
    # best_vals = deque()
    # best_hs.append(int(h)-(var_h-conflicts(state, var, 0))+random.random())
    # best_vals.append(0)

    # best_h_2 = int(h)-(var_h-conflicts(state, var, 0))+random.random()
    # best_val_2 = 0
    # best_h_3 = int(h) - (var_h - conflicts(state, var, 0)) + random.random()
    # best_val_3 = 0

    for col in range(1, size):
        nh = int(h)-(var_h - conflicts(state, var, col))+random.random()
        #nh += random.random()*(1/(nh+1))
        if nh < best_h:
            best_h = nh
            best_val = col

    return best_val, best_h


def min_conflicts_list(state, var, h):
    global size
    var_h = conflicts(state, var, state[var])
    moves = []
    # best_h = int(h) - (var_h - conflicts(state, var, 0)) + random.random()
    # best_val = 0

    for col in range(0, size):
        nh = int(h) - (var_h - conflicts(state, var, col)) + random.random()
        moves.append((nh, col))
        # nh += random.random()*(1/(nh+1))
        # if nh < best_h:
        #     best_h = nh
        #     best_val = col

    return sorted(moves, key=lambda x: x[0], reverse=False)


def conflicts(state, var, val):
    count = 0
    for row, col in enumerate(state):
        if row != var:
            if col == val:
                count += 1
            elif abs(var-row) == abs(val-col):
                count += 1
    return count


def next_row(state):
    global size
    max_c = 0
    max_var = 0
    for var in range(0, size):
        c = conflicts(state, var, state[var])+random.random()
        # c += random.random()*c#math.pow(c, 2)
        if c > max_c:
            max_c = c
            max_var = var

    return max_var


def make_state(n):
    state = []
    if n % 2 == 0:
        for col in range(0, int(n/2)):
            state.append(2*col)
        for col in range(0, int(n/2)):
            state.append(2*col+1)

    else:
        for col in range(0, int(n/2)+1):
            state.append(2*col)
        for col in range(0, int(n/2)):
            state.append(2*col+1)
        # return rotate(state)
    return state


def goal_test(state):
    for row in state:
        if row == -1:
            return False
    # if -1 in state:
    #     return False
    return True


def rotate(state):
    new_state = [-1]*len(state)
    for row, col in enumerate(state):
        new_state[col] = row
    return new_state


def display(state):
    board = ""
    for row in range(0, size):
        for col in range(0, size):
            if state[row] == col:
                board += "x "
            else:
                board += "· "
        board += "\n"
    return board[:len(board)-1]


if __name__ == "__main__":
    # main func!
    main()
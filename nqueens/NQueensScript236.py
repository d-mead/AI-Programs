import sys
import time
# from collections import deque
# import math
# from heapq import heappush, heappop
import random

import networkx as nx
import matplotlib.pyplot as plt2


def main():
    sys.setrecursionlimit(500000)

    global size, visited, very_visited, times, nodes, depths, fig, twos
    very_visited = 0
    visited = 0
    size = 0
    times = []
    nodes = []
    depths = []

    # test_code()

    # live_graph()

    visualize()

    # table()


def table():
    import xlsxwriter
    import datetime
    global size, visited

    workbook = xlsxwriter.Workbook(str(datetime.datetime.now()) + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "size")
    worksheet.write(0, 1, "visited")
    worksheet.write(0, 2, "runtime")
    count = 1

    for n in range(10, 201, 1):
        size = n

        state = make_state(n)
        # state = random_state(n)
        # state = [-1]*n

        start = time.perf_counter()

        # solution, d = csp(state, 0)
        solution, h = csp_2(state, full_invalids(state))

        end = time.perf_counter()
        runtime = round(end-start, 5)
        print(n, visited, runtime)  # , solution)

        worksheet.write(count, 0, n)
        worksheet.write(count, 1, visited)
        worksheet.write(count, 2, runtime)
        # worksheet.write(count, 3, h)

        count += 1

        visited = 0
        # worksheet.write(2, count, h)

    workbook.close()


def live_graph():
    import matplotlib.pyplot as plt
    plot()

    start = 10
    end = 100
    skip = 2

    # a: backtracking
    # b: csp random start state
    # c: csp winning start state
    type = "c"

    deeper_update(start, end, skip, type)  # (starting board size, ending board size)

    plot()
    plt.show()


def test_code():
    global size

    size = int(sys.argv[1])

    s = make_state(size)

    print(csp_2(s, full_invalids(s))[0])

    solve_time = 0
    size = 8
    while solve_time < 2:
        start = time.perf_counter()
        # s = make_state(size)                  # for a csp that doesn't solve immedietly, use the next line
        s = random_state(size)
        state, h = csp_2(s, full_invalids(s))
        end = time.perf_counter()
        solve_time = end - start
        print("%s: %s" % (size, solve_time))
        size += 1
    print("For size %s, the time was %s" % (size-1, solve_time))


def plot():
    global times, nodes, depths, fig, host, par1, color1, color2
    fig = plt2.figure(figsize=(13, 7))
    host = fig.add_subplot(111)

    plt2.grid(True, alpha=.5)
    # plt.ion()

    par1 = host.twinx()

    # host.set_xlim(0, 2)
    # host.set_ylim(0, 2)
    # par1.set_ylim(0, 4)

    color1 = "red"
    color2 = "blue"

    host.set_xlabel("Size")
    host.set_ylabel("Time")
    par1.set_ylabel("States Processed")

    p2, = par1.plot(depths, nodes, color=color2, label="States", picker=5, alpha = .5)
    p1, = host.plot(depths, times, color=color1, label="Time", picker=5)


    lns = [p1, p2]
    host.legend(handles=lns, loc='best')

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())

    fig.canvas.mpl_connect('pick_event', onpick)

    plt2.draw()
    plt2.pause(.00001)


def update():
    global fig, depths, times, nodes, host, par1, color1, color2

    par1.plot(depths, nodes, color=color2, label="States", picker=5, linewidth=.7, alpha = .5)
    host.plot(depths, times, color=color1, label="Time", picker=5)


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

    end = time.perf_counter()
    # print(display(solution))
    print("%s \t%s \t%s" % (round(end - start, 6), visited, is_valid(solution)))
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

    # print(display(solution))

    print("%s \t%s \t%s" % (round(end - start, 6), visited, is_valid(solution)))

    very_visited += visited
    times.append(round(end - start, 5))
    if round(end - start, 5) > 2:
        twos.append(n)
    nodes.append(visited)
    visited = 0

    print()


def try_one_3_2_r(n):
    global size
    global visited, very_visited, times, nodes, twos
    visited = 0
    state = random_state(n)#[int(n/2)]*n#make_state(n)#
    print(n)
    start = time.perf_counter()
    size = n

    solution, h = csp_2(state, full_invalids(state))

    end = time.perf_counter()
    # print(solution)

    # print(display(solution))

    print("%s \t%s \t%s" % (round(end - start, 6), visited, is_valid(solution)))

    very_visited += visited
    times.append(round(end - start, 5))
    if round(end - start, 5) > 2:
        twos.append(n)
    nodes.append(visited)
    visited = 0

    print()


def deeper_update(min, max, skip, type):
    global size, depths
    # depths = range(min, max + 1)
    if type == "a":
        for n in range(min, max + 1, skip):
            try_one(n)
            depths.append(n)
            update()

    elif type == "b":
        for n in range(min, max + 1, skip):
            try_one_3_2_r(n)
            depths.append(n)
            update()

    else:
        for n in range(min, max + 1, skip):
            try_one_3_2(n)
            depths.append(n)
            update()


def deeper_update_skip(min, max):
    global size, depths
    # depths = range(min, max + 1)
    for n in range(min, max + 1):
        if n % 6 == 5 or n % 6 == 1:
            try_one_3(n)


def deeper(min, max):
    global size, depths
    depths = range(min, max + 1)
    for n in range(min, max + 1):
        try_one_3_2(n)


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
    # count = invalids(state, var, col)
    return random.random()#count#


def is_valid_move(state, i, val):

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
            # return var
            # r = get_next_rating(state, var)
            # if r < m:
            #     m = r
            #     max_v = var
            vars.append((var, get_next_rating(state, var, depth)))
    return sorted(vars, key=lambda x: x[1], reverse=False)[0][0]


def get_next_rating(state, var, depth):
    return (count_valid_vals(state, var))#count_valids_in_row(state, var)#*random.randint(depth, size)random.random()#


def csp_2(state, h):
    global visited

    if h < 1:
        return state, h

    var = next_row(state)#random.randint(0, size-1)#

    visited += 1

    for nh, val in min_conflicts_list(state, var, h):
        new_state = state[:]
        new_state[var] = val
        # print(nh)
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

    for col in range(1, size):
        nh = int(h)-(var_h - conflicts(state, var, col))+random.random()
        if nh < best_h:
            best_h = nh
            best_val = col

    return best_val, best_h


def min_conflicts_list(state, var, h):
    global size
    var_h = conflicts(state, var, state[var])
    moves = []

    for col in range(0, size):
        nh = int(h) - (var_h - conflicts(state, var, col)) + random.random()
        moves.append((nh, col))

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
        if c > max_c:
            max_c = c
            max_var = var

    return max_var


def make_state(n):
    state = []
    if n % 6 != 2 and n % 6 != 3:
        evens = []
        odds = []
        for col in range(0, int(n / 2)):
            evens.append(2 * (col + 1))
            odds.append(2 * col + 1)
        if n % 2 == 1:
            odds.append(n)
        for even in evens:
            state.append(even-1)
        for odd in odds:
            state.append(odd-1)
    elif n % 6 == 3:
        evens = []
        odds = []
        for col in range(0, int(n / 2)):
            evens.append(2 * (col + 1))
            odds.append(2 * col + 1)
        evens.remove(2)
        evens.append(2)

        odds.remove(1)
        odds.remove(3)
        odds.append(n)
        odds.append(1)
        odds.append(3)
        for even in evens:
            state.append(even - 1)
        for odd in odds:
            state.append(odd - 1)
    else: # (n % 6 == 2)
        evens = []
        odds = []
        for col in range(0, int(n / 2)):
            evens.append(2 * (col + 1))
            odds.append(2 * col + 1)
        if n % 2 == 1:
            odds.append(n)

        odds.remove(3)
        odds.insert(0, 3)
        odds.remove(5)
        odds.append(5)

        for even in evens:
            state.append(even - 1)
        for odd in odds:
            state.append(odd - 1)

    return state


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


def graph_csp_2(state, h):
    global g
    global visited

    if h < 1:
        return state, h

    var = next_row(state)#random.randint(0, size-1)#

    visited += 1

    for nh, val in min_conflicts_list(state, var, h):
        new_state = state[:]
        new_state[var] = val
        # print(nh)
        g.add_edge(str(state), str(new_state))
        result = graph_csp_2(new_state, nh)
        if result is not None:
            return result

    return None


def graph_csp(state, depth):
    global g
    global visited

    if goal_test(state):
        return state, depth

    var = get_next_unassigned_var(state, depth)#random.randint(0, size-1)#

    visited += 1

    for val in get_sorted_values(state, var, depth):
        new_state = state[:]
        new_state[var] = val
        g.add_edge(str(state), str(new_state))
        result = graph_csp(new_state, depth + 1)
        if result is not None:
            return result

    return None


def visualize():
    global g, size, start, visited
    g = nx.Graph()
    filename = "16puzzle.txt"
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    length = 6

    size = 50

    # state = lines[length+1].split(" ")[0].replace("\n", "")

    plt2.figure().suptitle("N Queens Algorithm Network for n = " + str(size))

    state = [-1]*size#random_state(size)#make_state(size)#

    start = str(state)

    visited += 1
    g.add_node(str(state))

    # sol, h = graph_csp(state, 0)
    sol, h = graph_csp(state, full_invalids(state))
    print(sol)
    print(is_valid(sol))
    print(visited)
    draw_graph(g, 111, str(sol), "Backtracking (optimized)\n" + str(visited) + " nodes")

    # g, l = bfs_visualize(state)
    # draw_graph(g, l, 111, state, "BFS")

    plt2.show()


def draw_graph(g, subplot, state, title):
    from colour import Color
    global start
    edge_l = []
    color_list = ["#d2d2d2"] * len(g.edges())

    plt2.subplot(subplot)

    plt2.title(title, loc='center', size='medium', pad=-5)

    red = Color("lightgrey")

    colors = list(red.range_to(Color("black"), len(g.edges())))

    # print(str(colors[10]))

    for x in range(0, len(g.edges())):
        if str(colors[x])[0] == '#':
            # print(str(colors[x]))
            if len(str(colors[x])) >= 4:
                # print(str(str(colors[x])+str(colors[x])[1:]))
                color_list[x] = (str(colors[x]) + str(colors[x])[1:])[:5] + "FF"
            else:
                # print(str(colors[x]))
                color_list[x] = str(colors[x])[:5] + "FF"

    count = 0

    # nx.draw(g, pos=None, ax=None, with_labels=True)

    # end = str([-1]*size)

    # nx.draw_kamada_kawai(g, with_labels=False, font_size=7, node_color='blue', node_size=5, edge_color=color_list,
    #                      width=1.5, font_weight="bold", font_color="black")
    nx.draw_kamada_kawai(g, with_labels=True, labels={state: "solution", start: "start"}, font_size=7, node_color='blue', node_size=3, edge_color=color_list,
                         width=1.5, font_weight="bold", font_color="black")

    # nx.draw_kamada_kawai(g, with_labels=False, font_size=7, node_color='blue', node_size=5, edge_color=color_list, width=1.5, font_weight="bold", font_color="black")


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
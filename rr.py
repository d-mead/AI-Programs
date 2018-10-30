from math import pi , acos , sin , cos
from collections import deque
import time
import sys
from heapq import heappush, heappop
from tkinter import *
import pickle
# import pickle
from PIL import ImageTk
import matplotlib.pyplot as plt
import csv
import numpy as npbre
from mpl_toolkits.
from mpl_toolkits.basemap import Basemap
import random
import keyboard


def main():
    global edges, nodes, names
    edges, nodes = make_edges_dict("rrNodes.txt", "rrEdges.txt")
    names = make_names_dict("rrNodeCity.txt")

    # with open("edges_236.pkl", "wb") as outfile:
    #     pickle.dump(edges, outfile)
    # with open("nodes_236.pkl", "wb") as outfile:
    #     pickle.dump(nodes, outfile)
    # with open("names_236.pkl", "wb") as outfile:
    #     pickle.dump(names, outfile)
    #
    # with open("edges_236.pkl", "rb") as infile:
    #     edges = pickle.load(infile)
    # with open("nodes_236.pkl", "rb") as infile:
    #     nodes = pickle.load(infile)
    # with open("names_236.pkl", "rb") as infile:
    #     names = pickle.load(infile)

    start = sys.argv[1]
    end = sys.argv[2]

    start_id = names[start]
    end_id = names[end]



    # begin = time.perf_counter()
    # dij = dijkstra(start_id, end_id)
    # stop = time.perf_counter()
    # print("Dijkstra: \t%s \t%s seconds" % (dij, round(stop - begin, 5)))
    #
    #
    # begin = time.perf_counter()
    # a = a_star(start_id, end_id)
    # stop = time.perf_counter()
    # print("A-Star: \t%s \t%s seconds" % (a, round(stop - begin, 5)))
    #
    # draw()

    utm_nodes = dict()

    # for node, loc in nodes.items():
    #     utm_nodes[node] = utm.from_latlon(loc[0][0], loc[0][1])[0:2]

    global minx, maxx, miny, maxy, scalew, scaleh, height, width, shift
    minx = 500
    maxx = -500
    miny = 500
    maxy = -500
    scalew = 10.0
    scaleh = 10.0
    shift = 0

    for node, loc in nodes.items():
        if loc[0][0]<miny:
            miny = loc[0][0]

        if loc[0][0]>maxy:
            maxy = loc[0][0]

        if loc[0][1]<minx:
            minx = loc[0][1]

        if loc[0][1]>maxx:
            maxx = loc[0][1]

    height = abs(maxx-minx)
    width = abs(maxy)-abs(miny)

    scalew = 814/width# 12
    scaleh = 921/height# 10

    # start = "Chicago"
    # start_id = names[start]

    #print(answer)

    draw(full_send(names["Chicago"]), start_id, end_id)


def draw_2(lines, red_lines, all_lines):
    global minx, maxx, miny, maxy, scalew, scaleh, height, width
    master = Tk()

    for line in lines:
        w.create_line(line, fill="dimgrey")

    for line in all_lines:
        w.create_line(line, fill='mediumblue', width=1)

    for line in red_lines:
        w.create_line(line, fill='red', width=2)

    m = Basemap(projection='merc', llcrnrlat=float(min(lat_td)) - 2, \
                urcrnrlat=float(max(lat_lift)) + 2, llcrnrlon=float(max(long_td)) - 2, \
                urcrnrlon=float(min(long_lift)) + 2, lat_ts=40, resolution='l')

    lat_ = []
    lon = []

    x, y = m(lon, lat)

    # dark grey : 4E4E4E
    # naxy blue : 00137B
    # red       : BB0000

    m.plot(x, y, '-', markersize=5, linewidth=1, color=blue)

    m.drawcoastlines()
    m.fillcontinents(color='white')
    m.drawmapboundary(fill_color='white')
    m.drawstates(color='black')
    m.drawcountries(color='black')
    plt.title("#wedgez")
    plt.show()

    mainloop()


def draw(lines, start_id, end_id):
    global minx, maxx, miny, maxy, scalew, scaleh, height, width
    master = Tk()

    w = Canvas(master, width=height*scaleh, height=width*scalew)
    w.pack()

    # image = ImageTk.PhotoImage(file="rrImage.png")
    # w.create_image(0, 0, image=image, anchor=NW)
    # print(image.height())


    # for line in lines[::100]:
    #     print(line)
    global last_time
    last_time = time.perf_counter()

    global delay
    delay = 0

    # keyboard.add_hotkey('A', lambda: up())
    # keyboard.add_hotkey('S', lambda: down())

    global lines_dict
    lines_dict = dict()

    for line in lines:
        lines_dict[line] = w.create_line(line, fill="dimgrey")
        lines_dict[(line[2], line[3], line[0], line[1])] = w.create_line(line, fill="dimgrey")

    answer = a_star_tk(start_id, end_id, w, .7)
    #answer = dijkstra_tk(start_id, end_id, w)

    distance = answer[0]
    red_lines = answer[1]
    all_lines = answer[2]

    # for line in all_lines:
    #     w.itemconfig(lines_dict[line], fill="mediumblue")
    #     # w.create_line(line, fill='mediumblue', width=1)

    for line in red_lines:
        # w.itemconfig(lines_dict[line], fill="red")
        w.create_line(line, fill='red', width=2)
        # w.update()

    w.create_text(700, 100, fill = 'black', width = 100, text = ("%s miles" % (round(distance, 2))), anchor = "nw")

    mainloop()

def up():
    global delay
    delay = delay / 2
    print(delay)

def down():
    global delay
    delay = delay * 2
    print(delay)


def full_send(start):
    global minx, maxx, miny, maxy, scaleh, scalew

    lines = []

    fringe = [(0, 0, start, nodes[start][0], 0), ]
    visited = set()

    while len(fringe) is not 0:
        s = heappop(fringe)

        if s[2] in visited:
            continue

        visited.add(s[2])

        children = get_children(s[2])
        for child in children:
            if child[1] not in visited:
                heappush(fringe, (0, child[0], child[1], child[2], s[4] + child[0]))
                sy = (-abs((float(s[3][1]))+maxy)+height)*scaleh-2
                sx = abs((float(s[3][0]))+maxx)*scalew+8
                ey = (-abs(float(child[2][1])+maxy)+height)*scaleh-2
                ex = abs((float(child[2][0]))+maxx)*scalew+8
                lines.append((sy, sx, ey, ex))
                #w.create_line((abs(float(s[3][1])) - 70) * 20, (abs(float(s[3][0])) - 30) * 20, (abs(float(child[2][1])) - 70) * 20, (abs(float(child[2][0])) - 30) * 20)

    if len(fringe) is 0:
        return lines


def redraw(w):
    global last_time
    if time.perf_counter() - last_time > delay:
        last_time = time.perf_counter()
        w.update()


def a_star_tk(start, end, w, m):

    fringe = [(0, 0, start, nodes[start][0],  0, []), ]
    visited = set()
    all_lines = set()

    end_y = nodes[end][0][0]
    end_x = nodes[end][0][1]

    while len(fringe) is not 0:
        s = heappop(fringe)

        if len(s) > 6:

            sy = (-abs((float(s[3][1])) + maxy) + height) * scaleh - 2
            sx = abs((float(s[3][0])) + maxx) * scalew + 8
            ey = (-abs(float(s[6][1]) + maxy) + height) * scaleh - 2
            ex = abs((float(s[6][0])) + maxx) * scalew + 8

            w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="navyblue", width=2)

        if goal_test(s[2], end):  # if the state is won
            return s[0]/m, s[5], all_lines  # return the moves

        if s[2] in visited:
            continue

        visited.add(s[2])

        children = get_children(s[2])
        for child in children:
            if child[1] not in visited:
                try:
                    circle = calcd(child[2][0], child[2][1], end_y, end_x)
                except ValueError:
                    circle = 0
                red_lines = list(s[5])
                sy = (-abs((float(s[3][1])) + maxy) + height) * scaleh -2
                sx = abs((float(s[3][0])) + maxx) * scalew + 8
                ey = (-abs(float(child[2][1]) + maxy) + height) * scaleh -2
                ex = abs((float(child[2][0])) + maxx) * scalew + 8
                red_lines.append((sy, sx, ey, ex))
                all_lines.add((sy, sx, ey, ex))
                # w.create_line((sy, sx, ey, ex), fill="mediumblue", width = 2)
                w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="royalblue", width=2)
                heappush(fringe, (circle+(s[4]+child[0])*m, child[0], child[1], child[2], s[4]+child[0], red_lines, s[3]))
        redraw(w)
        # if random.randint(0, 1000) > 999:
        #     w.update()
        #         # print(abs(float(s[3][1]))-70, abs(float(s[3][0]))-30, abs(float(child[2][1]))-70, abs(float(child[2][0]))-30)
                # w.create_line((abs(float(s[3][1]))-70)*20, (abs(float(s[3][0]))-30)*20, (abs(float(child[2][1]))-70)*20, (abs(float(child[2][0]))-30)*20)

    if len(fringe) is 0:
        return -1


def dijkstra_tk(start, end, w):
    fringe = [(0, start, 0, nodes[start][0], []), ]
    visited = set()
    all_lines = set()

    while len(fringe) is not 0:
        s = heappop(fringe)

        if goal_test(s[1], end):  # if the state is won
            return s[0], s[4], all_lines  # return the moves

        if s[1] in visited:
            continue

        visited.add(s[1])

        children = get_children(s[1])
        for child in children:
            if child[1] not in visited:
                red_lines = list(s[4])
                sy = (-abs((float(s[3][1])) + maxy) + height) * scaleh - 2
                sx = abs((float(s[3][0])) + maxx) * scalew + 8
                ey = (-abs(float(child[2][1]) + maxy) + height) * scaleh - 2
                ex = abs((float(child[2][0])) + maxx) * scalew + 8
                red_lines.append((sy, sx, ey, ex))
                all_lines.add((sy, sx, ey, ex))
                w.create_line((sy, sx, ey, ex), fill="mediumblue", width=2)
                heappush(fringe, (s[2] + child[0], child[1], s[2] + child[0], child[2], red_lines))
        if random.randint(0, 1000) > 999:
            w.update()

    if len(fringe) is 0:
        return -1


def a_star(start, end):

    fringe = [(0, 0, start, nodes[start][0],  0, []), ]
    visited = set()
    all_lines = set()

    end_y = nodes[end][0][0]
    end_x = nodes[end][0][1]

    while len(fringe) is not 0:
        s = heappop(fringe)

        if goal_test(s[2], end):  # if the state is won
            return s[0], s[5], all_lines  # return the moves

        if s[2] in visited:
            continue

        visited.add(s[2])

        children = get_children(s[2])
        for child in children:
            if child[1] not in visited:
                try:
                    circle = calcd(child[2][0], child[2][1], end_y, end_x)
                except ValueError:
                    circle = 0
                red_lines = list(s[5])
                sy = (-abs((float(s[3][1])) + maxy) + height) * scaleh -2
                sx = abs((float(s[3][0])) + maxx) * scalew + 8
                ey = (-abs(float(child[2][1]) + maxy) + height) * scaleh -2
                ex = abs((float(child[2][0])) + maxx) * scalew + 8
                red_lines.append((sy, sx, ey, ex))
                all_lines.add((sy, sx, ey, ex))
                heappush(fringe, (circle+s[4]+child[0], child[0], child[1], child[2], s[4]+child[0], red_lines))
                # print(abs(float(s[3][1]))-70, abs(float(s[3][0]))-30, abs(float(child[2][1]))-70, abs(float(child[2][0]))-30)
                # w.create_line((abs(float(s[3][1]))-70)*20, (abs(float(s[3][0]))-30)*20, (abs(float(child[2][1]))-70)*20, (abs(float(child[2][0]))-30)*20)

    if len(fringe) is 0:
        return -1



def dijkstra(start, end):
    fringe = [(0, start, 0), ]
    visited = set()

    while len(fringe) is not 0:
        s = heappop(fringe)

        if goal_test(s[1], end):  # if the state is won
            return s[2]  # return the moves

        if s[1] in visited:
            continue

        visited.add(s[1])

        children = get_children(s[1])
        for child in children:
            if child[1] not in visited:
                heappush(fringe, (s[2]+child[0], child[1], s[2]+child[0]))

    if len(fringe) is 0:
        return -1


def get_children(location):
    return edges[location]


def find_longest():
    do = True
    for start, ids in names.items():
        for end, ide in names.items():
            if start == "Brooklyn":
                do = False
            if do:
                print("%s, %s: %s" % (start, end, a_star(ids, ide)))


def make_edges_dict(nodes_name, edges_name):
    nodes = {}
    node_file = open(nodes_name, "r")
    lines = [line.rstrip().split(" ") for line in node_file.readlines()]
    for line in lines:
        nodes[line[0]] = [(float(line[1]), float(line[2]))]

    edges = {}
    edges_file = open(edges_name, "r")
    lines = [line.rstrip().split(" ") for line in edges_file.readlines()]
    for line in lines:
        dist = calcd(nodes[line[0]][0][0], nodes[line[0]][0][1], nodes[line[1]][0][0], nodes[line[1]][0][1])
        if line[0] in edges.keys():
            edges.get(line[0]).append((dist, line[1], nodes[line[1]][0]))
        else:
            edges[line[0]] = [(dist, line[1], nodes[line[1]][0])]
        if line[1] in edges.keys():
            edges.get(line[1]).append((dist, line[0], nodes[line[0]][0]))
        else:
            edges[line[1]] = [(dist, line[0], nodes[line[0]][0])]
    for node in nodes.keys():
        if node not in edges.keys():
            edges[node] = []

    return edges, nodes


def make_names_dict(filename):
    names = {}
    name_file = open(filename, "r")
    lines = [line.rstrip().split(" ") for line in name_file.readlines()]
    for line in lines:
        names[" ".join(line[1:])] = line[0]
    return names


def calcd(y1,x1, y2,x2):
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    y1  = float(y1)
    x1  = float(x1)
    y2  = float(y2)
    x2  = float(x2)
    #
    R   = 3958.76 # miles = 6371 km
    #
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0
    # approximate great circle distance with law of cosines
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R


def goal_test(current, end):
    return current == end


if __name__ == "__main__":
    # main func!
    main()
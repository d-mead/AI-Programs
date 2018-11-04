from math import pi , acos , sin , cos
from collections import deque
import time
import sys
from heapq import heappush, heappop
from tkinter import *
# from pythonds.basic.stack import Stack
# import plotly.plotly as py
# import plotly.graph_objs as go
import pickle
# import pickle
from PIL import ImageTk
# sys.path.append('/Users/JackMead/Desktop/CompSci/PycharmProjects/AIPrograms/venv/lib/python3.7/site-packages/basemap-1.1.0/build/lib.macosx-10.9-x86_64-3.7/mpl_toolkits')
# from basemap import *

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import csv
import numpy as np
import networkx as nx
import pandas as pd
from geographiclib.geodesic import Geodesic


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

    start = "Vancouver" # sys.argv[1]
    end = "San Jose" # sys.argv[2]

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
    draw_3()
    # draw(full_send(names["Chicago"]), start_id, end_id)


def draw_3():
    # set up orthographic map projection with
    # perspective of satellite looking down at 50N, 100W.
    # use low resolution coastlines.
    # map = Basemap(projection='merc', llcrnrlon = -133, llcrnrlat= 14, urcrnrlon=-57, urcrnrlat= 62, resolution='l')
    # map = Basemap(projection='stere', llcrnrlon=-133, llcrnrlat=14, urcrnrlon=-57, urcrnrlat=62, lon_0 = 96, lat_0 = -38, resolution='l')
    map = Basemap(projection='lcc', resolution='l', width=5E6, height=5E6, lat_0=38, lon_0=-96)
    # map = Basemap(projection='ortho', lat_0=45, lon_0=-100, resolution='l')
    # draw coastlines, country boundaries, fill continents.
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    # map.bluemarble()
    map.fillcontinents(color='#001C35', lake_color='#012B51')
    # draw the edge of the map projection region (the projection limb)
    map.drawmapboundary(fill_color='#012B51')
    # draw lat/lon grid lines every 30 degrees.
    # make up some data on a regular lat/lon grid.
    # nlats = 73;
    # nlons = 145;
    # delta = 2. * np.pi / (nlons - 1)
    # lats = (0.5 * np.pi - delta * np.indices((nlats, nlons))[0, :, :])
    # lons = (delta * np.indices((nlats, nlons))[1, :, :])
    # wave = 0.75 * (np.sin(2. * lats) ** 8 * np.cos(4. * lons))
    # mean = 0.5 * np.cos(2. * lats) * ((np.sin(2. * lats)) ** 2 + 2.)
    # compute native map projection coordinates of lat/lon grid.
    # x, y = map(lons * 180. / np.pi, lats * 180. / np.pi)
    #     #     # # contour data over the map.
    #     #     # cs = map.contour(x, y, wave + mean, 15, linewidths=1.5)

    # position in decimal lat/lon

    ids = list()
    lats = list()
    lons = list()

    count = 0

    for id, coord in nodes.items():
        ids.append(id)
        lats.append(coord[0][0])
        lons.append(coord[0][1])
        count += 1
        # print(100 * count / len(nodes))

    # lats = [37.96, 42.82]
    # lons = [-121.29, -73.95]
    # convert lat and lon to map projection
    mx, my = map(lons, lats)

    # The NetworkX part
    # put map projection coordinates in pos dictionary
    G = nx.DiGraph(dircted=False)

    print(G.nodes)

    print("yes")

    count = 0

    for start, ends in list(edges.items())[::100]:
        for end in ends:
            # if len(start) < 5:
            #     print("ugh")
            if len(end[1]) < 5:
                G.add_edge(start, end)
                # print(end)
            else:
                G.add_edge(start, end[1])
        print(100*count/len(edges.keys()))
        count += 1

    # print(G.nodes)

    pos = {}
    count = 0
    for node in nodes:
        pos[node] = (mx[count], my[count])
        count += 1
        # print(100*count/len(nodes))

    # print(G.edges)

    # draw
    nx.draw_networkx(G, pos, edgelist=G.edges, with_labels=False, node_size=0.1, node_color='blue', edge_color='lime', arrowsize=0.01, width = .25)


    # lat = []
    # lon = []
    #
    # x, y = map(lon, lat)
    #
    #
    # plt.plot(x, y, 'o-', markersize=5, linewidth=1)

    # count = 0
    # total = len(edges.items())
    #
    # print((count/total)*100)
    #
    #
    # for start, ends in list(edges.items())[::10]:
    #     # print(nodes[start])
    #     # print(ends)
    #     count += 1
    #     print((count / total) * 100)
    #
    #     for end in ends:
    #         # print(nodes[start][0][1], nodes[start][0][0], end[2][1], end[2][0])
    #         map.drawgreatcircle(nodes[start][0][1], nodes[start][0][0], end[2][1], end[2][0], linewidth=.5, color='r')

    # map.drawgreatcircle(-60.119060, 46.166160, -100.000000, 21.940000, linewidth=.5, color='r')

    plt.title('railroads')
    plt.show()

    print("done")

# def draw_4():
#     graph = nx.from_pandas_dataframe(routes_us, source='Source Airport', target='Dest Airport', edge_attr='number of flights', create_using=nx.DiGraph())


def draw_2():
    py.offline.plot()
    py.offline.init_notebook_mode(connected=True)

    py.offline.iplot({
        "data": [go.Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
        "layout": go.Layout(title="hello world")
    })


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
    delay = 0.1

    # keyboard.add_hotkey('A', lambda: up())
    # keyboard.add_hotkey('S', lambda: down())

    m = 1

    global lines_dict
    lines_dict = dict()

    for line in lines:
        lines_dict[line] = w.create_line(line, fill="grey")
        lines_dict[(line[2], line[3], line[0], line[1])] = w.create_line(line, fill="grey")

    s = StringVar(w, value=list(names.keys())[0])
    e = StringVar(w, value=list(names.keys())[1])

    m = StringVar(w, value="1")

    start_window = w.create_window(750, 625, anchor = NW, window = OptionMenu(master, s, *list(names.keys())))

    end_window = w.create_window(750, 650, anchor=NW, window=OptionMenu(master, e, *list(names.keys())))

    global speed
    speed = Scale(master, from_=-.25, to=.5, orient=HORIZONTAL, resolution=0.01)

    speed_window = w.create_window(750, 675, anchor = NW, window=speed)

    # textentry_s = Entry(w, textvariable=s)
    # w.create_window(650, 625, window=textentry_s, height=25, width=100, anchor=NW)
    #
    # textentry_e = Entry(w, textvariable=e)
    # w.create_window(760, 625, window=textentry_e, height=25, width=100, anchor = NW)

    a_button = Button(text="A*", command=lambda: do_a_star(names[s.get()], names[e.get()], w, float(m.get())), anchor=CENTER)
    a_button.configure(width=10, activebackground="green", relief=FLAT)
    a_button_window = w.create_window(650, 625, anchor=NW, window=a_button)

    m_window = w.create_window(615, 622, anchor=NW, window=Entry(master, textvariable=m, width=2))

    d_button = Button(text="Dijkstra", command=lambda: do_dij(names[s.get()], names[e.get()], w), anchor=CENTER)
    d_button.configure(width=10, activebackground="green", relief=FLAT)
    d_button_window = w.create_window(650, 650, anchor=NW, window=d_button)

    db_button = Button(text="Bi Dijkstra", command=lambda: do_dij_bi(names[s.get()], names[e.get()], w), anchor=CENTER)
    db_button.configure(width=10, activebackground="green", relief=FLAT)
    db_button_window = w.create_window(650, 675, anchor=NW, window=db_button)

    df_button = Button(text="DFS", command=lambda: do_dfs(names[s.get()], names[e.get()], w), anchor=CENTER)
    df_button.configure(width=10, activebackground="green", relief=FLAT)
    df_button_window = w.create_window(650, 700, anchor=NW, window=df_button)

    t_button = Button(text="Terrible", command=lambda: do_bad(names[s.get()], names[e.get()], w), anchor=CENTER)
    t_button.configure(width=10, activebackground="green", relief=FLAT)
    t_button_window = w.create_window(650, 725, anchor=NW, window=t_button)

    c_button = Button(text="Clear Map", command=lambda: clear(w, lines), anchor=CENTER)
    c_button.configure(width=10, activebackground="green", relief=FLAT)
    c_button_window = w.create_window(750, 725, anchor=NW, window=c_button)

    # answer = a_star_tk(start_id, end_id, w, .5)
    # answer = dijkstra_tk(start_id, end_id, w)
    # answer = dfs_tk(start_id, end_id, w)

    # distance = answer[0]
    # red_lines = answer[1]
    # all_lines = answer[2]

    # for line in all_lines:
    #     w.itemconfig(lines_dict[line], fill="mediumblue")
    #     # w.create_line(line, fill='mediumblue', width=1)

    # for line in red_lines:
    #     w.itemconfig(lines_dict[line], fill="green", width = 3)
    #     w.itemconfig(lines_dict[(line[2], line[3], line[0], line[1])], fill="green", width = 3)
    #     # w.create_line(line, fill='red', width=2)
    #     w.update()

    global d
    d = w.create_text(700, 600, fill = 'black', width = 100, text = "", anchor = "nw")


    mainloop()


def clear(w, lines):
    global lines_dict

    for line in lines:
        w.itemconfig(lines_dict[line], fill = "grey", width = 1)
        w.itemconfig(lines_dict[(line[2], line[3], line[0], line[1])], fill = "grey", width = 1)
        # w.redraw()


def do_a_star(start_id, end_id, w, m):
    answer = a_star_tk(start_id, end_id, w, m)
    display(w, answer[0], answer[1], answer[2])


def do_dij(start_id, end_id, w):
    answer = dijkstra_tk(start_id, end_id, w)
    display(w, answer[0], answer[1], answer[2])


def do_dij_bi(start_id, end_id, w):
    answer = bi_dijkstra_tk(start_id, end_id, w)
    display(w, answer[0], answer[1], answer[2])


def do_dfs(start_id, end_id, w):
    answer = dfs_tk(start_id, end_id, w)
    display(w, answer[0], answer[1], answer[2])


def do_bad(start_id, end_id, w):
    answer = bad_tk(start_id, end_id, w, 10)
    display(w, answer[0], answer[1], answer[2])


def display(w, distance, red_lines, all_lines):
    for line in red_lines:
        w.itemconfig(lines_dict[line], fill="green", width = 3)
        w.itemconfig(lines_dict[(line[2], line[3], line[0], line[1])], fill="green", width = 3)
        # w.create_line(line, fill='red', width=2)
        redraw(w)
    global d
    w.itemconfig(d, text=("%s miles" % (round(distance, 2))))


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
                # w.create_line((abs(float(s[3][1])) - 70) * 20, (abs(float(s[3][0])) - 30) * 20, (abs(float(child[2][1])) - 70) * 20, (abs(float(child[2][0])) - 30) * 20)

    if len(fringe) is 0:
        return lines


def redraw(w):
    global last_time
    global speed
    if speed.get()>=0:
        time.sleep(speed.get())
        w.update()
    else:
        if time.perf_counter() - last_time > abs(speed.get()):
            last_time = time.perf_counter()
            w.update()
    # if time.perf_counter() - last_time > speed.get()/100:
    #     last_time = time.perf_counter()
    #     w.update()


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

            w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="blue", width=2)
            w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="blue", width=2)

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
                w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="red", width=2)
                w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="red", width=2)
                heappush(fringe, (circle+(s[4]+child[0])*m, child[0], child[1], child[2], s[4]+child[0], red_lines, s[3]))
                redraw(w)

        # if random.randint(0, 1000) > 999:
        #     w.update()
        #         # print(abs(float(s[3][1]))-70, abs(float(s[3][0]))-30, abs(float(child[2][1]))-70, abs(float(child[2][0]))-30)
                # w.create_line((abs(float(s[3][1]))-70)*20, (abs(float(s[3][0]))-30)*20, (abs(float(child[2][1]))-70)*20, (abs(float(child[2][0]))-30)*20)

    if len(fringe) is 0:
        return -1


def bad_tk(start, end, w, m):

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

            w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="blue", width=2)
            w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="blue", width=2)

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
                w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="red", width=2)
                w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="red", width=2)
                heappush(fringe, (-100*circle+(s[4]+child[0])*m, child[0], child[1], child[2], s[4]+child[0], red_lines, s[3]))
                redraw(w)
        # if random.randint(0, 1000) > 999:
        #     w.update()
        #         # print(abs(float(s[3][1]))-70, abs(float(s[3][0]))-30, abs(float(child[2][1]))-70, abs(float(child[2][0]))-30)
                # w.create_line((abs(float(s[3][1]))-70)*20, (abs(float(s[3][0]))-30)*20, (abs(float(child[2][1]))-70)*20, (abs(float(child[2][0]))-30)*20)

    if len(fringe) is 0:
        return -1


def bi_dijkstra_tk(start, end, w):
    fringe = [(0, start, 0, nodes[start][0], []), ]
    fringe_b = [(0, end, 0, nodes[end][0], []), ]
    fringe_set = set()
    fringe_set.add(start)
    fringe_set_b = set()
    fringe_set_b.add(end)
    visited = set()
    visited_b = set()
    all_lines = set()

    while len(fringe) is not 0:
        s = heappop(fringe)
        sb = heappop(fringe_b)

        if s[1] in fringe_set:
            fringe_set.remove(s[1])
        if sb[1] in fringe_set_b:
            fringe_set_b.remove(sb[1])

        if len(s) > 5:

            sy = (-abs((float(s[3][1])) + maxy) + height) * scaleh - 2
            sx = abs((float(s[3][0])) + maxx) * scalew + 8
            ey = (-abs(float(s[5][1]) + maxy) + height) * scaleh - 2
            ex = abs((float(s[5][0])) + maxx) * scalew + 8

            w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="blue", width=2)
            w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="blue", width=2)

        if len(sb) > 5:

            sby = (-abs((float(sb[3][1])) + maxy) + height) * scaleh - 2
            sbx = abs((float(sb[3][0])) + maxx) * scalew + 8
            eby = (-abs(float(sb[5][1]) + maxy) + height) * scaleh - 2
            ebx = abs((float(sb[5][0])) + maxx) * scalew + 8

            w.itemconfig(lines_dict[(sby, sbx, eby, ebx)], fill="blue", width=2)
            w.itemconfig(lines_dict[(eby, ebx, sby, sbx)], fill="blue", width=2)

        if sb[1] in fringe_set:
            print("yep1")
            for v in fringe:
                if v[1] == sb[1]:
                    return sb[0]+v[0], v[4]+sb[4][::-1], all_lines

        if s[1] in fringe_set_b:
            print("yep")
            for v in fringe_b:
                if v[1] == s[1]:
                    return s[0]+v[0], s[4]+v[4][::-1], all_lines

        if goal_test(sb[1], start):
            return sb[0], sb[4], all_lines  # return the moves

        if goal_test(s[1], end):  # if the state is won
            return s[0], s[4], all_lines  # return the moves



        go_t = True
        go_b = True

        if s[1] in visited:
            go_t = False

        if go_t:

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
                    w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="red", width=2)
                    w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="red", width=2)
                    fringe_set.add(child[1])
                    heappush(fringe, (s[2] + child[0], child[1], s[2] + child[0], child[2], red_lines, s[3]))
                    redraw(w)

        if sb[1] in visited_b:
           go_b = False

        if go_b:
            visited_b.add(sb[1])

            children = get_children(sb[1])
            for child in children:
                if child[1] not in visited_b:
                    red_lines = list(sb[4])
                    sy = (-abs((float(sb[3][1])) + maxy) + height) * scaleh - 2
                    sx = abs((float(sb[3][0])) + maxx) * scalew + 8
                    ey = (-abs(float(child[2][1]) + maxy) + height) * scaleh - 2
                    ex = abs((float(child[2][0])) + maxx) * scalew + 8
                    red_lines.append((sy, sx, ey, ex))
                    all_lines.add((sy, sx, ey, ex))
                    w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="red", width=2)
                    w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="red", width=2)
                    fringe_set_b.add(child[1])
                    heappush(fringe_b, (sb[2] + child[0], child[1], sb[2] + child[0], child[2], red_lines, sb[3]))
                    redraw(w)

    if len(fringe) is 0 and len(fringe_b) is 0:
        return -1


def dijkstra_tk(start, end, w):
    fringe = [(0, start, 0, nodes[start][0], []), ]
    visited = set()
    all_lines = set()

    while len(fringe) is not 0:
        s = heappop(fringe)

        if len(s) > 5:

            sy = (-abs((float(s[3][1])) + maxy) + height) * scaleh - 2
            sx = abs((float(s[3][0])) + maxx) * scalew + 8
            ey = (-abs(float(s[5][1]) + maxy) + height) * scaleh - 2
            ex = abs((float(s[5][0])) + maxx) * scalew + 8

            w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="blue", width=2)
            w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="blue", width=2)

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
                w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="red", width=2)
                w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="red", width=2)
                heappush(fringe, (s[2] + child[0], child[1], s[2] + child[0], child[2], red_lines, s[3]))
        redraw(w)

    if len(fringe) is 0:
        return -1


def dfs_tk(start, end, w):
    fringe = Stack()
    fringe.push((0, start, nodes[start][0], 0, []))
    visited = set()
    all_lines = set()

    end_y = nodes[end][0][0]
    end_x = nodes[end][0][1]

    while fringe.size() is not 0:
        s = fringe.pop()

        if len(s) > 5:
            sy = (-abs((float(s[2][1])) + maxy) + height) * scaleh - 2
            sx = abs((float(s[2][0])) + maxx) * scalew + 8
            ey = (-abs(float(s[5][1]) + maxy) + height) * scaleh - 2
            ex = abs((float(s[5][0])) + maxx) * scalew + 8

            w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="blue", width=2)
            w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="blue", width=2)

        if goal_test(s[1], end):  # if the state is won
            return s[3], s[4], all_lines  # return the moves

        if s[1] in visited:
            continue

        visited.add(s[1])

        children = get_children(s[1])
        for child in children:
            if child[1] not in visited:
                red_lines = list(s[4])
                sy = (-abs((float(s[2][1])) + maxy) + height) * scaleh - 2
                sx = abs((float(s[2][0])) + maxx) * scalew + 8
                ey = (-abs(float(child[2][1]) + maxy) + height) * scaleh - 2
                ex = abs((float(child[2][0])) + maxx) * scalew + 8
                red_lines.append((sy, sx, ey, ex))
                all_lines.add((sy, sx, ey, ex))
                # w.create_line((sy, sx, ey, ex), fill="mediumblue", width = 2)
                w.itemconfig(lines_dict[(sy, sx, ey, ex)], fill="red", width=2)
                w.itemconfig(lines_dict[(ey, ex, sy, sx)], fill="red", width=2)
                fringe.push((child[0], child[1], child[2], s[3] + child[0], red_lines, s[2]))
        redraw(w)
        # if random.randint(0, 1000) > 999:
        #     w.update()
        #         # print(abs(float(s[3][1]))-70, abs(float(s[3][0]))-30, abs(float(child[2][1]))-70, abs(float(child[2][0]))-30)
        # w.create_line((abs(float(s[3][1]))-70)*20, (abs(float(s[3][0]))-30)*20, (abs(float(child[2][1]))-70)*20, (abs(float(child[2][0]))-30)*20)

    if fringe.size() is 0:
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
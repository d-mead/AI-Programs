from math import pi , acos , sin , cos
from collections import deque
import time
import sys
from heapq import heappush, heappop
import pickle
# import pickle


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
    
    begin = time.perf_counter()
    dij = dijkstra(start_id, end_id)
    stop = time.perf_counter()
    print("Dijkstra: \t%s \t%s seconds" % (dij, round(stop - begin, 5)))


    begin = time.perf_counter()
    a = a_star(start_id, end_id)
    stop = time.perf_counter()
    print("A-Star: \t%s \t%s seconds" % (a, round(stop - begin, 5)))


def a_star(start, end):
    fringe = [(0, 0, start, nodes[start][0],  0), ]
    visited = set()

    end_y = nodes[end][0][0]
    end_x = nodes[end][0][1]

    while len(fringe) is not 0:
        s = heappop(fringe)

        if goal_test(s[2], end):  # if the state is won
            return s[0]  # return the moves

        if s[2] in visited:
            continue

        visited.add(s[2])

        children = get_children(s[2])
        for child in children:
            if child[1] not in visited:
                circle = calcd(child[2][0], child[2][1], end_y, end_x)
                heappush(fringe, (circle+s[4]+child[0], child[0], child[1], child[2], s[4]+child[0]))

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
    for start, ids in names.items():
        for end, ide in names.items():
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
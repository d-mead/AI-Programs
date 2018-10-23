from math import pi , acos , sin , cos
from collections import deque
import time
from heapq import heappush, heappop
# import pickle


def main():
    global edges, nodes, names
    edges, nodes = make_edges_dict("rrNodes.txt", "rrEdges.txt")
    names = make_names_dict("rrNodeCity.txt")
    start = "9100373"
    end = "9100042" #0100007, 4700027

    find_longest()
    # print(get_children("5500045"))
    # start = "9100373"
    # end = "9100042" #0100007, 4700023
    #
    # begin = time.perf_counter()
    # dij = dijkstra(start, end)
    # stop = time.perf_counter()
    # print("Dijkstra: \t%s, %s seconds" % (dij, round(stop - begin, 5)))
    #
    #
    # begin = time.perf_counter()
    # a = a_star(start, end)
    # stop = time.perf_counter()
    # print("A-Star: \t%s, %s seconds" % (a, round(stop - begin, 5)))


def a_star(start, end):
    fringe = [(0, 0, start, nodes[start][0],  0), ]
    visited = set()

    while len(fringe) is not 0:
        s = heappop(fringe)

        if goal_test(s[2], end):  # if the state is won
            return s[3]  # return the moves

        children = get_children(s[2])
        for child in children:
            if child[1] not in visited:
                circle = calcd(child[2][0], child[2][1], s[2][0], s[2][1])
                heappush(fringe, (circle+s[1], child[0], child[1], s[1]+child[0]))
                visited.add(child[1])
    if len(fringe) is 0:
        return -1


def dijkstra(start, end):
    fringe = [(0, start, 0), ]
    visited = set()
    visited.add(start)

    while len(fringe) is not 0:
        s = heappop(fringe)
        if goal_test(s[1], end):  # if the state is won
            return s[2]  # return the moves
        children = get_children(s[1])
        for child in children:
            if child[1] not in visited:
                heappush(fringe, (child[0], child[1], s[0]+child[0]))
                visited.add(child[1])

    if len(fringe) is 0:
        return -1

# def run(start, end):


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
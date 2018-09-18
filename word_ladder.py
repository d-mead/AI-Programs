import sys
import pickle
from collections import deque
import copy
import time

def main():
    global dict

    # dict = make_dict("words_6.txt")
    #
    # print(dict)
    #
    # with open("words_6.pkl", "wb") as outfile:
    #     pickle.dump(dict, outfile)

    with open("words_6.pkl", "rb") as infile:
        dict = pickle.load(infile)


    # print(connected_components(dict))

    # start, end, length = longest_path(dict)
    # print("start: %s, end: %s, length: %s" % (start, end, length))
    begin = time.process_time()

    # count, longest = connected_components(dict)
    # print("number of connected components: %s" % count)
    # print("fringe of the longest group: %s" % longest)
    # print("size of longest group: %s" % len(longest))
    start, end, length = longest_path(dict)
    print("start: %s, end: %s, length: %s" % (start, end, length))

    finish = time.process_time()
    print("seconds to run: %s" % (finish - begin))


def longest_path(dict):
    count, search_queue = connected_components(dict)
    total_set = set(dict.keys())
    max_path = deque()
    visited_words = {"", }
    count = 0
    max_path = deque()
    for start in total_set:
        visited_words.clear()
        visited_words.add(start)
        fringe = deque()
        starting_path = deque()
        starting_path.append(start)
        fringe.append(Word(start, starting_path))
        visited_words.add(start)
        while len(fringe) > 0:
            word = fringe.popleft()
            children = dict.get(word.get_string())
            for child in children:
                if child not in visited_words:
                    path = copy.copy(word.get_path())
                    path.appendleft(child)
                    fringe.append(Word(child, path))
                    if len(path) > len(max_path):
                        max_path = path
                    visited_words.add(child)
    return max_path.popleft(), max_path.pop(), len(max_path)


def connected_components(dict):
    total_set = set(dict.keys())
    start = total_set.pop()
    visited_words = {start}
    count = 0
    longest_fringe = deque()
    while len(total_set) > 0:
        start = total_set.pop()
        visited_words.add(start)
        fringe = deque()
        fringe.append(start)
        while len(fringe) > 0:
            word = fringe.popleft()
            children = dict.get(word)
            for child in children:
                if child not in visited_words:
                    fringe.append(child)
                    visited_words.add(child)
                    total_set.remove(child)
            if len(fringe) > len(longest_fringe):
                longest_fringe = deque(fringe)
        count += 1
    return count, longest_fringe


def read_many(filename):
    begin = time.process_time()
    file = open(filename, "r")
    lines = [line.rstrip() for line in file.readlines()]
    for line in lines:
        start = line.split(" ")[0]
        end = line.split(" ")[1]
        print("start: %s, finish: %s" % (start, end))
        path = find_path(start, end)
        if path != -1:
            print("\t path: %s" % (path,))
            print("\t path length: %s" % (len(path), ))
        else:
            print("\t no path found")
    finish = time.process_time()
    print("seconds to run: %s" % (finish - begin))


def make_dict(filename):
    file = open(filename, "r")
    lines = [line.rstrip() for line in file.readlines()]
    dict = {"": [], }
    words_set = set(lines)
    for line in lines:
        word = line.replace("\n", "")
        for comp in words_set:
            if sum(word[i] != comp[i] for i in range(len(word))) == 1:
                print("match found: " + word + ", " + comp)
                if word in dict.keys():
                    dict.get(word).append(comp)
                else:
                    dict[word] = [comp]
    return dict


def find_path(start, end):
    fringe = deque()
    starting_path = deque()
    starting_path.append(start)
    fringe.append(Word(start, starting_path))
    visited = {start, }

    while len(fringe) is not 0:
        word = fringe.popleft()
        if word.get_string() == end:
            return list(word.get_path())
        children = dict.get(word.get_string())
        for child in children:
            if child not in visited:
                path = copy.copy(word.get_path())
                path.appendleft(child)
                fringe.append(Word(child, path))
                visited.add(child)
    if len(fringe) == 0:
        return -1


class Word:

    def __init__(self, w, p):
        self.word = w  # state
        self.path = p  # path traveled to that state so far

    def get_path(self):
        # returns the path so far
        return self.path

    def get_string(self):
        # returns the state
        return self.word







if __name__ == "__main__":
    main()
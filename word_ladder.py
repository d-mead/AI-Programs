import sys
import pickle
from collections import deque

def main():
    #dict = make_dict("words_6.txt")

    #print(dict)

    #with open("words_6.pkl", "wb") as outfile:
        #pickle.dump(dict, outfile)
    global dict

    with open("words_6.pkl", "rb") as infile:
        dict = pickle.load(infile)

    print(dict)
    path = find_path("abased", "abases")
    print(path)


def make_dict(filename):
    file = open(filename, "r")
    lines = [line.rstrip() for line in file.readlines()]
    dict = {"": [], }
    words_set = set(lines)
    for line in lines:
        word = line.replace("\n", "")
        for comp in words_set:
            if sum(word[i] != comp[i] for i in range(len(word))) == 1:
                #print("match found: " + word + ", " + comp)
                if word in dict.keys():
                    dict.get(word).append(comp)
                else:
                    dict[word] = [comp]
                if comp in dict.keys():
                    dict.get(comp).append(word)
                else:
                    dict[comp] = [word]
    return dict


def find_path(start, end):
    fringe = deque()
    fringe.append(Word(start, []))
    visited = {start, }
    path = []

    while len(fringe) is not 0:
        word = fringe.popleft()
        if word.get_string() == end:
            retunrn path
        children = dict.get(word.get_string())
        for child in children:
            if child not in visited:
                path = word.get_path()
                path.append(child)
                fringe.append(Word(child, path))
                visited.add(child)
    if len(fringe) == 0:
        return -1

    # start = Puzzle(state, "")
    # fringe = deque()
    # fringe.append(start)
    # visited = {startState, }
    #
    # if parityCheck(state) == 1:  #
    #     return -1  # if parity determines its not solveable
    #
    # while len(fringe) is not 0:  #
    #     v = fringe.popleft()  # your standard BFS algorithm
    #     if goal_test(v.getState()):  #
    #         return v.getPath()  #
    #     children = getChildren(v.getState())  #
    #     for child in children.keys():  #
    #         if child not in visited:  #
    #             child_path = children.get(child, 0)  #
    #             puz = Puzzle(child, v.getPath() + child_path)  #
    #             fringe.append(puz)  #
    #             visited.add(child)  #
    # if len(fringe) is 0:
    #     return -1


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
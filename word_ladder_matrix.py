import sys
import pickle
from collections import deque
import copy
import time

import numpy as np
from scipy.sparse import csgraph
from scipy.spatial.distance import pdist, squareform
from scipy import sparse
import decimal


def main():
    global word_bytes, word_list, graph
    word_bytes, word_list = get_words("words_6_longer.txt")
    graph = graph()
    shortest_path()

def get_words(filename):
    word_list = open(filename, "r").read().split()
    # word_list = [line.rstrip() for line in file.readlines()]
    print(len(word_list))
    word_list = np.sort(word_list)
    print(word_list.shape)
    word_bytes = np.ndarray((len(word_list), len(word_list[0])), dtype = 'int8', buffer=word_list.data)
    print(word_bytes.shape)
    return word_bytes, word_list


def graph():
    hamming_dist = pdist(word_bytes, metric='hamming')
    graph = sparse.csr_matrix(squareform(hamming_dist < 1.01 / word_list.itemsize))
    print(graph.shape)
    return graph.toarray()


def shortest_path():
    begin = time.clock()

    i1 = word_list.searchsorted('embail')
    print(i1, word_list[i1])

    i2 = word_list.searchsorted('zaffar')
    print(i2, word_list[i2])

    distances, predecessors = csgraph.shortest_path(graph, return_predecessors=True)
    print("distance from '%s' to '%s': %s steps" % (word_list[i1], word_list[i2], str(decimal.Decimal(distances[i1, i2]))))

    i = i1
    while i != i2:
        print(word_list[i])
        i = predecessors[i2, i]
    print(word_list[i2])

    finish = time.clock()
    print("seconds to run: %s" % (finish - begin))




    # dict = {"": [], }
    # words_set = set(lines)
    # for line in lines:
    #     word = line.replace("\n", "")
    #     for comp in words_set:
    #         if sum(word[i] != comp[i] for i in range(len(word))) == 1:
    #             print("match found: " + word + ", " + comp)
    #             if word in dict.keys():
    #                 dict.get(word).append(comp)
    #             else:
    #                 dict[word] = [comp]
    #     if word not in dict.keys():
    #         dict[word] = []
    # return dict

if __name__ == "__main__":
    main()

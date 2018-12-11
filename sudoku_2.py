global N
global height
global width
global indices
import time
import random
import sys
from heapq import heappop,heappush
backtrack = 0
symbols = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
global symbol_set
global groups
def convert(state):
    d = dict()
    ind = []
    for index,value in enumerate(state):
        if value!='.':
            d[index]=value
            ind.append(index)
        else:
            d[index]=symbol_set
    '''
    for i in ind:
        for x in indices[i]:
            if state[i] in d[x]:
                d[x]=d[x].replace(state[i],'')
    '''
    for i in ind:
        cprop(d,i)
    #print(d)
    return d

def read(state):
    global N
    global width
    global height
    global indices
    global symbol_set
    global groups
    N = int(len(state)**0.5)
    symbol_set = symbols[0:N]
    height = N**0.5
    if height.is_integer():
        height = int(height)
        width = height
    else:
        height = int(height)
        width = height +1
    sets = []
    for i in range(N):
        rowset = set()
        columnset = set()
        for x in range(N):
            rowset.add(x+i*N)
            columnset.add(i+x*N)
        sets.append(rowset)
        sets.append(columnset)
    for c in range(int(N/width)):
        for r in range(int(N/height)):
            blockset = set()
            initialr = r*height #row 0,1,2,3...
            initialc = c*width
            for x in range(width):
                for y in range(height):
                    blockset.add((initialr+y)*N+initialc+x)
            sets.append(blockset)
            #print(blockset)
    store = dict()
    #print(sets)
    for i in range(N*N):
        for s in sets:
            if i in s:
                if i in store.keys():
                    store[i] = s.union(store[i])
                else:
                    store[i]=s.copy()
                store[i].remove(i)
    indices = store
    groups = sets


def goal_test(state):
    for i in state:
        if len(state[i])!=1:
            return False
    return True

def get_next_unassigned_variable(state):
    maxi = 0
    maxlen = N
    for i in state:
        if len(state[i])<=maxlen and len(state[i])!=1:
            maxlen = len(state[i])
            maxi = i
    return maxi



def get_sorted_values(state,var):
    return state[var]

def cprop(state,var):
    go = [var]
    store = True
    while len(go)!=0 and store:
        index = go.pop()
        val = state[index]
        for i in indices[index]:
            if val in state[i]:
                state[i]= state[i].replace(val,'')
                if len(state[i])==0:
                    #Going down wrong path? returns none
                    return False
                if len(state[i])==1:
                    go.append(i)
        store = not goal_test(state)
    return True



def csp(state): #LIMIT BACKTRACKING?
    global backtrack
    backtrack+=1
    if goal_test(state):
        return state
    var = get_next_unassigned_variable(state)
    for val in get_sorted_values(state,var):
        copy = state.copy()
        copy[var] = val
        if cprop(copy,var):
            if checkSets(copy):
                # if improvementC(copy):
                c= csp(copy)
                if c !=None:
                    return c
    return None


def numSymbols(state):
    d = dict()
    for i in symbol_set:
        d[i]=0
    for i in state:
        d[state[i]] = d[state[i]]+1
    return d


def display(state):
    s = ''
    for i in range(N*N):
        s+=state[i]
    return s


def checkSets(state): #THIS IS TE PROBLEM FIX
    for sets in groups:
        x = dict()
        for index in sets:
            v = state[index]
            if len(v)!=1:
                for i in v:
                    if i not in x:
                        x[i]=1
                    else:
                        x[i] = x[i]+1
        unique = ''
        for i in x:
            if x[i]==1:
                unique = unique+i
        for i in unique:
            for index in sets:
                if i in state[index]:
                    state[index]=i
                    if not cprop(state,index):
                        return False
    return True


def correct(state):
    for i in state:
        if len(state[i])==0:
            return False
    return True


#DO ANOTHER IMPORVEMENT
def improvementC(state): #FIX
    toC = []
    for sets in groups:
        pairs = dict()
        for index in sets:
            v = state[index]
            if len(v)==2:
                if v not in pairs:
                    pairs[v]=1
                else:
                    pairs[v] = pairs[v]+1
        unique = set()
        for i in pairs:
            if pairs[i]==2:
                unique.add(i)
        for pair in unique:
            for index in sets:
                if state[index]!=pair:
                    first = pair[0]
                    second = pair[1]
                    if first in state[index]:
                        state[index]=state[index].replace(first,'')
                        if len(state[index])==1:
                            toC.append(index)
                    if second in state[index]:
                        state[index]=state[index].replace(second,'')
                        if len(state[index])==1:
                            toC.append(index)
    for i in toC:
        if cprop(state,i)==False:
            return False
    return True

def check(state):
    s = set([x for x in symbol_set])
    for i in groups:
        temp = set()
        for index in i:
            temp.add(state[index])
        if temp!=s:
            return False
    return True

def main():
    #sys.setrecursionlimit(50000)
    name = "sudoku_puzzles_1.txt"#sys.argv[1]
    file = open(name)
    n = 0
    t=0.0
    lines = file.readlines()
    individualback = 0
    for i in lines:
        state = i.rstrip()
        read(state)
        individualback = backtrack
        state = convert(state)

        start = time.perf_counter()
        #cprop(state)
        solution = csp(state)

        end = time.perf_counter()
        #print('puzzle: '+str(n))
        #print('N, solution, time, backtracks')
        n += 1
        #checkSets(state)
        #solution = state


        s = display(solution)
        s = str(N)+'\t'+s +'\t'+str(end-start)+'\t'+str(backtrack-individualback)
        print(s)
        #print(numSymbols(solution)) #TAKE OUT FOR FINAL CODE
        #print(check(solution))

        t+=end-start
        #print()

    print(str(t))
    print(str(backtrack))

if __name__ == '__main__':
    main()
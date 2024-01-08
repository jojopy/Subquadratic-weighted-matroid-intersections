from HelperFunctions import findMaxWeightAddition, findMinWeightRemoval, findMin
from sage.all import *

def adjustB1(input_, S1, w1, B1, d, predecessor):
    for b in B1:
        vb = findMaxWeightAddition(input_.M1, input_.w, B1, S1.difference([b]))
        if vb is not None:
            wi = w1[b] - w1[vb]
            if(d[b] + wi < d[vb]):
                d[vb] = d[b] + wi
                predecessor[vb] = (b, 1)

def adjustB2(input_, S2, w2, B2, d, predecessor):
    for b in B2:
        vb = findMinWeightRemoval(input_.M2, input_.w, S2, S2.union([b]))
        if vb is not None:
            wi = w2[vb] - w2[b]
            if(d[b] + wi < d[vb]):
                d[vb] = d[b] + wi
                predecessor[vb] = (b, 2)

def clearB1(input_, S1, w1, B1, d, predecessor):
    for v in input_.V.difference(S1):
        b = findMinWeightRemoval(input_.M1, input_.w, B1, S1.union([v]))
        if b is not None:
            wi = w1[b] - w1[v]
            if(d[b] + wi < d[v]):
                d[v] = d[b] + wi
                predecessor[v] = (b, 1)

def clearB2(input_, S2, w2, B2, d, predecessor):
    for v in S2:
        b = findMaxWeightAddition(input_.M2, input_.w, B2, S2.difference([v]))
        if b is not None:
            wi = w2[v] - w2[b]
            if(d[b] + wi < d[v]):
                d[v] = d[b] + wi
                predecessor[v] = (b, 2)

def findDistances(input_, S1, S2, w1, w2):
    #Initalize d
    d = {x:len(input_.V)*max(input_.w.values())**len(input_.V) for x in input_.V}
    for x in S1.difference(S2):
        d[x] = 0

    #Intialize
    visited = set()
    predecessors = dict()
    B1, B2 = set(), set()

    while(not visited == input_.V): #For some reason != does not work
        #Find minimum distance element
        vt = findMin(input_.V.difference(visited), d)

        #Append element
        visited.add(vt)
        if vt in S1:
            B1.add(vt)
        if vt not in S2:
            B2.add(vt)

        #Update distances
        if len(B1) >= r**0.5:
            clearB1(input_, S1, w1, B1, d, predecessors)
            B1 = set()
        else:
            adjustB1(input_, S1, w1, B1, visited, d, predecessors)

        if len(B2) >= r**0.5:
            clearB2(input_, S2, w2, B2, d, predecessors)
            B2 = set()
        else:
            adjustB2(input_, S2, w2, B2, visited, d, predecessors)

    return d, predecessors

def graphAugmentationAlgorithm(input_, S1, S2, w1, w2, e):
    while(not S1 == S2): #For some reason != does not work
        d, predecessors = findDistances(input_, S1, S2, w1, w2)

        #Find head
        shortestD = oo
        head = None
        for x in S2.difference(S1):
            if d[x] < shortestD:
                head = x
                shortestD = d[x]

        #Find head and tails
        headE1 = []
        headE2 = []
        tailE1 = []
        tailE2 = []

        while(not (head in S1 and not head in S2)):
            if predecessors[head][1] == 1:
                headE1.append(head)
                tailE1.append(predecessors[head][0])
            if predecessors[head][1] == 2:
                headE2.append(head)
                tailE2.append(predecessors[head][0])
            head = predecessors[head][0]

        #Update S1 S2
        S1 = S1.difference(tailE1).union(headE1)
        S2 = S2.difference(headE2).union(tailE2)

        #Update w1 w2
        for x in  input_.V:
            w1[x] = w1[x] + d[x]
            w2[x] = w2[x] - d[x]
    return S1, S2, w1, w2
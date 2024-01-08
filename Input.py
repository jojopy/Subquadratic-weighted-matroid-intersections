from sage.all import *
from HelperFunctions import weightOfSet
import random

class Input:
    def __init__(self, M1, M2, w):
        self.M1 = M1
        self.M2 = M2
        self.w = w
        self.V = M1.groundset()
        self.r = M1.rank()

    def getRandomRank(n):
        return random.randint(ceil((2*n)**0.5),floor(n*4/5))

    def getRandomMatroid(n, r):
        T = graphs.RandomTree(r + 1)
        G = T.union(graphs.RandomGNM(r+1,n - r))
        while(len(G.edges()) != n):
            v1 = G.random_vertex()
            v2 = G.random_vertex()
            while(v1 == v2):
                v2 = G.random_vertex()
            G.add_edge((v1, v2))
        G = Graph([(edge[0], edge[1], i) for i, edge in enumerate(G.edges())])
        G.edges()
        M = Matroid(G)

        assert M.size() == n
        assert M.rank() == r
        return M

    def getRandomWeight(n):
        return {i: random.randint(0,100) for i in range(n)}

    def getRandomInput(n, counter=0):
        w = Input.getRandomWeight(n)
        r = Input.getRandomRank(n)
        M1 = Input.getRandomMatroid(n,r)
        M2 = Input.getRandomMatroid(n,r)
        
        if len(M1.intersection(M2, w)) != r:
            if counter > 100:
                raise Exception("Cannot find input of size {} with intersection of rank {}".format(n, r))
            return Input.getRandomInput(n, counter + 1)

        return Input(M1, M2, w)
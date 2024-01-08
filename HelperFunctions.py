def findMin(S, w):
    min_y = None
    min_w = None
    for y in S:
        if min_y == None or w[y] < min_w:
            min_w = w[y]
            min_y = y
    return min_y

def is_independent(M, S):
    return M.rank(S) == len(S)

def findMaxWeightAddition(M, w, B, S):
    #No element y exists
    if(M.rank(set(B).union(S)) == M.rank(S)):
        return None
        
    #Sorting B
    B = sorted(B, key=lambda x: w[x])

    #Binary search
    while(len(B) > 1):
        B1 = B[:round(len(B)/2)]
        B2 = B[round(len(B)/2):]

        if(M.rank(set(B2).union(S)) > M.rank(S)):
            B = B2
        else:
            B = B1
    return B[0]


def findMinWeightRemoval(M, w, B, S):
    #No element y exists
    if(M.rank(S.difference(B)) != len(S.difference(B))):
        return None
        
    #Sorting B
    B = sorted(B, key=lambda x: w[x])

    #Binary search
    while(len(B) > 1):
        B1 = B[:round(len(B)/2)]
        B2 = B[round(len(B)/2):]

        if(M.rank(S.difference(B1)) == len(S.difference(B1))):
            B = B1
        else:
            B = B2
    return B[0]

def greedy(M, w):
    #Sorting the groundset
    B = sorted(M.groundset(), key=lambda x:w[x], reverse=True)

    #Greedy algorithm
    S = []
    for b in B:
        if is_independent(M, S + [b]):
            S.append(b)
    return set(S)

### DEBUG ###
def weightOfSet(S, w):
    total = 0
    for x in S:
        total += w[x]
    return total

def assertStillOptimal(input_, S1, S2, w1, w2, e):
    for x in input_.w:
        assert input_.w[x] + e == w1[x] + w2[x] or input_.w[x] == w1[x] + w2[x], "Weight split incorrect for x {}. w = {}, w1 = {}, w2 = {}".format(x, input_.w[x],w1[x],w2[x])
    assert input_.M1.is_independent(S1), "S1 not independent"
    assert input_.M2.is_independent(S2), "S2 not independent"
    assert weightOfSet(greedy(input_.M1, w1),w1) == weightOfSet(S1,w1), "S1 not optimal. greedy: {} - {}, S1: {}".format(greedy(input_.M1, w1), weightOfSet(greedy(input_.M1, w1),w1), weightOfSet(S1,w1))
    assert weightOfSet(greedy(input_.M2, w2),w2) == weightOfSet(S2,w2), "S2 not optimal. greedy: {} - {}, S2: {}".format(greedy(input_.M2, w2), weightOfSet(greedy(input_.M2, w2),w2), weightOfSet(S2,w2))



def checkResult(input_, S):
    return input_.M1.is_independent(S) and input_.M2.is_independent(S) and weightOfSet(S, input_.w) == weightOfSet(input_.M1.intersection(input_.M2,input_.w), input_.w)
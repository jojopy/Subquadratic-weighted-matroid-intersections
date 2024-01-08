from HelperFunctions import findMaxWeightAddition, findMinWeightRemoval

def weightAdjustAlgorithm(input_, S1, S2, w1, w2, e):
    #Initialize
    k = input_.r**(3/4)
    p = {x:0 for x in input_.V}

    #Main loop
    adjustables = list(S1.difference(S2))
    for x in adjustables:
        while p[x] < k:
            if input_.w[x] == w1[x] + w2[x]:
                #Option 1 - Increase w2
                w2[x] += e
                p[x] += 1
                y = findMinWeightRemoval(input_.M2, w2, S2, S2.union([x]))
                if y is not None and w2[x] > w2[y]: #If an element with higher weight is found
                    if y in S1:
                        adjustables.append(y)
                    S2 = S2.difference([y]).union([x])
                    break
            elif input_.w[x] + e == w1[x] + w2[x]:
                #Option 2 - Decrease w1
                w1[x] -= e
                y = findMaxWeightAddition(input_.M1, w1, input_.V.difference(S1), S1.difference([x]))
                if y is not None and w1[x] < w1[y]: #If an element with higher weight is found
                    if y not in S2:
                        adjustables.append(y)
                    S1 = S1.difference([x]).union([y])
                    break
            else:
                raise Exception()
    return S1, S2, w1, w2
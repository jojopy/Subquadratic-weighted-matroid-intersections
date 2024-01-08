from HelperFunctions import greedy
from weightAdjustments import weightAdjustAlgorithm
from graphAugmentation import graphAugmentationAlgorithm
from Input import Input

def twoEtoE(input_, w1, w2, e):
    #Initialize S1 and S2 with greedy
    S1 = greedy(input_.M1, w1)
    S2 = greedy(input_.M2, w2)

    #Weight adjustment algorithm
    S1, S2, w1, w2 = weightAdjustAlgorithm(input_, S1, S2, w1, w2, e)

    #Graph exchange algorithm
    S1, S2, w1, w2 = graphAugmentationAlgorithm(input_, S1, S2, w1, w2, e)

    return w1, w2, S1, S2

def maxWeightIntersection(input_: Input):
    #Initialize
    e = max(input_.w.values())
    w1 = {x:e/2 for x in input_.w}
    w2 = None
    S1 = None
    S2 = None

    #Main loop
    while e >= 1/input_.r:
        e = e/2
        w2 = {x:input_.w[x]-w1[x]+e for x in input_.w}

        w1, w2, S1, S2= twoEtoE(input_, w1, w2, e)

    assert S1 == S2
    return S1
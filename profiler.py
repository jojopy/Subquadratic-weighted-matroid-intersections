from sage.all import *
from Input import Input
from max_weight_intersection import maxWeightIntersection
from HelperFunctions import checkResult
import cProfile
import pstats
from math import log
import matplotlib.pyplot as plt
import numpy as np


def getDataPoint(size):
    input_ = Input.getRandomInput(size)

    profiler = cProfile.Profile()
    profiler.enable()

    S = maxWeightIntersection(input_)

    profiler.disable()

    assert checkResult(input_, S)

    ncalls = pstats.Stats(profiler).get_stats_profile().func_profiles["<method 'rank' of 'sage.matroids.matroid.Matroid' objects>"].ncalls
    return ncalls, input_.r, max(input_.w.values())

def getData(points):
    results = []
    for n in range(10, 10 + points):
        if(n % int(points/10) == 0):
            print("{}% done...".format((n-10)/points*100))
        ncalls, r, W = getDataPoint(n)
        results.append((n, int(ncalls), r, W))
    return results

def plot(results):
    x, y = [], []
    for result in results:
        n = result[0]
        ncalls = result[1]
        r = result[2]
        W = result[3]

        y.append(ncalls)
        x.append(n*r**(3/4)*log(r*W)*log(n))

    plt.title("Time complexity of subquadratic weighted matroid intersections")
    plt.xlabel("n*r**(3/4)*log(r*W)*log(n)")
    plt.ylabel("Calls to rank oracle")
    plt.scatter(x,y)

    axes = plt.gca()
    x_vals = np.array([0, axes.get_xlim()[-1]])
    plt.plot(x_vals, x_vals * 0.25, '--', label='slope=0.25')
    plt.plot(x_vals, x_vals * 0.5, '--', label='slope=0.5')
    plt.plot(x_vals, x_vals * 0.75, '--', label='slope=0.75')
    plt.legend()

    plt.show()

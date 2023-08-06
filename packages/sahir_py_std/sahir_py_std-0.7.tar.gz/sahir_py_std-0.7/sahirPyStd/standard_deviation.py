## This is just to practice creating packages

import numpy as np
import itertools

def standard_deviation(x):
    if type(x[0]) == list:
        list_flat = list(itertools.chain(*x))
    else:
        list_flat = x
    n = len(list_flat)
    mean = sum(list_flat) / n
    ssq = sum((x_i-mean)**2 for x_i in list_flat)
    stdev = (ssq/n)**0.5
    return(stdev)

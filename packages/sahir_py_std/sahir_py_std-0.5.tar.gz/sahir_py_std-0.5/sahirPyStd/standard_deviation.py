## This is just to practice creating packages

import numpy as np

def standard_deviation(x):
    ary =  np.array(x).flatten()
    n = len(ary)
    mean = sum(ary) / n
    ssq = sum((x_i-mean)**2 for x_i in ary)
    stdev = (ssq/n)**0.5
    return(stdev)

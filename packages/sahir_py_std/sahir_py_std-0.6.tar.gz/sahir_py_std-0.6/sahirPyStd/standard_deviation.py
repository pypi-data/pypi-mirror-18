## This is just to practice creating packages

import numpy as np

def standard_deviation(x):
    list_flat =  np.array(x).flatten().tolist()
    n = len(list_flat)
    mean = sum(list_flat) / n
    ssq = sum((x_i-mean)**2 for x_i in list_flat)
    stdev = (ssq/n)**0.5
    return(stdev)

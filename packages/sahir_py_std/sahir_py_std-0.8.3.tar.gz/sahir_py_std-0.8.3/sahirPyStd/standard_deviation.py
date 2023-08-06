import numpy as np
import itertools

def standard_deviation(x):
    
    if len(x) == 0:
        raise ValueError('No Values')
    elif len(x) == 1 and type(x[0]) != list:
        raise ValueError('No standard deviation of one number')
    else:
        list_flat = []
        for element in x:
            if type(element) != list:
                list_flat = list_flat + [[element]]
            else:
                list_flat = list_flat + [element]

list_flat = list(itertools.chain(*list_flat))
    n = len(list_flat)
    mean = sum(list_flat) / n
    ssq = sum((x_i-mean)**2 for x_i in list_flat)
    stdev = (ssq/n)**0.5
    return(stdev)

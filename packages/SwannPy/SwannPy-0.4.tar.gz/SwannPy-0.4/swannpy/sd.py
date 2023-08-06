def standard_deviation(x):
    '''
    Calculates the standard deviation of a vector of numerical values.
    Inputs: x, numerical vector
    Outputs float, the standard deviation of the numbers in x
    '''
    n = len(x)
    mean = sum(x) / n
    ssq = sum((x_i-mean)**2 for x_i in x)
    stdev = (ssq/n)**0.5
    return(stdev)

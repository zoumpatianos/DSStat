import numpy

def euclidean_distance(a, b):
    a = numpy.array(a)
    b = numpy.array(b)
    return numpy.linalg.norm(a-b)

def euclidean_distance_1arg(vals):
    a = numpy.array(val[0])
    b = numpy.array(val[1])
    return numpy.linalg.norm(a-b)

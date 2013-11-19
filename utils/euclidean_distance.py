import numpy

def euclidean_distance(a, b):
    a = numpy.array(a)
    b = numpy.array(b)
    return numpy.linalg.norm(a-b)

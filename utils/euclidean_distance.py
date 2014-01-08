import numpy
#import numexpr as ne
def euclidean_distance(a, b):
    a = numpy.array(a)
    b = numpy.array(b)
    r = numpy.linalg.norm(a-b)
    #r = numpy.sqrt(ne.evaluate("sum((a-b)**2)"))
    return r
def euclidean_distance_1arg(vals):
    a = numpy.array(val[0])
    b = numpy.array(val[1])
    return numpy.linalg.norm(a-b)

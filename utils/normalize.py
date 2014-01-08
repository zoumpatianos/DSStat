from __future__ import division
import numpy
import numexpr as ne

def normalize(q):
    q = numpy.array(q)
    std = numpy.std(q)
    mean = numpy.mean(q)
    q = (q - mean) / std
    return q

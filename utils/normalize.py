from __future__ import division
import numpy

def normalize(q):
    q = numpy.array(q)
    std = numpy.std(q)
    mean = numpy.mean(q)
    q = (q - std) / mean
    return q

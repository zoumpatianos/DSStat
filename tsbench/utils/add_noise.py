import numpy
import random

def add_noise(q, intensity=0.1, seed=4564):
    random.seed(seed)
    q = numpy.array(q)
    std = numpy.std(q)
    for pid in range(0, len(q)):
        q[pid] = q[pid] + (random.uniform(-1 * std, std)) * intensity
    return q

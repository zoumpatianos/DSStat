import random
from generator import Generator
from utils import normalize

class RandomWalkGenerator(Generator):
    def __init__(self, ts_length, seed=1422, mu=0, sigma=1):
        self.seed = seed
        self.ts_length = ts_length
        self.mu = mu
        self.sigma = sigma
        random.seed(1422)

    def generate(self, dataset_size):
        for i in range(dataset_size):
            ts = [[]] * self.ts_length
            ts[0] = 0
            for j in range(1, self.ts_length):
                ts[j] = ts[j-1] + random.gauss(self.mu, self.sigma)
            yield ts

if __name__ == "__main__":
    print "Testing Random Walk Generator..."
    rwalk = RandomWalkGenerator(ts_length=10)

    for ts in rwalk.generate(dataset_size=100000):
        print np.array(ts)
        #print "".join(map(lambda x: "\t%.5lf " % x, ts))

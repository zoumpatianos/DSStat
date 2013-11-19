import random
from utils.euclidean_distance import euclidean_distance
from utils.add_noise import add_noise
from utils.normalize import normalize

class InMemoryDistancesExperiment(object):
    def __init__(self, normalize=False, window=None):
        self.dataset = []
        self.loaded = 0
        self.normalize = normalize
        self.window = window

    def _load(self, ts):
        if self.window:
            for ts_win in self.window.window(ts):
                if normalize:
                    ts_win = normalize(ts_win)
                self.dataset += [ts_win]
        else:
            if normalize:
                ts = normalize(ts)
            self.dataset += [ts]

    def load_data(self, parser, size=None):
        self.loaded = 0
        for ts in parser.parse():
            self._load(ts)
            self.loaded += 1
            if size:
                if self.loaded >= size:
                    break

    def calculate_distances(self, qid, noise, sort=True):
        distances = []
        query = self.dataset[qid]
        if noise:
            query = add_noise(query, noise)
        for i in range(0, self.loaded):
            if i == qid:
                continue
            point = self.dataset[i]
            distances += [euclidean_distance(point, query)]

        if sort:
            distances = sorted(distances)
        return distances

    def run_queries(self, queries, noise, seed=10251):
        for i in range(0, queries):
            random.seed(seed + i)
            qid = random.randint(0, self.loaded - 1)
            yield self.calculate_distances(qid, noise)




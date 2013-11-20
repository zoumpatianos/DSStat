import random
import os
import datetime
import time
from utils.euclidean_distance import euclidean_distance
from utils.add_noise import add_noise
from utils.normalize import normalize
from plot.timeseries_plot import TimeSeriesPlot
from plot.distances_plot import DistancesPlot
from results.results_directory import ResultsDirectory


class InMemoryDistancesExperiment(object):
    def __init__(self, experiment=None, normalize=False, window=None):
        self.dataset = []
        self.loaded = 0
        self.normalize = normalize
        self.window = window
        if experiment:
            self.results_directory = ResultsDirectory(experiment)
        else:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
            self.results_directory = ResultsDirectory(st)
        print "Starting experiment (%s) with normalization: %s and window: %s" % (experiment, self.normalize, self.window)
        self.dataset_plot = TimeSeriesPlot()

    def _load(self, ts):
        if self.window:
            for ts_win in self.window.window(ts):
                if self.normalize:
                    ts_win = normalize(ts_win)
                self.dataset_plot.add_timeseries(ts_win)
                self.dataset += [ts_win]
        else:
            ts_win = ts
            if self.normalize:
                ts_win = normalize(ts)
            else:
                ts_win = ts
            self.dataset_plot.add_timeseries(ts_win)
            self.dataset += [ts_win]

    def load_data(self, parser, size=None):
        self.loaded = 0
        for ts in parser.parse():
            ts = self._load(ts)
            self.loaded += 1
            if size:
                if self.loaded >= size:
                    break
        self.dataset_plot.save(self.results_directory.create_filename("dataset.png"))

    def calculate_distances(self, qid, noise, sort=True):
        distances = []
        query = self.dataset[qid]
        if noise:
            plot = TimeSeriesPlot()
            plot.add_timeseries(query)
            query = add_noise(query, noise)
            plot.add_timeseries(query)
            plot.save(self.results_directory.create_filename("query_" + str(qid)+".pdf"))
        for i in range(0, self.loaded):
            if i == qid:
                continue
            point = self.dataset[i]
            distances += [euclidean_distance(point, query)]

        if sort:
            distances = sorted(distances)

        distances_histogram = DistancesPlot()
        distances_histogram.add_distances(distances)
        distances_histogram.save(self.results_directory.create_filename("query_" + str(qid) + "_dist_hist.pdf"))

        distnaces_ratio = DistancesPlot()
        distnaces_ratio.add_distances(distances / distances[0])
        distances_histogram.save(self.results_directory.create_filename("query_" + str(qid) + "_dist_ratio_hist.pdf"))

        return distances

    def run_queries(self, queries, noise, seed=10251):
        for i in range(0, queries):
            random.seed(seed + i)
            qid = random.randint(0, self.loaded - 1)
            yield self.calculate_distances(qid, noise)




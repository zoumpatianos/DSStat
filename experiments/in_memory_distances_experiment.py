import random
import os
import datetime
import time
import numpy
from utils.euclidean_distance import euclidean_distance, euclidean_distance_1arg
from utils.add_noise import add_noise
from utils.normalize import normalize
from plot.timeseries_plot import TimeSeriesPlot
from plot.distances_plot import DistancesPlot
from plot.workload_plot import WorkloadPlot
from results.results_directory import ResultsDirectory
from containers.file_container import FileContainer
from net.scp import SCP

class InMemoryDistancesExperiment(object):
    def __init__(self, experiment=None, normalize=False, window=None, overwrite=True):
        self.dataset = []
        self.loaded = 0
        self.queryset = []
        self.loaded_queries = 0
        self.normalize = normalize
        self.window = window
        if experiment:
            self.results_directory = ResultsDirectory(experiment, overwrite)
        else:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
            self.results_directory = ResultsDirectory(st)
        print "Starting experiment (%s) with normalization: %s and window: %s" % (experiment, self.normalize, self.window)
        self.dataset_plot = TimeSeriesPlot()
        self.queryset_plot = TimeSeriesPlot()

    def _load_query(self, ts):
        if self.window:
            for ts_win in self.window.window(ts):
                if self.normalize:
                    ts_win = normalize(ts_win)
                self.queryset_plot.add_timeseries(ts_win)
                self.queryset += [ts_win]
        else:
            ts_win = ts
            if self.normalize:
                ts_win = normalize(ts)
            else:
                ts_win = ts
            self.queryset_plot.add_timeseries(ts_win)
            self.queryset += [ts_win]

    def load_queries(self, parser, size=None):
        self.loaded_queries = 0
        for ts in parser.parse():
            ts = self._load_query(ts)
            self.loaded_queries += 1
            if size:
                if self.loaded_queries >= size:
                    break
        self.queryset_plot.save(self.results_directory.create_filename("queryset.png"))

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

    def calculate_distances(self, qid, noise, job_server=None, sort=True):
        distances = []
        if self.queryset:
            query = self.queryset[qid]
        else:
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
            if job_server:
                distances += [job_server.submit(euclidean_distance, (point, query,), (), ('numpy',))]
            else:
                distances += [euclidean_distance(point, query)]

        if job_server:
            for i in range(0,len(distances)):
                distances[i] = distances[i]()

        if sort:
            distances = sorted(distances)
        query_container = FileContainer(self.results_directory.create_filename("query_%d.txt" % qid), binary=False)
        query_container.write(query)
        query_container.close()

        distances_container = FileContainer(self.results_directory.create_filename("query_%d_distances.txt" % qid), binary=False)
        distances_container.write(distances)
        distances_container.close()

        distances_histogram = DistancesPlot()
        bins = distances_histogram.add_distances(distances, division_by=self.loaded)
        distances_histogram.save(self.results_directory.create_filename("query_" + str(qid) + "_dist_hist.pdf"))

        #distances_ratio = DistancesPlot()
        #distances_ratio.add_distances(distances / distances[0], ylabel="ratio to 1nn")
        #distances_ratio.save(self.results_directory.create_filename("query_" + str(qid) + "_dist_ratio_hist.pdf"))

        distances_plot = TimeSeriesPlot()
        distances_plot.add_timeseries(distances[0:100], ylabel="distance")
        distances_plot.save(self.results_directory.create_filename("query_" + str(qid) + "_dist_top100.png"))

        distances_plot = TimeSeriesPlot()
        distances_plot.add_timeseries((distances / distances[0])[0:100], ylabel="ratio to 1nn")
        distances_plot.save(self.results_directory.create_filename("query_" + str(qid) + "_dist_top100_ratios.png"))
        return distances

    def run(self, queries, noise, seed=10251, job_server = None):
        all_distances = []
        for i in range(0, queries):
            random.seed(seed + i)
            qid = random.randint(0, self.loaded_queries - 1)
            all_distances += [self.calculate_distances(qid, noise, job_server)]

        workload_plot = WorkloadPlot()
        workload_plot.add_workload(all_distances)
        workload_plot.save(self.results_directory.create_filename("workload_plot.pdf"))

    def finalize(self):
        remote_server = SCP("zoumpatianos@disi.unitn.it")
        self.results_directory.create_listing()
        remote_server.copy(self.results_directory.name, "public_html/", True)
        return self.results_directory.name


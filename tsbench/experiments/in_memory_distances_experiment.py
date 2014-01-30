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
    def __init__(self, experiment=None, normalize=False, window=None, overwrite=True, only_aggregates=True, in_memory=True):
        self.in_memory = in_memory
        self.dataset = []
        self.loaded = 0
        self.queryset = []
        self.loaded_queries = 0
        self.normalize = normalize
        self.window = window
        self.only_aggregates = only_aggregates
        if experiment:
            self.results_directory = ResultsDirectory(experiment, overwrite)
        else:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
            self.results_directory = ResultsDirectory(st)
        print "Starting experiment (%s) with normalization: %s and window: %s" % (experiment, self.normalize, self.window)
        if not self.only_aggregates:
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
            if not self.only_aggregates:
                self.queryset_plot.add_timeseries(ts_win)
            self.queryset += [ts_win]

    def load_queries(self, parser, size=None, progress_update=lambda x: x):
        self.loaded_queries = 0
        for ts in parser.parse():
            ts = self._load_query(ts)
            self.loaded_queries += 1
            progress_update((self.loaded_queries, size))
            if size:
                if self.loaded_queries >= size:
                    break
        if not self.only_aggregates:
            self.queryset_plot.save(self.results_directory.create_filename("queryset.png"))

    def _load(self, ts):
        if self.window:
            for ts_win in self.window.window(ts):
                if self.normalize:
                    ts_win = normalize(ts_win)
                if not self.only_aggregates:
                    self.dataset_plot.add_timeseries(ts_win)
                self.dataset += [ts_win]
        else:
            ts_win = ts
            if self.normalize:
                ts_win = normalize(ts)
            else:
                ts_win = ts

            if not self.only_aggregates:
                self.dataset_plot.add_timeseries(ts_win)
            self.dataset += [ts_win]

    def load_data(self, parser, size=None, progress_update=lambda x: x):
        if self.in_memory == False:
            self.dataset = parser
            self.loaded = size
            return

        self.loaded = 0
        for ts in parser.parse():
            ts = self._load(ts)
            self.loaded += 1
            progress_update((self.loaded, size))
            if size:
                if self.loaded >= size:
                    break
        if not self.only_aggregates:
            self.dataset_plot.save(self.results_directory.create_filename("dataset.png"))

    def calculate_contrasts(self, queries, kset, job_server=None, sort=True):
        all_contrasts = {}
        for k in kset:
            all_contrasts[k] = []
        all_distances = []
        for i in range(len(queries)):
            all_distances += [[]]

        for i in range(0, self.loaded):
            if self.in_memory:
                point = self.dataset[i]
            else:
                point = next(self.dataset.parse())

            for query_id in range(len(queries)):
                query = queries[query_id]
                if job_server:
                    all_distances[query_id] += [job_server.submit(euclidean_distance, (point, query,), (), ('numpy',))]
                else:
                    all_distances[query_id] += [euclidean_distance(point, query)]


        if job_server:
            for i in range(0,len(all_distances)):
                for j in range(0, len(all_distances[i])):
                    all_distances[i][j] = all_distances[i][j]()


        for i in range(0,len(all_distances)):
            all_distances[i] = sorted(all_distances[i])

        writter = FileContainer("output.txt", False)
        for d in all_distances:
            writter.write(d)
        writter.close()

        for k in kset:
            for distances in all_distances:
                all_contrasts[k] += [distances[k] / distances[k-1]]

        return all_contrasts

    def run(self, nqueries, noise, kset=[1], seed=10251, job_server = None, progress_update=lambda x: x):
        all_distances = []
        queries = []

        # Prepare queries and load them in memory
        for i in range(0, nqueries):
            random.seed(seed + i)
            qid = random.randint(0, self.loaded_queries - 1)
            if self.queryset:
                query = self.queryset[qid]
            else:
                query = self.dataset[qid]
            if noise:
                if not self.only_aggregates:
                    plot = TimeSeriesPlot()
                    plot.add_timeseries(query)
                query = add_noise(query, noise)
                if not self.only_aggregates:
                    plot.add_timeseries(query)
                    plot.save(self.results_directory.create_filename("query_" + str(qid)+".pdf"))
            queries += [query]

        # Calculate contrasts for each k
        all_contrasts = self.calculate_contrasts(queries, kset, job_server)
        for k in kset:
            distances_plot = DistancesPlot()
            distances_plot.add_distances(all_contrasts[k], division_by=len(all_contrasts[k]), max_bin=2, bin_step=0.01)
            print all_contrasts[k]
            distances_plot.save(self.results_directory.create_filename("contrasts_distribution_top-%d.pdf" % k))

    def finalize(self):
        remote_server = SCP("zoumpatianos@disi.unitn.it")
        self.results_directory.create_listing()
        remote_server.copy(self.results_directory.name, "public_html/", True)
        return self.results_directory.name


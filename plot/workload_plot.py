from plot import Plot
import matplotlib.pyplot as plt
import numpy

class WorkloadPlot(Plot):
    def add_workload(self, workload, num_bins=20):
        all_distances = [item for sublist in workload for item in sublist]
        min_max = (min(all_distances), max(all_distances))
        all_histograms = []
        for distances in all_distances:
            all_histograms += [numpy.array(map(float, numpy.histogram(distances, range=min_max, bins=num_bins)[0]))/distances.size]
        bins = num_bins * [[]]
        means = num_bins * [[]]
        stds = num_bins * [[]]
        for cbin in range(0, num_bins):
            for histogram in all_histograms:
                bins[cbin] += [histogram[cbin]]
            means[cbin] = numpy.mean(bins[cbin])
            stds[cbin] = numpy.std(bins[cbin])
        plt.errorbar(x=range(0, num_bins), y=means, yerr=stds)
        print stds
        print means

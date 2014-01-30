from plot import Plot
import matplotlib.pyplot as plt
import numpy

# ADD plot (Average Distance Distribution)
class WorkloadPlot(Plot):
    def add_workload(self, workload, num_bins=20, xlabel="distance", ylabel="percentage"):
        print len(workload)
        all_distances = [item for sublist in workload for item in sublist]
        min_max = (min(all_distances), max(all_distances))
        all_histograms = []
        for distances in workload:
            all_histograms += [numpy.array(map(float, numpy.histogram(distances, range=min_max, bins=num_bins)[0]))/len(distances)]
        bins = num_bins * [[]]
        means = num_bins * [[]]
        stds = num_bins * [[]]
        for cbin in range(0, num_bins):
            val = []
            for histogram in all_histograms:
                val += [histogram[cbin]]
            means[cbin] = numpy.mean(val)
            stds[cbin] = numpy.std(val)
            #print bins[cbin]
        plt.errorbar(x=range(0, num_bins), y=means, yerr=stds)
        plt.xlabel(xlabel, fontsize=self.fontsize)
        plt.ylabel(ylabel, fontsize=self.fontsize)
#        print stds
#        print means

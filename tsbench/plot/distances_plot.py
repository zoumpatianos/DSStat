from plot import Plot
import numpy as np
import matplotlib.pyplot as plt

class DistancesPlot(Plot):
    def add_distances(self, values, xlabel="absolute distance", ylabel="percentage", division_by=1, max_bin=100, bin_step=1):
        ax = self.fig.add_subplot(111)
        hist = np.histogram(values, bins=np.arange(max_bin, step=bin_step))
        y = np.array(map(float, hist[0]))/division_by

        ax.plot(range(0, len(y)), y)
        plt.xlabel(xlabel, fontsize=self.fontsize)
        plt.ylabel(ylabel, fontsize=self.fontsize)
        return y

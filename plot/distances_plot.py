from plot import Plot
import numpy as np
class DistancesPlot(Plot):
    def add_distances(self, values):
        ax = self.fig.add_subplot(111)
        hist = np.histogram(values, bins=np.arange(100))
        y = hist[0]
        ax.plot(range(0, len(y)), y)

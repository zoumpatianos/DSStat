from plot import Plot
from matplotlib import pyplot as plt

class TimeSeriesPlot(Plot):
    def add_timeseries(self, values, xlabel="time", ylabel="value"):
        ax = self.fig.add_subplot(111)
        ax.plot(range(0, len(values)), values)
        plt.xlabel(xlabel, fontsize=self.fontsize)
        plt.ylabel(ylabel, fontsize=self.fontsize)

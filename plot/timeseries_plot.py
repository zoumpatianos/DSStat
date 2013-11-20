from plot import Plot

class TimeSeriesPlot(Plot):
    def add_timeseries(self, values):
        ax = self.fig.add_subplot(111)
        ax.plot(range(0, len(values)), values)

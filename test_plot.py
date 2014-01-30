from plot.timeseries_plot import TimeSeriesPlot

if __name__ == "__main__":
    plot = TimeSeriesPlot()
    plot.add_timeseries([1,2,5,6,3,2,9,8,1,5,2,3,6,8])
    plot.add_timeseries([3,6,8,7,8,9,3,1,4,5,6,8,7,1])
    plot.save("plot.pdf")

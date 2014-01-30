import sys
import numpy as np
from parsers.binary_parser import BinaryParser
from plot.timeseries_plot import TimeSeriesPlot
from containers.file_container import FileContainer

if __name__ == "__main__":
    filecontainer = FileContainer("good.bin")
    wrongplot = TimeSeriesPlot()
    goodplot = TimeSeriesPlot()
    parser = BinaryParser(sys.argv[1], int(sys.argv[2]))
    generator = parser.parse()
    total = 0
    not_sane = 0
    for ts in generator:
        normts = (np.array(ts) - np.mean(ts)) / np.std(ts)
        if np.std(ts) < float(sys.argv[3]) or np.amax(normts) > int(sys.argv[4]) or np.amin(normts) < (int(sys.argv[4]) * -1):
            wrongplot.add_timeseries(ts)
            not_sane += 1
        else:
            filecontainer.write(ts)
            goodplot.add_timeseries(normts)
        total += 1
        if total % 1000 == 0:
            print "\r%d %d" % (total, not_sane)
    print "Not sane: %d out of %d (%lf percent)" % (not_sane, total, not_sane / total)
    wrongplot.save("wrong.png")
    goodplot.save("good.png")
    filecontainer.close()

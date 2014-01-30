from tsbench.plot.timeseries_plot import TimeSeriesPlot
from tsbench.parsers.binary_parser import BinaryParser
from tsbench.net.scp import SCP
import sys
import numpy as np

if __name__ == "__main__":
    dataset = sys.argv[1]
    datalength = int(sys.argv[2])
    plotfile = sys.argv[3]
    if len(sys.argv) > 4:
        normalized = (sys.argv[4] == "normalize")
    else:
        normalized = False

    plot = TimeSeriesPlot()
    parser = BinaryParser(dataset, datalength)
    count = 0
    for ts in parser.parse():
        count += 1
        if count % 1000 == 0:
            print "Processed: %d" % (count)
        if normalized:
            normts = (ts - np.mean(ts)) / np.std(ts)
            plot.add_timeseries(normts)
        else:
            plot.add_timeseries(ts)
    plot.save(plotfile)
    scp = SCP("disi.unitn.it")
    scp.copy(plotfile, "public_html/")

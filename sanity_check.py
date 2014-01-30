import sys
import numpy as np
from tsbench.parsers.binary_parser import BinaryParser
from tsbench.plot.timeseries_plot import TimeSeriesPlot
from tsbench.containers.file_container import FileContainer

if __name__ == "__main__":
    filecontainer = FileContainer("good.bin")
    wrongplot = TimeSeriesPlot()
    parser = BinaryParser(sys.argv[1], int(sys.argv[2]))
    if len(sys.argv) > 5:
        limit = int(sys.argv[5])
    else:
        limit = 0

    generator = parser.parse()
    total = 0
    not_sane = 0
    for ts in generator:
        if limit:
            if limit <= (total - not_sane):
                break;

        normts = (np.array(ts) - np.mean(ts)) / np.std(ts)
        if np.std(ts) < float(sys.argv[3]) or np.amax(normts) > int(sys.argv[4]) or np.amin(normts) < (int(sys.argv[4]) * -1):
            wrongplot.add_timeseries(normts)
            not_sane += 1
        else:
            filecontainer.write(ts)
        total += 1
        if total % 1000 == 0:
            print "\r%d %d" % (total, not_sane)
    print "Not sane: %d out of %d (%lf percent)" % (not_sane, total, not_sane / total)
    wrongplot.save("wrong.png")
    filecontainer.close()

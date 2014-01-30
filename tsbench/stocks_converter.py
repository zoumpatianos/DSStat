import sys
import numpy
from parsers.stocks_file_parser import StocksFileParser
from filters.size_filter import SizeFilter
from window.sliding_window import SlidingWindow
from containers.file_container import FileContainer

def sane(ts):
    return numpy.std(ts) != 0

if __name__ == "__main__":
    parser = StocksFileParser(sys.argv[1])

#    parser.add_filter(SizeFilter(int(sys.argv[2])))
    filecontainer = FileContainer(sys.argv[3])
    window = SlidingWindow(int(sys.argv[2]), int(sys.argv[2]))

    generator = parser.parse()

    total = 0
    for ts in generator:
        for ts_slide in window.window(ts):
            if not sane(ts_slide):
                print ts_slide
                continue

            total += 1
            print "\r%d" % total
            filecontainer.write(ts_slide)

    filecontainer.close()

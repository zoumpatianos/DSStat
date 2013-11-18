import sys
from parsers.stocks_file_parser import StocksFileParser
from filters.size_filter import SizeFilter
from window.sliding_window import SlidingWindow
from containers.file_container import FileContainer

if __name__ == "__main__":
    stock = StocksFileParser(sys.argv[1])
    stock.add_filter(SizeFilter(int(sys.argv[2])))
    sliding = SlidingWindow(int(sys.argv[3]))
    filecontainer = FileContainer(sys.argv[4])
    total = 0
    for ts in sliding.window(stock.parse()):
        total += 1
        print "\r%d" % total
        filecontainer.write(ts)
    filecontainer.close()

import sys
from parsers.stocks_file_parser import StocksFileParser
from filters.size_filter import SizeFilter
from window.sliding_window import SlidingWindow
from containers.file_container import FileContainer

if __name__ == "__main__":
    parser = StocksFileParser(sys.argv[1])

    parser.add_filter(SizeFilter(int(sys.argv[2])))
    filecontainer = FileContainer(sys.argv[3])

    generator = parser.parse()

    total = 0
    for ts in generator:
        total += 1
        print "\r%d" % total
        filecontainer.write(ts)
    filecontainer.close()

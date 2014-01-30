import sys
from tsbench.parsers.ascii_parser import AsciiParser
from tsbench.filters.size_filter import SizeFilter
from tsbench.window.sliding_window import SlidingWindow
from tsbench.containers.file_container import FileContainer

if __name__ == "__main__":
    parser = AsciiParser(sys.argv[1])
    filecontainer = FileContainer(sys.argv[2])

    generator = parser.parse()

    total = 0
    for ts in generator:
        total += 1
        if total % 1000 == 0:
            print "\r%d" % total
        filecontainer.write(ts)
    filecontainer.close()

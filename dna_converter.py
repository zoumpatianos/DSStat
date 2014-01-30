import sys
from tsbench.parsers.dna_parser import DNAParser
from tsbench.filters.size_filter import SizeFilter
from tsbench.window.sliding_window import SlidingWindow
from tsbench.containers.file_container import FileContainer

if __name__ == "__main__":
    dnaparser = DNAParser(sys.argv[1])
    filecontainer = FileContainer(sys.argv[2])
    containers = []
    for ts in dnaparser.parse():
        filecontainer.write(ts)
    filecontainer.close()


import sys
from parsers.dna_parser import DNAParser
from filters.size_filter import SizeFilter
from window.sliding_window import SlidingWindow
from containers.file_container import FileContainer

if __name__ == "__main__":
    dnaparser = DNAParser(sys.argv[1])
    filecontainer = FileContainer(sys.argv[2])
    containers = []
    for ts in dnaparser.parse():
        filecontainer.write(ts)
    filecontainer.close()


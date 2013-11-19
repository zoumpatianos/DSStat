import sys
from parsers.physionet_parser import PhysionetParser
from filters.size_filter import SizeFilter
from window.sliding_window import SlidingWindow
from containers.file_container import FileContainer

if __name__ == "__main__":
    physioparser = PhysionetParser(sys.argv[1])
    for ts in physioparser.parse():
        print ts

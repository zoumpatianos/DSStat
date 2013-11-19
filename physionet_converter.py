import sys
from parsers.physionet_parser import PhysionetParser
from filters.size_filter import SizeFilter
from window.sliding_window import SlidingWindow
from containers.file_container import FileContainer

if __name__ == "__main__":
    physioparser = PhysionetParser(sys.argv[1])
    containers = []
    for channels in physioparser.parse():
        for channel in range(0, len(channels)):
            if len(containers) < channel + 1:
                containers += [FileContainer(sys.argv[2] + ".channel_%d" % channel)]
            containers[channel].write(channels[channel])


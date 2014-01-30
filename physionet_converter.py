import sys
from tsbench.parsers.physionet_parser import PhysionetParser
from tsbench.filters.size_filter import SizeFilter
from tsbench.window.sliding_window import SlidingWindow
from tsbench.containers.file_container import FileContainer

if __name__ == "__main__":
    physioparser = PhysionetParser(sys.argv[1])
    containers = []
    for channels in physioparser.parse():
        for channel in range(0, len(channels)):
            if len(containers) < channel + 1:
                containers += [FileContainer(sys.argv[2] + ".channel_%d" % channel, binary=False)]
            containers[channel].write(channels[channel])


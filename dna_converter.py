import sys
from parsers.dna_parser import DNAParser
from filters.size_filter import SizeFilter
from window.sliding_window import SlidingWindow
from containers.file_container import FileContainer

if __name__ == "__main__":
    dnaparser = DNAParser(sys.argv[1])
    containers = []
    for channels in dnaparser.parse():
        for channel in range(0, len(channels)):
            if len(containers) < channel + 1:
                containers += [FileContainer(sys.argv[2] + ".channel_%d" % channel, binary=False)]
            containers[channel].write(channels[channel])


import tarfile
import sys
import struct
from itertools import islice

class Parser(object):
    def __init__(self, input_file):
        self.input_file = input_file
        self._filters = []

    def _apply_filters(self, ts):
        for f in self._filters:
            ts = f.apply(ts)
        return ts

    def add_filter(self, f):
        self._filters += [f]

class Filter(object):
    def __init__(self):
        pass

class Container(object):
    def __init__(self):
        pass

class Window(object):
    def __init__(self):
        pass

class SlidingWindow(Window):
    def __init__(self, win_size, step=1):
        self.winSize = win_size
        self.step = step

    def window(self, parser):
        for sequence in parser:
            # Verify the inputs
            try:
                it = iter(sequence)
            except TypeError:
                raise Exception("**ERROR** sequence must be iterable.")
            numOfChunks = ((len(sequence)-self.winSize)/self.step)+1
            # Do the work
            for i in range(0,numOfChunks*self.step,self.step):
                yield sequence[i:i+self.winSize]


class SizeFilter(Filter):
    def __init__(self, size):
        self.size = size

    def apply(self, ts):
        if len(ts) > self.size:
            return ts[0:self.size]
        else:
            return None

class FileContainer(object):
    def __init__(self, filename, binary=True):
        self.filename = filename
        self.binary = binary
        if self.binary:
            self.f = open(filename, "wb")
        else:
            self.f = open(filename, "w")

    def write(self, ts):
        if self.binary:
            s = struct.pack('f'*len(ts), *ts)
            self.f.write(s)
        else:
            self.f.write(" ".join(ts))

    def close(self):
        self.f.close()


class StocksFileParser(Parser):
    def parse(self):
        tar = tarfile.open(self.input_file, "r:gz")
        for file in tar.getmembers():
            ts = []
            f=tar.extractfile(file)
            content=f.read()
            lines = content.split("\n")[1:]
            for line in lines:
                tokens = line.split(",")
                try:
                    if len(tokens) > 4:
                        ts += [float(tokens[4])]
                except:
                    pass
            ts = self._apply_filters(ts)
            if ts:
                yield ts

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

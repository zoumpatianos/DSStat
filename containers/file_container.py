import struct
from container import Container

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

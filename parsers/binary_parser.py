import struct
from parser import Parser

class BinaryParser(Parser):
    MULTICHANNEL=False

    def __init__(self, filename, ts_size):
        self.filename = filename
        self.ts_size = ts_size
        self._filters = []

    def read(self):
        ts = []
        with open(self.filename, "rb") as f:
            while True:
                buf = f.read(4)
                if not buf: break
                val = struct.unpack('f', buf)
                ts += [val[0]]
                if len(ts) == self.ts_size:
                    yield ts
                    ts = []

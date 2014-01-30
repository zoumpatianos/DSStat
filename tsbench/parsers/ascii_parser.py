import struct
from parser import Parser
import re

class AsciiParser(Parser):
    MULTICHANNEL=False

    def __init__(self, filename):
        self.filename = filename
        self._filters = []

    def read(self):
        ts = []
        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    ts = map(float, line.split(" "))
                    yield ts

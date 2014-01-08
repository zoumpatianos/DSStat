import glob
import subprocess
import os
import re
from parser import Parser

class DNAParser(Parser):
    MULTICHANNEL=True

    def __init__(self, dataset):
        self.dataset = dataset
        self._filters = []

    def read(self):
        filenames = glob.glob("%s/*.fa" % self.dataset)
        print filenames
        return
        for filepath in filenames:
            channels = None
            filename = os.path.basename(filepath)
            p = subprocess.Popen(self.BINARY + filename, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 cwd=self.dataset)
            for line in p.stdout.readlines():
                line = re.sub(r' +', ' ', line)
                line = re.sub(r'^ ', '', line)
                channel_values = line.split(" ")
                if not channels:
                    channels = [[]] * len(channel_values)
                chid = 0
                # In case of error
                if channel_values[0] == "getvec:":
                    continue
                for val in channel_values:
                    channels[chid] += [float(val)]
                    chid += 1

            yield channels

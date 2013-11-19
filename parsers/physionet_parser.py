import glob
import subprocess
import os
import re
from parser import Parser

class PhysionetParser(Parser):
    BINARY="LD_LIBRARY_PATH=/home/zoumpatianos/tsbench-datasets/CODE/tscandy/bin/wfdb-10.5.20/build/lib64 /home/zoumpatianos/tsbench-datasets/CODE/tscandy/bin/wfdb-10.5.20/build/bin/rdsamp -r "

    def __init__(self, dataset):
        self.dataset = dataset

    def parse(self, channel=None):
        filenames = glob.glob("%s/*.hea" % self.dataset)
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
                print channel_values
                print channels
                for val in channel_values:
                    channels[chid] += [float(val)]
                    chid += 1
            if not channel:
                yield channels
            else:
                yield channels[channel]

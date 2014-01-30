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
        filenames = map(lambda x: x[1], sorted(zip(map(lambda x: int(x.split(".")[-2]), filenames), filenames), key = lambda key: key[0]))
        for filename in filenames:
            fid = open(filename, "r")
            time_series = []
            prev = 0
            for line in fid:
                if line[0] == ">":
                    continue
                for nucleo_base in line:
                    if nucleo_base == '\n':
                        continue
                    index = 0
                    if nucleo_base =='a' or nucleo_base == 'A':
                        index = 2;
                    elif nucleo_base=='g' or nucleo_base=='G':
                        index = 1;
                    elif nucleo_base=='c' or nucleo_base=='C':
                        index = -1;
                    elif nucleo_base=='t' or nucleo_base=='T':
                        index = -2;
                    else:
                        #print "Got: ", nucleo_base, line
                        #print "Found a non A,T,C,G!!!"
                        index = 0;
                    time_series += [prev + index]
                    prev = time_series[-1]
                    if len(time_series) == 640:
                        yield time_series
                        time_series = []


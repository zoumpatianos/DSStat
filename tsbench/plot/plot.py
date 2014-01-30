import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Plot(object):
    def __init__(self, fontsize=18):
        self.fig = plt.figure()
        self.fontsize = fontsize
    def save(self, filename):
        plt.savefig(filename)
    def show(self):
        plt.show()


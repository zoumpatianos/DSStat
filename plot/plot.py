import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Plot(object):
    def __init__(self):
        self.fig = plt.figure()
    def save(self, filename):
        plt.savefig(filename)
    def show(self):
        plt.show()


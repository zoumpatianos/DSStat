from filter import Filter

class SizeFilter(Filter):
    def __init__(self, size):
        self.size = size

    def apply(self, ts):
        if len(ts) > self.size:
            return ts[0:self.size]
        else:
            return None

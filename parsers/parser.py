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


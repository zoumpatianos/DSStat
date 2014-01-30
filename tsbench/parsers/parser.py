class Parser(object):
    MULTICHANNEL=False

    def __init__(self, input_file):
        self.input_file = input_file
        self._filters = []

    def _apply_filters(self, ts):
        for f in self._filters:
            ts = f.apply(ts)
        return ts

    def add_filter(self, f):
        self._filters += [f]

    def parse(self):
        for ts in self.read():
            if self.MULTICHANNEL:
                for chid in range(0, len(ts)):
                    ts[chid] = self._apply_filters(ts[chid])
            else:
                 ts = self._apply_filters(ts)

            if not ts:
                continue
            else:
                yield ts

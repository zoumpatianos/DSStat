from window import Window


class SlidingWindow(Window):
    def __init__(self, win_size, step=1):
        self.winSize = win_size
        self.step = step

    def window(self, parser):
        for sequence in parser:
            # Verify the inputs
            try:
                it = iter(sequence)
            except TypeError:
                raise Exception("**ERROR** sequence must be iterable.")
            numOfChunks = ((len(sequence)-self.winSize)/self.step)+1
            # Do the work
            for i in range(0,numOfChunks*self.step,self.step):
                yield sequence[i:i+self.winSize]

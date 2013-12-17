from parser import Parser

class GeneratorWrapperParser(Parser):
    MULTICHANNEL=False

    def __init__(self, generator, dataset_size):
        self.generator = generator
        self.dataset_size = dataset_size
        self._filters = []

    def read(self):
        for ts in self.generator.generate(self.dataset_size):
            yield ts

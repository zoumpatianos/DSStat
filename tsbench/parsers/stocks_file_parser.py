import tarfile
from parser import Parser

class StocksFileParser(Parser):
    MULTICHANNEL=False
    def read(self):
        tar = tarfile.open(self.input_file, "r:gz")
        for file in tar.getmembers():
            ts = []
            f=tar.extractfile(file)
            content=f.read()
            lines = content.split("\n")[1:]
            for line in lines:
                tokens = line.split(",")
                try:
                    if len(tokens) > 4:
                        ts += [float(tokens[4])]
                except:
                    pass
            yield ts

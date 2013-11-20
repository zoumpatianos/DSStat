import os
import shutil
import tarfile
from experiments.results.utils.make_html_page import makeHTMLpage

class ResultsDirectory(object):
    def __init__(self, name, overwrite=True):
        self.name = name
        if os.path.exists(self.name):
            if overwrite:
                shutil.rmtree(self.name)
                os.mkdir(self.name)
        else:
            os.mkdir(self.name)
    def create_filename(self, filename):
        return os.path.join(self.name, filename)
    def create_listing(self):
        index = makeHTMLpage(self.name)
        index_file = open(self.create_filename("index.html"), "w")
        index_file.write(index)
        index_file.close()
    def zip_directory(self):
        filename = self.name + ".tar.gz"
        tar = tarfile.open(filename, 'w:gz')
        tar.add(self.name)
        tar.close()
        return filename

import os
import tarfile
from experiments.results.utils.make_html_page import makeHTMLpage

class ResultsDirectory(object):
    def __init__(self, name):
        self.name = name
        os.mkdir(name)
    def create_filename(self, filename):
        return os.path.join(self.name, filename)
    def create_listing(self):
        index = makeHTMLpage(self.name)
        index_file = open(self.create_filename("index.html"), "w")
        index_file.write(index)
        index_file.close()
    def zip_directory(self, target_file):
        tar = tarfile.open(self.name + '.tar.gz'), 'w:gz')
        tar.add(self.name)
        tar.close()
    def copy_directory(self, target):
        pass

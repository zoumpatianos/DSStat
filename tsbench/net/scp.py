import subprocess

class SCP(object):
    def __init__(self, server):
        self.server = server
    def copy(self, filename, destination, is_directory=False):
        command = ["scp"]
        if is_directory:
            command += ["-r"]
        command += [filename]
        command += [self.server + ":" + destination]
        subprocess.call(command)

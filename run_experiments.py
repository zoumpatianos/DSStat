from __future__ import division
from math import floor
import pp
import sys
from experiments.in_memory_distances_experiment import InMemoryDistancesExperiment
from parsers.binary_parser import BinaryParser
from parsers.ascii_parser import AsciiParser
from containers.file_container import FileContainer

def progress_f(progress):
    if not progress[1]:
        return
    percentage = ((progress[0] / progress[1]) * 100)
    if (percentage % 1 == 0):
        sys.stdout.write("\r%d%%" % percentage)
        sys.stdout.flush()

if __name__ == "__main__":
    ncpus = 1
    ppservers = ()
    job_server = None#pp.Server(ncpus=ncpus, ppservers=ppservers)

    #parser = BinaryParser(filename=sys.argv[1], ts_size=int(sys.argv[2]))
    dataset_filename = sys.argv[1]
    queryset_filename = sys.argv[2]
    ts_size = int(sys.argv[3])
    dataset_size = int(sys.argv[4])
    queries_size = int(sys.argv[5])

    experiment = InMemoryDistancesExperiment("test_experiment", normalize=True, window=None)
    dataset_parser = AsciiParser(filename=dataset_filename, ts_size=ts_size)
    query_parser = AsciiParser(filename=queryset_filename, ts_size=ts_size)

    print "Loading data..."
    experiment.load_data(dataset_parser, dataset_size, progress_update=progress_f)
    print "Loaded: %d time series." % len(experiment.dataset)

    print "Loading queries..."
    experiment.load_queries(query_parser, progress_update=progress_f)
    print "Loaded: %d time series." % len(experiment.queryset)

    print "Running experiment..."
    experiment.run(queries_size, noise=0, job_server=job_server, progress_update=progress_f)

    print "Experiment finished..."
    output = experiment.finalize()

    print "Created: %s" % output


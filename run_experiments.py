from experiments.in_memory_distances_experiment import InMemoryDistancesExperiment
from parsers.binary_parser import BinaryParser
from containers.file_container import FileContainer

if __name__ == "__main__":
    import sys
    parser = BinaryParser(filename=sys.argv[1], ts_size=int(sys.argv[2]))
    experiment = InMemoryDistancesExperiment("test_experiment", normalize=True, window=None)

    print "Loading data..."
    experiment.load_data(parser)
    print "Loaded: %d time series." % len(experiment.dataset)

    print "Running experiment..."
    experiment.run(10, noise=0.5)

    print "Experiment finished..."
    output = experiment.finalize()

    print "Created: %s" % output


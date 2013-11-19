from experiments.random_queries_experiment import RandomQueriesExperiment
from parsers.binary_parser import BinaryParser

if __name__ == "__main__":
    import sys
    parser = BinaryParser(sys.argv[1], int(sys.argv[2]))
    experiment = RandomQueriesExperiment(normalize=True, window=None)
    print "Loading data..."
    experiment.load_data(parser, 100)
    print "Loaded: %d time series." % len(experiment.dataset)
    print "Running 10 queries with 0 noise"
    experiment.run(10, noise=0.1)

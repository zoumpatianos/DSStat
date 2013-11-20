from experiments.in_memory_distances_experiment import InMemoryDistancesExperiment
from parsers.binary_parser import BinaryParser
from containers.file_container import FileContainer

if __name__ == "__main__":
    import sys
    parser = BinaryParser(sys.argv[1], int(sys.argv[2]))
    experiment = InMemoryDistancesExperiment(normalize=True, window=None)

    print "Loading data..."
    experiment.load_data(parser, 100)
    print "Loaded: %d time series." % len(experiment.dataset)


    print "Running queries..."
    experiment_output_container = FileContainer("output.txt", binary=False)
    for query_result in experiment.run_queries(10, noise=0.1):
        experiment_output_container.write(query_result)
    experiment_output_container.close()

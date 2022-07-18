from os import listdir
from os.path import isfile, join
from executeCallGraphGenerator import executeCallGraphGenerator

def collectingGeneratedAndRetrievedCallGraphs(args, unknown_pkgs, url):

    print("Call Graphs Retrieval:")

    call_graphs = executeCallGraphGenerator(unknown_pkgs, args.fasten_data)

    return call_graphs

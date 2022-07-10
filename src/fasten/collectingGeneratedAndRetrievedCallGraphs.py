from executeCallGraphGenerator import executeCallGraphGenerator
from os import listdir
from os.path import isfile, join

def collectingGeneratedAndRetrievedCallGraphs(args, unknown_pkgs, url):

    print("Call Graphs Retrieval:")

    executeCallGraphGenerator(unknown_pkgs, args.fasten_data)

    cg_path = args.fasten_data
    generated_cg_paths = [f for f in listdir(cg_path) if isfile(join(cg_path, f))]
    generated_cg_paths_mod = []

    for cg in generated_cg_paths:
        cg = cg_path + "/" + cg
        generated_cg_paths_mod.append(cg)

    cg_list = generated_cg_paths_mod

    return cg_list

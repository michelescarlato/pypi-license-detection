from executeCallGraphGenerator import executeCallGraphGenerator, deleteCallGraphsDir
from requestFastenKnownAndUnknownLists import RequestFastenKnownAndUnknownLists
from os import listdir
from os.path import isfile, join
def collectingGeneratedAndRetrievedCallGraphs(args, all_pkgs, url):

    cg_directory_local = "cg_producing"
    deleteCallGraphsDir(cg_directory_local)
    print("Call Graphs Retrieval:")
    received_cg_location, known_call_graphs, unknown_call_graphs, call_graphs_connectivity_issues = RequestFastenKnownAndUnknownLists.requestFastenKnownAndUnknownLists(args, all_pkgs, url, "rcg")
    unknown_call_graphs_and_connectivity_issues = {**unknown_call_graphs, **call_graphs_connectivity_issues}
    generated_cg_paths_broken = executeCallGraphGenerator(unknown_call_graphs_and_connectivity_issues, args.fasten_data)#,cg_directory_local)
    # merging lists of retrieved and generated call graphs location

    cg_path = args.fasten_data
    generated_cg_paths = [f for f in listdir(cg_path) if isfile(join(cg_path, f))]
    generated_cg_paths_mod = []
    for cg in generated_cg_paths:
        cg = cg_path + "/" + cg
        generated_cg_paths_mod.append(cg)
    cg_list = generated_cg_paths_mod + received_cg_location
    return cg_list

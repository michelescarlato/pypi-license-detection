import os.path
from pycg_producer.producer import CallGraphGenerator


def executeCallGraphGenerator(unknown_pkgs, fasten_data):
    """Create dictonary necessary for 'CallGraphGenerator'."""

    global cg_paths
    cg_paths = []

    for package in unknown_pkgs:

        pkg_version = unknown_pkgs[package]

        coord = { "product": ""+package+"",
              "version": ""+pkg_version+"",
              "version_timestamp": "2000",
              "requires_dist": [] }

        cg_path_local = fasten_data + "callgraphs"+ "/" + package[0] + "/" + package + "/" + pkg_version + "/" + "cg.json"
        executeSingleCallGraphGeneration(coord, fasten_data, cg_path_local)

    return cg_paths


def executeSingleCallGraphGeneration(coord, directoryName, cg_path_local):
    """Create Call Graph for a single package."""

    generator = CallGraphGenerator(directoryName, coord)
    generator.generate()

    if os.path.isfile(cg_path_local):
        print("Call graph generated at: "+cg_path_local)
        cg_paths.append(cg_path_local)
    else:
        print("%s has not been generated!" % cg_path_local)

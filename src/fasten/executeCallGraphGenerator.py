import os.path
from pycg_producer.producer import CallGraphGenerator


def executeCallGraphGenerator(args, unknown_pkgs):
    """Create dictonary necessary for 'CallGraphGenerator'."""

    global call_graphs
    call_graphs = []

    for package in unknown_pkgs:

        pkg_version = unknown_pkgs[package]

        coord = { "product": ""+package+"",
              "version": ""+pkg_version+"",
              "version_timestamp": "2000",
              "requires_dist": [] }

        cg_path = args.fasten_data + "callgraphs"+ "/" + package[0] + "/" + package + "/" + pkg_version + "/" + "cg.json"
        executeSingleCallGraphGeneration(args.fasten_data, coord, cg_path)


    return call_graphs


def executeSingleCallGraphGeneration(fasten_data, coord, cg_path):
    """Create Call Graph for a single package."""

    generator = CallGraphGenerator(fasten_data, coord)
    generator.generate()

    if os.path.isfile(cg_path):
        print(f"Call graph generated at: {cg_path}")
        call_graphs.append(cg_path)
    else:
        print(f"{cg_path} has not been generated!")

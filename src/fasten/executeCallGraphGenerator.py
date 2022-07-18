import time
import os.path
import shutil
from pycg_producer.producer import CallGraphGenerator


def executeCallGraphGenerator(unknown_pkgs, fasten_data):

    global cg_paths
    cg_paths = []

    for package in unknown_pkgs:

        pkg_version = unknown_pkgs[package]

        coord = { "product": ""+package+"",
              "version": ""+pkg_version+"",
              "version_timestamp": "2000",
              "requires_dist": []}

        cg_path_local = fasten_data + "callgraphs"+ "/" + package[0] + "/" + package + "/" + pkg_version + "/" + "cg.json"
        executeSingleCallGraphGeneration(coord, package, pkg_version, fasten_data, cg_path_local, fasten_data)

    return cg_paths


def executeSingleCallGraphGeneration(coord, pkg_name, pkg_version, directoryName, cg_path_local,fasten_data):

    generator = CallGraphGenerator(directoryName, coord)
    generator.generate()

    if os.path.isfile(cg_path_local):
        print("Call graph generated at: "+cg_path_local)
        cg_paths.append(cg_path_local)
    else:
        print("%s has not been generated!" % cg_path_local)

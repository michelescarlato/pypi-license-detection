from pycg_producer.producer import CallGraphGenerator
import time
import os.path
import shutil


def executeCallGraphGenerator(unknown_call_graphs, fasten_data):
    cg_directory_local = "cg_sources_dir"

    global cg_paths
    cg_paths = []
    for key in unknown_call_graphs:
        #print(key, unknown_call_graphs[key])
        pkg_name = key
        pkg_version = unknown_call_graphs[key]

        coord = { "product": ""+pkg_name+"",
              "version": ""+pkg_version+"",
              "version_timestamp": "2000",
              "requires_dist": []}

        cg_path_local = cg_directory_local + "/" + "callgraphs"+ "/" + pkg_name[0] + "/" + pkg_name + "/" + pkg_version + "/" + "cg.json"
        executeSingleCallGraphGeneration(coord, pkg_name, pkg_version, cg_directory_local, cg_path_local, fasten_data)
    return cg_paths


def executeSingleCallGraphGeneration(coord, pkg_name, pkg_version, directoryName, cg_path_local,fasten_data):

    generator = CallGraphGenerator(directoryName, coord)
    generator.generate()
    if os.path.isfile(cg_path_local):
        print("Call graph generated at: "+cg_path_local)
        cg_path_local_renamed = cg_path_local.replace("cg.json", pkg_name+"-"+pkg_version+".json")
        os.rename(cg_path_local, cg_path_local_renamed)
        shutil.copy(cg_path_local_renamed, fasten_data )
        cg_paths.append(fasten_data+"/"+pkg_name+"-"+pkg_version+".json")
        pass
    else:
        print("%s has not been generated!" % cg_path_local)

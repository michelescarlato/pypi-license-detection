import argparse
import os
import shutil
from fasten.createDirectories import CreateDirectories
from fasten.executePypiResolver import ExecutePypiResolver
from fasten.readRequirementsFile import ReadRequirementsFile
from fasten.checkPackageAvailability import CheckPackageAvailability
from fasten.requestFasten import RequestFasten
from fasten.executeCallGraphGenerator import executeCallGraphGenerator
from fasten.createCallGraph import CreateCallGraph
from fasten.stitchCallGraphs import StitchCallGraphs
from fasten.findEntrypoints import FindEntrypoints
from fasten.createAdjacencyList import CreateAdjacencyList
from fasten.depthFirstSearch import DepthFirstSearch
from fasten.optimizeStitchedCallGraph import OptimizeStitchedCallGraph
from fasten.enrichOSCG import EnrichOSCG


def main():

    parser = argparse.ArgumentParser(prog='PyPI-plugin')
    parser.add_argument("--product", type=str, help="Package name") # pypiPlugin-test-online
    parser.add_argument("--pkg_name", type=str, help="Package containing the code to be analyzed") # pypiPlugin-test-online
    parser.add_argument("--project_path", type=str, help="Path to package to be analyzed") # /mnt/stuff/projects/work/pypi-plugin/src/fasten/
    parser.add_argument("--timestamp", type=int, help="Timestamp of the package's version") # 42
    parser.add_argument("--version", type=str, help="Version of the product") # 1.0
    parser.add_argument("--requirements", type=str, help="Path to the requirements file") # /mnt/stuff/projects/work/pypi-plugin/requirements.txt
    parser.add_argument("--fasten_data", type=str, help="Path to the folder where the received FASTEN data will be stored")
    parser.add_argument("--scg_path", type=str, help="Path to the folder where the Stitched Call Graph will be stored")
    args = parser.parse_args()

    url = 'https://api.fasten-project.eu/api/pypi/' # URL to the FASTEN API
    local_package = {args.product: args.version}
    cg_location = [] # Location of Call Graphs.
    vul_location = [] # Location of vulnerabilities.
    unknown_pkgs = { } # Storage for package not known by FASTEN.

    dirs_to_delete = [args.fasten_data, args.scg_path ]
    for dir in dirs_to_delete :
        isExist = os.path.exists(dir)
        if isExist:
            print("removing: " + dir)
            shutil.rmtree(dir)


    CreateDirectories.DirectoryCheck(args.fasten_data, args.scg_path) # Create directories to store the Call Graphs and the Stitched Call Graph
    DependenciesTree = ExecutePypiResolver.executePypiResolver(args.requirements)
    all_pkgs = ReadRequirementsFile.readFile(DependenciesTree) # Read requirements.txt
    cg_location = CreateCallGraph().createCallGraph(args, cg_location)
    pkgs, unknown_pkgs = CheckPackageAvailability.checkPackageAvailability(all_pkgs, unknown_pkgs, url) # Check if packages are known by FASTEN
    cg_received, cg_pkgs, unknown_pkgs = RequestFasten.requestFasten(args, all_pkgs, unknown_pkgs, url, "rcg")
    cg_location += cg_received


    cg_generated = executeCallGraphGenerator(args, unknown_pkgs)
    cg_location += cg_generated


    vul_location, vul_pkgs, unknown_pkgs = RequestFasten.requestFasten(args, all_pkgs, unknown_pkgs, url, "vulnerabilities")


    stitched_call_graph = StitchCallGraphs().stitchCallGraphs(args, cg_location)
    entry_points = FindEntrypoints.findEntrypoints(args, stitched_call_graph)

    adjList = CreateAdjacencyList
    adjList.createAdjacencyList(stitched_call_graph)
    list_of_nodes = [False] * adjList.getNodes()

    # Run a depth first search for each entry point to create a list of all called nodes.
    for x in entry_points:
        list_of_nodes = DepthFirstSearch.depthFirstSearch(adjList, int(x), list_of_nodes)


    oscg = OptimizeStitchedCallGraph.optimizeStitchedCallGraph(args, stitched_call_graph, list_of_nodes)
    callables, callable_pkgs , unknown_pkgs = RequestFasten.requestFasten(args, local_package, unknown_pkgs, url, "callables?limit=1000000")

    if callables:
        EnrichOSCG.enrichOSCG(args, oscg, callables)

    for package in vul_pkgs:
        print(f"The package {package}: {vul_pkgs[package]} is vulnerable!")
        print(f"Vulnerabilities can be found in {args.fasten_data} {package}.vulnerabilities.json")

if __name__ == "__main__":
    main()

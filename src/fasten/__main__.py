import argparse
import json

from readRequirementsFile import ReadRequirementsFile
from checkPackageAvailability import CheckPackageAvailability
from createCallGraph import CreateCallGraph
from requestFasten import RequestFasten
from stitchCallGraphs import StitchCallGraphs
from createAdjacencyList import CreateAdjacencyList
from enrichCallGraph import EnrichCallGraph
from stitchedCallGraphAnalyzer import StitchedCallGraphAnalyzer
from createDirectories import CreateDirectories
from executePypiResolver import ExecutePypiResolver
from receiveCallGraphs import ReceiveCallGraphs


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
    forge = "local" # Source the product was downloaded from
    max_iter = -1 # Maximum number of iterations through source code (from pycg).
    operation = "call-graph" # or key-error for key error detection on dictionaries (from pycg).
    call_graphs = []
    vulnerabilities = []

    CreateDirectories.DirectoryCheck(args.fasten_data, args.scg_path) # Create directories to store the Call Graphs and the Stitched Call Graph
    DependenciesTree = ExecutePypiResolver.executePypiResolver(args.requirements)

    all_pkgs = ReadRequirementsFile.readFile(DependenciesTree) # Read requirements.txt
    pkgs, unknown_pkgs = CheckPackageAvailability.checkPackageAvailability(all_pkgs, url) # Check if packages are known by FASTEN


    call_graphs = RequestFasten.requestFasten(args, pkgs, url, "rcg")
    print("Received call graphs:")
    print(call_graphs)

    call_graphs = CreateCallGraph().createCallGraph(args, forge, max_iter, operation, call_graphs)
    print("Generated call graphs")
    print(call_graphs)
    vulnerabilities = RequestFasten.requestFasten(args, pkgs, url, "vulnerabilities")

#    pathsToCallGraphs = parser.parse_args(call_graphs)

    stitched_call_graph = StitchCallGraphs().stitchCallGraphs(args, call_graphs)

    adjList = CreateAdjacencyList
    adjList.createAdjacencyList("./StitchedCallGraph/testGraph.json")

    # Michele work - after dependencies tree resolution using pypi-resolver.
    pkgs = json.loads(pkgs)
    print(str(len(pkgs))+" known packages from fasten are:")
    print(pkgs)
    unknown_pkgs = json.loads(unknown_pkgs)
    print(str(len(unknown_pkgs)) + " unknown packages from fasten are:")
    print(unknown_pkgs)

    call_graphs, known_call_graphs, unknown_call_graphs = ReceiveCallGraphs.receiveCallGraphs(all_pkgs,url)
    print(str(len(known_call_graphs)) + " known call graphs received from fasten are:")
    print(known_call_graphs)
    #print(len(known_call_graphs.keys()))

    print(str(len(unknown_call_graphs)) + " unknown call graphs. Proceeding with local graph generation:")
    print(unknown_call_graphs)
    print(type(unknown_call_graphs))
    #print(len(unknown_call_graphs.keys()))

    # Here goes the local call graph generation for the unknown_call_graphs


#    StitchedCallGraphAnalyzer.analyzeStitchedCallGraph(stitched_call_graph)

if __name__ == "__main__":
    main()

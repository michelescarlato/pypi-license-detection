import argparse
import json
import time
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
#from receiveCallGraphs import ReceiveCallGraphs
from requestFastenKnownAndUnknownLists import RequestFastenKnownAndUnknownLists
from retrieveLocallyLicensesInformation import ReceiveLocallyLicensesInformation
from executeCallGraphGenerator import executeCallGraphGenerator, deleteCallGraphsDir

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
    time.sleep(20)
    all_pkgs = ReadRequirementsFile.readFile(DependenciesTree) # Read requirements.txt
    pkgs, unknown_pkgs = CheckPackageAvailability.checkPackageAvailability(all_pkgs, url) # Check if packages are known by FASTEN

    '''
    call_graphs = RequestFasten.requestFasten(args, pkgs, url, "rcg")
    print("Received call graphs:")
    print(call_graphs)

    call_graphs = CreateCallGraph().createCallGraph(args, forge, max_iter, operation, call_graphs)
    print("Generated call graphs")
    print(call_graphs)
    
    vulnerabilities = RequestFasten.requestFasten(args, all_pkgs, url, "vulnerabilities")
    print(vulnerabilities)
#    pathsToCallGraphs = parser.parse_args(call_graphs)
    '''


    

    # Michele work - after dependencies tree resolution using pypi-resolver.

    ################################ CALL GRAPHS #############################
    CallGraphsDirLocal = "directoryName"
    deleteCallGraphsDir(CallGraphsDirLocal)
    print("CALL GRAPHS Retrieval:")
    call_graphs_location, known_call_graphs, unknown_call_graphs, call_graphs_connectivity_issues = RequestFastenKnownAndUnknownLists.requestFastenKnownAndUnknownLists(args, all_pkgs, url, "rcg")
    print(str(len(known_call_graphs)) + " call graphs related queries had connectivity issues. Queries performed for these packages :")
    print(known_call_graphs)

    print(str(len(known_call_graphs)) + " known call graphs received from fasten are:")
    print(known_call_graphs)
    print("Call graphs location:")
    print(call_graphs_location)
    #print(len(known_call_graphs.keys()))

    print(str(len(unknown_call_graphs)) + " unknown call graphs. Proceeding with local graph generation:")
    print(unknown_call_graphs)
    #print(type(unknown_call_graphs))
    #print(len(unknown_call_graphs.keys()))
    CallGraphPaths = executeCallGraphGenerator(unknown_call_graphs, args.fasten_data)#,CallGraphsDirLocal)
    print(CallGraphPaths)
    # Martin stitch call graph approach
    stitched_call_graph = StitchCallGraphs().stitchCallGraphs(args, CallGraphPaths)# call_graphs)

    adjList = CreateAdjacencyList
    adjList.createAdjacencyList("./callGraphs/fasten-pypi-plugin.json")
    '''
    ################################## VULNERABILITIES ##############################################à
    print("VULNERABILITIES Retrieval:")
    vulnerabilities_location, known_vulnerabilities, unknown_vulnerabilities, vulnerabilities_connectivity_issues = RequestFastenKnownAndUnknownLists.requestFastenKnownAndUnknownLists(
        args, all_pkgs, url, "vulnerabilities")
    # Here goes the local call graph generation for the unknown_call_graphs
    print(str(len(vulnerabilities_connectivity_issues)) + " vulnerabilities related queries had connectivity issues. Queries performed for these packages :")
    print(vulnerabilities_connectivity_issues)

    print(str(len(known_vulnerabilities)) + " known vulnerabilities received from fasten are:")
    print(known_vulnerabilities)
    print("Vulnerabilities location:")
    print(vulnerabilities_location)
    # print(len(known_call_graphs.keys()))

    print(str(len(unknown_vulnerabilities)) + " unknown vulnerabilities. Proceeding with vulnerabilities retrieval:")
    print(unknown_vulnerabilities)


    ######################### LICENSES #############################################

    # waiting for a licensing endpoint in the REST APIs - meanwhile parsing the metadata field can be a possible solution

    known_pkgs = json.loads(pkgs)
    print(str(len(known_pkgs)) + " [Licensing] known packages from fasten are:")
    print(known_pkgs)
    
    unknown_pkgs = json.loads(unknown_pkgs)
    print(str(len(unknown_pkgs)) + " [Licensing] unknown packages from fasten are:")
    print(unknown_pkgs)

    # implementing local retrieval for license information
    licenses = ReceiveLocallyLicensesInformation.receiveLocallyLicensesInformation(unknown_pkgs)
    print("License information retrieved: ")
    print(licenses)
#    StitchedCallGraphAnalyzer.analyzeStitchedCallGraph(stitched_call_graph)
'''
if __name__ == "__main__":
    main()

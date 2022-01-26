import argparse
import sys
from readRequirementsFile import ReadRequirementsFile
from createCallGraph import CreateCallGraph
from receiveCallGraphs import ReceiveCallGraphs
from stitchCallGraph import StitchCallGraph
from fasten import FastenPackage


class Main:

    parser = argparse.ArgumentParser()
    parser.add_argument("call_graph", nargs="*",help="Paths to Call Graph files")
    url = 'http://127.0.0.1:9080' # URL to the FASTEN API
    product = "fasten-pypi-plugin" # Package name
    forge = "local" # Source the product was downloaded from
    pkg_name = "fasten-pypi-plugin" # Package containing the code to be analyzed
    version = "1.0" # Version of the product
    timestamp = "42" # Timestamp of the package's version
    requirements = '../../requirements.txt' # Path to the requirements.txt file of the project to be analyzed
    project_path = "./" # Path to project to be analyzed
    packages = ReadRequirementsFile(requirements)
    pkgs = packages.readFile() # read requirements.txt
    max_iter = -1 # Maximum number of iterations through source code (from pycg).
    operation = "call-graph" # or key-error for key error detection on dictionaries (from pycg).

# TODO: Enable plugin to receive Call Graphs and metadata information from FASTEN as soon as the pypi-API is ready
#    package = FastenPackage(url, forge, pkg_name, pkg_version)
#    result = package.get_pkg_metadata()
#    print(result)
#    call_graphs = ReceiveCallGraphs.receiveCallGraphs(pkgs, url)
#    call_graphs = CreateCallGraph().createCallGraph(pkg_name, product, forge, version, timestamp, call_graphs, project_path, max_iter, operation)
#    pathsToCallGraphs = parser.parse_args(call_graphs)

    call_graphs = []
    call_graphs.append("./callGraphs/cryptography-3.4.7.json")
    call_graphs.append("./callGraphs/fabric-2.6.0.json")
    pathsToCallGraphs = parser.parse_args(call_graphs)

    call_graphs = CreateCallGraph().createCallGraph(pkg_name, product, forge, version, timestamp, call_graphs, project_path, max_iter, operation)

    StitchCallGraph().stitchCallGraph(pathsToCallGraphs.call_graph)

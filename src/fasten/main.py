import argparse
import sys
from readRequirementsFile import ReadRequirementsFile
from createCallGraph import CreateCallGraph
from receiveCallGraphs import ReceiveCallGraphs
from stitchCallGraph import StitchCallGraph
from fasten import FastenPackage


class Main:

    parser = argparse.ArgumentParser()
    parser.add_argument("--product", type=str, help="Package name")
    parser.add_argument("--pkg_name", type=str, help="Package containing the code to be analyzed")
    parser.add_argument("--project_path", type=str, help="Path to package to be analyzed")
    parser.add_argument("--timestamp", type=int, help="Timestamp of the package's version")
    parser.add_argument("--version", type=str, help="Version of the product")
    parser.add_argument("--requirements", type=str, help="Path to the requirements file")
    args = parser.parse_args()

    url = 'https://api.fasten-project.eu/api/pypi/' # URL to the FASTEN API
    forge = "local" # Source the product was downloaded from
    max_iter = -1 # Maximum number of iterations through source code (from pycg).
    operation = "call-graph" # or key-error for key error detection on dictionaries (from pycg).
    call_graphs = []

    pkgs = ReadRequirementsFile.readFile(args.requirements) # Read requirements.txt

# TODO: Enable plugin to receive Call Graphs and metadata information from FASTEN as soon as the pypi-API is ready
#    package = FastenPackage(url, forge, pkg_name, pkg_version)
#    result = package.get_pkg_metadata()
#    print(result)
    call_graphs = ReceiveCallGraphs.receiveCallGraphs(pkgs, url)
    call_graphs = CreateCallGraph().createCallGraph(args, forge, max_iter, operation, call_graphs)
#    pathsToCallGraphs = parser.parse_args(call_graphs)

    StitchCallGraph().stitchCallGraph(args, call_graphs)

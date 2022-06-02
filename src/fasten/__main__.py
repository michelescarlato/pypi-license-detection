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
from collectingGeneratedAndRetrievedCallGraphs import collectingGeneratedAndRetrievedCallGraphs
#from licenseComplianceVerification import licenseComplianceVerification
from licenseComplianceVerification import generateInboundLicenses, licenseComplianceVerification, parseLCVAssessmentResponse#, provideReport
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
    parser.add_argument("--spdx_license", type=str, help="SPDX id of the license declared for this project")
    args = parser.parse_args()

    url = 'https://api.fasten-project.eu/api/pypi/' # URL to the FASTEN API
    LCVurl = 'https://lima.ewi.tudelft.nl/lcv/'

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

    ######################### LICENSES #############################################

    # waiting for a licensing endpoint in the REST APIs - meanwhile parsing the metadata field can be a possible solution

    known_pkgs = json.loads(pkgs)
    unknown_pkgs = json.loads(unknown_pkgs)

    # implementing local retrieval for license information
    licenses = ReceiveLocallyLicensesInformation.receiveLocallyLicensesInformation(unknown_pkgs, LCVurl)
    InboundLicenses = generateInboundLicenses(licenses, LCVurl)
    OutboundLicense = args.spdx_license
    LCVAssessmentResponse = licenseComplianceVerification(InboundLicenses, OutboundLicense, LCVurl)
    LicenseReport = parseLCVAssessmentResponse(LCVAssessmentResponse, licenses)
    print(LicenseReport)

    #provideReport(LicenseReport, licenses)



'''
    # Michele work - after dependencies tree resolution using pypi-resolver.

    ################################ CALL GRAPHS #############################
    call_graphs_list = collectingGeneratedAndRetrievedCallGraphs(args, all_pkgs, url)
    # Martin stitch call graph approach
    stitched_call_graph = StitchCallGraphs().stitchCallGraphs(args, call_graphs_list)


    adjList = CreateAdjacencyList
    adjList.createAdjacencyList(stitched_call_graph)#"./callGraphs/fasten-pypi-plugin.json")
'''


#    StitchedCallGraphAnalyzer.analyzeStitchedCallGraph(stitched_call_graph)

if __name__ == "__main__":
    main()

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
from requestFastenKnownAndUnknownListsMockup import RequestFastenKnownAndUnknownListsMockup
from retrieveLocallyLicensesInformation import ReceiveLocallyLicensesInformation
from executeCallGraphGenerator import executeCallGraphGenerator, deleteCallGraphsDir
from collectingGeneratedAndRetrievedCallGraphs import collectingGeneratedAndRetrievedCallGraphs
#from licenseComplianceVerification import licenseComplianceVerification
from licenseComplianceVerification import generateInboundLicenses, licenseComplianceVerification, parseLCVAssessmentResponse#, provideReport
from licensesApplicationToTheStitchedCallGraph import licensesApplicationToTheStitchedCallGraph

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

    #metadata_JSON_File_Locations,known_pkg_metadata, unknown_pkg_metadata, connectivity_issues = RequestFastenKnownAndUnknownLists.requestFastenKnownAndUnknownLists(args, all_pkgs, url, "metadata")

    #using mockup
    licenses_retrieved_from_fasten, known_pkgs_metadata, unknown_pkgs_metadata, connectivity_issues, index = RequestFastenKnownAndUnknownListsMockup.requestFastenKnownAndUnknownListsMockup(args, all_pkgs, url, "metadata", LCVurl)
    print(licenses_retrieved_from_fasten)
    print(index)
    print("known_pkg_metadata:")
    print(known_pkgs_metadata)
    print("Unknown_pkg_metadata:")
    print(unknown_pkgs_metadata)


    # implementing local retrieval for license information


    licenses_retrieved_locally = ReceiveLocallyLicensesInformation.receiveLocallyLicensesInformation(unknown_pkgs_metadata, LCVurl, index)
    print(licenses_retrieved_locally)

    print("Merged licenses dictionaries")
    licenses_unified = {**licenses_retrieved_from_fasten, **licenses_retrieved_locally}
    print(licenses_unified)

    licenses_retrieved_from_fasten_at_files_level, known_pkgs_metadata_at_files_level, unknown_pkgs_metadata_at_files_level, connectivity_issues_at_files_level, index = RequestFastenKnownAndUnknownListsMockup.requestFastenKnownAndUnknownListsMockup(
        args, all_pkgs, url, "files", LCVurl)
    print(licenses_retrieved_from_fasten_at_files_level)
    print(known_pkgs_metadata_at_files_level)
    print(unknown_pkgs_metadata_at_files_level)
    print(connectivity_issues_at_files_level)

    stitched_call_graph = "StitchedCallGraph/fasten-pypi-plugin.json"
    callablesReportedForLicenseViolation = licensesApplicationToTheStitchedCallGraph(stitched_call_graph,
                                                                                     licenses_retrieved_from_fasten_at_files_level,
                                                                                     licenses_retrieved_locally)

    '''
    InboundLicenses = generateInboundLicenses(licenses, LCVurl)
    OutboundLicense = args.spdx_license
    LCVAssessmentResponse = licenseComplianceVerification(InboundLicenses, OutboundLicense, LCVurl)
    LicenseReport = parseLCVAssessmentResponse(LCVAssessmentResponse, licenses)
    print(licenses)

    #call_graphs, cg_pkgs = RequestFasten.requestFasten(args, pkgs, url, "rcg")
    #call_graphs = CreateCallGraph().createCallGraph(args, forge, max_iter, operation, call_graphs)

    print("Requesting vulnerabilities:")
    vulnerabilities, vul_pkgs = RequestFasten.requestFasten(args, pkgs, url, "vulnerabilities")
    print("Requested vulnerabilities.")
    #provideReport(LicenseReport, licenses)
    '''
    # Michele work - after dependencies tree resolution using pypi-resolver.

    '''
    ################################ CALL GRAPHS #############################
    print("Generating call_graphs_list:")
    call_graphs_list = collectingGeneratedAndRetrievedCallGraphs(args, all_pkgs, url)
    # Martin stitch call graph approach
    print("Stitching the call graph:")
    stitched_call_graph = StitchCallGraphs().stitchCallGraphs(args, call_graphs_list)
    '''

    '''
    
    adjList = CreateAdjacencyList

    print("Creating adjacency list:")
    adjList.createAdjacencyList(stitched_call_graph)
    
    # adjList.createAdjacencyList(stitched_call_graph)#"./callGraphs/fasten-pypi-plugin.json")



#    StitchedCallGraphAnalyzer.analyzeStitchedCallGraph(stitched_call_graph)

    for package in vul_pkgs:
        print("The package " + package + ":" + vul_pkgs[package] + " is vulnerable!")
        print("Vulnerabilities can be found in " + args.fasten_data + package + "." + "vulnerabilities.json")

    print(LicenseReport)
'''
if __name__ == "__main__":
    main()

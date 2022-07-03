import json
import re

def licensesApplicationToTheStitchedCallGraph(stitched_call_graph, licenses_retrieved_from_fasten_at_files_level, licenses_retrieved_at_the_package_level ):
    callablesReportedForLicenseViolation = {}
    callablesEnrichedWithLicenseInformation = {}
    f = open(stitched_call_graph)
    data = json.load(f)
    LicensePackagesList = []

    print(licenses_retrieved_at_the_package_level)

    for j in licenses_retrieved_at_the_package_level:
        LicensePackagesList.append(licenses_retrieved_at_the_package_level[j]["packageName"])

    for i in data["nodes"]:
        callablesEnrichedWithLicenseInformation[i] = {}
        for element in LicensePackagesList:
            # look for package name inside of the URI
            URI = data["nodes"][i]["URI"]
            # extract the package name from the URI
            packageNameMatch = re.findall("(?<=\!)(.*?)(?=\$)", URI)
            # match the package name in the URI, using ! and $ as a delimiter
            if packageNameMatch[0] == element:
                callablesEnrichedWithLicenseInformation[i]["URI"] = URI
                print(element + " found in " + str(URI))
                for j in licenses_retrieved_at_the_package_level:
                    # look for package name inside of the licenses package level
                    if element in licenses_retrieved_at_the_package_level[j]["packageName"]:
                        if "PyPILicenseSPDX" in licenses_retrieved_at_the_package_level[j]:
                            callablesEnrichedWithLicenseInformation[i]["PyPILicenseSPDX_at_package_level"] = licenses_retrieved_at_the_package_level[j]["PyPILicenseSPDX"]
                            print(callablesEnrichedWithLicenseInformation[i]["PyPILicenseSPDX_at_package_level"])
                        else:
                            if "GitHubLicenseSPDX" in licenses_retrieved_at_the_package_level[j]:
                                callablesEnrichedWithLicenseInformation[i]["GitHubLicenseSPDX_at_package_level"] = licenses_retrieved_at_the_package_level[j]["GitHubLicenseSPDX"]
                                print(callablesEnrichedWithLicenseInformation[i]["GitHubLicenseSPDX_at_package_level"])
    #print("callablesEnrichedWithLicenseInformation:")
    #print(callablesEnrichedWithLicenseInformation)

    return callablesEnrichedWithLicenseInformation

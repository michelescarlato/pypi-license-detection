import json
import re

def licensesAtThePackageLevelApplicationToTheStitchedCallGraph(stitched_call_graph, licenses_retrieved_at_the_package_level ):

    callablesEnrichedWithLicenseInformation = {}
    f = open(stitched_call_graph)
    data = json.load(f)
    LicensePackagesList = []

    print(licenses_retrieved_at_the_package_level)

    # create a list of package names, used to loop over each callable
    for j in licenses_retrieved_at_the_package_level:
        LicensePackagesList.append(licenses_retrieved_at_the_package_level[j]["packageName"])

    for i in data["nodes"]:

        for element in LicensePackagesList:
            # look for package name inside of the URI
            URI = data["nodes"][i]["URI"]
            # extract the package name from the URI
            packageNameMatch = re.findall("(?<=\!)(.*?)(?=\$)", URI)
            # match the package name in the URI, using ! and $ as a delimiter
            if packageNameMatch[0] == element:
                #print(element + " found in " + str(URI))
                for j in licenses_retrieved_at_the_package_level:
                    # look for package name inside of the licenses package level
                    if element in licenses_retrieved_at_the_package_level[j]["packageName"]:
                        if "PyPILicenseSPDX" in licenses_retrieved_at_the_package_level[j]:
                            callablesEnrichedWithLicenseInformation[i] = {}
                            callablesEnrichedWithLicenseInformation[i]["URI"] = URI
                            callablesEnrichedWithLicenseInformation[i]["PyPILicenseSPDX_at_package_level"] = licenses_retrieved_at_the_package_level[j]["PyPILicenseSPDX"]
                            #print(callablesEnrichedWithLicenseInformation[i]["PyPILicenseSPDX_at_package_level"])
                        else:
                            if "GitHubLicenseSPDX" in licenses_retrieved_at_the_package_level[j]:
                                callablesEnrichedWithLicenseInformation[i] = {}
                                callablesEnrichedWithLicenseInformation[i]["URI"] = URI
                                callablesEnrichedWithLicenseInformation[i]["GitHubLicenseSPDX_at_package_level"] = licenses_retrieved_at_the_package_level[j]["GitHubLicenseSPDX"]
                                #print(callablesEnrichedWithLicenseInformation[i]["GitHubLicenseSPDX_at_package_level"])

    with open('callablesEnrichedWithLicenseInformation.json', 'w') as convert_file:
        json.dump(callablesEnrichedWithLicenseInformation, convert_file, indent=4)

    return callablesEnrichedWithLicenseInformation

def licensesAtTheFileLevelApplicationToTheStitchedCallGraph(licenses_retrieved_at_the_file_level, callablesEnrichedWithLicenseInformation, stitched_call_graph):
    callablesEnrichedWithLicenseAtFileLevel = {}
    # loading the stitch call graph
    f = open(stitched_call_graph)
    data = json.load(f)

    # list of packages with licenses declared at the file level
    FileLicensePackagesList = []
    for j in licenses_retrieved_at_the_file_level:
        for i in licenses_retrieved_at_the_file_level[j]:
            if "packageName" in licenses_retrieved_at_the_file_level[j][i]:
                if str(licenses_retrieved_at_the_file_level[j][i]["packageName"]) not in FileLicensePackagesList:
                    FileLicensePackagesList.append(licenses_retrieved_at_the_file_level[j][i]["packageName"])
    print("FileLicensePackagesList")
    print(FileLicensePackagesList)

    for i in data["nodes"]:

        # look for package name inside of the URI
        URI = data["nodes"][i]["URI"]
        # extract the package name from the URI
        packageNameMatch = re.findall("(?<=\!)(.*?)(?=\$)", URI)

        for j in licenses_retrieved_at_the_file_level:
            for k in licenses_retrieved_at_the_file_level[j]:
                if "packageName" in licenses_retrieved_at_the_file_level[j][k]:
                    print(licenses_retrieved_at_the_file_level[j][k]["packageName"])
                    # match the package name in the URI, using ! and $ as a delimiter - against the licenses at file level list
                    if packageNameMatch[0] == licenses_retrieved_at_the_file_level[j][k]["packageName"]:
                        # path conversion into fasten cg format
                        path = licenses_retrieved_at_the_file_level[j][k]["path"]
                        path = path.replace("/",".")
                        path = path.replace(".py","")
                        print(path)
                        if path in URI:
                            callablesEnrichedWithLicenseAtFileLevel[i] = {}
                            callablesEnrichedWithLicenseAtFileLevel[i]["URI"] = URI
                            # here should go a check for all the keys with spdx_license_key_
                            callablesEnrichedWithLicenseAtFileLevel[i]["SPDX_license_at_the_file_level"] = \
                            licenses_retrieved_at_the_file_level[j][k]["spdx_license_key_1"]
    with open('callablesEnrichedWithLicenseAtFileLevel.json', 'w') as convert_file:
        json.dump(callablesEnrichedWithLicenseAtFileLevel, convert_file, indent=4)

    return callablesEnrichedWithLicenseAtFileLevel
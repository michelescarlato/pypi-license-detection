import json

def licensesApplicationToTheStitchedCallGraph(stitched_call_graph, licenses_retrieved_from_fasten_at_files_level, licenses_retrieved_locally ):
    callablesReportedForLicenseViolation = {}
    callablesEnrichedWithLicenseInformation = {}
    f = open(stitched_call_graph)
    data = json.load(f)
    LicensePackagesList = []

    print(licenses_retrieved_locally)

    for j in licenses_retrieved_locally:
        LicensePackagesList.append(licenses_retrieved_locally[j]["packageName"])

    for i in data["nodes"]:
        callablesEnrichedWithLicenseInformation[i] = {}
        for element in LicensePackagesList:
            #print(element)
            #print(data["nodes"][i]["URI"])
            if element in data["nodes"][i]["URI"]:
                callablesEnrichedWithLicenseInformation[i]["URI"] = data["nodes"][i]["URI"]
                print(element + "found in " + str(data["nodes"][i]["URI"]))
                for j in licenses_retrieved_locally:
                    if element in licenses_retrieved_locally[j]["packageName"]:
                        if "PyPILicenseSPDX" in licenses_retrieved_locally[j]:
                            callablesEnrichedWithLicenseInformation[i]["PyPILicenseSPDX"] = licenses_retrieved_locally[j]["PyPILicenseSPDX"]
                        else:
                            if "GitHubLicenseSPDX" in licenses_retrieved_locally[j]:
                                callablesEnrichedWithLicenseInformation[i]["GitHubLicenseSPDX"] = licenses_retrieved_locally[j]["GitHubLicenseSPDX"]
    print("callablesEnrichedWithLicenseInformation:")
    print(callablesEnrichedWithLicenseInformation)
    return callablesEnrichedWithLicenseInformation

 #licenses[i]['packageName'] = packageName



    #return
from licenseComplianceVerification import parseLCVAssessmentResponse, licenseComplianceVerification
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

def licensesAtTheFileLevelApplicationToTheStitchedCallGraph(licenses_retrieved_at_the_file_level, stitched_call_graph):
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
                    # print(licenses_retrieved_at_the_file_level[j][k]["packageName"])
                    # match the package name in the URI, using ! and $ as a delimiter - against the licenses at file level list
                    if packageNameMatch[0] == licenses_retrieved_at_the_file_level[j][k]["packageName"]:
                        # path conversion into fasten cg format
                        path = licenses_retrieved_at_the_file_level[j][k]["path"]
                        path = path.replace("/",".")
                        path = path.replace(".py","")
                        #print(path)
                        if path in URI:
                            callablesEnrichedWithLicenseAtFileLevel[i] = {}
                            callablesEnrichedWithLicenseAtFileLevel[i]["URI"] = URI
                            # here should go a check for all the keys with spdx_license_key_
                            callablesEnrichedWithLicenseAtFileLevel[i]["SPDX_license_at_the_file_level"] = []
                            for license in licenses_retrieved_at_the_file_level[j][k]["spdx_license_key"]:
                                callablesEnrichedWithLicenseAtFileLevel[i]["SPDX_license_at_the_file_level"].append(license)#licenses_retrieved_at_the_file_level[j][k]["spdx_license_key"][])
    with open('callablesEnrichedWithLicenseAtFileLevel.json', 'w') as convert_file:
        json.dump(callablesEnrichedWithLicenseAtFileLevel, convert_file, indent=4)

    return callablesEnrichedWithLicenseAtFileLevel

def LCVAssessmentAtTheFileLevel(callablesEnrichedWithLicenseAtTheFileLevel, OutboundLicense, LCVurl):

    data = callablesEnrichedWithLicenseAtTheFileLevel
    callablesWithLicenseViolation = {}
    # considering that only 1 license is detected for a file
    for i in data:
        InboundLicense = data[i]["SPDX_license_at_the_file_level"]
        LCVResponse = licenseComplianceVerification(InboundLicense, OutboundLicense, LCVurl)
        if len(LCVResponse) == 0:
            pass
        if "it is the same of the outbound license" in LCVResponse[0]:
            pass
        else:
            callablesWithLicenseViolation[i] = {}
            callablesWithLicenseViolation[i] = LCVResponse[0]
            callablesWithLicenseViolation[i]["URI"] = data[i]["URI"]

    with open('callablesWithLicenseViolation.json', 'w') as convert_file:
        json.dump(callablesWithLicenseViolation, convert_file, indent=4)

    callablesWithLicenseViolationParsed = {}

    for i in callablesWithLicenseViolation:
        if callablesWithLicenseViolation[i]["status"] == "not compatible":
            callablesWithLicenseViolationParsed[i] = {}
            callablesWithLicenseViolationParsed[i]["URI"] = callablesWithLicenseViolation[i]["URI"]
            callablesWithLicenseViolationParsed[i]["message"] = callablesWithLicenseViolation[i]["message"]
            callablesWithLicenseViolationParsed[i]["inbound_SPDX"] = callablesWithLicenseViolation[i]["inbound_SPDX"]
            callablesWithLicenseViolationParsed[i]["outbound_SPDX"] = callablesWithLicenseViolation[i]["outbound_SPDX"]

    with open('callablesWithLicenseViolationParsed.json', 'w') as convert_file:
        json.dump(callablesWithLicenseViolation, convert_file, indent=4)

    return callablesWithLicenseViolationParsed



def LCVAssessmentAtTheFileLevelGenerateReport(callablesWithLicenseViolationParsed):
    LCVAssessmentAtTheFileLevelReport = []
    for i in callablesWithLicenseViolationParsed:
        output = (str(callablesWithLicenseViolationParsed[i]["URI"]) + " detected with " + str(callablesWithLicenseViolationParsed[i]["inbound_SPDX"]) + " " + \
                  " as a declared license (found with Scancode, from the FASTEN server) " + ". " + str(callablesWithLicenseViolationParsed[i]["inbound_SPDX"]) + " is not compatible with " + \
                " " + str(callablesWithLicenseViolationParsed[i]["outbound_SPDX"]) + " declared as the outbound license .")
        LCVAssessmentAtTheFileLevelReport.append(output)

    with open(r'LCVAssessmentAtTheFileLevelReport.txt', 'w') as fp:
        for item in LCVAssessmentAtTheFileLevelReport:
            # write each item on a new line
            fp.write("%s\n" % item)

    return LCVAssessmentAtTheFileLevelReport


# this method should be reviewed since now the licenses at the file level are a list
def CompareLicensesAtThePackageLevelWithTheFileLevel(licenses_retrieved_data, licenses_retrieved_at_the_file_level):
    ReportLicensesPackageComparedWithFile = {}
    z = 0 # Report index
    f = open("licenses_retrieved.json")
    licenses_retrieved = json.load(f)
    for i in licenses_retrieved:
        for j in licenses_retrieved_at_the_file_level:
            for k in licenses_retrieved_at_the_file_level[j]:
                if "packageName" in licenses_retrieved_at_the_file_level[j][k]:
                    if licenses_retrieved[i]["packageName"] == licenses_retrieved_at_the_file_level[j][k]["packageName"]:
                        if "PyPILicenseSPDX" in licenses_retrieved[i]:
                            for license in licenses_retrieved_at_the_file_level[j][k]["spdx_license_key"]:
                                if licenses_retrieved[i]["PyPILicenseSPDX"] != license:
                                    ReportLicensesPackageComparedWithFile[z] = {}
                                    ReportLicensesPackageComparedWithFile[z]["packageName"] = licenses_retrieved[i]["packageName"]
                                    ReportLicensesPackageComparedWithFile[z]["PyPILicenseSPDX"] = licenses_retrieved[i]["PyPILicenseSPDX"]
                                    ReportLicensesPackageComparedWithFile[z]["filePath"] = licenses_retrieved_at_the_file_level[j][k]["path"]
                                    ReportLicensesPackageComparedWithFile[z]["ScancodeLicense"] = license
                                    ReportLicensesPackageComparedWithFile[z]["MessageReport"] = "Scancode detected a license which is not the one declared at the package level"
                                    z += 1
                        if "GitHubLicenseSPDX" in licenses_retrieved[i]:
                            for license in licenses_retrieved_at_the_file_level[j][k]["spdx_license_key"]:
                                if licenses_retrieved[i]["GitHubLicenseSPDX"] != license:
                                    ReportLicensesPackageComparedWithFile[z] = {}
                                    ReportLicensesPackageComparedWithFile[z]["packageName"] = licenses_retrieved[i]["packageName"]
                                    ReportLicensesPackageComparedWithFile[z]["PyPILicenseSPDX"] = licenses_retrieved[i]["PyPILicenseSPDX"]
                                    ReportLicensesPackageComparedWithFile[z]["filePath"] = licenses_retrieved_at_the_file_level[j][k]["path"]
                                    ReportLicensesPackageComparedWithFile[z]["ScancodeLicense"] = license
                                    ReportLicensesPackageComparedWithFile[z]["MessageReport"] = "Scancode detected a license which is not the one declared at the package level"
                                    z += 1
    with open('ReportLicensesPackageComparedWithFile.json', 'w') as convert_file:
        json.dump(ReportLicensesPackageComparedWithFile, convert_file, indent=4)

    return ReportLicensesPackageComparedWithFile


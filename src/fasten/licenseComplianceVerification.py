import time
import requests

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''

def licenseComplianceVerification(InboundLicenses, OutboundLicense, LCVurl):
    InboundLicensesString = ';'.join([str(item) for item in InboundLicenses])
    LCVComplianceAssessment = LCVurl + "LicensesInput?InboundLicenses=" + InboundLicensesString + "&OutboundLicense=" + OutboundLicense
    print(LCVComplianceAssessment)
    try:
        response = requests.get(url=LCVComplianceAssessment)
        print(response)
        if response.status_code == 200:
            LCVComplianceAssessmentResponse = response.json()

    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    return LCVComplianceAssessmentResponse

def generateInboundLicenses(licenses):

    InboundLicenses = []

    for i in licenses:

        PyPILicenseSPDX = licenses[i].get("PyPILicenseSPDX")

        if PyPILicenseSPDX is not None:
            InboundLicenses.append(PyPILicenseSPDX)
        else:
            GitHubLicenseSPDX = licenses[i].get("GitHubLicense")
            if GitHubLicenseSPDX is not None:
                InboundLicenses.append(GitHubLicenseSPDX)

    # removing duplicates from the list
    InboundLicenses = list( dict.fromkeys(InboundLicenses) )
    print(InboundLicenses)
    return InboundLicenses

def parseLCVAssessmentResponse(LCVAssessmentResponseList, licenses):
    assessment = {}
    j = 0 # assessment index
    for dict in LCVAssessmentResponseList:
        if (dict.get("status")) == "not compatible":
            assessment[j] = {}
            InboundNotCompatibleLicense = (dict.get("inbound_SPDX"))
            outputNotCompatibleInboundLicense = (dict.get("message"))
            for i in licenses:
                packageName = licenses[i].get("packageName")
                packageVersion = licenses[i].get("packageVersion")
                if licenses[i].get("PyPILicenseSPDX") == InboundNotCompatibleLicense:
                    outputPackageInformationNotCompatibleInboundLicensePyPI = "License " + InboundNotCompatibleLicense + \
                        ", declared in PyPI, found in " + packageName + " v. " + packageVersion + "."
                    assessment[j]["packageInformation"] = outputPackageInformationNotCompatibleInboundLicensePyPI
                if licenses[i].get("GitHubLicense") == InboundNotCompatibleLicense:
                    outputPackageInformationNotCompatibleInboundLicenseGitHub = "License " + InboundNotCompatibleLicense + \
                        " declared in GitHub found in " + packageName + " v. " + packageVersion + "."
                    "."
                    assessment[j]["packageInformation"] = outputPackageInformationNotCompatibleInboundLicenseGitHub

            assessment[j]["licenseViolation"] = outputNotCompatibleInboundLicense
            j += 1


    if len(assessment) == 0:
        assessment[j] = {}
        output = "Licensing issues at the package level have not been found"
        assessment[j]["noLicensesIssues"] = output
    return assessment

def transitiveLicenseComplianceVerification(InboundLicenses, LCVurl):
    LCVComplianceAssessmentResponse = []
    length = len(InboundLicenses)
    i = 0
    # to prevent double computation against outbound licenses already assessed
    OutboundLicensesList = []
    while i < length:
        if InboundLicenses[i] not in OutboundLicensesList:
            OutboundLicense = InboundLicenses[i]
            OutboundLicensesList.append(OutboundLicense)
            TransitiveInboundLicenses = InboundLicenses.copy()
            TransitiveInboundLicenses.remove(OutboundLicense)
            InboundLicensesString = ';'.join([str(item) for item in TransitiveInboundLicenses])
            LCVComplianceAssessment = LCVurl + "LicensesInput?InboundLicenses=" + InboundLicensesString + "&OutboundLicense=" + OutboundLicense
            try:
                response = requests.get(url=LCVComplianceAssessment)
                if response.status_code == 200:
                    ResponseLength = len(response.json())
                    ResponseList = response.json()
                    #print(ResponseList)
                    j = 0
                    while j < ResponseLength:
                        #print(ResponseLength)
                        #print(type(ResponseList[j]))
                        #print(ResponseList[j])
                        LCVComplianceAssessmentResponse.append(ResponseList[j])
                        j += 1
            except requests.exceptions.ReadTimeout:
                print('Connection timeout: ReadTimeout')
            except requests.exceptions.ConnectTimeout:
                print('Connection timeout: ConnectTimeout')
            except requests.exceptions.ConnectionError:
                print('Connection timeout: ConnectError')
                time.sleep(30)
        i += 1
    return LCVComplianceAssessmentResponse

def parseLCVTransitiveAssessmentResponse(LCVAssessmentResponseList, licenses):
    transitiveAssessment = {}
    j = 0 #transitiveAssessment index
    for dict in LCVAssessmentResponseList:
        if (dict.get("status")) == "not compatible":
            transitiveAssessment[j] = {}
            InboundNotCompatibleLicense = (dict.get("inbound_SPDX"))
            outputNotCompatibleInboundLicense = (dict.get("message"))
            for i in licenses:
                packageName = licenses[i].get("packageName")
                packageVersion = licenses[i].get("packageVersion")
                if licenses[i].get("PyPILicenseSPDX") == InboundNotCompatibleLicense:
                    outputPackageInformationNotCompatibleInboundLicensePyPI = "License " + InboundNotCompatibleLicense + \
                        ", declared in PyPI, found in " + packageName + " v. " + packageVersion + "."
                    transitiveAssessment[j]["packageInformation"] = outputPackageInformationNotCompatibleInboundLicensePyPI
                if licenses[i].get("GitHubLicense") == InboundNotCompatibleLicense:
                    outputPackageInformationNotCompatibleInboundLicenseGitHub = "License " + InboundNotCompatibleLicense + \
                        " declared in GitHub found in " + packageName + " v. " + packageVersion + "."
                    "."
                    transitiveAssessment[j]["packageInformation"] = outputPackageInformationNotCompatibleInboundLicenseGitHub
            transitiveAssessment[j]["licenseViolation"] = "[License violation at the package level between dependencies] "+outputNotCompatibleInboundLicense
            j += 1


    if len(transitiveAssessment) == 0:
        transitiveAssessment[j] = {}
        output = "Licensing issues at the package level have not been found"
        transitiveAssessment[j]["noLicensesIssues"] = output
    return transitiveAssessment


def parseLicenseDeclared(licenses):
    licenseDeclaredReport = {}
    i = 0  # assessment index
    for i in licenses:
        licenseDeclaredReport[i] = {}
        if licenses[i].get("PyPILicenseSPDX"):
            licenseDeclaredReport[i]["License declared"] = licenses[i].get("packageName") +" v."+ licenses[i].get("packageVersion") \
                                                           + " has been declared with " + licenses[i].get("PyPILicenseSPDX") +", on PyPI.org."
        if licenses[i].get("GitHubLicense"):
            licenseDeclaredReport[i]["License declared"] = licenses[i].get("packageName") +" v."+ licenses[i].get("packageVersion") \
                                                           + " has been declared with " + licenses[i].get("GitHubLicense") +", on GitHub API."
        i += 1

    return licenseDeclaredReport
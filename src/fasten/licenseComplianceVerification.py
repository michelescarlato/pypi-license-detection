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
    try:
        response = requests.get(url=LCVComplianceAssessment)
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
    return InboundLicenses

def parseLCVAssessmentResponse(LCVAssessmentResponseList, licenses):
    # LCVAssessmentResponse = json.loads(LCVAssessmentResponseJSON)
    assessment = {}
    j = 0 # assessment index
    # print(licenses)
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
        output = "Licensing issues at the package level have not been found"
        assessment.append(output)
    return assessment

# def provideReport(LicenseReport, licenses):

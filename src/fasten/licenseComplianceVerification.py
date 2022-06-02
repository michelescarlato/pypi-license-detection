import json
import time
import requests
from gitHubAndPyPIParsingUtils import IsAnSPDX


def licenseComplianceVerification(InboundLicenses, OutboundLicense, LCVurl):
    InboundLicensesString = ';'.join([str(item) for item in InboundLicenses])
    print ("InboundLicensesString:")
    print(InboundLicensesString)
    LCVComplianceAssessment = LCVurl + "LicensesInput?InboundLicenses=" + InboundLicensesString + "&OutboundLicense=" + OutboundLicense
    try:
        response = requests.get(url=LCVComplianceAssessment)  # get Call Graph for specified package
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

def generateInboundLicenses(licenses, LCVurl):

    InboundLicenses = []

    for i in licenses:

        PyPILicenseSPDX = licenses[i].get("PyPILicenseSPDX")

        if len(PyPILicenseSPDX) > 0:
            InboundLicenses.append(PyPILicenseSPDX)
        else:
            GitHubLicenseSPDX = licenses[i].get("GitHubLicense")
            if len(GitHubLicenseSPDX) > 0:
                InboundLicenses.append(GitHubLicenseSPDX)
    return InboundLicenses

def parseLCVAssessmentResponse(LCVAssessmentResponseList, licenses):
    #LCVAssessmentResponse = json.loads(LCVAssessmentResponseJSON)
    assessment = []
    #print(licenses)
    for dict in LCVAssessmentResponseList:
        if (dict.get("status")) == "not compatible":
            InboundNotCompatibleLicense = (dict.get("inbound_SPDX"))
            outputNotCompatibleInboundLicense = (dict.get("message"))
            for i in licenses:
                packageName = licenses[i].get("packageName")
                packageVersion = licenses[i].get("packageVersion")
                if licenses[i].get("PyPILicenseSPDX") == InboundNotCompatibleLicense:
                    outputPackageInformationNotCompatibleInboundLicensePyPI = "License " + InboundNotCompatibleLicense + \
                        ", declared in PyPI, found in " + packageName + " v. " + packageVersion + "."
                    assessment.append(outputPackageInformationNotCompatibleInboundLicensePyPI)
                if licenses[i].get("GitHubLicense") == InboundNotCompatibleLicense:
                    outputPackageInformationNotCompatibleInboundLicenseGitHub = "License " + InboundNotCompatibleLicense + \
                        " declared in GitHub found in " + packageName + " v. " + packageVersion + "."
                    "."
                    assessment.append(outputPackageInformationNotCompatibleInboundLicenseGitHub)
            assessment.append(outputNotCompatibleInboundLicense)



        #status = LCVAssessmentResponse[i].get("status")
        '''
        if status == "not compatible":
            InboundLicense = LCVAssessmentResponse[i].get("inbound_SPDX")
            OutboundLicense = LCVAssessmentResponse[i].get("outbound_SPDX")
            Output = InboundLicense + " is not compatible with " + OutboundLicense
            assessment.append(Output)
            for i in licenses:
                if InboundLicense == licenses[i].get("PyPILicenseSPDX"):
                    outputMatching = "PyPI provides for the package " + licenses[i].get("packageName") + " v. "+ \
                                     licenses[i].get("packageVersion") + " the license " + licenses[i].get("PyPILicenseSPDX") + "," + \
                        " which is not compatible with the one declared " + OutboundLicense + "."
                    assessment.append(outputMatching)
                if InboundLicense == licenses[i].get("GitHubLicense"):
                licenses[i].get("PyPILicenseSPDX")
        '''
    return assessment

#def provideReport(LicenseReport, licenses):


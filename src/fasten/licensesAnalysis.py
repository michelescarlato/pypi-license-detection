import json
from retrieveLicenseInformation import retrieveLicenseInformation
from licenseComplianceVerification import generateInboundLicenses, licenseComplianceVerification, parseLCVAssessmentResponse#, provideReport
from licensesApplicationToTheStitchedCallGraph import licensesAtThePackageLevelApplicationToTheStitchedCallGraph, licensesAtTheFileLevelApplicationToTheStitchedCallGraph, LCVAssessmentAtTheFileLevel, LCVAssessmentAtTheFileLevelGenerateReport, CompareLicensesAtThePackageLevelWithTheFileLevel

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''

def licensesAnalysis(args, package_list, url, LCVurl, oscg):

    print("Start license analysis...")
    licenses_retrieved_from_fasten, licenses_retrieved_locally, licenses_retrieved_at_the_file_level = retrieveLicenseInformation(args, package_list, url, LCVurl)
    licenses_retrieved = {**licenses_retrieved_from_fasten, **licenses_retrieved_locally}
    inbound_licenses = generateInboundLicenses(licenses_retrieved)
    outbound_license = args.spdx_license
    lcv_assessment_response = licenseComplianceVerification(inbound_licenses, outbound_license, LCVurl)
    license_report = parseLCVAssessmentResponse(lcv_assessment_response, licenses_retrieved)
    full_report = ""

    if len(license_report) > 0:
        #print("License violation found at the package level: " +str(len(license_report)) + " ." )
        for i in license_report:
            if "noLicensesIssues" in license_report[i]:
                full_report = license_report[i]["noLicensesIssues"]
            else:
                full_report = "\n" + "############# - violation number " + str(i + 1) + " #################\n"  + str(license_report)  + "\n" + str(license_report[i]["packageInformation"]) + "\n" + str(license_report[i]["licenseViolation"]) + "\n"


    callablesEnrichedWithLicenseInformation = licensesAtThePackageLevelApplicationToTheStitchedCallGraph(oscg, licenses_retrieved)

    callablesEnrichedWithLicenseAtTheFileLevel = licensesAtTheFileLevelApplicationToTheStitchedCallGraph(licenses_retrieved_at_the_file_level, oscg)

    callablesWithLicenseViolationParsed = LCVAssessmentAtTheFileLevel(callablesEnrichedWithLicenseAtTheFileLevel, outbound_license, LCVurl)

    LCVAssessmentAtTheFileLevelReport = LCVAssessmentAtTheFileLevelGenerateReport(callablesWithLicenseViolationParsed)

    if len(LCVAssessmentAtTheFileLevelReport) > 0:
        full_report += "License compliance assessment at the file level:\n"
        for i in LCVAssessmentAtTheFileLevelReport:
            full_report += i + "\n"
    else:
        full_report += "\nThe license compliance assessment at the file level doesn't detect licenses issues.\n"

    ReportLicensesPackageComparedWithFile = CompareLicensesAtThePackageLevelWithTheFileLevel(licenses_retrieved, licenses_retrieved_at_the_file_level)

    if len(ReportLicensesPackageComparedWithFile) > 0:
        full_report += "\nReport upon incompatible licenses: scancode detected file licenses compared with the license declared at the package level:\n" + ReportLicensesPackageComparedWithFile + "\n"
    else:
        full_report += "\nThe report upon incompatible licenses between files and packages didn't show incompatibilities."

    print("License analysis done.")
    return full_report

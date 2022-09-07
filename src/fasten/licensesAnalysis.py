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
    licenses_retrieved_from_fasten, licenses_retrieved_locally, licenses_retrieved_at_the_file_level = retrieveLicenseInformation(args, package_list, url, LCVurl)
    licenses_retrieved = {**licenses_retrieved_from_fasten, **licenses_retrieved_locally}
    inbound_licenses = generateInboundLicenses(licenses_retrieved)
    outbound_license = args.spdx_license
    lcv_assessment_response = licenseComplianceVerification(inbound_licenses, outbound_license, LCVurl)
    license_report = parseLCVAssessmentResponse(lcv_assessment_response, licenses_retrieved)

    if len(license_report) > 0:
        #print("License violation found at the package level: " +str(len(license_report)) + " ." )
        for i in license_report:
            if "noLicensesIssues" in license_report[i]:
                print(license_report[i]["noLicensesIssues"])
            else:
                print("\n")
                print("############# - violation number " + str(i + 1) + " #################")
                print(license_report)
                print(license_report[i]["packageInformation"])
                print(license_report[i]["licenseViolation"])


    callablesEnrichedWithLicenseInformation = licensesAtThePackageLevelApplicationToTheStitchedCallGraph(oscg, licenses_retrieved)

    callablesEnrichedWithLicenseAtTheFileLevel = licensesAtTheFileLevelApplicationToTheStitchedCallGraph(licenses_retrieved_at_the_file_level, oscg)

    callablesWithLicenseViolationParsed = LCVAssessmentAtTheFileLevel(callablesEnrichedWithLicenseAtTheFileLevel, outbound_license, LCVurl)

    LCVAssessmentAtTheFileLevelReport = LCVAssessmentAtTheFileLevelGenerateReport(callablesWithLicenseViolationParsed)

    if len(LCVAssessmentAtTheFileLevelReport) > 0:
        print("\n")
        print("License compliance assessment at the file level:")
        for i in LCVAssessmentAtTheFileLevelReport:
            print(i)
    else:
        print("\n")
        print("The license compliance assessment at the file level doesn't detect licenses issues.")

    ReportLicensesPackageComparedWithFile = CompareLicensesAtThePackageLevelWithTheFileLevel(licenses_retrieved, licenses_retrieved_at_the_file_level)

    if len(ReportLicensesPackageComparedWithFile) > 0:
        print("\n")
        print("Report upon incompatible licenses: scancode detected file licenses compared with the license declared at the package level:")
        print(ReportLicensesPackageComparedWithFile)
    else:
        print("\n")
        print("The report upon incompatible licenses between files and package didn't show incompatibilities.")

from analyzeFastenLicenseInformation import AnalyzeFastenLicenseInformation
from retrieveLocallyLicensesInformation import ReceiveLocallyLicensesInformation
from retrieveLicensesAtTheFileLevel import RetrieveLicensesAtTheFileLevel

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''

def retrieveLicenseInformation(args, package_list, url, LCVurl):

    # request to fasten license information at the package level.
    unknown_pkgs_metadata, licenses_retrieved_from_fasten, index = AnalyzeFastenLicenseInformation.analyzeFastenLicenseInformation(args, package_list, url, LCVurl)

    # retrieve license information at the package level, querying PyPI and GitHub.
    licenses_retrieved_locally = ReceiveLocallyLicensesInformation.receiveLocallyLicensesInformation(package_list, LCVurl, index)


    # request to fasten license information at the file level.
    metadata_JSON_File_Locations, known_files_metadata, unknown_files_metadata, connectivity_issues, file_licenses = RetrieveLicensesAtTheFileLevel.retrieveLicensesAtTheFileLevel(args, package_list, url)

    return licenses_retrieved_from_fasten, licenses_retrieved_locally, file_licenses

from requestFastenLicenseInformation import RequestFastenLicenseInformation
from retrieveLocallyLicensesInformation import ReceiveLocallyLicensesInformation
from retrieveLicensesAtTheFileLevel import RetrieveLicensesAtTheFileLevel


def retrieveLicenseInformation(args, all_pkgs, url, LCVurl):

    # request to fasten license information at the package level.
    metadata_JSON_File_Locations, known_pkgs_metadata, unknown_pkgs_metadata, connectivity_issues, \
licenses_retrieved_from_fasten, index = RequestFastenLicenseInformation.requestFastenLicenseInformation(args, all_pkgs, url, LCVurl)
    #print("license retrieved from fasten:")
    #print(licenses_retrieved_from_fasten)

    # retrieve license information at the package level, querying PyPI and GitHub.
    licenses_retrieved_locally = ReceiveLocallyLicensesInformation.receiveLocallyLicensesInformation(unknown_pkgs_metadata, LCVurl, index)
    #print("license retrieved locally:")
    #print(licenses_retrieved_locally)


    # request to fasten license information at the file level.
    metadata_JSON_File_Locations, known_files_metadata, unknown_files_metadata, connectivity_issues, file_licenses = RetrieveLicensesAtTheFileLevel.retrieveLicensesAtTheFileLevel(args, all_pkgs, url)
    #print("license retrieved from fasten at the file level:")
    #print(file_licenses)

    return licenses_retrieved_from_fasten, licenses_retrieved_locally, file_licenses
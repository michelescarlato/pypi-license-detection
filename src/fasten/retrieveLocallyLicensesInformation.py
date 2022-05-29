# Send package name and version to FASTEN and receive a Call Graph for it.

from gitHubAndPyPIParsingUtils import *

class ReceiveLocallyLicensesInformation:

    @staticmethod
    # add the source (e.g. GitHub or PyPI) to the dict!
    def receiveLocallyLicensesInformation(pkgs):
        print("Retrieval of license information:")

        #licenses = {0: {'packageName' : '', 'PyPILicense' : '', 'GitHubLicense' : ''}}
        licenses = {}
        i = 1
        for package in pkgs:
            licenses[i] = {}
            packageVersion = pkgs[package]
            packageName = package
            licenses[i]['packageName'] = packageName
            licenses[i]['packageVersion'] = packageVersion
            PyPILicense,jsonResponse = retrieveLicenseInformationFromPyPI(packageName, packageVersion)
            if len(PyPILicense) > 0:
                licenses[i]['PyPILicense'] = PyPILicense
            #if len(PyPILicense) == 0:
            GitHubURL = retrieveGitHubUrl(jsonResponse, package)
            print("URL Retrieved:")
            print(GitHubURL)
            if len(GitHubURL) > 0:
                GitHubAPIurl = RetrieveGitHubAPIurl(GitHubURL)
                if len(GitHubURL) > 0:
                    GitHubLicense = RetrieveLicenseFromGitHub(GitHubAPIurl)
                    if GitHubLicense is not None:
                        if len(GitHubLicense) > 0:
                            licenses[i]['GitHubLicense'] = GitHubLicense
            i+=1
        return licenses
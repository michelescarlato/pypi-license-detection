# Send package name and version to FASTEN and receive a Call Graph for it.

from gitHubAndPyPIParsingUtils import *

class ReceiveLocallyLicensesInformation:

    @staticmethod
    # add the source (e.g. GitHub or PyPI) to the dict!
    def receiveLocallyLicensesInformation(pkgs, LCVurl, i):
        print("Retrieval of license information:")

        #licenses = {0: {'packageName' : '', 'PyPILicense' : '', 'GitHubLicense' : ''}}
        licenses = {}
        for package in pkgs:
            licenses[i] = {}
            packageVersion = pkgs[package]
            packageName = package
            licenses[i]['packageName'] = packageName
            licenses[i]['packageVersion'] = packageVersion
            PyPILicense, PyPILicenseSPDX, jsonResponse = retrieveLicenseInformationFromPyPI(packageName, packageVersion, LCVurl)
            if len(PyPILicense) > 0:
                licenses[i]['PyPILicense'] = PyPILicense
            if len(PyPILicenseSPDX) > 0:
                licenses[i]['PyPILicenseSPDX'] = PyPILicenseSPDX
            #if len(PyPILicense) == 0:
            GitHubURL = retrieveGitHubUrl(jsonResponse, package)
            print("GitHub URL Retrieved:")
            print(GitHubURL)
            if len(GitHubURL) > 0:
                GitHubAPIurl = RetrieveGitHubAPIurl(GitHubURL)
                if len(GitHubURL) > 0:
                    print(GitHubURL)
                    GitHubLicense, GitHubLicenseSPDX = RetrieveLicenseFromGitHub(GitHubAPIurl, LCVurl)
                    if GitHubLicense != "":
                        if GitHubLicense is not None:
                            licenses[i]['GitHubLicense'] = GitHubLicense
                    if GitHubLicenseSPDX != "":
                        if GitHubLicenseSPDX is not None:
                            licenses[i]['GitHubLicenseSPDX'] = GitHubLicenseSPDX
            i+=1
        return licenses
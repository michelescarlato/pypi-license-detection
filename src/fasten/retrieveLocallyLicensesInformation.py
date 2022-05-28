# Send package name and version to FASTEN and receive a Call Graph for it.

import re
import json
import time
import requests
from gitHubParsingUtils import *

class ReceiveLocallyLicensesInformation:

    @staticmethod
    def receiveLocallyLicensesInformation(pkgs):

        print("Querying PyPI.org APIs for license information:")
        #pkgs = json.loads(pkgs)
        licenses = {}
        print(pkgs)
        for package in pkgs:
            URL = "https://pypi.org/" + "pypi/" + package + "/" + pkgs[package] + "/json"
            print(URL)
            packageVersion = pkgs[package]
            try:
                response = requests.get(url=URL)  # get Call Graph for specified package
                if response.status_code == 200:
                    jsonResponse = response.json()  # save Call Graph as JSON format
                    license = (jsonResponse["info"]["license"])
                    # here a call to the LCV endpoint convertToSPDX endpoint should be performed
                    if len(license) == 0 :
                        GitHubURL = retrieveGitHubUrl(jsonResponse, package)
                        print("URL Retrieved:")
                        print(GitHubURL)
                    if len(license) > 0:
                        licenses[package] = license
            except requests.exceptions.ReadTimeout:
                print('Connection timeout: ReadTimeout')
            except requests.exceptions.ConnectTimeout:
                print('Connection timeout: ConnectTimeout')
            except requests.exceptions.ConnectionError:
                print('Connection timeout: ConnectError')
                time.sleep(30)
        return licenses
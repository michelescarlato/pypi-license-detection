import time
from urllib.parse import urlparse
import requests

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''

def retrieveGitHubUrl(data, packageName):
    global url
    url = ""
    if data['info']['home_page'] is not None:
        if packageName in data['info']['home_page']:
            if "https://github.com/" in data['info']['home_page']:
                url = data['info']['home_page']
                return url
    if data['info']['project_urls'] is not None:
        if 'Homepage' in data['info']['project_urls']:
            if packageName in data['info']['project_urls']['Homepage']:
                if "https://github.com/" in data['info']['project_urls']['Homepage']:
                    url = data['info']['home_page']
                    return url
    iterdict(data, packageName)
    return url

def iterdict (d,packageName):
    global url
    for k,v in d.items():
        if k != "description":
            if isinstance(v, dict):
                iterdict(v,packageName)
            else:
                if "https://github.com/" in str(v):
                    if packageName in str(v):
                        url = str(v)
                        return url

def RetrieveGitHubAPIurl(GitHubURL):
    parts = urlparse(GitHubURL)
    directories = parts.path.strip('/').split('/')
    owner = directories[0]
    repo = directories[1]
    GitHubAPIurl = "https://api.github.com/repos/" + owner + "/" + repo + "/license"
    return GitHubAPIurl

def RetrieveLicenseFromGitHub(GitHubAPIurl, LCVurl):
    GitHubLicense = ""
    GitHubLicenseSPDX = ""
    try:
        response = requests.get(url=GitHubAPIurl)  # get Call Graph for specified package
        if response.status_code == 200:
            jsonResponse = response.json()  # save Call Graph as JSON format
            GitHubLicense = (jsonResponse["license"]["spdx_id"])
            if len(GitHubLicense) == 0:
                GitHubLicense = (jsonResponse["license"]["key"])
            if len(GitHubLicense) == 0:
                GitHubLicense = (jsonResponse["license"]["name"])
            # here a call to the LCV endpoint convertToSPDX endpoint should be performed
            if len(GitHubLicense) > 0:
                # check if the retrieved license is an SPDX id
                IsSPDX = IsAnSPDX(GitHubLicense, LCVurl)
                if IsSPDX is False:
                    SPDXConversion = ConvertToSPDX(GitHubLicense, LCVurl)
                    IsSPDX = IsAnSPDX(SPDXConversion, LCVurl)
                    if IsSPDX is True:
                        GitHubLicenseSPDX = SPDXConversion
                else :
                    GitHubLicenseSPDX = GitHubLicense
    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)

    return GitHubLicense, GitHubLicenseSPDX

def IsAnSPDX(License, LCVurl):
    LCVIsAnSPDXJsonResponse = None
    LCVIsAnSPDXurl = LCVurl + "IsAnSPDX?SPDXid=" + License
    try:
        response = requests.get(url=LCVIsAnSPDXurl)  # get Call Graph for specified package
        if response.status_code == 200:
            LCVIsAnSPDXJsonResponse = response.json()
    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    return LCVIsAnSPDXJsonResponse

def ConvertToSPDX(License, LCVurl):
    LCVConvertToSPDXurl = LCVurl + "ConvertToSPDX?VerboseLicense=" + License
    try:
        response = requests.get(url=LCVConvertToSPDXurl)  # get Call Graph for specified package
        if response.status_code == 200:
            LCVConvertToSPDXJsonResponse = response.json()
    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    return LCVConvertToSPDXJsonResponse

def retrieveLicenseInformationFromPyPI(packageName, packageVersion, LCVurl):
#    print("Querying PyPI.org APIs for license information:")
    URL = "https://pypi.org/" + "pypi/" + packageName + "/" + packageVersion + "/json"
#    print(URL)
    PyPILicenseSPDX = ""
    try:
        response = requests.get(url=URL)
        if response.status_code == 200:
            jsonResponse = response.json()
            PyPILicense = (jsonResponse["info"]["license"])
            if PyPILicense is not None:
                if len(PyPILicense) > 0:
                    # check if the retrieved license is an SPDX id
                    IsSPDX = IsAnSPDX(PyPILicense, LCVurl)
                    if IsSPDX is False:
    #                    print("converting " +PyPILicense + " to SPDX")
                        SPDXConversion = ConvertToSPDX(PyPILicense, LCVurl)
                        IsSPDX = IsAnSPDX(SPDXConversion, LCVurl)
                        if IsSPDX is True:
                            PyPILicenseSPDX = SPDXConversion
    #                        print(PyPILicense + " converted into " + SPDXConversion )
                    else:
                        PyPILicenseSPDX = PyPILicense
    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    return PyPILicenseSPDX, PyPILicenseSPDX, jsonResponse
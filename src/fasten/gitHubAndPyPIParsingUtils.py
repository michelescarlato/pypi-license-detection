import json
import requests
import time
from urllib.parse import urlparse

import re


def retrieveGitHubUrl(jsonResponse, packageName):
    global url
    response = json.dumps(jsonResponse)
    data = json.loads(response)
    iterdict(data, packageName)
    return url

def iterdict (d,packageName):
    #print(packageName)
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
    print(parts)
    directories = parts.path.strip('/').split('/')
    print(directories)
    owner = directories[0]
    repo = directories[1]
    GitHubAPIurl = "https://api.github.com/repos/" + owner + "/" + repo + "/license"
    return GitHubAPIurl

def RetrieveLicenseFromGitHub(GitHubAPIurl):
    print(GitHubAPIurl)
    GitHubLicense = None
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
    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    if GitHubLicense is not None:
        return GitHubLicense
    else:
        return


def retrieveLicenseInformationFromPyPI(packageName, packageVersion):
    print("Querying PyPI.org APIs for license information:")
    #pkgs = json.loads(pkgs)
    URL = "https://pypi.org/" + "pypi/" + packageName + "/" + packageVersion + "/json"
    print(URL)
    try:
        response = requests.get(url=URL)  # get Call Graph for specified package
        if response.status_code == 200:
            jsonResponse = response.json()  # save Call Graph as JSON format
            PyPILicense = (jsonResponse["info"]["license"])
            # here a call to the LCV endpoint convertToSPDX endpoint should be performed


    except requests.exceptions.ReadTimeout:
        print('Connection timeout: ReadTimeout')
    except requests.exceptions.ConnectTimeout:
        print('Connection timeout: ConnectTimeout')
    except requests.exceptions.ConnectionError:
        print('Connection timeout: ConnectError')
        time.sleep(30)
    return PyPILicense,jsonResponse

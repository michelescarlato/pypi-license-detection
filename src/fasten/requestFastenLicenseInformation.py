import json
import requests
from gitHubAndPyPIParsingUtils import IsAnSPDX, ConvertToSPDX

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''

class RequestFastenLicenseInformation:

    @staticmethod
    def requestFastenLicenseInformation(args, package_list, url, LCVurl):

        print("Receive metadata from FASTEN:")
        metadata_JSON_File_Locations = [] # Call Graphs and metadata file location
        known_pkg_metadata = {}
        unknown_pkg_metadata = {}
        connectivity_issues = {}
        licenses = {}
        i = 0

        for package in package_list:
            packageName = package["name"]
            packageVersion = package["version"]

            URL = url + "packages/" + package["name"] + "/" + package["version"] + "/metadata"
            try:
                response = requests.get(url=URL) # get Call Graph or metadata for specified package

                if response.status_code == 200:

                    metadata_JSON = response.json() # save in JSON format
                    with open(args.fasten_data + package["name"] + ".metadata.json", "w") as f:
                        f.write(json.dumps(metadata_JSON)) # save metadata in a file

                    #look for licenses
                    if "licenses" in metadata_JSON["metadata"]:
                        licensesFasten = metadata_JSON["metadata"]["licenses"]
                        if len(licensesFasten) > 0:
                            print("License available for " + package["name"] + " from FASTEN server. ")
                            licenses[i] = {}
                            for licenseListElement in licensesFasten:
                                if licenseListElement["source"] == "GITHUB":
                                    IsSPDX = IsAnSPDX(str(licenseListElement["name"]), LCVurl)
                                    if IsSPDX is not True:
                                        License = ConvertToSPDX(str(licenseListElement["name"]), LCVurl)
                                        if IsAnSPDX(License, LCVurl):
                                            LicenseSPDX = License
                                        else:
                                            licenses[i]['packageName'] = packageName
                                            licenses[i]['packageVersion'] = packageVersion
                                            licenses[i]['GitHubLicense'] = str(licenseListElement["name"])
                                            pass

                                        if "LicenseSPDX" in locals():
                                            # add to licenses the license under the GitHubSPDX key
                                            licenses[i]['packageName'] = packageName
                                            licenses[i]['packageVersion'] = packageVersion
                                            licenses[i]['GitHubLicenseSPDX'] = LicenseSPDX
                                            pass
                                    else:
                                        License = str(licenseListElement["name"])
                                        licenses[i]['packageName'] = packageName
                                        licenses[i]['packageVersion'] = packageVersion
                                        licenses[i]['GitHubLicenseSPDX'] = License
                                        pass
                                        # add to licenses the license under the GitHubSPDX key
                                if licenseListElement["source"] == "PYPI":
                                    IsSPDX = IsAnSPDX(str(licenseListElement["name"]), LCVurl)
                                    if IsSPDX is not True:
                                        License = ConvertToSPDX(str(licenseListElement["name"]), LCVurl)
                                        if IsAnSPDX(License, LCVurl):
                                            LicenseSPDX = License
                                        else:
                                            licenses[i]['packageName'] = packageName
                                            licenses[i]['packageVersion'] = packageVersion
                                            licenses[i]['PyPI_not_SPDX'] = str(licenseListElement["name"])
                                            pass

                                    if "LicenseSPDX" in locals():
                                        # add to licenses the license under the GitHubSPDX key
                                        licenses[i]['packageName'] = packageName
                                        licenses[i]['packageVersion'] = packageVersion
                                        licenses[i]['PyPILicenseSPDX'] = LicenseSPDX
                                        pass
                                    else:
                                        License = str(licenseListElement["name"])
                                        licenses[i]['packageName'] = packageName
                                        licenses[i]['packageVersion'] = packageVersion
                                        licenses[i]['PyPILicenseSPDX'] = License
                                        pass
                                known_pkg_metadata[package["name"]] = package["version"]
                                i += 1
                            i += 1
                        else:
                            print("Empty licenses for " + package["name"] + " from FASTEN server. ")
                    else:
                        print("License unavailable for " + package["name"] + " from FASTEN server. ")

                    metadata_JSON_File_Locations.append(args.fasten_data + package["name"] + ".metadata.json") # append Call Graph or metadata file location to a list

                    print(package["name"] + ":" + package["version"] + ": metadata received.")
                    known_pkg_metadata[package["name"]] = package["version"]

                elif response.status_code == 404:
                    print(package["name"] + ":" + package["version"] + ": metadata not available!")
                    unknown_pkg_metadata[package["name"]] = package["version"]
                else:
                    print("Querying " + package["name"] + ":" + package["version"] + ": metadata something went wrong.")
                    print(response.status_code)
                    connectivity_issues[package["name"]] = package["version"]

            except requests.exceptions.ReadTimeout:
                print('Connection timeout: ReadTimeout')
            except requests.exceptions.ConnectTimeout:
                print('Connection timeout: ConnectTimeout')
            except requests.exceptions.ConnectionError:
                print('Connection timeout: ConnectError')

        return metadata_JSON_File_Locations, known_pkg_metadata, unknown_pkg_metadata, connectivity_issues, licenses, i

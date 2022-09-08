import json
import requests


'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''

class RetrieveLicensesAtTheFileLevel:
    @staticmethod
    def retrieveLicensesAtTheFileLevel(args, package_list, url):
#        print("Receive metadata from FASTEN:")
        metadata_JSON_File_Locations = []  # Call Graphs and metadata file location
        known_files_metadata = {}
        unknown_files_metadata = {}
        files_connectivity_issues = {}
        file_licenses = {}


        for package in package_list:
            packageName = package["name"]
            packageVersion = package["version"]
            URL = url + "packages/" + package["name"] + "/" + package["version"] + "/files"
            try:
                response = requests.get(url=URL)  # get Call Graph or metadata for specified package

                if response.status_code == 200:

                    metadata_JSON = response.json()  # save in JSON format
                    with open(args.fasten_data + package["name"] + ".files.json", "w") as f:
                        f.write(json.dumps(metadata_JSON))  # save Call Graph or metadata in a file
                    # create a dictionary for the package only if files are listed from FASTEN
                    if len(metadata_JSON) > 0:
                        file_licenses[packageName] = {}
                    # look for licenses
                    for file in metadata_JSON:
                        filePath = file["path"]
                        file_licenses[packageName][filePath] = {}
                        if file["metadata"] is not None:
                            # counter for same licenses for the same file
                            i = 0
                            if "licenses" in file["metadata"]:
                                licensesFasten = file["metadata"]["licenses"]
                                if len(licensesFasten) > 0:
                                    #print("License available for file: " + filePath + " - " + package + " from FASTEN server.")
                                    file_licenses[packageName][filePath] = {}
                                    file_licenses[packageName][filePath]["spdx_license_key"] = []
                                    for license in licensesFasten:
                                        if "spdx_license_key" in license:
                                            licenseSPDX = license["spdx_license_key"]
                                            # stores only 1 instance of the same license for the same path
                                            if i > 0:
                                                if file_licenses[packageName][filePath]["path"] == file["path"]:
                                                    if file_licenses[packageName][filePath]["spdx_license_key"][i-1] != licenseSPDX:
                                                        file_licenses[packageName][filePath]["spdx_license_key"].append(licenseSPDX)
                                                        i += 1
                                            if i == 0:
                                                file_licenses[packageName][filePath]["packageName"] = packageName
                                                file_licenses[packageName][filePath]["packageVersion"] = packageVersion
                                                file_licenses[packageName][filePath]["path"] = file["path"]
                                                file_licenses[packageName][filePath]["spdx_license_key"].append(licenseSPDX)
                                                i += 1

                                known_files_metadata[package["name"]] = package["version"]
                        else:
#                            print("License unavailable for " + package["name"] + " from FASTEN server. ")

                            metadata_JSON_File_Locations.append(
                                args.fasten_data + package["name"] + ".metadata.json")  # append Call Graph or metadata file location to a list

#                            print(package["name"] + ":" + package["version"] + ": metadata received.")
                            known_files_metadata[package["name"]] = package["version"]
                elif response.status_code == 404:
#                    print(package["name"] + ":" + package["version"] + ": metadata not available!")
                    unknown_files_metadata[package["name"]] = package["version"]
                else:
#                    print("Querying " + package["name"] + ":" + package["version"] + ": metadata something went wrong.")
#                    print(response.status_code)
                    files_connectivity_issues[package["name"]] = package["version"]

            except requests.exceptions.ReadTimeout:
                print('Connection timeout: ReadTimeout')
            except requests.exceptions.ConnectTimeout:
                print('Connection timeout: ConnectTimeout')
            except requests.exceptions.ConnectionError:
                print('Connection timeout: ConnectError')
        with open('file_licenses_original.json', 'w') as convert_file:
            json.dump(file_licenses, convert_file, indent=4)
        return metadata_JSON_File_Locations, known_files_metadata, unknown_files_metadata, files_connectivity_issues, file_licenses

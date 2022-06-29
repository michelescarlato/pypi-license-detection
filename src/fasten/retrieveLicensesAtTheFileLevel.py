import json
import time
import requests
from gitHubAndPyPIParsingUtils import IsAnSPDX, ConvertToSPDX


class RetrieveLicensesAtTheFileLevel:
    @staticmethod
    def retrieveLicensesAtTheFileLevel(args, pkgs, url):
        print("Receive metadata from FASTEN:")
        pkgs = json.loads(pkgs)
        metadata_JSON_File_Locations = []  # Call Graphs and metadata file location
        known_files_metadata = {}
        unknown_files_metadata = {}
        files_connectivity_issues = {}
        file_licenses = {}
        i = 0

        for package in pkgs:
            packageName = package
            packageVersion = pkgs[package]
            file_licenses[packageName] = {}
            URL = url + "packages/" + package + "/" + pkgs[package] + "/files"
            print(URL)
            try:
                response = requests.get(url=URL)  # get Call Graph or metadata for specified package

                if response.status_code == 200:

                    metadata_JSON = response.json()  # save in JSON format
                    with open(args.fasten_data + package + ".files.json", "w") as f:
                        f.write(json.dumps(metadata_JSON))  # save Call Graph or metadata in a file

                    # print(type(metadata_JSON))
                    # look for licenses
                    for l in metadata_JSON:
                        print(l["metadata"])
                        if l["metadata"] is not None:
                            if "licenses" in l["metadata"]:
                                licensesFasten = l["metadata"]["licenses"]
                                if len(licensesFasten) > 0:
                                    print("License available for " + package + " from FASTEN server. ")
                                    print(licensesFasten)

                                    for element in licensesFasten:
                                        print(element)
                                        if "spdx_license_key" in element:
                                            print("element[spdx_license_key]:")
                                            print(element["spdx_license_key"])
                                            print("PackageName:" + packageName)
                                            print("file index:" + str(i))
                                            if i == 0:
                                                file_licenses[packageName][i] = {}
                                                file_licenses[packageName][i]["packageName"] = packageName
                                                file_licenses[packageName][i]["packageVersion"] = packageVersion
                                                file_licenses[packageName][i]["path"] = l["path"]
                                                file_licenses[packageName][i]["spdx_license_key"] = element[
                                                    "spdx_license_key"]
                                                i += 1
                                            if i > 0:
                                                if (file_licenses[packageName][i - 1]["path"] == l["path"]):
                                                    if (file_licenses[packageName][i - 1]["spdx_license_key"] != element[
                                                        "spdx_license_key"]):
                                                        file_licenses[packageName][i] = {}
                                                        file_licenses[packageName][i]["packageName"] = packageName
                                                        file_licenses[packageName][i]["packageVersion"] = packageVersion
                                                        file_licenses[packageName][i]["path"] = l["path"]
                                                        file_licenses[packageName][i]["spdx_license_key"] = element[
                                                            "spdx_license_key"]
                                                        i += 1
                                                else:
                                                    file_licenses[packageName][i] = {}
                                                    file_licenses[packageName][i]["packageName"] = packageName
                                                    file_licenses[packageName][i]["packageVersion"] = packageVersion
                                                    file_licenses[packageName][i]["path"] = l["path"]
                                                    file_licenses[packageName][i]["spdx_license_key"] = element[
                                                        "spdx_license_key"]
                                                    i += 1
                                    known_files_metadata[package] = pkgs[package]
                        else:
                            print("License unavailable for " + package + " from FASTEN server. ")

                            metadata_JSON_File_Locations.append(
                                args.fasten_data + package + ".metadata.json")  # append Call Graph or metadata file location to a list

                            print(package + ":" + pkgs[package] + ": metadata received.")
                            known_files_metadata[package] = pkgs[package]

                elif response.status_code == 404:
                    print(package + ":" + pkgs[package] + ": metadata not available!")
                    unknown_files_metadata[package] = pkgs[package]
                else:
                    print("Querying " + package + ":" + pkgs[package] + ": metadata something went wrong.")
                    print(response.status_code)
                    files_connectivity_issues[package] = pkgs[package]

            except requests.exceptions.ReadTimeout:
                print('Connection timeout: ReadTimeout')
            except requests.exceptions.ConnectTimeout:
                print('Connection timeout: ConnectTimeout')
            except requests.exceptions.ConnectionError:
                print('Connection timeout: ConnectError')
                time.sleep(30)
        return metadata_JSON_File_Locations, known_files_metadata, unknown_files_metadata, files_connectivity_issues, file_licenses
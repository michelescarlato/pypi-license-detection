import json
import time
import requests
from gitHubAndPyPIParsingUtils import IsAnSPDX, ConvertToSPDX


def licensesAtTheFileLevel(args, pkgs, url):

        print("Receive metadata from FASTEN:")
        pkgs = json.loads(pkgs)
        metadata_JSON_File_Locations = [] # Call Graphs and metadata file location
        known_pkg_metadata = {}
        unknown_pkg_metadata = {}
        connectivity_issues = {}
        licenses = {}
        i = 0

        for package in pkgs:
            packageName = package
            packageVersion = pkgs[package]
            licenses[packageName] = {}
            URL = url + "packages/" + package + "/" + pkgs[package] + "/files"
            print(URL)
            try:
                response = requests.get(url=URL) # get Call Graph or metadata for specified package

                if response.status_code == 200:

                    metadata_JSON = response.json() # save in JSON format
                    with open(args.fasten_data + package + ".files.json", "w") as f:
                        f.write(json.dumps(metadata_JSON)) # save Call Graph or metadata in a file

                    #print(type(metadata_JSON))
                    #look for licenses
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
                                            print("PackageName:"+packageName)
                                            print("file index:" + str(i))
                                            if i == 0:
                                                licenses[packageName][i] = {}
                                                licenses[packageName][i]["packageName"] = packageName
                                                licenses[packageName][i]["packageVersion"] = packageVersion
                                                licenses[packageName][i]["path"] = l["path"]
                                                licenses[packageName][i]["spdx_license_key"] = element[
                                                    "spdx_license_key"]
                                                i += 1
                                            if i > 0:
                                                if (licenses[packageName][i-1]["path"] == l["path"] ):
                                                    if (licenses[packageName][i - 1]["spdx_license_key"] != element["spdx_license_key"]):
                                                        licenses[packageName][i] = {}
                                                        licenses[packageName][i]["packageName"] = packageName
                                                        licenses[packageName][i]["packageVersion"] = packageVersion
                                                        licenses[packageName][i]["path"] = l["path"]
                                                        licenses[packageName][i]["spdx_license_key"] = element["spdx_license_key"]
                                                        i += 1
                                                else:
                                                    licenses[packageName][i] = {}
                                                    licenses[packageName][i]["packageName"] = packageName
                                                    licenses[packageName][i]["packageVersion"] = packageVersion
                                                    licenses[packageName][i]["path"] = l["path"]
                                                    licenses[packageName][i]["spdx_license_key"] = element["spdx_license_key"]
                                                    i += 1
                                    known_pkg_metadata[package] = pkgs[package]
                        else:
                            print("License unavailable for " + package + " from FASTEN server. ")
            
                            metadata_JSON_File_Locations.append(args.fasten_data + package + ".metadata.json") # append Call Graph or metadata file location to a list

                            print(package + ":" + pkgs[package] + ": metadata received.")
                            known_pkg_metadata[package] = pkgs[package]
            
                elif response.status_code == 404:
                    print(package + ":" + pkgs[package] + ": metadata not available!")
                    unknown_pkg_metadata[package] = pkgs[package]
                else:
                    print("Querying " + package + ":" + pkgs[package] + ": metadata something went wrong.")
                    print(response.status_code)
                    connectivity_issues[package] = pkgs[package]

            except requests.exceptions.ReadTimeout:
                print('Connection timeout: ReadTimeout')
            except requests.exceptions.ConnectTimeout:
                print('Connection timeout: ConnectTimeout')
            except requests.exceptions.ConnectionError:
                print('Connection timeout: ConnectError')
                time.sleep(30)
        return metadata_JSON_File_Locations, known_pkg_metadata, unknown_pkg_metadata, connectivity_issues, licenses
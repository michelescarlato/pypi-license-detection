# Send package name and version to FASTEN and receive a Call Graph or metadata information for it.

import json
import time
import requests
from gitHubAndPyPIParsingUtils import IsAnSPDX, ConvertToSPDX
from pathlib import Path

class RequestFastenKnownAndUnknownListsMockup:

    @staticmethod
    def requestFastenKnownAndUnknownListsMockup(args, pkgs, url, path, LCVurl):

        print("Receive " + path + " from FASTEN:")
        pkgs = json.loads(pkgs)
        #metadata_JSON_File_Locations = [] # Call Graphs and metadata file location
        known_pkg_metadata = {}
        unknown_pkg_metadata = {}
        connectivity_issues = {}
        licenses = {}
        print(pkgs)
        i = 0
        for package in pkgs:
            print(package)
            f = open("fasten-restapi-mockup/"+path+".json")# save in JSON format
            packageVersion = pkgs[package]
            packageName = package
            metadata_JSON = json.load(f)
            #print(metadata_JSON)

            # this condition is a mockup of the query
            if path == "metadata":
                if metadata_JSON["package_name"] == package:
                    if "licenses" in metadata_JSON["metadata"]:
                        licenses[i] = {}
                        list = metadata_JSON["metadata"]["licenses"]
                        for element in list:
                            print(element)
                            if element["source"] == "GITHUB":
                                IsSPDX = IsAnSPDX(str(element["name"]), LCVurl)
                                if IsSPDX is not True:
                                    License = ConvertToSPDX(str(element["name"]), LCVurl)
                                    if IsAnSPDX(License, LCVurl):
                                        LicenseSPDX = License
                                    else:
                                        licenses[i]['packageName'] = packageName
                                        licenses[i]['packageVersion'] = packageVersion
                                        licenses[i]['GitHubLicense'] = str(element["name"])
                                        pass

                                    if "LicenseSPDX" in locals():
                                        # add to licenses the license under the GitHubSPDX key
                                        licenses[i]['packageName'] = packageName
                                        licenses[i]['packageVersion'] = packageVersion
                                        licenses[i]['GitHubLicenseSPDX'] = LicenseSPDX
                                        pass
                                else:
                                    License = str(element["name"])
                                    licenses[i]['packageName'] = packageName
                                    licenses[i]['packageVersion'] = packageVersion
                                    licenses[i]['GitHubLicenseSPDX'] = License
                                    pass
                                    # add to licenses the license under the GitHubSPDX key
                            if element["source"] == "PYPI":
                                IsSPDX = IsAnSPDX(str(element["name"]), LCVurl)
                                if IsSPDX is not True:
                                    License = ConvertToSPDX(str(element["name"]), LCVurl)
                                    if IsAnSPDX(License, LCVurl):
                                        LicenseSPDX = License
                                    else:
                                        licenses[i]['packageName'] = packageName
                                        licenses[i]['packageVersion'] = packageVersion
                                        licenses[i]['PyPI_not_SPDX'] = str(element["name"])
                                        pass

                                if "LicenseSPDX" in locals():
                                    # add to licenses the license under the GitHubSPDX key
                                    licenses[i]['packageName'] = packageName
                                    licenses[i]['packageVersion'] = packageVersion
                                    licenses[i]['PyPILicenseSPDX'] = LicenseSPDX
                                    pass
                                else:
                                    License = str(element["name"])
                                    licenses[i]['packageName'] = packageName
                                    licenses[i]['packageVersion'] = packageVersion
                                    licenses[i]['PyPILicenseSPDX'] = License
                                    pass
                            '''
                            with open(args.fasten_data + package + "." + path + ".json", "w") as f:
                                f.write(json.dumps(metadata_JSON)) # save Call Graph or metadata in a file
                            metadata_JSON_File_Locations.append(args.fasten_data + package + "." + path + ".json") # append Call Graph or metadata file location to a list
                            '''
                            print(package + ":" + pkgs[package] + ": " + path + " received.")
                            known_pkg_metadata[package] = pkgs[package]
                            i += 1

                else:
                    print("this package is not in fasten-restapi-mockup")
                    unknown_pkg_metadata[package] = pkgs[package]


            # this condition is a mockup of the query
            if path == "files":
                for element in metadata_JSON:
                    FilePath = element["path"]
                    p = Path(FilePath) ;
                    # take the first directory of the path - useful only for mockup
                    p = p.parts[0]
                    if package in p:
                        print(package+" is equal to " + p)
                        licenses[package] = {}
                        licenses[package]["packageName"] = package
                        licenses[package]["packageVersion"] = pkgs[package]
                        licenses[package]["path"] = element["path"]
                        licenses[package]["ScancodeSPDXLicenses"] = element["metadata"]



                '''
                for i in metadata_JSON:
                    if package in metadata_JSON[i]["path"]:
                        print(metadata_JSON[i]["metadata"])'''

        return licenses, known_pkg_metadata, unknown_pkg_metadata, connectivity_issues, i#, metadata_JSON_File_Locations,

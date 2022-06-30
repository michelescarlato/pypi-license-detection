# Send package name and version to FASTEN and receive a Call Graph or metadata information for it.

import json
import time
import requests

class RequestFastenKnownAndUnknownLists:

    @staticmethod
    def requestFastenKnownAndUnknownLists(args, pkgs, url, path):

        pkgs = json.loads(pkgs)
        metadata_JSON_File_Locations = [] # Call Graphs and metadata file location
        known_pkg_metadata = {}
        unknown_pkg_metadata = {}
        connectivity_issues = {}

        for package in pkgs:

            URL = url + "packages/" + package + "/" + pkgs[package] + "/" + path
            #print(URL)
            try:
                response = requests.get(url=URL) # get Call Graph or metadata for specified package

                if response.status_code == 200:

                    metadata_JSON = response.json() # save in JSON format
                    with open(args.fasten_data + package + "." + path + ".json", "w") as f:
                        f.write(json.dumps(metadata_JSON)) # save Call Graph or metadata in a file


                    metadata_JSON_File_Locations.append(args.fasten_data + package + "." + path + ".json") # append Call Graph or metadata file location to a list

                    print(package + ":" + pkgs[package] + ": " + path + " received.")
                    known_pkg_metadata[package] = pkgs[package]

                elif response.status_code == 404:
                    print(package + ":" + pkgs[package] + ": " + path + " not available!")
                    unknown_pkg_metadata[package] = pkgs[package]
                else:
                    print("Querying " + package + ":" + pkgs[package] + ": " + path + " something went wrong.")
                    print(response.status_code)
                    connectivity_issues[package] = pkgs[package]

            except requests.exceptions.ReadTimeout:
                print('Connection timeout: ReadTimeout')
            except requests.exceptions.ConnectTimeout:
                print('Connection timeout: ConnectTimeout')
            except requests.exceptions.ConnectionError:
                print('Connection timeout: ConnectError')

        return metadata_JSON_File_Locations, known_pkg_metadata, unknown_pkg_metadata, connectivity_issues

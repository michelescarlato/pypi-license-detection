# TODO: Request all information of a package in one run.
#       Call Graphs           \rcg
#       Vulnerabilities       \vulnerabilities
#       Callables             \callables?limit=1000000
#       Licenses              \metadata

import json
import requests
from createDirectory import CreateDirectory

class SavePackageInformation:

    @staticmethod
    def savePackageInformation(fasten_data, pkgs, url, package_list):

        keys = ['name', 'version', 'cg_file', 'vulnerabilities', 'callables',
                'licenses']

        for package in pkgs:

            dct =   {   "name": package,
                        "version": pkgs[package]
                    }

            url_pkg = url + "packages/" + package + "/" + pkgs[package] + "/"
            print()
            print(f"Start request for {package}:{pkgs[package]}...")
            print("Request Call Graph:")
            rcg = SavePackageInformation.requestFastenNew(package, pkgs[package], url_pkg, "rcg")
            if rcg:
                rcg_json = rcg.json() # save Call Graph in JSON format

#               Create directories to store the Call Graphs
                directory = fasten_data + "callgraphs/" + package[0] + "/" + package + "/" + pkgs[package]
                CreateDirectory.createDirectory(directory)
                cg_file = directory + "/cg.json"

                with open(cg_file, "w") as f:
                    f.write(json.dumps(rcg_json))

                dct["cg_file"] = cg_file
            else:
                dct["cg_file"] = None

            print("Request vulnerabilities")
            vulnerabilities = SavePackageInformation.requestFastenNew(package, pkgs[package], url_pkg, "vulnerabilities")
            dct["vulnerabilities"] = vulnerabilities

            print("Request callables")
            callables = SavePackageInformation.requestFastenNew(package, pkgs[package], url_pkg, "callables?limit=1000000")
            dct["callables"] = callables

            package_list.append(dct)

        return package_list


    @staticmethod
    def requestFastenNew(name, version, url, path):

        try:
            response = requests.get(url=url + path)

            if response.status_code == 200:
                return response

            if response.status_code == 404 or response.status_code == 400 or response.status_code == 201:
                if path == "callables?limit=1000000":
                    path = "callables"
                print(f"{response.status_code}: {name}:{version}: {path} not available!")

            else:
                print(f"{response.status_code}: Something went wrong for the package {name}:{version} on the server side!")

        except requests.exceptions.ReadTimeout:
            print('Connection timeout: ReadTimeout')
        except requests.exceptions.ConnectTimeout:
            print('Connection timeout: ConnectTimeout')
        except requests.exceptions.ConnectionError:
            print('Connection timeout: ConnectError')

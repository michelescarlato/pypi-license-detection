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
    def savePackageInformation(fasten_data, url, package_list):

        keys = ['name', 'version', 'cg_file', 'vulnerabilities', 'callables',
                'licenses']

        for package in package_list:

            url_pkg = url + "packages/" + package["name"] + "/" + package["version"] + "/"
            print()
            print(f"Start request for {package['name']}:{package['version']}...")


            print("Request Call Graph:")
            rcg = SavePackageInformation.requestFastenNew(package['name'], package['version'], url_pkg, "rcg")
            if rcg:
                rcg_json = rcg.json() # save Call Graph in JSON format

#               Create directories to store the Call Graphs
                directory = fasten_data + "callgraphs/" + package['name'][0] + "/" + package['name'] + "/" + package['version']
                CreateDirectory.createDirectory(directory)
                cg_file = directory + "/cg.json"

                with open(cg_file, "w") as f:
                    f.write(json.dumps(rcg_json))

                package["cg_file"] = cg_file
            else:
                package["cg_file"] = None


            print("Request vulnerabilities")
            vulnerabilities = SavePackageInformation.requestFastenNew(package['name'], package['version'], url_pkg, "vulnerabilities")
            package["vulnerabilities"] = vulnerabilities


            print("Request callables")
            callables = SavePackageInformation.requestFastenNew(package['name'], package['version'], url_pkg, "callables?limit=1000000")
            if callables:
                callables_json = callables.json()
                if callables_json == []:
                    package["callables"] = None
                else:
                    package["callables"] = callables_json

        return package_list


    @staticmethod
    def requestFastenNew(name, version, url, path):

        try:
            response = requests.get(url=url + path)

            if response.status_code == 200:
                return response

            if response.status_code in (201, 400, 401):
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

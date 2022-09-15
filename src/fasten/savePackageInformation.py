# TODO: Request all information of a package in one run.
#       Call Graphs           \rcg
#       Vulnerabilities       \vulnerabilities
#       Callables             \callables?limit=1000000
#       Licenses              \metadata

import json
from createDirectory import CreateDirectory
from requestFasten import RequestFasten

class SavePackageInformation:

    @staticmethod
    def savePackageInformation(fasten_data, url, package_list):
        """
        Loop through the list of all transitive dependencies of the local
        package to request FASTEN for information about it.
        Save the received Call Graphs in an extra file for each package and
        store the file location in a new list.
        """

        keys = ['name', 'version', 'cg_file', 'vulnerabilities', 'callables',
                'licenses']

        print("Request FASTEN for package information. This can take a while...")
        for package in package_list:

            url_pkg = url + "packages/" + package["name"] + "/" + package["version"] + "/"
#            print()
#            print(f"Start request for {package['name']}:{package['version']}...")


#            print("Request Call Graph:")
            rcg = RequestFasten.requestFasten(package['name'], package['version'], url_pkg, "rcg")
            if rcg:
                rcg_json = rcg.json() # save Call Graph in JSON format

                # Create directories to store the Call Graphs
                directory = fasten_data + "callgraphs/" + package['name'][0] + "/" + package['name'] + "/" + package['version']
                CreateDirectory.createDirectory(directory)
                cg_file = directory + "/cg.json"

                with open(cg_file, "w") as f:
                    f.write(json.dumps(rcg_json))

                package["cg_file"] = cg_file
            else:
                package["cg_file"] = None

            package = SavePackageInformation.createDictEntry(package, "vulnerabilities", url_pkg)
            package = SavePackageInformation.createDictEntry(package, "callables", url_pkg)
            package = SavePackageInformation.createDictEntry(package, "metadata", url_pkg)

        return package_list


    @staticmethod
    def createDictEntry(package, path, url_pkg):
        """Create dictionary to store information for each package."""

#        print(f"Request {path}")
        response = RequestFasten.requestFasten(package['name'], package['version'], url_pkg, path)
        if response:
            response_json = response.json()
            if response_json == []:
                package[path] = None
            else:
                package[path] = response_json
        else:
            package[path] = None

        return package

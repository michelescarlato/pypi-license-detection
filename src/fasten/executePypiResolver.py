import pypiResolver

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''

class ExecutePypiResolver:

    @staticmethod
    def executePypiResolver(requirementsTxt, package_list):
        """
        Use the 'requirements.txt' file of the local package to resolve
        and download all the transitive dependencies of it.
        """
        print("Resolve dependencies...")
        resolved_packages = pypiResolver.run_pip(requirementsTxt, True)

        # Read in file which contains packages that troubles pycg.
        broken_list = []
        with open("../../broken_packages.txt", "r") as broken_file:
            for package in broken_file:
                broken_list.append(package.rstrip())

        for package in resolved_packages[1]:

            dct =   {   "name": package[0],
                        "version": package[1],
                        "cg_file": None,
                        "vulnerabilities": None,
                        "callables": None
                    }

            # Don't append broken package to package_list
            if package[0] not in broken_list:
                package_list.append(dct)

        print("Dependencies resolved.")
        return package_list

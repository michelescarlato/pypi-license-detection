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

        broken_list = ["pytest","future","python-heatclient","PyYAML","rcssmin","Click","py","openstacksdk","Django","pyScss","python-neutronclient","Pygments","Pint","cryptography","django_openstack_auth","setuptools","pyinotify","rjsmin","tqdm","fonttools","pycodestyle","pyrsistent","Dj","Pt"]
        for package in resolved_packages[1]:

            dct =   {   "name": package[0],
                        "version": package[1],
                        "cg_file": None,
                        "vulnerabilities": None,
                        "callables": None
                    }
            if package[0] not in broken_list:
                package_list.append(dct)

        print("Dependencies resolved.")
        return package_list

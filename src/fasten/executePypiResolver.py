import pypiResolver

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''

class ExecutePypiResolver:

    @staticmethod
    def executePypiResolver(requirementsTxt, package_list):
        filename = requirementsTxt+"_pypi_resolved.txt"
        resolved_packages = pypiResolver.run_pip(requirementsTxt, True)

        broken_list = ["Click","py","openstacksdk","Django","pyScss","python-neutronclient","Pygments","Pint","cryptography","django_openstack_auth","setuptools","pyinotify","rjsmin","tqdm","fonttools", "pycodestyle", "pyrsistent", "Dj", "Pt"]
        for package in resolved_packages[1]:

            dct =   {   "name": package[0],
                        "version": package[1],
                        "cg_file": None,
                        "vulnerabilities": None,
                        "callables": None
                    }
            package_list.append(dct)

        for package in package_list:
            for broken in broken_list:
                if broken == package["name"]:
                    package_list.remove(package)
        return package_list

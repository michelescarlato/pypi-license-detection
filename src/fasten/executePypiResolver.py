import os
import pypiResolver

'''
* SPDX-FileCopyrightText: 2022 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: Apache-2.0
'''

class ExecutePypiResolver:

    @staticmethod
    def executePypiResolver(requirementsTxt):
        filename = requirementsTxt+"_pypi_resolved.txt"
        package_list = pypiResolver.run_pip(requirementsTxt, True)

        if os.path.exists(filename):
            os.remove(filename)

        for i in package_list[1]:

            packageAndVersion = i[0]+"=="+i[1]+"\n"
            with open(filename, "a") as myfile:
                myfile.write(packageAndVersion)

        return filename

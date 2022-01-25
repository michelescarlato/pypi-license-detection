# Retrieve package name and version from requirements.txt file

import re
import json

class ReadRequirementsFile:

    def __init__(self, requirements):
        self.requirements = requirements

#TODO make static method
    def readFile(self):

        with open(self.requirements, "r") as requirements:

            pkgs = { }
            for x in requirements:
                name = "".join(re.findall(r".+(?===)", x))
                version = "".join(re.findall(r"(?<===).+", x))
                pkgs[name] = version

            pkgs = json.dumps(pkgs)

            return pkgs

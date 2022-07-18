# Check if a package with a specific version is known by FASTEN.

import json
import requests

class CheckPackageAvailability:

    @staticmethod
    def checkPackageAvailability(pkgs, url):

        print("Check if packages from requirements.txt are available on FASTEN.")
        unknown_pkgs = { } # Store packages which are not yet known by FASTEN (to wait for lazy ingestion).
        known_pkgs = { } # Store packages which are known by FASTEN.

        for package in pkgs:

            URL = url + "packages/" + package + "/" + pkgs[package]

            try:
                response = requests.get(url=URL)

                if response.status_code == 200:
                    print(f"{package}:{pkgs[package]} is available.")
                    known_pkgs[package] = pkgs[package]

                else:
                    print(f"{package}:{pkgs[package]} is not available, saved for later.")
                    unknown_pkgs[package] = pkgs[package]

            except requests.exceptions.ReadTimeout:
                print('Connection timeout: ReadTimeout')
            except requests.exceptions.ConnectTimeout:
                print('Connection timeout: ConnectTimeout')
            except requests.exceptions.ConnectionError:
                print('Connection timeout: ConnectError')

        return known_pkgs, unknown_pkgs

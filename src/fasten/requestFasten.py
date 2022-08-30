# Send package name and version to FASTEN and receive a Call Graph or metadata information for it.

import json
import time
import requests

class RequestFasten:

    @staticmethod
    def requestFasten(name, version, url, path):

        try:
            print("Open connection to:")
            print(url+path)
            response = requests.get(url=url + path)
            print(response)

            if response.status_code == 200:
                print(f"{name}:{version}: {path} received!")
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

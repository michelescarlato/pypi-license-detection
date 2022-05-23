# Send package name and version to FASTEN and receive a Call Graph for it.

import re
import json
import time
import requests
from createCallGraph import CreateCallGraph
from pycg.pycg import CallGraphGenerator
from pathlib import Path

class ReceiveCallGraphs:

    @staticmethod
    def receiveCallGraphs(args, pkgs, url):

        print("Read Call Graphs from FASTEN:")
        pkgs = json.loads(pkgs)
        call_graphs = []

        for package in pkgs:

            URL = url + "packages/" + package + "/" + pkgs[package] + "/rcg"

            try:
                response = requests.get(url=URL) # get Call Graph for specified package

                if response.status_code == 200:

                    call_graph = response.json() # save Call Graph as JSON format
                    with open(args.cg_path + package + ".json", "w") as f:
                        f.write(json.dumps(call_graph)) # save Call Graph in a file

                    call_graphs.append(args.cg_path + package + ".json") # append Call Graph file location to list

                    print(package + ":" + pkgs[package] + ": Call Graph received.")

#                    call_graphs.append(call_graph) # append Call Graph to list
                elif response.status_code == 500:
                    print(package + ":" + pkgs[package] + ": Call Graph not available!")
                    print("Proceeding with local call graph generation...")

                    # Here we need to create the call graph locally
                    '''
                    entry_point = []  # List of python files related to the current project

                    for file_path in Path(args.project_path).glob("**/*.py"):
                        entry_point.append(str(file_path))
                    cg = CallGraphGenerator(entry_point, args.pkg_name, max_iter, operation)
                    '''

                else:
                    print("something went wrong")

            except requests.exceptions.ReadTimeout:
                print('Connection timeout: ReadTimeout')
            except requests.exceptions.ConnectTimeout:
                print('Connection timeout: ConnectTimeout')
            except requests.exceptions.ConnectionError:
                print('Connection timeout: ConnectError')
                time.sleep(30)

        return call_graphs

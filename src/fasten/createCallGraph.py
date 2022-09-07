import json
from pathlib import Path
from pycg.pycg import CallGraphGenerator
from pycg import formats

class CreateCallGraph:

    @staticmethod
    def createCallGraph(args):

        entry_point = [] # List of python files related to the current project
        forge = "local" # Source the product was downloaded from
        max_iter = -1 # Maximum number of iterations through source code (from pycg).
        operation = "call-graph" # or key-error for key error detection on dictionaries (from pycg).

        for file_path in Path(args.project_path).glob("**/*.py"):
            entry_point.append(str(file_path))

        print(f"Creating Call Graph for {args.product}...")
        cg = CallGraphGenerator(entry_point, args.pkg_name, max_iter, operation)
#        print("Call Graph created.")
#        print("Analyze Call Graph...")
        cg.analyze()
#        print("Call Graph analyzed.")
#        print("Format Call Graph...")
        formatter = formats.Fasten(cg, args.pkg_name, args.product, forge, args.version, args.timestamp)
#        print("Call Graph formatted.")

        cg_file = args.fasten_data + args.pkg_name + ".json"
        with open(cg_file, "w+") as f:
            f.write(json.dumps(formatter.generate()))

        print(f"Call Graph written in file {cg_file}")

        return cg_file

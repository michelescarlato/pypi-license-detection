# Create Optimized Stitched Call Graph.
import os
import json


class OptimizeStitchedCallGraph:

    @staticmethod
    def optimizeStitchedCallGraph(args, stitched_call_graph, list_of_nodes):
        print("Optimize Stitched Call Graph...")

        with open(stitched_call_graph, "r") as scg_file:
            scg = json.load(scg_file)

            oscg = {"nodes": {}}

            i = 0
            for node in list_of_nodes:
                if node:
                    node_number = {str(i): {}}
                    oscg["nodes"].update(node_number)
                    oscg["nodes"][str(i)].update(scg["nodes"][str(i)])
                i = i + 1

            oscg_file_path = os.path.join(args.scg_path, "oscg.json")
            with open(oscg_file_path, "w") as oscg_file:
                oscg_file.write(json.dumps(oscg))
            print(f"Optimized Stitched Call Graph written in file {oscg_file_path}.")
        return oscg

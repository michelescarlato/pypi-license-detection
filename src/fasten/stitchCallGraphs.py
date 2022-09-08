# Stitch Call Graphs together.

import json
import os
from stitcher.stitcher import Stitcher

class StitchCallGraphs:

    @staticmethod
    def stitchCallGraphs(args, package_list):

        print("Stitch Call Graphs...")
        call_graphs = [ ]

        for pkg in package_list:
            if pkg["cg_file"] is not None:
                call_graphs.append(pkg["cg_file"])

        stitcher = Stitcher(call_graphs, False)
        stitcher.stitch()
        output = json.dumps(stitcher.output(), indent=2)
        stitched_graph_file = os.path.join(args.scg_path, args.product + ".json")
        with open(stitched_graph_file, "w+") as f:
            f.write(output)
        print(f"Stitched Call Graph written in file {stitched_graph_file}.")

        return stitched_graph_file

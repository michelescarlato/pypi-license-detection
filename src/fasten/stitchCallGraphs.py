# Stitch Call Graphs together.

import json
import os
from stitcher.stitcher import Stitcher

class StitchCallGraphs:

    @staticmethod
    def stitchCallGraphs(args, call_graphs):
        """"Merge all Call Graphs to one single 'Stitched Call Graph'."""

        print("Stitch Call Graphs...")

        stitcher = Stitcher(call_graphs, False)
        stitcher.stitch()
        output = json.dumps(stitcher.output(), indent=2)
        stitched_graph_file = os.path.join(args.fasten_data, args.product + "-scg.json")
        with open(stitched_graph_file, "w+") as f:
            f.write(output)
        print(f"Stitched Call Graph written in file {stitched_graph_file}.")

        return stitched_graph_file

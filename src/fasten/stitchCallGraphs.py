# Stitch Call Graphs together.

import json
from stitcher.stitcher import Stitcher

class StitchCallGraphs:

    @staticmethod
    def stitchCallGraphs(args, call_graphs):

        print("Stitch Call Graphs")

        stitcher = Stitcher(call_graphs, "simple")
        stitcher.stitch()
        output = json.dumps(stitcher.output())
        stitched_call_graph = args.scg_path + args.product + ".json"

        with open(stitched_call_graph, "w+") as f:
            f.write(output)
        print('Saved Stiched Call Graph in: ' + stitched_call_graph)

        return stitched_call_graph

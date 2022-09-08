# Enrich the Optimized Stitched Call Graph with metadata information from FASTEN.

import re
import json

class EnrichOSCG:

    @staticmethod
    def enrichOSCG(args, oscg, package_list):
        """
        Enrich the Optimized Stitched Call Graph
        with metadata information from FASTEN.
        """

        print("Enrich Optimized Stitched Call Graph...")

        for node in oscg["nodes"]:
            oscg_uri = "".join(re.findall(rf"(?<={args.version}).+",
                               oscg["nodes"][node]["URI"]))
            for pkg in package_list:
                if pkg["callables"] is not None:
                    if pkg["callables"][1]["fasten_uri"] == oscg_uri:
                        if pkg["callables"][1]["metadata"]:
                            oscg["nodes"][node]["metadata"] = pkg["callables"]["metadata"]

        with open(args.scg_path + "enrichedCallGraph.json", "w+") as ecg_file:
            ecg_file.write(json.dumps(oscg))

        print(f"Enriched Call Graph written in file {args.scg_path}enrichedCallGraph.json.")

from pycg_producer.producer import CallGraphGenerator
import time

class ExecuteCallGraphGenerator:
    @staticmethod
    def executeCallGraphGenerator(unknown_call_graphs):
        for key in unknown_call_graphs:
            print(key, unknown_call_graphs[key])
            packageName = key
            packageVersion = unknown_call_graphs[key]

            coord = { "product": ""+packageName+"",
                  "version": ""+packageVersion+"",
                  "version_timestamp": "2000",
                  "requires_dist": []}
            generator = CallGraphGenerator("directoryName", coord)
            print(generator.generate())
            time.sleep(600)
            
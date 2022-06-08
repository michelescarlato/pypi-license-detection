# Create adjacency list for Stitched Call Graph.

import json


class CreateAdjacencyList:

    @classmethod
    def createAdjacencyList(cls, stitched_call_graph):

#       Read the list of calls from Stitched Call Graph.
        print("Read the list of calls from the Stitched Call Graph...")
        with open(stitched_call_graph) as f:
            scg = json.loads(f.read())

        cls.nodesPair = scg["edges"]
        cls.edges = len(scg["edges"])
#        print("Nodes pairs:")
#        print(cls.nodesPair)
#        print("Number of Edges:")
#        print(cls.edges)
#        print("Number of Nodes:")
        cls.nodes = cls.getNumberOfNodes() + 1
#        print(cls.nodes)

        cls.graph = [None] * cls.nodes
        cls.addEdges()
        cls.print_agraph()


#   Add edges to adjacency list.
    @classmethod
    def addEdges(cls):

        for pair in cls.nodesPair:

            node = AdjNode(pair[0])
            node.next = cls.graph[pair[1]]
            cls.graph[pair[1]] = node
            node = AdjNode(pair[1])
            node.next = cls.graph[pair[0]]
            cls.graph[pair[0]] = node


#   Print adjacency list.
    @classmethod
    def print_agraph(cls):

        cls.adj = {}

        for i in range(cls.nodes): # 0 -> 13
#            print(str(i) + ":", end="")
            temp = cls.graph[i]
            cls.adj[i] = []

            while temp:
                cls.adj[i].append(int("{}".format(temp.node)))
#                print(" {}".format(temp.node), end="")
                temp = temp.next
#            print("")

#        print(cls.adj)
#        print(cls.graph[0])


#   Get number of nodes existent in the Stitched Call Graph.
    @classmethod
    def getNumberOfNodes(cls):

        nodes = 0

        for pair in cls.nodesPair:
            if pair[0] > nodes:
                nodes = pair[0]
            if pair[1] > nodes:
                nodes = pair[1]
        return nodes


#   Return number of nodes.
    @classmethod
    def getNodes(cls):
        return  cls.nodes


#   Return number of edges.
    @classmethod
    def getEdges(cls):
        return  cls.edges


#   Return adjacency list:
    @classmethod
    def getAdjacencyList(cls, node):
#        print(cls.adj[node])
        return  cls.adj[node]


class AdjNode:

    def __init__(self, value):

        self.node = value
        self.next = None

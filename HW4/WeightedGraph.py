class WeightedEdge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def getNode1(self):
        return self.node1

    def getNode2(self):
        return self.node2

    def getWeight(self):
        return self.weight
    
class WeightedGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def getKeys(self):
        keys = []
        for key in self.nodes.keys():
            keys.append(key)
        return keys

    def nodeExists(self, testNode):
        return testNode in self.nodes

    def getEdgeId(self, node1, node2):
        return f"{node1}-{node2}"

    def addNode(self, nodeId, data):
        self.nodes[nodeId] = data

    def getNodeData(self, nodeId):
        return self.nodes.get(nodeId)

    def addEdge(self, node1, node2, weight):
        edgeId = self.getEdgeId(node1, node2)
        edge = WeightedEdge(node1, node2, weight)
        self.edges[edgeId] = edge

    def removeEdge(self, node1, node2):
        edgeId = self.getEdgeId(node1, node2)
        del self.edges[edgeId]

    def getNeighbors(self, neighbors, node):
        for edgeId in self.edges:
            startNode, endNode = edgeId.split('-')
            if startNode == node:
                neighbors.append(endNode)

    def areNeighbors(self, node1, node2):
        neighbors = []
        self.getNeighbors(neighbors, node1)
        return node2 in neighbors

    def getNeighborWeight(self, node1, node2):
        if self.areNeighbors(node1, node2):
            edgeId = self.getEdgeId(node1, node2)
            edge = self.edges.get(edgeId)
            if edge:
                return edge.getWeight()
        return 0.0

    def findPath(self, path, node1, node2):
        print(f"Finding path from {node1} to {node2}")
        if node1 not in self.nodes or node2 not in self.nodes:
            return
        path.append(node1)
        visited = {node1: node1}
        while path:
            last = path[-1]
            neighbors = []
            self.getNeighbors(neighbors, last)
            closestIndex = -1
            closestDistance = 100000.0
            for i, testNeighbor in enumerate(neighbors):
                if testNeighbor == node2:
                    path.append(testNeighbor)
                    return
                if testNeighbor not in visited:
                    edgeId = self.getEdgeId(last, testNeighbor)
                    edge = self.edges.get(edgeId)
                    if edge and edge.getWeight() < closestDistance:
                        closestIndex = i
                        closestDistance = edge.getWeight()
            if closestIndex >= 0:
                closestNode = neighbors[closestIndex]
                visited[closestNode] = closestNode
                path.append(closestNode)
            elif path:
                path.pop()

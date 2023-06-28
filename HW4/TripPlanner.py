from typing import List
from pTPS import pTPS_Transaction

class AppendStop_Transaction(pTPS_Transaction):
    def __init__(self, initStops: List[str], initCode: str):
        self.code = initCode
        self.tripStops = initStops

    def doTransaction(self):
        self.tripStops.append(self.code)

    def undoTransaction(self):
        self.tripStops.pop()

    def toString(self):
        return "Appending Stop"
    

from typing import List
from WeightedGraph import WeightedGraph
from pTPS import pTPS
from Airport import Airport

stops: List[str] = []
graph = WeightedGraph()
tps: pTPS = pTPS()

def displayAirports():
    print("AIRPORTS YOU CAN TRAVEL TO AND FROM:")
    keys = graph.getKeys()
    for key in keys:
        airport = graph.getNodeData(key)
        print(f"{airport.getCode()}")

def displayCurrentTrip():
    wss = []
    wss.append("Current Trip Stops:")
    for i, stop in enumerate(stops):
        wss.append(f"\t{i+1}. {stop}")
    wss.append("")
    wss.append("Current Trip Legs:")
    legNum = 1
    tripDistance = 0.0
    legDistance = 0.0
    for i in range(len(stops)):
        lastStop = ""
        nextStop = ""
        legDistance = 0.0
        if legNum < len(stops):
            wss.append(f"\t{i+1}. ")
            lastStop = stops[legNum - 1]
            nextStop = stops[legNum]
            route = []
            graph.findPath(route, lastStop, nextStop)
            if len(route) < 2:
                wss.append(f"No Route Found from {lastStop} to {nextStop}")
            else:
                legOutput = ""
                for j in range(len(route) - 1):
                    a1 = graph.getNodeData(route[j])
                    a2 = graph.getNodeData(route[j + 1])
                    distance = a1.calculateDistance(a1, a2)
                    legDistance += distance
                    if j == 0:
                        legOutput += a1.code
                    legOutput += f"-{a2.code}"
                wss.append(f"{legOutput} (Leg Distance: {legDistance} miles)")
            legNum += 1
            tripDistance += legDistance

    wss.append(f"Total Trip Distance: {tripDistance} miles")
    output = "\n".join(wss)
    print(output)

def displayMenu():
    print("ENTER A SELECTION")
    print("S) Add a Stop to your Trip")
    print("U) Undo")
    print("R) Redo")
    print("E) Empty Trip")
    print("Q) Quit")
    print("-")

def processUserInput():
    global stops 
    entry = input()
    if entry == "S":
        print("\nEnter the Airport Code: ", end="")
        entry = input()
        if graph.nodeExists(entry):
            neighbors = []
            graph.getNeighbors(neighbors, entry)
            if len(stops) > 0:
                lastStop = stops[-1]
                if lastStop == entry:
                    print("DUPLICATE STOP ERROR - NO STOP ADDED")
                else:
                    transaction = AppendStop_Transaction(stops, entry)
                    tps.addTransaction(transaction)
            else:
                transaction = AppendStop_Transaction(stops, entry)
                tps.addTransaction(transaction)
        else:
            print("INVALID AIRPORT CODE ERROR - NO STOP ADDED")
    elif entry == "U":
        tps.undoTransaction()
    elif entry == "R":
        tps.doTransaction()
    elif entry == "E":
        tps.clearAllTransactions()
        if len(stops) > 0:
            stops = []
    elif entry == "Q":
        return False
    return True

import json
from typing import Dict, Any

def createAirportFromData(aiports: Dict[str, Any]):
    code = aiports['code']
    latitudeDegrees = aiports['latitudeDegrees']
    latitudeMinutes = aiports['latitudeMinutes']
    longitudeDegrees = aiports['longitudeDegrees']
    longitudeMinutes = aiports['longitudeMinutes']
    return Airport(code, latitudeDegrees, latitudeMinutes, longitudeDegrees, longitudeMinutes)

def initEdge(node1, node2):
    a1 = graph.getNodeData(node1)
    a2 = graph.getNodeData(node2)
    if a1 and a2:
        distance = Airport.calculateDistance(a1, a2)
        graph.addEdge(node1, node2, distance)
        graph.addEdge(node2, node1, distance)

def initAllAirports():
    with open('airports.json', 'r') as file:
        data = json.load(file)
    airports = data['airports']
    connections = data['connections']
    for airportData in airports:
        airport = createAirportFromData(airportData)
        graph.addNode(airport.getCode(), airport)
    for connectionData in connections:
        source = connectionData['source']
        target = connectionData['target']
        initEdge(source, target)

def main():
    initAllAirports()
    keepGoing = True
    while keepGoing:
        displayAirports()
        displayCurrentTrip()
        displayMenu()
        keepGoing = processUserInput()

    print("GOODBYE")
if __name__ == "__main__":
    main()

import random

#*************************************************************************************************************
# Function to parse input from a file and prepare data structures
#*************************************************************************************************************
def parseInput(getDetailsSet):
    with open(getDetailsSet, 'r') as inpFile:
        lines = inpFile.readlines()

    # Parse the location data
    count = len(lines[0].strip().split(','))
    locations = []

    for y in range(count):
        t = []
        for s in lines[y].strip().split(','):
            if s == 'N':
                t.append(0)
            else:
                t.append(int(s))
        locations.append(t)

    # Parse vehicle information
    vehicleInfo = {}
    for line in lines[count:]:
        items = line.split('#')
        vehicle_name = items[0].strip()
        storage = int(items[1].strip())
        vehicleInfo[vehicle_name] = {
            'storage': storage,
            'deliveries': [],
            'tempNode': 0,
            'finalGap': 0
        }

    return count, locations, vehicleInfo

#*************************************************************************************************************
# Define a class for the town plan
#*************************************************************************************************************
class TownPlan:

    def __init__(self, adjacencyMat):
        self.adjacencyMat = adjacencyMat
        self.adjecLst = self.adjacencyMatrixToList(adjacencyMat)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Function to convert the adjacency matrix to adjacency lists
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def adjacencyMatrixToList(self, adjacencyMat):
        nodeCount = len(adjacencyMat)
        adjecLst = {}

        for i in range(nodeCount):
            adjecLst[i] = []
            for j in range(nodeCount):
                if adjacencyMat[i][j] != 0:
                    adjecLst[i].append(j)

        return adjecLst

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Function to compute the gap of a given chain
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def computeGap(self, chain):
        chain = [0] + chain
        gap = 0
        for i in range(len(chain) - 1):
            gap += self.dijkstra(chain[i], chain[i + 1])
        return gap

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Function to compute the shortest path between two nodes using Dijkstra's algorithm
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def dijkstra(self, startLoc, endLoc):
        """Dijkstra's algorithm, which utilizes an adjacency matrix, is employed to determine the most efficient route connecting two nodes within the town plan."""
        nodeCount = len(self.adjacencyMat)
        checked = [False] * nodeCount
        gap = [float('inf')] * nodeCount
        gap[startLoc] = 0
        path = [None] * nodeCount

        for _ in range(nodeCount):
            leastGap = float('inf')
            leastLoc = -1
            for node in range(nodeCount):
                if not checked[node] and gap[node] < leastGap:
                    leastGap = gap[node]
                    leastLoc = node

            checked[leastLoc] = True

            for neighbor, weight in enumerate(self.adjacencyMat[leastLoc]):
                if weight != 0 and gap[neighbor] > gap[leastLoc] + weight:
                    gap[neighbor] = gap[leastLoc] + weight
                    path[neighbor] = leastLoc

        return gap[endLoc]

#*************************************************************************************************************
# Function to generate a random shipment chain
#*************************************************************************************************************
def giveRandomShipmentChain(n, vehicleInfo):
    shipmentChain = {}
    temp = list(range(1, n))
    random.shuffle(temp)
    i = 0
    for vehicle in vehicleInfo:
        shipmentChain[vehicle] = temp[i: i + vehicleInfo[vehicle]['storage']]
        i += vehicleInfo[vehicle]['storage']
    return shipmentChain

#*************************************************************************************************************
# Hill climbing algorithm to optimize the shipment chain
#*************************************************************************************************************
def hillClimbing(n, locations, vehicleInfo, townPlan: TownPlan):
    shipmentChain = giveRandomShipmentChain(n, vehicleInfo)
    print(f"Initial chain is {shipmentChain}")
    better = True
    tempGap = sum(townPlan.computeGap(shipmentChain[vehicle]) for vehicle in shipmentChain)
    newChain = shipmentChain.copy()
    maxIterations = 0
    while better:
        improved = False
        newChain = giveRandomShipmentChain(n, vehicleInfo)
        newGap = sum(townPlan.computeGap(newChain[vehicle]) for vehicle in newChain)
        if newGap < tempGap:
            better = True
            shipmentChain = newChain
            tempGap = newGap
        if not improved:
            maxIterations += 1
            if maxIterations == 1000:
                print(shipmentChain)
                print(f"gap is {tempGap}")
                return shipmentChain, tempGap
                break

#*************************************************************************************************************
# Function to write output information to a file
#*************************************************************************************************************
def putoutInfoSet(outInfoSet, vehicleInfo, gap):
    with open(outInfoSet, 'w') as file:
        for vehicle in vehicleInfo:
            charOrder = ','.join(chr(num + 97) for num in vehicleInfo[vehicle])
            file.write(f"{vehicle}#{charOrder}\n")
        file.write(f"{gap}")

if __name__ == "__main__":
    getDetailsSet = "input.txt"

    n, locations, vehicleInfo = parseInput(getDetailsSet)
    townPlan = TownPlan(locations)
    del_chain, gap = hillClimbing(n, locations, vehicleInfo, townPlan)

    putoutInfoSet("210401T.txt", del_chain, gap)

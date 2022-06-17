# Data given

# airports = [
#     "BGI", "CDG", "DEL", "DOH", "DSM", "EWR", "EYW", "HND", "ICN",
#     "JFK", "LGA", "LHR", "ORD", "SAN", "SFO", "SIN", "TLV", "BUD"]


airports = []
routes = []
def aircradts():
    file1 = open('/Users/salpecoraro/Downloads/PORTS.txt', 'r')
    Lines = file1.readlines()
    count = 0
    # Strips the newline character
    for line in Lines:
        store = line.strip()
        airports.append(store)



def convertRoute():
  file1 = open('/Users/salpecoraro/Downloads/ROUTESSSSS.txt')
  Lines = file1.readlines()
  count = 0
  # Strips the newline charac
  for line in Lines:
      count += 1
      store = line.strip()
      a = store.split(" ")
      routes.append(a)


# routes = [
#     ["DSM", "ORD"],
#     ["ORD", "BGI"],
#     ["BGI", "LGA"],
#     ["SIN", "CDG"],
#     ["CDG", "SIN"],
#     ["CDG", "BUD"],
#     ["DEL", "DOH"],
#     ["DEL", "CDG"],
#     ["TLV", "DEL"],
#     ["EWR", "HND"],
#     ["HND", "ICN"],
#     ["HND", "JFK"],
#     ["ICN", "JFK"],
#     ["JFK", "LGA"],
#     ["EYW", "LHR"],
#     ["LHR", "SFO"],
#     ["SFO", "SAN"],
#     ["SFO", "DSM"],
#     ["SAN", "EYW"]]

Start = "LGA"

# Answer

class Airport():

    # Initialize the class with the airport name, the list of airports, the list of routes
    def __init__(self, name, airports=airports, routes=routes.copy()):
        aircradts()
        convertRoute()
        self.Connections = [name]
        self.MissingAirports = airports.copy()

        # Remove from the missing airports the starting airport
        self.MissingAirports.remove(name)

        # Find all connections in current routes not in the existing list of connections and remove them from the list of missingAirports
        for i in routes:
            if i[0] == name and i[1] not in self.Connections:
                self.Connections.append(i[1])
                self.MissingAirports.remove(i[1])

        # Recursive method : when I add a connection to self.Connection it will be taken into account
        for i in self.Connections:
            for j in routes:
                if j[0] == i and j[1] not in self.Connections:
                    self.Connections.append(j[1])
                    self.MissingAirports.remove(j[1])

    # I now have the connections with the current routes.


    # Find out the number of new connections obtained when connecting to a missing airport
    def CountNewConnection(self, name):
        newAirport = Airport(name)
        Connections = self.Connections.copy()
        count = 0
        for i in newAirport.Connections:
            if i not in Connections:
                count += 1
        return count

    # Connect to an airport using its name and add the new connections to self.Connections
    def ConnectTo(self, name):
        newAirport = Airport(name)
        for i in newAirport.Connections:
            if i not in self.Connections:
                self.Connections.append(i)
                self.MissingAirports.remove(i)


# Create object using Airport class with the starting airport.
Start = Airport(Start)

#initialise the iteration count
iterations = 0

# #Loop : while the length of unique connections is different than the length of airports
while len(Start.Connections) != len(airports):
    # Count the number of new connections when connecting to an airport for each missing airport
    count = [Start.CountNewConnection(i) for i in Start.MissingAirports]
    # Connect to the missing airport with the maximum of new connections
    Start.ConnectTo(Start.MissingAirports[count.index(max(count))])
    # add 1 to iteration count
    iterations += 1

# return the number of iterations.
print(iterations)

# Possible to print to which airport it has to connect and in which order in the while loop.
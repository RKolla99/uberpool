import sys
max_int = 100

class Driver():
    def __init__(self,name,pos,rating):
        self.name = name
        self.position = pos
        self.rating = rating
    def changePosition(self,pos):
        self.position = pos
    def getPositon(self):
        return self.position
    # Add function to update rating after each ride




class Graph(): 
    
    # Graph initialization
    def __init__(self, vertices): 

        
        self.V = vertices 
        self.graph = [[0 for column in range(vertices)]  
                    for row in range(vertices)]
        

        self.driverInfo = []
        
    
    #driver setup
    def addDriver(self,name,pos,rating):
        self.driverInfo.append(Driver(name,pos,rating))
        

    def printSolution(self, dist): 
        print ("Vertex \tDistance from Source")
        for node in range(self.V): 
            print (node, "\t", dist[node]) 
  
    def minDistance(self, dist, sptSet):
   
        min = 1e6 
 
        for v in range(self.V): 
            if dist[v] < min and sptSet[v] == False: 
                min = dist[v] 
                min_index = v 
  
        return min_index 
  
    
    def dijkstra(self, src): 
  
        dist = [1e6] * self.V 
        dist[src] = 0
        sptSet = [False] * self.V 
        parentArray = [-1]*self.V

        for cout in range(self.V): 
  
         
            u = self.minDistance(dist, sptSet) 
  
            sptSet[u] = True

            for v in range(self.V): 
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]: 
                        dist[v] = dist[u] + self.graph[u][v]
                        parentArray[v] = u
        return (dist,parentArray)
    def findClosestDriver(self,src):
        
        distanceArray = self.dijkstra(src)[0]
        print(distanceArray)
        minDist = 1e8
        closestDriver = None

        for i in self.driverInfo:
            if(distanceArray[i.position] < minDist):
                minDist = distanceArray[i.position]
                closestDriver = i
        return closestDriver

    def generatePath(self,src,dst):

        if(src == dst):
            return []
        
        parentArray = self.dijkstra(src)[1]
        print(parentArray)

        path = []
        path.append(dst)

        finished = False
        child = dst

        while(not finished):
            parent = parentArray[child]
            path.append(parent)
            child = parent
            if(parent == src):
                break

        return path[::-1]
            

        
        

g = Graph(9) 
g.graph = [ [0, 4, 0, 0, 0, 0, 0, 8, 0], 
            [4, 0, 8, 0, 0, 0, 0, 11, 0], 
            [0, 8, 0, 7, 0, 4, 0, 0, 2], 
            [0, 0, 7, 0, 9, 14, 0, 0, 0], 
            [0, 0, 0, 9, 0, 10, 0, 0, 0], 
            [0, 0, 4, 14, 10, 0, 2, 0, 0], 
            [0, 0, 0, 0, 0, 2, 0, 1, 6], 
            [8, 11, 0, 0, 0, 0, 1, 0, 7], 
            [0, 0, 2, 0, 0, 0, 6, 7, 0] 
            ]; 

print(g.generatePath(0,8))
# print(g.parentArray)
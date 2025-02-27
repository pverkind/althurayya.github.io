from networkx.readwrite import json_graph
import io, json, csv
import re
import networkx as nx
import matplotlib.pyplot as plt	
import sys  
from decimal import *
from pyproj import *
from shapely.geometry import *
from shapely.ops import cascaded_union
from rtree import index

def createGraph(fileName):
    #roots = set()
    
   #G = nx.read_edgelist(fileName, delimiter=",", data=[("Distance_Meter", float)], encoding="utf8")
   #G.edges(data=True)
   #edge_labels = dict( ((u, v), d["Distance_Meter"]) for u, v, d in G.edges(data=True) )
   G = nx.Graph()
   getcontext().prec = 4
   with open(fileName, 'r') as meterFile:
      distReader = csv.reader(meterFile, delimiter=',')
      next(distReader, None)
      for row in distReader:
        G.add_node(row[0], lat=row[1], lng=row[2])
        G.add_node(row[3], lat=row[4], lng=row[5])
        G.add_edge(row[0],row[3], length= row[-1])
   neighbors = dict()
   # find nodes without coordinate
   null_coord_nodes = []
   for node in G.nodes():
     if G.node[node]['lat'] == "null" and G.node[node]['lng'] == "null":
       null_coord_nodes.append(node)
   proj1 = Proj(init='epsg:26915')
   # check neighbors of nodes without coordinate, whether they have coordinate or not
   with open("../Data/newCoords_general.csv", "w", encoding="utf8") as distMeter:
     fWriter = csv.writer(distMeter, delimiter=',',)
     fWriter.writerow(["lat", "lng", "name", "property"])
     for node in null_coord_nodes:
    
       neighbors[node] = []
       for n in G.neighbors(node):
         if G.node[n]['lat'] != "null" and G.node[n]['lng'] != "null": 
           neighbors[node].append(n) 
       # TODO: check nodes with one neighbour 
       # if a point has more than two neighbours in the network 
       neiLen = len(neighbors[node])
       if neiLen >= 2:
         coordsArr = []
         radArr = []
         cirArr = []
         for i in range(0, neiLen):          
           coordsArr.append(proj1(G.node[neighbors[node][i]]['lat'],G.node[neighbors[node][i]]['lng']))
           radArr.append(G[node][neighbors[node][i]]['length'])
           cirArr.append(Point(coordsArr[i]).buffer(Decimal(radArr[i])))
           print(i, "coords: ",coordsArr, "rad: ", radArr[i], "cir: ", cirArr[i])
         #if not circle1.intersects(circle2):
         #  fWriter.writerow(["null","null",node, "new"])
         #if circle1.intersects(circle2):
          # lat1,lon1= proj1(circle1.intersection(circle2).geoms[0].coords[0][0],circle1.intersection(circle2).geoms[0].coords[0][1],inverse=True)
           #lat2,lon2= proj1(circle1.intersection(circle2).geoms[1].coords[0][0],circle1.intersection(circle2).geoms[1].coords[0][1],inverse=True)
           #getcontext().prec = 4
           #fWriter.writerow([float("{0:0.5f}".format(lat1)),float("{0:0.5f}".format(lon1)),node, "new"])
           #fWriter.writerow([float("{0:0.5f}".format(lat2)),float("{0:0.5f}".format(lon2)),node, "new"])
           #print(node)
       #for nei in neighbors[node]:
         #print("nei: ",nei)
        # fWriter.writerow([G.node[nei]['lat'],G.node[nei]['lng'], nei, "old"])

   #for e in G.edges(data=True): 
   #  print("e ", e)
   #pos = nx.spring_layout(G)
   #nx.draw(G, pos)
   #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
   #nx.draw_graphviz(G)
   #plt.show()
   #with open(fileName, "r") as routesFile:
   # routesFile =csv.reader(routesFile, delimiter=',', quotechar='|')
   # for r in routesFile:
   #   print(r[0], " ", G[r[0]])
       

	
createGraph("../Data/tripleRoutes_withMeter2")


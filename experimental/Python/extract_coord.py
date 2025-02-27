"""
To extract coordinates and regions of sttl names of geographical text that are found in Cornu, using fuzzywuzzy library (or complete match commented!)
This scripts is initial and more complete functionalities is included in extract_coordWithHierarchy.py and then in extract_coordWithHierarchy_Normalized.py.

"""
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from networkx.readwrite import json_graph

import io, json
import re
import sys 
import csv
from json import load


reload(sys)  
sys.setdefaultencoding('utf8')

def getSetOfSttl(fileName,name):
    """
    Finds the sttls from the hierarchy file (geographical text)
    """
    names = list()
    with open(fileName, "r") as f1:
        f1 = f1.read().split("\n")
        for l in f1:
          ls = l.split(",")
          #print(ls[-1])
          if ls[-1].startswith(name):
            names.append(ls[-1].strip('STTL ').strip(' '))
    print("name count: ", len(names))
    return names


def findCoord(fileName, name, fWriter):
  """
  Using the sttl names, find the coordinates from cornu and writes them into a csv file
  """
  coords = []
  with open(fileName) as jsonFile:    
    allData = json.load(jsonFile)
    for d in allData["data"]:
      fName = d["arTitle"]
      sName = d["arTitleOther"].split(",")
#      if name == fName:
      # using fuzzywuzzy library
      if fuzz.ratio(name, fName) >= 90:
        fWriter.writerow([name, fName, sName[0], d["lat"], d["lon"], d["region"]])
      else:
        for n in sName:
#          if name == n.strip():
          # using fuzzywuzzy library
          if fuzz.ratio(name, n.strip()) >= 90:
            fWriter.writerow([name, fName, n.strip(), d["lat"], d["lon"], d["region"]])
            break


def getCornuSttlWithCoord(hierarchyFile, coordsFile):
    """
    The main function
    """
    global cnt
    data = []
    sttlNames = getSetOfSttl(hierarchyFile,"STTL")
    with open("../Data/STTLCoordsCSV_fuzzyWuzzy", 'w') as csvCoord:
      fWriter = csv.writer(csvCoord, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      fWriter.writerow(["geoTitle", "cornuName", "geoTitleOther", "lat", "lon", "cornuRegion"])
    
      for st in sttlNames:
        findCoord(coordsFile, st,fWriter)
           
      
getCornuSttlWithCoord("../Data/Shamela_0023696_Triples_H", "../Data/cornu_all_new2.json")
print("Done!")  
    

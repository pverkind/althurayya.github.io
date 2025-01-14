"""
Extracts region, coords, and topURI for the route sections of a geographic text, all from Cornu.
It also uses some Arabic normalizations on the word while searching and matching toponyms from both sources.
For those toponyms in route sections (i.e. FROM/TO) which doesn't find any match in cornu, fills the information with "null" value.
The out put is a csv file, with all data lines of route sections (from geo text), extended as:
["From", "From_lat", "From_long", "From_Region(Cornu)", "From_URI(Cornu)", "To", "To_lat", "To_long", "To_Region(Cornu)", "To_URI", "original distance in classic text"]
"""
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from networkx.readwrite import json_graph
import io, json
import re
import sys, codecs
import csv
from json import load
import operator

# used for python 2.7
#reload(sys)  
#sys.setdefaultencoding('utf8')


def normalizeArabic(text):
    """
    Normalization function
    """
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ه", "ة", text)
    text = re.sub("ک", "ك", text)
    if text.startswith("ال"):
      text = text[2:] 
    return(text)


def populateDict(string, data):
    """
    Populates a dictionay values with coordinates, region, and TOP_URI values for a toponym as key.
    used in getStartEndCoords function
    """
    dictionary = {}
    fName = data["arTitle"]
    sName = data["arTitleOther"].split(",")
    if string not in dictionary: 
      if normalizeArabic(string) == normalizeArabic(fName):
        dictionary[string] = []
        dictionary[string].extend([data["lat"], data["lon"], data['source'], data['topURI']])
      else:
        for n in sName:
          if normalizeArabic(string) == normalizeArabic(n.strip()):
            dictionary[string] = []
            dictionary[string].extend([data["lat"], data["lon"], data['source'], data['topURI']])
            break
    return dictionary

def getStartEndCoords(fileName1, fileName2):
    """
    Extracts the coordinates, region, and URI for each toponym at start or end of a route section.
    The result is a dictionary with toponyms as key, and extracted data as values.
    It calls populateDict function to populate the dictionsry.
    """
    uniqueNames = dict()
    with open(fileName1, "r", encoding="utf8") as f1:
        f1 = csv.reader(f1, delimiter='\t')
        for ls in f1:
            start = ls[0][4:].strip()
            end = ls[1][4:].strip()
            with open(fileName2, "r", encoding="utf8") as jsonFile:    
              allData = json.load(jsonFile)
              for d in allData["data"]:
                # populates the uniqueNames dictionary for start and end toponyms
                uniqueNames.update(populateDict(start, d))
                uniqueNames.update(populateDict(end, d))
        return uniqueNames


def getCornuCoord_forDistances(distanceFile, cornuRoutesFile, cornuCoordsFile):
    """
    The main function which calls the other functions to create a structure ans write it to a csv file.
    """
    dataToWrite = []
    not_common = []
    coords = getStartEndCoords(distanceFile,cornuCoordsFile)
    with open("../Data/Distances_withCoords_normalized", 'w', encoding="utf8") as csvCoord:
      fWriter = csv.writer(csvCoord, delimiter=',')
      fWriter.writerow(["From", "From_lat", "From_long", "From_Region", "From_URI", "To", "To_lat", "To_long", "To_Region", "To_URI", "distance"])
      with open(distanceFile, "r", encoding="utf8") as csvfile:
        distances = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for line in distances:
          start = line[0][5:].strip()
          end = line[1][5:].strip()
          distance = line[-1][5:].strip()
          fWriter.writerow([start, ",".join( str(e) for e in coords[start]) if start in coords else "null,null,null,null", 
                            end, ",".join( str(e) for e in coords[end]) if end in coords else "null,null,null,null", distance])
        #fWriter.writerow(dataToWrite)
          if start not in coords:
             not_common.append(start)
          if end not in coords:
             not_common.append(end)
    with open("../Data/Distances_withoutCoords_normalized", 'w', encoding="utf8") as f:
          writer = csv.writer(f, delimiter=',') 
          writer.writerow(["not_common"]) 
          for nc in not_common:
            writer.writerow([nc])

getCornuCoord_forDistances("../Data/Shamela_0023696_Triples_Dist", "../Data/all_routes_new.json", "../Data/cornu_all_new2.json")
print("Done!")  
    

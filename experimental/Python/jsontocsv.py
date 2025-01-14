"""
Converts json to csv
"""

import json
import csv
from json import load

def cornuJsonToCsv(openFile, writeFile):
  with open(openFile) as jsonFile:    
      allData = json.load(jsonFile)
      with open(writeFile, 'w') as csvCornu:
        fWriter = csv.writer(csvCornu, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fWriter.writerow(["arBW","source","arTitle","lat", "eiSearch","lon","region", "translitTitleOther","topURI","searchNames", "topTypeAlt", "topType", "translitTitle", "arTitleOther", "UStranslitTitle"])
      #print(allData["data"][0])  
        for d in allData["data"]:
          fWriter.writerow([d["arBW"], d["source"], d["arTitle"], d["lat"], d["eiSearch"], d["lon"], d["region"], d["translitTitleOther"], d["topURI"], d["searchNames"], d["topTypeAlt"], d["topType"], d["translitTitle"], d["arTitleOther"], d["UStranslitTitle"]])
  print("All done!")


cornuJsonToCsv("../Data/cornu_all_new2.js", "../Data/cornu.csv")

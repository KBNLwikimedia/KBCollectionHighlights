
import os, os.path, glob
import json
from pprint import pprint
from lxml import html
import requests

def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is not None:
                return item

def resolveIconClass(IconClassCode):
    import urllib.request
    with urllib.request.urlopen("http://iconclass.org/"+IconClassCode+".json") as url:
        IconClassData = json.loads(url.read().decode())
        IconClassText = IconClassData["txt"]["en"].capitalize()
        IconClassKeywords = IconClassData["kw"]["en"]
    return [IconClassText, IconClassKeywords]


jsonfile="KB79K2_illum.json" # the longer one
with open(jsonfile) as data_file:
    data = json.load(data_file)

foliolist =[]
typelist=[]
descriptionlist=[]
iconclasscodelist=[]

for i in range(len(data["records"]["record"])):
    foliolist.append(finditem(data["records"]["record"][i], "folio"))
    typelist.append(finditem(data["records"]["record"][i], "type"))
    descriptionlist.append(finditem(data["records"]["record"][i], "description"))
    iconclasscodelist.append(finditem(data["records"]["record"][i], "iconClass"))

    print("Folio: " + str(foliolist[i]))
    if isinstance(typelist[i], list): # more than 1 illumination on a folio, see for instance 080r, 083r
        for j in range(len(typelist[i])):
            print("The " + typelist[i][j] + " shows " + descriptionlist[i][j])
    else: # 1 illumination on a folio
        print("The " + typelist[i] + " shows " + descriptionlist[i])

# Add extra description (+ keywords) from Iconclass
    if isinstance(iconclasscodelist[i], list):
        print("Extra information from IconClass:")
        for k in range(len(iconclasscodelist[i])):
            print("   * " + str(resolveIconClass(iconclasscodelist[i][k])[0]) + " (http://iconclass.org/rkd/" + iconclasscodelist[i][k] + ")")
    elif isinstance(iconclasscodelist[i], str):
        print("Extra information from IconClass:")
        print("   * " + str(resolveIconClass(iconclasscodelist[i])[0]) + " (http://iconclass.org/rkd/" + iconclasscodelist[i] + ")")
    else:
        print("")
    print("-------------------------------------------")





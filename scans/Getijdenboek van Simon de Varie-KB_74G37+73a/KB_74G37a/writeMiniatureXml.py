
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
#In: Iconclass code
#Out: IconClassText and IconClassKeywords in English
    import urllib.request
    with urllib.request.urlopen("http://iconclass.org/" + IconClassCode + ".json") as url:
        IconClassData = json.loads(url.read().decode())
        #print("aaaaaaaaaaaaaaaaaaaaaaaaaa "+str(IconClassData))
        if str(IconClassData) != "None":
            IconClassText = IconClassData["txt"]["en"].capitalize()
            IconClassKeywords = IconClassData["kw"]["en"]
            return [IconClassText, IconClassKeywords]
        else:
            return None


# Get data about the miniature:
# In: miniature filename, bv 043r_b2.jpg
# Out:
# 1 Description: string
# 2 Width of miniature, in mmm (string)
# 3 Height of miniature, in mmm (string)
# 4 Iconclass Codes: string (if 1 Iconclass code) or list (if >1 IC code)
# 5 Folio in which the miniature is contained
# 6 Miniaturist who made the miniature
def getMiniatureData(miniatureFile):
    ICString="" #IconClass String
    miniaturistString = ""
    jsonfile = "KB74G37a_illum.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["records"]["record"])):
        if data["records"]["record"][i]["miniature"] == miniatureFile:
            miniatureDescription = finditem(data["records"]["record"][i], "description")
            folio = finditem(data["records"]["record"][i], "folio")
            miniatureDimensions = finditem(data["records"]["record"][i], "dimensions") #75x60
            miniatureWidth= miniatureDimensions.split("x")[0]
            miniatureHeight=miniatureDimensions.split("x")[1]
            miniatureICCode = finditem(data["records"]["record"][i], "iconClass")
            miniaturist = finditem(data["records"]["record"][i], "miniaturist")
            if miniaturist == "Master of Jean Rolin II":
                miniaturistString = "{{Creator:Maître de Jean Rolin}}"
            elif miniaturist == "Dunois Master":
                miniaturistString = "{{Creator:Maître de Dunois}}"
            elif miniaturist == "Jean Fouquet":
                miniaturistString = "{{Creator:Jean Fouquet}}"

            if miniatureICCode != None:
                if isinstance(miniatureICCode, list):  # more than 1 IC code for a miniature
                    for k in miniatureICCode:
                        if resolveIconClass(k) != None:
                            ICString += "*"+str(resolveIconClass(k)[0]) +  " ([http://iconclass.org/rkd/"+str(k) + " " + str(k) + "])\n"
                        else:
                            ICString += ""
                else:
                    if resolveIconClass(miniatureICCode) != None:
                        ICString += "*"+str(resolveIconClass(miniatureICCode)[0]) +  " ([http://iconclass.org/rkd/"+miniatureICCode + " " + miniatureICCode + "])\n"
                    else: ICString += ""
    data_file.close()
    #print(miniatureDescriptionEN, miniatureWidth, miniatureHeight, ICString, folio)
    return (miniatureDescription, miniatureWidth, miniatureHeight, ICString, folio, miniaturistString)


#===========================================================

#config paths/ urls
current_dir = os.path.dirname(os.path.realpath(__file__))
imagedir= current_dir + "\\images\\miniaturen\\"
images_base_url="https://www.kb.nl/kbhtml/simondevarie2/miniaturen/"
sourcetemplate = "{{Koninklijke Bibliotheek}}"


# {{Artwork}} template on Commons, as stated in GWToolset
# accessionnumber =	"" (=ppn)
# artist =	""
# author =	""
# creditline =	""
# date =	""
# demo =		""
# department =		""
# description =		""
# dimensions =		""
# exhibitionhistory =	""
# inscriptions =		""
# institution =		""
# medium =		""
# notes =		""
# objecthistory =	""
# objecttype =		""
# otherfields =		""
# otherversions =		""
# permission =		""
# placeofcreation =		""
# placeofdiscovery =		""
# references =		""
# source =		""
# strict =		""
# title =		""
# wikidata =
# wikidatacat =	""
# GWToolsettitle =	""
# URLtothemediafile =""

#---------------------------
institution = "Koninklijke Bibliotheek"
medium = "Miniature on parchment"
permission = "{{PD-art|PD-old-70-1923}}"
wikidata = "Q3831825"
source =  sourcetemplate
date = "1455"
placeofcreation = "{{Paris}}"
permission = "{{PD-art|PD-old-70-1923}}"

base_titleGWT1 = "Book of hours Simon de Varie - KB 74 G37a" # Voor de titel van de File: op Commons
base_titleGWT2 = "Book of Hours of Simon de Varie - KB 74 G37a" # foutje gemaakt in de naamgeving...
base_title    = "from the Book of Hours of Simon de Varie - KB 74 G37a" #Titel in de metadata
base_description = " from the [[:en:Book_of_Hours_of_Simon_de_Varie|Book of Hours of Simon de Varie]] - KB 74 G37a"
#=====================================================================

XMLoutputfile = open("simondevarie_miniaturenKB74G37a.xml", "w", encoding="UTF-8")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

#filenames for miniatures are in the format 74g37_017v_min.jpg

for infile in glob.glob(os.path.join(imagedir, '*.jpg')):
    picname = infile.replace(imagedir, "") #  74g37_017v_min.jpg
    print("picname = " + picname)

    folio = getMiniatureData(picname)[4] # 74g37_017v_min.jpg --> 017v
    print(folio)

    dimensions = "{{Size|mm|" + getMiniatureData(picname)[1] +"|"+ getMiniatureData(picname)[2] + "}}"

    GWToolsettitle = getMiniatureData(picname)[0] + " - " + base_titleGWT1 + " - " + str(picname).split(".")[0][6:]
    title = getMiniatureData(picname)[0] + " - miniature from folio " + folio + base_title
    if getMiniatureData(picname)[5] != "":
        artist = str(getMiniatureData(picname)[5])

    #File:Book of Hours of Simon de Varie - KB 74 G37 - folio 017v.jpg

    description = getMiniatureData(picname)[0] + " - miniature from [[:c:File:"+ base_titleGWT2 + " - folio " + str(folio) + ".jpg" + "|folio " + str(folio)+ "]]" + base_description+ "\n"
    if getMiniatureData(picname)[3] != "":
        description += "===== Topics depicted in this miniature ===== \n\n"
        description += getMiniatureData(picname)[3] + "\n"
    description += "[[File:"+ base_titleGWT2 + " - folio " + str(folio) + ".jpg" + "|thumb|left|This miniature is part of [[:c:File:"+ base_titleGWT2 + " - folio " + str(folio) + ".jpg" + "|folio " + str(folio)+ "]]]]"

    xmlstring += "<record>\n"
    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(folio)+"</folio>\n"
    xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"
    xmlstring += "    <medium>" + str(medium) + "</medium>\n"
    xmlstring += "    <date>" + str(date) + "</date>\n"
    xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
    xmlstring += "    <miniatureFile>" + str(picname) + "</miniatureFile>\n"
    xmlstring += "    <dimensions>" +str(dimensions)+ "</dimensions>\n"
    xmlstring += "    <artist>" + str(artist) + "</artist>\n"
    xmlstring += "    <URLtothemediafile>" + images_base_url + str(picname) + "</URLtothemediafile>\n"
    xmlstring += "    <title>" + str(title) + "</title>\n"
    xmlstring += "    <GWToolsettitle>" + str(GWToolsettitle) + "</GWToolsettitle>\n"
    xmlstring += "    <description>"+ str(description) + "</description>\n"
    xmlstring += "</record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()






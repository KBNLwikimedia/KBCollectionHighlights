
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
# 1 DescriptionEN: string
# 2 Width of miniature, in mmm (string)
# 3 Height of miniature, in mmm (string)
# 4 Iconclass Codes: string (if 1 Iconclass code) or list (if >1 IC code)
# 5 Folio in which the miniature is contained
def getMiniatureData(miniatureFile):
    ICString="" #IconClass String
    jsonfile = "KBKA16_illum.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["records"]["record"])):
        if data["records"]["record"][i]["miniature"] == miniatureFile:
            miniatureDescriptionEN = finditem(data["records"]["record"][i], "descriptionEN")
            folio = finditem(data["records"]["record"][i], "folio")
            miniatureDimensions = finditem(data["records"]["record"][i], "dimensions") #75x60
            miniatureWidth= miniatureDimensions.split("x")[0]
            miniatureHeight=miniatureDimensions.split("x")[1]
            miniatureICCode = finditem(data["records"]["record"][i], "iconClass")

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
    return (miniatureDescriptionEN, miniatureWidth, miniatureHeight, ICString, folio)


#===========================================================

#config paths/ urls
current_dir = os.path.dirname(os.path.realpath(__file__))
imagedir= current_dir + "\\images\\bladerboek\\7r - 25v De natuurkunde van het geheelal\\miniaturen\\"
images_base_url="https://www.kb.nl/kbhtml/dernaturenbloeme/miniaturen/"
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
medium = "Illumination on parchment"
permission = "{{PD-art|PD-old-70-1923}}"
wikidata = "Q46995981"
source =  sourcetemplate
date = "{{other date|circa|1340|1350}}"
placeofcreation = "Utrecht, Northern Netherlands"


base_titleGWT = "De natuurkunde van het geheelal by Gheraert van Lienhout - part of Der naturen bloeme - KB KA 16" # Voor de titel van de File: op Commons
base_title    = " from De natuurkunde van het geheelal by Gheraert van Lienhout. This text is contained in Der naturen bloeme - KB KA 16" #Titel in de metadata
base_description = " from De natuurkunde van het geheelal by Gheraert van Lienhout. This text is contained in [[:c:Category:Der naturen bloeme - KB KA 16|Der naturen bloeme]] (KB KA 16)"

#=====================================================================

XMLoutputfile = open("dernaturenbloeme_miniaturen.xml", "w", encoding="UTF-8")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

#filenames for miniatures can be in the formats:
# 046r.jpg
# 046v_a1.jpg

for infile in glob.glob(os.path.join(imagedir, '*.jpg')):
    picname = infile.replace(imagedir, "") # 046v_a1.jpg or 046r.jpg
    print("picname = " + picname)
    dimensions = "{{Size|mm|" + getMiniatureData(picname)[1] +"|"+ getMiniatureData(picname)[2] + "}}"

    folio = getMiniatureData(picname)[4] # string
    folio_number = folio[0:3] # folio = "040v" --> folio_number = "040" (string)
    folio_int = int(folio_number) #convert string to integer -->  folio_int = 40 (without leading 0)
    side = folio[3] # lefthand or rightside folio - folio = "040v" --> side = "v"
    folio_0 = folio[0] # first character of folio: 0 (bv folio 040r) or 1 (bv folio 117v)

    #print("XXXXXX " + folio[0:3] + " ---- " + str(side))
    if side == "r":
        hand = "righthand" #folio=041r
        if folio_0 == "0":
            opening = "0" + str(folio_int - 1) + "v-" + str(folio)  # opening die bij het folium hoort, bv bij folium "041r" hoort opening "040v-041r"
        elif folio_0 == "1":
            opening = str(folio_int-1)+ "v-" + str(folio)# opening die bij het folium hoort, bv bij folium "041r" hoort opening "040v-041r"
        else: print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        print(opening)
    elif side == "v":
        hand = "lefthand" #folio=040v
        if folio_0 == "0":
            opening = str(folio) + "-0" + str(folio_int+1)+ "r"
        elif folio_0 == "1":
            opening = str(folio) + "-" + str(folio_int + 1) + "r"
        else: print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
        print(opening)
    else: print ("AAAAAAAAAAAAAAAAAAAAAAAAAAA")

    GWToolsettitle = getMiniatureData(picname)[0] + " - " + base_titleGWT + " - " + str(picname).split(".")[0]
    title = getMiniatureData(picname)[0] + " - miniature from folio " + folio + base_title

    description = getMiniatureData(picname)[0] + " - miniature from [[:c:File:"+ base_titleGWT + " - " + str(opening) + ".jpg" + "|folio " + str(folio)+ "]]" + base_description+ "\n"

    if getMiniatureData(picname)[3] != "":
        description += "===== Topics depicted in this miniature ===== \n\n"
        description += getMiniatureData(picname)[3] + "\n"

    description += "[[File:"+ base_titleGWT + " - " + str(opening) + ".jpg" + "|thumb|left|This miniature is part of the "+ str(hand) + " side [[:c:File:"+ base_titleGWT + " - " + str(opening) + ".jpg" + "|folio " + str(folio)+ "]]]]"

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
    xmlstring += "    <dimensions>" +str(dimensions)+ " </dimensions>\n"
    xmlstring += "    <URLtothemediafile>" + images_base_url + str(picname) + "</URLtothemediafile>\n"
    xmlstring += "    <title>" + str(title) + "</title>\n"
    xmlstring += "    <GWToolsettitle>" + str(GWToolsettitle) + "</GWToolsettitle>\n"
    xmlstring += "    <description>"+ str(description) + "</description>\n"
    xmlstring += "</record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()






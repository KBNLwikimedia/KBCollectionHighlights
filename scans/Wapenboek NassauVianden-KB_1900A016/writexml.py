
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

#config paths/ urls
current_dir = os.path.dirname(os.path.realpath(__file__))
imagedir_hires= current_dir + "\\images\\bladerboek\\"
images_base_url_hires="https://www.kb.nl/kbhtml/nassauvianden/"

# Open annotations json file
annotationsfile="annotations.json"
with open(annotationsfile) as annofile:
    annotationsdata = json.load(annofile)


homepageNL = "https://www.kb.nl/themas/middeleeuwse-handschriften/wapenboek-nassau-vianden-ca-1490"
#homepageEN = "https://www.kb.nl/en/themes/middle-ages/beatrijs"
browse_entry = "https://galerij.kb.nl/kb.html#/nl/nassauvianden/page/1/zoom/3/lat/-75.16330024622059/lng/-94.39453125"

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

#----------------------
ppn = "412678861"
signature = "KB 1900 A 016"
institution = "Koninklijke Bibliotheek"
medium = "{{Technique|drawing|paper}}"
dimensions = "{{Size|mm|215|145}}"
permission = "{{PD-art|PD-old-70-1923}}"
source =  "{{Koninklijke Bibliotheek}}"
date = "{{complex date|~|1485|1495}}"
placeofcreation = "[[:en:Duchy of Brabant|Brabant]], [[:en:Breda|Breda]]?"
notes= "Script is [[:nl:Littera cursiva|Littera cursiva]]"
#nfolios = "The manuscripts contains 34 complete and 1 incomplete hand-colored coats of arms and two portraits of its creator, the Herald of Nassau-Vianden."
#language = "Dutch"
#script = "mainly [[:nl:Littera hybrida|littera hybrida]], on occasion [[:nl:Littera_textualis|littera textualis]]"
#wikidata = "Q1929931"

#Meertalige velden
artistEN = "Herald of Nassau-Vianden"
artistNL = "Heraut Nassau-Vianden"

titleNL = "Wapenboek Nassau-Vianden"
titleEN = "Nassau-Vianden armorial"

objecthistoryEN ="This armorial was presumably commissioned by [[:en:Engelbert II of Nassau|Engelbert II of Nassau]] (1451-1504). After him it was possibly owned by [[:en:William the Silent|William I, Prince of Orange (William the Silent)]] (1533-1584) and [[:nl:Jacques Wijts|Jacques Wijts]] (ca. 1579-1643). In 1898 the manuscripts is known to be in the library of the German graphical artist [[:en:Otto Hupp|Otto Hupp]]."
objecthistoryNL ="Dit wapenboek werd vermoedelijk gemaakt in opdracht voor graaf [[:nl:Engelbrecht II van Nassau|Engelbrecht II van Nassau]] (1451-1504). Het is mogelijk in bezit geweeest van van [[:nl:Willem van Oranje|Willem van Oranje (Willem de Zwijger)]] (1533-1584) en [[:nl:Jacques Wijts|Jacques Wijts]] (ca. 1579-1643). In 1898 maakte het deel uit van de verzameling van heraldiek schilder [[:en:Otto Hupp|Otto Hupp]] (1859-1949)."

#references = ""


#===================================================================

XMLoutputfile = open("nassauvianden.xml", "w")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname = infile.replace(imagedir_hires, "") #"002r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"002r"
    #print(picname_trunc)

    xmlstring += "  <record>\n"
    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(picname_trunc)+"</folio>\n"
    xmlstring += "    <date>" + str(date) + "</date>\n"
    xmlstring += "    <notes>" + str(notes) + "</notes>\n"
    xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
    xmlstring += "    <dimensions>" + str(dimensions) + "</dimensions>\n"
    xmlstring += "    <medium>" + str(medium) + "</medium>\n"

    #xmlstring += "    <references>" + str(references) + "</references>\n"
    #xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"
    #xmlstring += "    <otherversions>"+ str(otherversions) +"</otherversions>\n"

    xmlstring += "    <artist lang='nl'>" + str(artistNL) + "</artist>\n"
    xmlstring += "    <artist lang='en'>" + str(artistEN) + "</artist>\n"
    xmlstring += "    <objecthistory lang='nl'>"+ str(objecthistoryNL)+"</objecthistory>\n"
    xmlstring += "    <objecthistory lang='en'>"+ str(objecthistoryEN)+"</objecthistory>\n"
    xmlstring += "    <accessionnumber>*[" + browse_entry + " Browse this armorial] on the website of the KB." + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch]" + "\n*" + "Description of the armorial in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN="+str(ppn)+"</accessionnumber>\n"

# Get data from annotations
    #print(str(picname_trunc))
    annodic = finditem(annotationsdata, picname_trunc)

    GWbaseTitle = annodic["Title"]
    xmlstring += "    <GWToolsettitle>" + str(GWbaseTitle) + " - Wapenboek Nassau-Vianden - " + signature + ", folium " + str(picname_trunc) + "</GWToolsettitle>\n"
    xmlstring += "    <title lang='nl'>" + str(GWbaseTitle) +  " - folium " + str(picname_trunc) + " van het Wapenboek Nassau-Vianden uit de collectie van de [[:nl:Koninklijke Bibliotheek_(Nederland)|Koninklijke Bibliotheek]].</title>\n"
    xmlstring += "    <title lang='en'>" + str(GWbaseTitle) +  " - folium " + str(picname_trunc) + " from the Nassau-Vianden armorial from the collection of the [[:en:National Library of the Netherlands|National Library of the Netherlands]].</title>\n"


    baseDescriptionNL = annodic["Description"]
    xmlstring += "    <description lang='nl'>"+ str(baseDescriptionNL) + "</description>\n"

    #if folio == "moderneband-voor":
        #xmlstring += ""
        # xmlstring += "    <description>Front of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
        # xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        # xmlstring += "    <GWToolsettitle>"+ signature+ " - Front of brown leather binding from 1993. Inside is the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
        # xmlstring += "    <title>Front of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
        # xmlstring += "    <medium>Brown leather binding</medium>\n"
        # xmlstring += "    <date>" + "1993" + "</date>\n"
        # xmlstring += "    <artist>" + "Lucie M. Gimbr&#xe8;re" + "</artist>\n"
        # xmlstring += "    <placeofcreation>" + "[[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]" + "</placeofcreation>\n"
        # xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"

    #else: #all the normal folio



    xmlstring += "  </record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()
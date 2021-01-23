
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

def countMiniatures(folio):
#In : folio (string)
#Returns: Number of miniatures for this folio
    numberOfminiatures = 0  # number of miniatures on a given folio
    jsonfile = "KB74G37a_illum.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["records"]["record"])):
        if data["records"]["record"][i]["folio"] == folio:
            numberOfminiatures += 1
    data_file.close()
    #print(numberOfminiatures)
    return numberOfminiatures #integer

def findMiniatures(folio):
#In : folio (string)
#Returns: miniatureString: string with miniatures on this particular folio
    miniatureString = ""
    jsonfile = "KB74G37a_illum.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["records"]["record"])):
        if data["records"]["record"][i]["folio"] == folio:
            #print("-----------------"+str(folio)+"-------------------------")
            miniatureFile = finditem(data["records"]["record"][i], "miniature")
            miniatureDesc = finditem(data["records"]["record"][i], "description")
            if countMiniatures(folio) > 0 : #build <gallery> of minitures
                miniatureString += "File:" + str(miniatureDesc) + " - Book of hours Simon de Varie - KB 74 G37a - " + str(miniatureFile)+ "##" + str(miniatureDesc)+ "\n\n"
            # We'll replace the '##' with '|' with VisualFileChange.js later on
            # print(str(folio_dict))
    data_file.close()
    return (miniatureString)

#config paths/ urls
current_dir = os.path.dirname(os.path.realpath(__file__))
imagedir= current_dir + "\\images\\losseFolio\\"


images_base_url="https://www.kb.nl/kbhtml/simondevarie2/" #nog aanvragen bij Marcel... custom scans gebruiken

homepageNL = "https://www.kb.nl/themas/middeleeuwen/getijdenboek-van-simon-de-varie"
homepageEN = "https://www.kb.nl/en/themes/middle-ages/book-of-hours-of-simon-de-varie"

sourcetemplate = "{{Koninklijke Bibliotheek}}"

# calendar_dic={
#     '003_fl000v-001r':'Laumaent (January)',
#     '004_001v-002r':'Sporkelle (February) and Maerte (March)',
#     '005_002v-003r':'Aprul (April) and Meye (May)',
#     '006_003v-004r':'Ghersmaent? (June) and Hoymaent (July)',
#     '007_004v-005r':'Oestmaent? (August) and Spelmaent (September)' ,
#     '008_005v-006r':'De maent van Bamisse?? (October) and De maent van alrehelige misse?? (November)'
#}
#Slachmaent (December)


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

ppn = "31177864X"
institution = "Koninklijke Bibliotheek"
medium = "Manuscript with illuminations on parchment"
#medium = "Manuscript on parchment" #for calendar
dimensions = "The folio size is {{Size|mm|116|85}}, the block size is {{Size|mm|57|36}} with 1 column and 15 lines"
#dimensions_calendar = "Folio size: {{Size|mm|116|84}} - Block size: {{Size|mm|68|43}} with 1 column and 16 lines"
permission = "{{PD-art|PD-old-70-1923}}"
wikidata = "Q3831825"
browse_entry = "https://galerij.kb.nl/kb.html#/nl/devarie2/page/7/zoom/3/lat/-73.2773532019247/lng/-66.005859375"
source =  sourcetemplate
date = "1455"
placeofcreation = "{{Paris}} and {{Tours}} for the miniatures by Jean Fouquet"
language = "Latin"
script = "[[:en:Bastarda|Bastarda]]"
notes= "Text in "+str(language)+ ", script is " + str(script)
artist = "{{Creator:Maître de Jean Rolin}} {{Creator:Maître de Dunois}} {{Creator:Jean Fouquet}}"
otherversions = ""
objecthistory = ""
base_titleGWT = "Book of Hours of Simon de Varie - KB 74 G37a" # Voor de titel van de File: op Commons
base_title    = "[[:en:Book_of_Hours_of_Simon_de_Varie|Book of Hours of Simon de Varie]] - KB 74 G37a" #Titel in de metadata


XMLoutputfile = open("simondevarie_74G37a.xml", "w", encoding="UTF-8")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

for infile in glob.glob(os.path.join(imagedir, '*.jpg')):
    picname = infile.replace(imagedir, "") #"74g37_008r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"74g37_008r"
    # split in 2 parts: 74g37 + 008r
    imagenumber = picname_trunc.split("_")[0] #74g37 - we can further ignore this part, this is always the same
    folio = picname_trunc.split("_")[1] #f008r
    #print(imagenumber + " -- " + str(folio) + " -- " + str(countMiniatures(folio)) + " -- " + str(findMiniatures(folio)))
    #print(imagenumber + " -- " + str(folio) + " -- " + str(countMiniatures(folio)))# + " -- " + str(findMiniatures(folio)))
    if countMiniatures(folio) > 0 :
        print('"'+str(folio)+'",' + " -- " + str(countMiniatures(folio)))


    xmlstring += "<record>\n"
    xmlstring += "    <accessionnumber>*[" + browse_entry + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(picname_trunc)+"</folio>\n"
    #xmlstring += "    <author>"+ str(author) + "</author>\n"
    xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"
    #xmlstring += "    <otherversions>"+ str(otherversions) +"</otherversions>\n"
    #xmlstring += "    <objecthistory>"+ str(objecthistory)+"</objecthistory>\n"
    # else:  # all the normal pages
    xmlstring += "    <artist>" + str(artist) + "</artist>\n"
    xmlstring += "    <notes>" + str(notes) + "</notes>\n"
    xmlstring += "    <dimensions>" + dimensions + "</dimensions>\n"
    xmlstring += "    <medium>" + str(medium) + "</medium>\n"
    xmlstring += "    <date>" + str(date) + "</date>\n"
    xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
    xmlstring += "    <URLtothemediafile>" + images_base_url + str(picname) + "</URLtothemediafile>\n"
    xmlstring += "    <GWToolsettitle>" + base_titleGWT + " - folio " + str(folio) + "</GWToolsettitle>\n"
    xmlstring += "    <title>Folio " + str(folio) + " from the " + str(base_titleGWT) + "</title>\n"
    xmlstring += "    <description>Folio " + str(folio) + " from the " + str(base_title) + "\n"
    if countMiniatures(folio) > 0 :
        if countMiniatures(folio) == 1 :
            xmlstring += "=====Miniature on the folio " + str(folio) + "=====" + "\n\n"
        if countMiniatures(folio) > 1:
            xmlstring += "=====Miniatures on the folio " + str(folio) + "=====" + "\n\n"
        xmlstring += "gallery mode='packed-hover' style='text-align:left'" + "\n\n"
        xmlstring += findMiniatures(str(folio))
        xmlstring += "/gallery" + "\n\n"             # We'll fix the <gallery> tag with VisualFileChange.js later on
    xmlstring += "    </description>\n"

    xmlstring += "</record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()


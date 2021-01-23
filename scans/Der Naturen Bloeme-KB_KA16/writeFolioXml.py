
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

def hasMiniatures(folio):
#In : folio (string)
#Returns: Boolan True is folio has maniatures, otherwise False
    hasMiniatures = False
    jsonfile = "KBKA16_illum.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["records"]["record"])):
        if data["records"]["record"][i]["folio"] == folio:
            hasMiniatures = True
    data_file.close()
    return hasMiniatures

def findMiniatures(folio):
#In : folio (string)
#Returns: miniatureString: string with miniatures on this particular folio
    miniatureString = ""
    jsonfile = "KBKA16_illum.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["records"]["record"])):
        if data["records"]["record"][i]["folio"] == folio:
            #print("-----------------"+str(folio)+"-------------------------")
            miniatureFile = finditem(data["records"]["record"][i], "miniature")
            miniatureDescEN = finditem(data["records"]["record"][i], "descriptionEN")
            miniatureString += "File:" + str(miniatureDescEN) + " - Der naturen bloeme - Jacob van Maerlant - KB KA 16 - " + str(miniatureFile) + "##" + str(miniatureDescEN)+ "\n\n"
            # We'll replace the '##' with '|' with VisualFileChange.js later on
            # print(str(folio_dict))
    data_file.close()
    return (miniatureString)


def KBurlString(folio):
# In : folio (string)
# Returns: this sort of string of KB-urls
#[https://galerij.kb.nl/kb.html#/nl/dernaturenbloeme/page/42/zoom/4/lat/-3.601142320158722/lng/-118.30078125 Naecte Vroede] - [https://galerij.kb.nl/kb.html#/nl/dernaturenbloeme/page/42/zoom/4/lat/30.826780904779774/lng/-40.42968749999999 Braghmannen] - [https://galerij.kb.nl/kb.html#/nl/dernaturenbloeme/page/42/zoom/4/lat/-50.792047064406844/lng/-39.7265625 Volk dat zijn doden verbrandt] - [https://galerij.kb.nl/kb.html#/nl/dernaturenbloeme/page/42/zoom/4/lat/-75.20824498631067/lng/-37.96875 Volk dat zijn oude ouders dood slaat]
    KBurlString = ""
    jsonfile = "KBKA16-miniaturen-namenNL-coordinaten.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["miniatures"]["miniature"])):
        if data["miniatures"]["miniature"][i]["folio"] == folio:
            print("-----------------"+str(folio)+"-------------------------")
            miniatureKBurl =  finditem(data["miniatures"]["miniature"][i], "url")
            miniatureDescNL = finditem(data["miniatures"]["miniature"][i], "descriptionNL")
            KBurlString += "[" + miniatureKBurl + " " + miniatureDescNL + "] - "
    return(KBurlString)


#config paths/ urls
current_dir = os.path.dirname(os.path.realpath(__file__))
imagedir= current_dir + "\\images\\bladerboek\\1r - 6v Utrechtse kalender\\"


images_base_url="https://www.kb.nl/kbhtml/dernaturenbloeme/"

homepageNL = "https://www.kb.nl/themas/middeleeuwen/der-naturen-bloeme-jacob-van-maerlant"
homepageEN = "https://www.kb.nl/en/themes/middle-ages/der-naturen-bloeme-jacob-van-maerlant"

sourcetemplate = "{{Koninklijke Bibliotheek}}"

calendar_dic={
    '003_fl000v-001r':'Laumaent (January)',
    '004_001v-002r':'Sporkelle (February) and Maerte (March)',
    '005_002v-003r':'Aprul (April) and Meye (May)',
    '006_003v-004r':'Ghersmaent? (June) and Hoymaent (July)',
    '007_004v-005r':'Oestmaent? (August) and Spelmaent (September)' ,
    '008_005v-006r':'De maent van Bamisse?? (October) and De maent van alrehelige misse?? (November)'
}
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
ppn = "311784593"
institution = "Koninklijke Bibliotheek"
#medium = "Manuscript with illuminations on parchment"
medium = "Manuscript on parchment" #for calendar
dimensions = "Folio size: {{Size|mm|278|208}} - Block size: {{Size|mm|215|160}} with 2 columns and 38-40 lines"
#dimensions_calendar = "Folio size: {{Size|mm|116|84}} - Block size: {{Size|mm|68|43}} with 1 column and 16 lines"
permission = "{{PD-art|PD-old-70-1923}}"
wikidata = "Q46995981"
browse_entry = "https://galerij.kb.nl/kb.html#/nl/dernaturenbloeme/page/2/zoom/2/lat/-61.68987220045999/lng/66.26953125"
source =  sourcetemplate
base_titleGWT = "Utrecht calendar - part of Der naturen bloeme - KB KA 16" # Voor de titel van de File: op Commons
base_title    = "Utrecht calendar" #Titel in de metadata

date = "{{other date|circa|1340|1350}}"
placeofcreation = "Utrecht, Northern Netherlands"
language = "Dutch"
script = "Littera textualis"
notes= "Text in "+str(language)+ ", script is " + str(script)
artist = ""
otherversions = ""

objecthistory = ""
#illuminations = "XXXX27 full-page miniatures (possibly 15 missing); 16 historiated initials; decorated initials with border decoration; penwork initials"
#nfolios = "xxx"

XMLoutputfile = open("dernaturenbloemeTEST.xml", "w", encoding="UTF-8")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"


for infile in glob.glob(os.path.join(imagedir, '*.jpg')):
    picname = infile.replace(imagedir, "") #"004_001v-002r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"004_001v-002r"
    # split in 3 parts: 010 + 002v + 003r - where applicable formatwise
    if picname_trunc != "001_voorplat" and picname_trunc != "160_achterplat":
        imagenumber = picname_trunc.split("_")[0] #010
        folio_left = picname_trunc.split("_")[1].split("-")[0]  # 002v
        folio_right = picname_trunc.split("-")[1] #003r
        #print(imagenumber + " -- " + folio_left + " -- " + str(folio_right))
    else:
        imagenumber = picname_trunc.split("_")[0] #160
        cover = picname_trunc.split("_")[1] #achterplat

    xmlstring += "<record>\n"
   #xmlstring += "    <accessionnumber>*[" + browse_entry + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"

    #for calendar
    xmlstring += "    <accessionnumber>*[" + browse_entry + " View this calendar] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"


    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(picname_trunc)+"</folio>\n"
    #xmlstring += "    <author>"+ str(author) + "</author>\n"
    xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"
    xmlstring += "    <otherversions>"+ str(otherversions) +"</otherversions>\n"
    xmlstring += "    <objecthistory>"+ str(objecthistory)+"</objecthistory>\n"
    # else:  # all the normal pages
    #xmlstring += "    <artist>" + str(artist) + "</artist>\n"
    xmlstring += "    <notes>" + str(notes) + "</notes>\n"
    xmlstring += "    <dimensions>" + dimensions + "</dimensions>\n"
    xmlstring += "    <medium>" + str(medium) + "</medium>\n"
    xmlstring += "    <date>" + str(date) + "</date>\n"
    xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
    xmlstring += "    <URLtothemediafile>" + images_base_url + str(picname) + "</URLtothemediafile>\n"
    xmlstring += "    <title>Calendar for the months of " + calendar_dic[picname_trunc] + " - " + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
    xmlstring += "    <GWToolsettitle>" + calendar_dic[picname_trunc] + " - " + base_titleGWT + " - " + folio_left + "-" + folio_right + "</GWToolsettitle>\n"

    #aaaaaaaa w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]] - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</description>\n"

    xmlstring += "    <description>Calendar for the months of " + calendar_dic[picname_trunc] + ". This calendar from Utrecht is contained in [[:c:Category:Der naturen bloeme - KB KA 16|Der naturen bloeme]] (KB KA 16)\n"
    #if hasMiniatures(folio_left):
    #     xmlstring += "=====Miniatures on the left folio " + str(folio_left) + "=====" + "\n\n"
    #     xmlstring += "gallery mode='packed-hover' style='text-align:left'" + "\n\n"
    #     xmlstring += findMiniatures(str(folio_left))
    #     xmlstring += "/gallery" + "\n\n"
    #     xmlstring += "See these miniatures on the website of the KB: " + KBurlString(folio_left) + "\n\n"
    # if hasMiniatures(folio_right):
    #     xmlstring += "=====Miniatures on the right folio " + str(folio_right) + "=====" + "\n\n"
    #     xmlstring += "gallery mode='packed-hover' style='text-align:left'" + "\n\n"
    #     xmlstring += findMiniatures(folio_right)
    #     xmlstring += "/gallery" + "\n\n"
    #     xmlstring += "See these miniatures on the website of the KB: " +  KBurlString(folio_right) + "\n\n"
    xmlstring += "    </description>\n"

    xmlstring += "</record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()

    # if picname_trunc == "001_voorplat":
    #     xmlstring += "    <description>Front of red velvet binding from 18th century with silver locks and gilded edges. Inside is the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]</description>\n"
    #     xmlstring += "    <URLtothemediafile>"+images_base_url+str(picname)+"</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Front of red velvet binding from 18th century with silver locks  and gilded edges</GWToolsettitle>\n"
    #     xmlstring += "    <title>"+ base_title + " - Front of red velvet binding from 18th century with silver locks and gilded edges</title>\n"
    #     xmlstring += "    <medium>Red velvet binding with silver locks and gilded edges</medium>\n"
    #     xmlstring += "    <dimensions>" + "Approx. {{Size|mm|116|84}}" + "</dimensions>\n"
    #     xmlstring += "    <date>" + "18th century" + "</date>\n"
    #
    # elif picname_trunc == "160_achterplat":
    #     xmlstring += "    <description>Back of red velvet binding from 18th century with silver locks and gilded edges. Inside is the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]</description>\n"
    #     xmlstring += "    <URLtothemediafile>"+images_base_url+str(picname)+"</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Back of red velvet binding from 18th century with silver locks  and gilded edges</GWToolsettitle>\n"
    #     xmlstring += "    <title>"+ base_title + " - Back of red velvet binding from 18th century with silver locks and gilded edges</title>\n"
    #     xmlstring += "    <medium>Red velvet binding with silver locks and gilded edges</medium>\n"
    #     xmlstring += "    <dimensions>" + "Approx. {{Size|mm|116|84}}" + "</dimensions>\n"
    #     xmlstring += "    <date>" + "18th century" + "</date>\n"
    #
    # elif picname_trunc == "003_fl001v-001r": # Calendar - month of January
    #     xmlstring += "    <description>Folio 001r from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]. Calendar of the diocese of Utrecht, month of January, first half</description>\n"
    #     xmlstring += "    <URLtothemediafile>"+images_base_url+str(picname)+"</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Folio 001r - Calendar of the diocese of Utrecht, month of January, first half</GWToolsettitle>\n"
    #     xmlstring += "    <title>"+ base_title + " - Folio 001r - Calendar of the diocese of Utrecht, month of January, first half</title>\n"
    #     xmlstring += "    <artist>"+ str(artist) + "</artist>\n"
    #     xmlstring += "    <notes>"+str(notes)+"</notes>\n"
    #     xmlstring += "    <dimensions>" + dimensions_calendar + "</dimensions>\n"
    #     xmlstring += "    <medium>"+ str(medium) +"</medium>\n"
    #     xmlstring += "    <date>" + str(date) + "</date>\n"
    #     xmlstring += "    <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n"
    #
    # elif picname_trunc in calendar_dic.keys():  # fol. 1r-12v: kalender - Jan t/m Dec
    #     xmlstring += "<description>Lefthand side folio "+folio_left+" and righthand side folio "+folio_right +" from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]] - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</description>\n"
    #     xmlstring += "<URLtothemediafile>" + images_base_url + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "<GWToolsettitle>" + base_titleGWT + " - folios " + folio_left + " (left) and " + folio_right + " (right) - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</GWToolsettitle>\n"
    #     xmlstring += "<title>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right) - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</title>\n"
    #     xmlstring += "    <artist>"+ str(artist) + "</artist>\n"
    #     xmlstring += "    <notes>"+str(notes)+"</notes>\n"
    #     xmlstring += "    <dimensions>" + dimensions_calendar + "</dimensions>\n"
    #     xmlstring += "    <medium>"+ str(medium) +"</medium>\n"
    #     xmlstring += "    <date>" + str(date) + "</date>\n"
    #     xmlstring += "    <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n"
    #
    # elif picname_trunc == "158_155v-ep001r":
    #     xmlstring += "    <description>Folio 155v from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]</description>\n"
    #     xmlstring += "    <URLtothemediafile>"+images_base_url+str(picname)+"</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Folio 155v</GWToolsettitle>\n"
    #     xmlstring += "    <title>"+ base_title + " - Folio 155v</title>\n"
    #     xmlstring += "    <artist>"+ str(artist) + "</artist>\n"
    #     xmlstring += "    <notes>"+str(notes)+"</notes>\n"
    #     xmlstring += "    <dimensions>" + dimensions + "</dimensions>\n"
    #     xmlstring += "    <medium>"+ str(medium) +"</medium>\n"
    #     xmlstring += "    <date>" + str(date) + "</date>\n"
    #     xmlstring += "    <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n"




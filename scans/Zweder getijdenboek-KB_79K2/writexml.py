
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
        IconClassText = IconClassData["txt"]["en"].capitalize()
        IconClassKeywords = IconClassData["kw"]["en"]
    return [IconClassText, IconClassKeywords]

def hasIlluminations(folio):
#In : folio (string)
#Returns: Boolan True is folio has illuminations, otherwise False

    hasIllums = False
    jsonfile = "KB79K2_illum.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)

    for i in range(len(data["records"]["record"])):
        if data["records"]["record"][i]["folio"] == folio:
            hasIllums = True
    data_file.close()
    return hasIllums

def findIlluminations(folio):
#In : folio (string)
#Returns: illumString: string with info about illuminations on this particular folio
    illumString = ""
    jsonfile = "KB79K2_illum.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["records"]["record"])):
        if data["records"]["record"][i]["folio"] == folio:
            print("-----------------"+str(folio)+"-------------------------")
            illumType = finditem(data["records"]["record"][i], "type")
            illumDesc = finditem(data["records"]["record"][i], "description")
            illumIconclassCode = finditem(data["records"]["record"][i], "iconClass")
            if isinstance(illumType, list):  # more than 1 illumination on a folio, see for instance 080r, 083r
                for j in range(len(illumType)):
                    illumString += "*The " + illumType[j] + " shows " + illumDesc[j]+ "\n"
            else:  # 1 illumination on a folio
                illumString += "*The " + illumType + " shows " + illumDesc + "\n"
            if illumIconclassCode != None:
                if isinstance(illumIconclassCode, list): # more than 1 iconclass code for this illum
                    for k in illumIconclassCode:
                        illumString += "*"+str(resolveIconClass(k)[0]) +  " ([http://iconclass.org/rkd/"+str(k) + " " + str(k) + "])\n"
                else:
                    illumString += "*"+str(resolveIconClass(illumIconclassCode)[0]) +  " ([http://iconclass.org/rkd/"+illumIconclassCode + " " + illumIconclassCode + "])\n"
            print(illumString)
    data_file.close()
    return illumString

#config paths/ urls
current_dir = os.path.dirname(os.path.realpath(__file__))
imagedir_hires= current_dir + "\\images\\bladerboek\\"
images_base_url_hires="https://www.kb.nl/kbhtml/zweder/"

homepageNL = "https://www.kb.nl/themas/middeleeuwen/zweder-getijdenboek"
homepageEN = "https://www.kb.nl/en/themes/middle-ages/book-of-hours-by-the-master-of-zweder-van-culemborg"
sourcetemplate = "{{Koninklijke Bibliotheek}}"

calendar_dic={
              '004_001v-002r':'January (2nd half) and March (February missing)',
              '005_002v-003r':'March and April',
              '006_003v-004r':'April and May',
              '007_004v-005r':'May and June',
              '008_005v-006r':'June and July',
              '009_006v-007r':'July and August',
              '010_007v-008r':'Augustus and September',
              '011_008v-009r':'September and October',
              '012_009v-010r':'October and November',
              '013_010v-011r':'November and December',
              '014_011v-012r':'December(2nd half)'
}
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
ppn = "311780776"
institution = "Koninklijke Bibliotheek"
medium = "Manuscript with illuminations on parchment"
dimensions = "Folio size: {{Size|mm|116|84}} - Block size: {{Size|mm|68|43}} with 1 column and 13 lines"
dimensions_calendar = "Folio size: {{Size|mm|116|84}} - Block size: {{Size|mm|68|43}} with 1 column and 16 lines"
permission = "{{PD-art|PD-old-70-1923}}"
wikidata = "Q1516034"
browse_entry = "https://galerij.kb.nl/kb.html#/nl/zweder/page/0/zoom/2/lat/-41.90227704096369/lng/-10.546875"
source =  sourcetemplate
base_titleGWT = "Book of hours by the Master of Zweder van Culemborg - KB 79 K 2"
base_title    = "Book of hours by the Master of Zweder van Culemborg - KB 79 K 2"
date = "Circa 1430-1435"
placeofcreation = "Utrecht, Northern Netherlands"
language = "Dutch"
script = "Littera textualis"
notes= "Text in "+str(language)+ ", script: " + str(script)
nfolios = "155"
artist = "Illuminator(s): [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]] (ca. 1415-1440) {{Creator:Master of Zweder van Culemborg‎}}"
otherversions = "[http://opc4.kb.nl/PPN?PPN=216444977 Facsimile KB 79 K 2 1999]"
objecthistory = "Mabel Ward Savage (1884-1956). Probably owned by [[w:en:A._S._W._Rosenbach|A.S.W. Rosenbach]] in the early 1920s. Private collection in the United States. Presented in 1998 by [[w:en:Paul_Fentener_van_Vlissingen|P. Fentener van Vlissingen]] on the occasion of the 200th anniversary of the KB as a 99-year loan"
illuminations = "27 full-page miniatures (possibly 15 missing); 16 historiated initials; decorated initials with border decoration; penwork initials"

XMLoutputfile = open("zwedergetijdenboek.xml", "w", encoding="UTF-8")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"


for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname = infile.replace(imagedir_hires, "") #"004_001v-002r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"004_001v-002r"
    # split in 3 parts: 010 + 002v + 003r - where applicable formatwise
    if picname_trunc != "001_voorplat" and picname_trunc != "160_achterplat":
        imagenumber = picname_trunc.split("_")[0] #010
        folio_left = picname_trunc.split("_")[1].split("-")[0]  # 002v
        folio_right = picname_trunc.split("-")[1] #003r
        print(imagenumber + " -- " + folio_left + " -- " + str(folio_right))
    else:
        imagenumber = picname_trunc.split("_")[0] #160
        cover = picname_trunc.split("_")[1] #achterplat

    xmlstring += "<record>\n"
    xmlstring += "    <accessionnumber>*[" + browse_entry + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(picname_trunc)+"</folio>\n"
    #xmlstring += "    <author>"+ str(author) + "</author>\n"
    xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"
    xmlstring += "    <otherversions>"+ str(otherversions) +"</otherversions>\n"
    xmlstring += "    <objecthistory>"+ str(objecthistory)+"</objecthistory>\n"

    if picname_trunc == "001_voorplat":
        xmlstring += "    <description>Front of red velvet binding from 18th century with silver locks and gilded edges. Inside is the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]</description>\n"
        xmlstring += "    <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Front of red velvet binding from 18th century with silver locks  and gilded edges</GWToolsettitle>\n"
        xmlstring += "    <title>"+ base_title + " - Front of red velvet binding from 18th century with silver locks and gilded edges</title>\n"
        xmlstring += "    <medium>Red velvet binding with silver locks and gilded edges</medium>\n"
        xmlstring += "    <dimensions>" + "Approx. {{Size|mm|116|84}}" + "</dimensions>\n"
        xmlstring += "    <date>" + "18th century" + "</date>\n"

    elif picname_trunc == "160_achterplat":
        xmlstring += "    <description>Back of red velvet binding from 18th century with silver locks and gilded edges. Inside is the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]</description>\n"
        xmlstring += "    <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Back of red velvet binding from 18th century with silver locks  and gilded edges</GWToolsettitle>\n"
        xmlstring += "    <title>"+ base_title + " - Back of red velvet binding from 18th century with silver locks and gilded edges</title>\n"
        xmlstring += "    <medium>Red velvet binding with silver locks and gilded edges</medium>\n"
        xmlstring += "    <dimensions>" + "Approx. {{Size|mm|116|84}}" + "</dimensions>\n"
        xmlstring += "    <date>" + "18th century" + "</date>\n"

    elif picname_trunc == "003_fl001v-001r": # Calendar - month of January
        xmlstring += "    <description>Folio 001r from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]. Calendar of the diocese of Utrecht, month of January, first half</description>\n"
        xmlstring += "    <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Folio 001r - Calendar of the diocese of Utrecht, month of January, first half</GWToolsettitle>\n"
        xmlstring += "    <title>"+ base_title + " - Folio 001r - Calendar of the diocese of Utrecht, month of January, first half</title>\n"
        xmlstring += "    <artist>"+ str(artist) + "</artist>\n"
        xmlstring += "    <notes>"+str(notes)+"</notes>\n"
        xmlstring += "    <dimensions>" + dimensions_calendar + "</dimensions>\n"
        xmlstring += "    <medium>"+ str(medium) +"</medium>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n"

    elif picname_trunc in calendar_dic.keys():  # fol. 1r-12v: kalender - Jan t/m Dec
        xmlstring += "<description>Lefthand side folio "+folio_left+" and righthand side folio "+folio_right +" from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]] - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</description>\n"
        xmlstring += "<URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "<GWToolsettitle>" + base_titleGWT + " - folios " + folio_left + " (left) and " + folio_right + " (right) - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</GWToolsettitle>\n"
        xmlstring += "<title>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right) - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</title>\n"
        xmlstring += "    <artist>"+ str(artist) + "</artist>\n"
        xmlstring += "    <notes>"+str(notes)+"</notes>\n"
        xmlstring += "    <dimensions>" + dimensions_calendar + "</dimensions>\n"
        xmlstring += "    <medium>"+ str(medium) +"</medium>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n"

    elif picname_trunc == "158_155v-ep001r":
        xmlstring += "    <description>Folio 155v from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]</description>\n"
        xmlstring += "    <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Folio 155v</GWToolsettitle>\n"
        xmlstring += "    <title>"+ base_title + " - Folio 155v</title>\n"
        xmlstring += "    <artist>"+ str(artist) + "</artist>\n"
        xmlstring += "    <notes>"+str(notes)+"</notes>\n"
        xmlstring += "    <dimensions>" + dimensions + "</dimensions>\n"
        xmlstring += "    <medium>"+ str(medium) +"</medium>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n"

    else: #all the normal pages
        xmlstring += "    <artist>"+ str(artist) + "</artist>\n"
        xmlstring += "    <notes>"+str(notes)+"</notes>\n"
        xmlstring += "    <dimensions>" + dimensions + "</dimensions>\n"
        xmlstring += "    <medium>"+ str(medium) +"</medium>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n"
        xmlstring += "    <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "    <title>"+ base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
        xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"
        xmlstring += "    <description>Lefthand side folio "+folio_left+" and righthand side folio "+folio_right +" from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]\n"
        if hasIlluminations(folio_left):
            xmlstring += "=====Illuminations on the left folio "+ str(folio_left)+ "=====" + "\n"
            xmlstring += findIlluminations(folio_left) + "\n"
        if hasIlluminations(folio_right):
            xmlstring += "=====Illuminations on the right folio "+ str(folio_right)+ "=====" + "\n"
            xmlstring += findIlluminations(folio_right) + "\n"
        xmlstring += "</description>\n"

    xmlstring += "</record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()


# coding=utf-8
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
images_base_url_hires="https://www.kb.nl/kbhtml/trivulzio/"

homepageNL = "https://www.kb.nl/themas/middeleeuwen/trivulzio-getijdenboek"
homepageEN = "https://www.kb.nl/en/themes/middle-ages/trivulzio-book-of-hours-ca-1465"
browse_entry = "https://galerij.kb.nl/kb.html#/nl/trivulzio/page/0/zoom/2/lat/-46.67959446564018/lng/-65.21484375"
sourcetemplate = "{{Koninklijke Bibliotheek}}"
institution = "Koninklijke Bibliotheek"

calendar_dic={'005_fl003v-001r':'January','006_001v-002r':'February','007_002v-003r':'March','008_003v-004r':'April','009_004v-005r':'May','010_005v-006r':'June','011_006v-007r':'July','012_007v-008r':'August','013_008v-009r':'September','014_009v-010r':'October','015_010v-011r':'November','016_011v-012r':'December','017_012v-013r':'December (2nd half)'}

# {{Artwork}} template on Commons, as stated in GWToolset # https://commons.wikimedia.org/wiki/Template:Artwork
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


# Den Haag, Koninklijke Bibliotheek, SMC 1.
# Vlaanderen, ca. 1470.
# Perkament, 382 fol., ca. 130×90 mm, 1 kolom, 16 regels (kalender 18 regels).
#
#     fol. 1r-12v: kalender
#     fol. 13v-126v: Getijden van de zeven weekdagen, elk gevolgd door een mis
#     fol. 128r-138v: zestien gebeden tot heiligen
#     fol. 139v-155v: drie gebeden tot Maria (fol. 139v-144r: Stabat Mater; fol. 149r-153r: Obsecro te; fol. 153r-155v: O Intemerata)
#     fol. 157v-165v: vier passages uit de evangeliën (fol. 157v-159r: Johannes; fol. 159v-161r: Lucas; fol. 161v-163v: Mattheus; fol. 164v-165v: Marcus)
#     fol. 166v-247r: Mariagetijden
#     fol. 248v-270r: Zeven Boetpsalmen
#     fol. 271v-318v: Dodenvigilie (=dodenwake)

#---------------------------
#Generic stuff, for all images
ppn = "311783767"
permission = "{{PD-art|PD-old-70-1923}}"
source = "["+ browse_entry + " Browse this manuscript] on the website of the KB. Or read [" + homepageNL + " backgroud information in Dutch] and in ["+ homepageEN + " English]<br/>"+ sourcetemplate
date = "{{circa|1470}}"
placeofcreation = "[[:w:en:Flanders|Flanders]]"
wikidata = "Q15875651"
author = "Scribe: Nicolas Spierinc"
artist = "Illuminators: {{Creator:Lieven van Lathem}} {{Creator:Simon Marmion}} [[:w:nl:Weense_meester_van_Maria_van_Bourgondie|Weense Meester van Maria van Bourgondie]] (2nd half of 15th century)"
objecthistory =	"Donation to the [[:w:en:National_Library_of_the_Netherlands|national library of the Netherlands]] by an anonymous private person in 2001. The family of that person bought it at an auction. Before that it was owned by Luigi Alberico Trivulzio (1868-1938). He inherited it from his father Gian Giacomo Trivulzio (1839-1902)."
base_title = "[[:w:nl:Trivulzio-getijdenboek|Trivulzio Book of Hours]] - KW SMC 1"

XMLoutputfile = open("trivulzio.xml", "w")

xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname=infile.replace(imagedir_hires, "") #"004_001v-002r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"004_001v-002r"
# split in 3 parts: 010 + 002v + 003r - where applicable formatwise
    if picname_trunc != "001_voorplat" and picname_trunc != "328_achterplat": #only double folio openings
        imagenumber = picname_trunc.split("_")[0] #004
        folio_left = picname_trunc.split("_")[1].split("-")[0]  # 001v
        folio_right = picname_trunc.split("-")[1] #002r
        #print(imagenumber + " -- " + folio_left + " -- " + str(folio_right))
    else: #single openings
        imagenumber = picname_trunc.split("_")[0] #160
        cover = picname_trunc.split("_")[1] #achterplat

    xmlstring += "<record>\n"
    xmlstring += "<accessionnumber>Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN="+ ppn +"</accessionnumber>\n"
    xmlstring += "<Institution>" + institution + "</Institution>\n"
    xmlstring += "<permission>"+permission+"</permission>\n"
    xmlstring += "<source>"+source+"</source>\n"
    xmlstring += "<folio>"+str(picname_trunc)+"</folio>\n"
    xmlstring += "<wikidata>"+str(wikidata)+"</wikidata>\n"

    # creditline =	""
    # demo =		""
    # department =		""
    # description =		""
    # exhibitionhistory = ""
    # inscriptions =		""
    # otherfields =		""
    # placeofdiscovery =	""
    # references =		""
    # strict =	""
    # title =	""
    # wikidatacat =	""



#Exceptions for non-typical pages
    if picname_trunc == "001_voorplat":
        xmlstring += "<description>Front side of red morocco leather binding from the 18th century with gilt stamped</description>\n"
        xmlstring += "<URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "<GWToolsettitle>Trivulzio book of hours - KW SMC 1 - Front side of red morocco leather binding from the 18th century with gilt stamped</GWToolsettitle>\n"
        xmlstring += "<title>"+ base_title + " - Front side of red morocco leather binding from the 18th century with gilt stamped</title>\n"
        xmlstring += "<medium>Red morocco leather from the 18th century with gilt stamped</medium>\n"
        xmlstring += "<dimensions>Circa {{Size|mm|130|90}}</dimensions>\n"
        xmlstring += "<date>" + "The binding is from the 18th century" + "</date>\n"
        xmlstring += "<placeofcreation>" + "Not known" + "</placeofcreation>\n"

    elif picname_trunc == "328_achterplat":
        xmlstring += "<description>Back side of red morocco leather binding from the 18th century with gilt stamped</description>\n"
        xmlstring += "<URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "<GWToolsettitle>Trivulzio book of hours - KW SMC 1 - Back side of red morocco leather binding from the 18th century with gilt stamped</GWToolsettitle>\n"
        xmlstring += "<title>" + base_title + " - Back side of red morocco leather binding from the 18th century with gilt stamped</title>\n"
        xmlstring += "<medium>Red morocco leather from the 18th century with gilt stamped</medium>\n"
        xmlstring += "<dimensions>Circa {{Size|mm|130|90}}</dimensions>\n"
        xmlstring += "<date>" + "The binding is from the 18th century" + "</date>\n"
        xmlstring += "<placeofcreation>" + "Not known" + "</placeofcreation>\n"

    elif picname_trunc in calendar_dic.keys(): # fol. 1r-12v: kalender
        xmlstring += "<description>Calendar for the month of "+ calendar_dic[picname_trunc] +"</description>\n"
        xmlstring += "<URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "<GWToolsettitle>Trivulzio book of hours - KW SMC 1 - Calendar for the month of "+ calendar_dic[picname_trunc] +"</GWToolsettitle>\n"
        xmlstring += "<title>" + base_title + " - Calendar for the month of "+ calendar_dic[picname_trunc] +"</title>\n"
        xmlstring += "<medium>Manuscript with illuminations on parchment, littera cursiva (lettre bourguignonne)</medium>\n"
        xmlstring += "<dimensions>Circa {{Size|mm|130|90}}, 1 column, 18 lines</dimensions>\n"
        xmlstring += "<objecthistory>" + str(objecthistory) + "</objecthistory>\n"
        xmlstring += "<author>" + str(author) + "</author>\n"
        xmlstring += "<artist>" + str(artist) + "</artist>\n"
        xmlstring += "<date>" + str(date) + "</date>\n"
        xmlstring += "<placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"

    else: # all the normal folia
        xmlstring += "<description>Lefthand side folio " + folio_left + "; righthand side folio " + folio_right + " from the Trivulzio book of hours - KB SMC 1</description>\n"
        xmlstring += "<URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "<GWToolsettitle>Trivulzio book of hours - KW SMC 1 - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"
        xmlstring += "<title>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
        xmlstring += "<medium>Manuscript with illuminations on parchment, littera cursiva (lettre bourguignonne)</medium>\n"
        xmlstring += "<dimensions>Circa {{Size|mm|130|90}}, 1 column, 16 lines</dimensions>\n"
        xmlstring += "<author>" + str(author) + "</author>\n"
        xmlstring += "<artist>" + str(artist) + "</artist>\n"
        xmlstring += "<date>" + str(date) + "</date>\n"
        xmlstring += "<placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
        if picname_trunc == "323_318v-319r":
            xmlstring += "<notes>Text at the bottom: 'eies an v(ost)re bo(n)ne grase / lamilleure de vos hu(m)ble cousin' (from the 15th century)</notes>\n"
        xmlstring += "<objecthistory>" + str(objecthistory) + "</objecthistory>\n"

    xmlstring += "</record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()

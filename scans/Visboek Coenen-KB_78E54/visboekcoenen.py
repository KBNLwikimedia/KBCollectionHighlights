
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
images_base_url_hires="https://www.kb.nl/kbhtml/visboek/"

homepageNL = "https://www.kb.nl/themas/middeleeuwen/visboek-van-adriaen-coenen"
homepageEN = "https://www.kb.nl/en/themes/middle-ages/adriaen-coenens-visboek"

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
ppn = "310842611"
institution = "Koninklijke Bibliotheek"
medium = "Manuscript with colored drawing(s) on paper"
#dimensions = "External size: {{Size|mm|hh|bb}}"
permission = "{{PD-art|PD-old-70-1923}}"
placeofcreation = "[[w:en:Scheveningen|Scheveningen]], [[w:en:The_Hague|The Hague]], [[w:en:Netherlands|The Netherlands]]"
wikidata = "Q2528115"

author = "{{Creator:Adriaen_Coenen}}"
artist = "{{Creator:Adriaen_Coenen}}"
base_titleGWT = "Adriaen Coenen's Visboeck - KB 78 E 54"
base_title    = "Adriaen Coenen's Visboeck - KB 78 E 54"
browse_entry = "https://galerij.kb.nl/kb.html#/nl/visboek/page/5/zoom/3/lat/-55.12864906848878/lng/52.55859375"
source =  "{{Koninklijke Bibliotheek}}"
notes= "Text in Dutch"
nfolios = "412"
date = "1577-1579"

XMLoutputfile = open("visboekcoenen.xml", "w", encoding="UTF-8")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"


for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname = infile.replace(imagedir_hires, "") #"004_001v-002r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"004_001v-002r"
    # split in 3 parts: 010 + 002v + 003r - where applicable formatwise
    if picname_trunc != "001_voorplat" and picname_trunc != "429_achterplat":
        imagenumber = picname_trunc.split("_")[0] #010
        folio_left = picname_trunc.split("_")[1].split("-")[0]  # 002v
        folio_right = picname_trunc.split("-")[1] #003r
        print(imagenumber + " -- " + folio_left + " -- " + str(folio_right))
    else:
        imagenumber = picname_trunc.split("_")[0] #160
        cover = picname_trunc.split("_")[1] #achterplat

    xmlstring += "<record>\n"
    xmlstring += "    <accessionnumber>*[" + browse_entry + " View the Visboeck] on the website of the KB" + "\n*" + "[" + homepageNL + " Backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the Visboeck in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(picname_trunc)+"</folio>\n"
    xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"

    if picname_trunc == "001_voorplat":
        xmlstring += "    <description>Front of modern leather binding from circa 2000. Inside is the [[w:nl:Visboeck|Visboeck]] by [[w:nl:Adriaen_Coenen|Adriaen Coenen]]</description>\n"
        xmlstring += "    <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Front of modern leather binding from 2004</GWToolsettitle>\n"
        xmlstring += "    <title>"+ base_title + " - Front of modern leather binding from 2004</title>\n"
        xmlstring += "    <medium>Modern leather binding</medium>\n"
        xmlstring += "    <date>" + "2004" + "</date>\n"

    elif picname_trunc == "429_achterplat":
        xmlstring += "    <description>Back of modern leather binding from circa 2000. Inside is the [[w:nl:Visboeck|Visboeck]] by [[w:nl:Adriaen_Coenen|Adriaen Coenen]]</description>\n"
        xmlstring += "    <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Back of modern leather binding from 2004</GWToolsettitle>\n"
        xmlstring += "    <title>"+ base_title + " - Back of modern leather binding from 2004</title>\n"
        xmlstring += "    <medium>Modern leather binding</medium>\n"
        xmlstring += "    <date>" + "2004" + "</date>\n"

    elif picname_trunc == "006_schutblad-001r":
        xmlstring += "    <description>Folio 001r from the [[:w:nl:Visboeck|Visboeck]] by [[:w:nl:Adriaen Coenen|Adriaen Coenen]]</description>\n"
        xmlstring += "    <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ base_titleGWT + " - Folio 001r</GWToolsettitle>\n"
        xmlstring += "    <title>"+ base_title + " - Folio 001r</title>\n"
        xmlstring += "    <artist>" + str(artist) + "</artist>\n"
        xmlstring += "    <author>" + str(author) + "</author>\n"
        xmlstring += "    <notes>" + str(notes) + "</notes>\n"
        xmlstring += "    <medium>" + str(medium) + "</medium>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"


    elif picname_trunc == "424_413-schutblad":
        xmlstring += "    <description>Folio 413 from the [[:w:nl:Visboeck|Visboeck]] by [[:w:nl:Adriaen Coenen|Adriaen Coenen]]</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>" + base_titleGWT + " - Folio 413</GWToolsettitle>\n"
        xmlstring += "    <title>" + base_title + " - Folio 413</title>\n"
        xmlstring += "    <artist>" + str(artist) + "</artist>\n"
        xmlstring += "    <author>" + str(author) + "</author>\n"
        xmlstring += "    <notes>" + str(notes) + "</notes>\n"
        xmlstring += "    <medium>" + str(medium) + "</medium>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"

    else:  # all the normal pages
        xmlstring += "    <description>Lefthand side folio "+folio_left+" and righthand side folio "+folio_right +" from the [[:w:nl:Visboeck|Visboeck]] by [[:w:nl:Adriaen Coenen|Adriaen Coenen]]</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>" + base_titleGWT + " - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"
        xmlstring += "    <title>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
        xmlstring += "    <artist>" + str(artist) + "</artist>\n"
        xmlstring += "    <author>" + str(author) + "</author>\n"
        xmlstring += "    <notes>" + str(notes) + "</notes>\n"
        xmlstring += "    <medium>" + str(medium) + "</medium>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
    xmlstring += "</record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()


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

imagedir_lowres= current_dir + "\\lowres\\"
images_base_url_lowres="https://www.kb.nl/bladerboek/wapenboek/browse/images/large/"

imagedir_hires= current_dir + "\\hires\\"
images_base_url_hires="https://www.kb.nl/kbhtml/wapenboek/"

transcription_base_url = "http://localhost:8080/page_" #Mongoose webservertje op C:\temp\webserver aanzetten - in de subfolder ""browse" staan de trancriptie-bestanden (de htmls)

homepage = "https://www.kb.nl/themas/middeleeuwen/wapenboek-beyeren-1405"
sourcetemplate = "{{Koninklijke Bibliotheek}}"
provider = "Koninklijke Bibliotheek"


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
accessionnumber = "327494182"
institution = provider
medium = "Illustrations (coat of arms) on parchment and paper"
dimensions = "{{Size|mm|230|155}}"
permission = "{{PD-art|PD-old-70-1923}}"
source = "Browse this manuscript on the website of the KB: " + homepage + " (also includes backgroud information in Dutch)<br/>"+ sourcetemplate
date = "Between 1402 and 1405"
artist = "Binder: [[:w:en:Lodewijk_Elzevir|Lodewijk Elzevier I]] (ca. 1547-1617)"
author = "Author and scribe: [[:w:nl:Claes_Heynensoon|Claes Heynensoon]] / heraut Beyeren voorheen Gelre (ca. 1345-1414) {{Creator:Claes Heynenzoon}}"
title = "[[:w:nl:Wapenboek_Beyeren|Wapenboek Beyeren]] (armorial)  - KB79K21"
placeofcreation = "Holland"
wikidata = "Q3372028"


# creditline =	""
# demo =		""
# department =		""
# description =		""
# exhibitionhistory =	""
# inscriptions =		""
# objecthistory =	""
# objecttype =		""
# otherfields =		""
# otherversions =		""
# placeofdiscovery =		""
# references =		""
# strict =		""

#f = open('transcriptions.txt','w')
XMLoutputfile = open("wapenboekbeyeren.xml", "w")

XMLoutputfile.write("<?xml version='1.0' encoding='UTF-8'?>\n")
XMLoutputfile.write("<records>\n")

for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname=infile.replace(imagedir_hires, "") #"010_002v-003r.jpg"

    picname_trunc=picname.replace(".jpg", "") #"010_002v-003r."
# split in 3 parts: 010 + 002v + 003r - where applicable formatwise
    if picname_trunc != "001_voorplat" and picname_trunc != "078_achterplat":
        imagenumber = picname_trunc.split("_")[0] #010
        folio_left = picname_trunc.split("_")[1].split("-")[0]  # 002v
        folio_right = picname_trunc.split("-")[1] #003r
        print(imagenumber + " -- " + folio_left + " -- " + str(folio_right))
    else:
        imagenumber = picname_trunc.split("_")[0] #078
        cover = picname_trunc.split("_")[1] #achterplat

    XMLoutputfile.write("   <record>\n")
    XMLoutputfile.write("       <accessionnumber>Description of the entire Beyeren armorial in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN="+ accessionnumber +"</accessionnumber>\n")
    XMLoutputfile.write("       <dimensions>" + dimensions + "</dimensions>\n")
    XMLoutputfile.write("       <Institution>" + institution + "</Institution>\n")
    XMLoutputfile.write("       <permission>"+permission+"</permission>\n")
    XMLoutputfile.write("       <source>"+source+"</source>\n")
    XMLoutputfile.write("       <folio>"+str(picname_trunc)+"</folio>\n")
    XMLoutputfile.write("       <author>"+ str(author) + "</author>\n")
    XMLoutputfile.write("       <artist>"+ str(artist) + "</artist>\n")
    XMLoutputfile.write("       <date>" + str(date) + "</date>\n")
    XMLoutputfile.write("       <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n")
    XMLoutputfile.write("       <wikidata>"+str(wikidata)+"</wikidata>\n")

#Exceptions for non-typical pages
    if picname_trunc == "001_voorplat":
        XMLoutputfile.write("       <description>Brown leather binding by [[:w:en:Lodewijk_Elzevir|Lodewijk Elzevier I]] (ca. 1547-1617) from 1581 with gilded impression and text *WAPEN**BOECK / *CORNELIS*VAN*AECKEN*</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>Wapenboek Beyeren (armorial) - KB79K21 - Brown leather binding by Lodewijk Elzevier from 1581 with gilded impression and text *WAPEN**BOECK / *CORNELIS*VAN*AECKEN*</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>"+ title + " - Brown leather binding by [[:w:en:Lodewijk_Elzevir|Lodewijk Elzevier I]] (ca. 1547-1617) from 1581 with gilded impression and text *WAPEN**BOECK / *CORNELIS*VAN*AECKEN*</title>\n")
        XMLoutputfile.write("       <medium>Brown leather binding with gilded impression and text</medium>\n")

    elif picname_trunc == "078_achterplat":
        XMLoutputfile.write("       <description>Brown leather binding by [[:w:en:Lodewijk_Elzevir|Lodewijk Elzevier I]] (ca. 1547-1617) from 1581 with gilded impression and text *ANNO* / *1581*</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>Wapenboek Beyeren (armorial) - KB79K21 - Brown leather binding by Lodewijk Elzevier from 1581 with gilded impression and text *ANNO* / *1581*</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>"+ title + " - Brown leather binding by [[:w:en:Lodewijk_Elzevir|Lodewijk Elzevier I]] (ca. 1547-1617) from 1581 with gilded impression and text *ANNO* / *1581*</title>\n")
        XMLoutputfile.write("       <medium>Brown leather binding with gilded impression and text</medium>\n")

    elif picname_trunc == "002_schutblad-voorfl001r":
        XMLoutputfile.write("       <description>Cover sheet with on the left hand side an [[:w:en:Bookplate|ex-libris]] with a coat of arms and motto 'PERSEVERANDO', below that the name '[[:w:nl:Coenen_(geslacht)|Coenen]]'</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>Wapenboek Beyeren (armorial) - KB79K21 - Cover sheet with on the left hand side an ex-libris with a coat of arms and motto 'PERSEVERANDO', below that the name 'Coenen'</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>"+ title + " - Cover sheet with on the left hand side an [[:w:en:Bookplate|ex-libris]] with a coat of arms and motto 'PERSEVERANDO', below that the name '[[:w:nl:Coenen_(geslacht)|Coenen]]'</title>\n")
        XMLoutputfile.write("       <medium>Illustrations (coat of arms) on parchment and paper</medium>\n")

    elif picname_trunc == "070_062v-063r":
        XMLoutputfile.write("       <description>Folio 062v (left) from the Beyeren armorial / Wapenboek Beyeren. Here it is stated that the book was completed on 23 June 1405; it is written: ''Explicit iste liber per manus beyeren quondam gelre armorum regis de ruris [anno domini milesimo quadringentesimo quinto in profesto sancti Johannis baptiste]''. Translation in Dutch: ''Hier eindigt dit boek van de hand van Beyeren, voorheen Gelre, wapenkoning van de Ruwieren, in het jaar des Heren duizend vierhonderd vijf op de dag voor die van de heilige Johannes de Doper''.</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>Wapenboek Beyeren (armorial) - KB79K21 - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>"+ title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n")
        XMLoutputfile.write("       <medium>Illustrations (coat of arms) on parchment and paper</medium>\n")

    else:
        XMLoutputfile.write("       <description>Lefthand side folio "+folio_left+"; righthand side folio "+folio_right +" from the Beyeren armorial / [[:w:nl:Wapenboek_Beyeren|Wapenboek Beyeren]]</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>Wapenboek Beyeren (armorial) - KB79K21 - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>"+ title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n")
        XMLoutputfile.write("       <medium>"+ medium +"</medium>\n")

    if picname_trunc != "001_voorplat" and picname_trunc != "078_achterplat":
        #scrape inscription transcription from KB-site
    #lefthand pages
        left_transcription_url= transcription_base_url+folio_left+".html"
        #print(left_transcription_url)
        left_page = requests.get(left_transcription_url)
        left_tree = html.fromstring(left_page.text)
        left_transcriptionlist = left_tree.xpath('//div[@class="line"]//text()')
        left_transcription = []
        for a in left_transcriptionlist:
            if a != "\r\n":
                left_transcription.append(a)
        #print(str(left_transcription))
        XMLoutputfile.write("       <inscriptions>")
        if left_transcription:
            XMLoutputfile.write("Inscriptions on the left folio, from top left to right bottom:\n")
            XMLoutputfile.write("           {{plainlist|")
            for left_line in left_transcription:
                XMLoutputfile.write("*"+left_line+"\n")
            XMLoutputfile.write("}}\n")
    # right hand pages
        right_transcription_url= transcription_base_url+folio_right+".html"
        #print(right_transcription_url)
        right_page = requests.get(right_transcription_url)
        right_tree = html.fromstring(right_page.text)
        right_transcriptionlist = right_tree.xpath('//div[@class="line"]//text()')
        right_transcription = []
        for b in right_transcriptionlist:
            if b != "\r\n":
                right_transcription.append(b)
        if right_transcription:
            XMLoutputfile.write("Inscriptions on the right folio, from top left to right bottom:\n")
            XMLoutputfile.write("           {{plainlist|")
            for right_line in right_transcription:
                XMLoutputfile.write("*"+right_line+"\n")
            XMLoutputfile.write("}}")
        XMLoutputfile.write("</inscriptions>\n")

    XMLoutputfile.write("   </record>\n")
XMLoutputfile.write("</records>\n")

XMLoutputfile.close()

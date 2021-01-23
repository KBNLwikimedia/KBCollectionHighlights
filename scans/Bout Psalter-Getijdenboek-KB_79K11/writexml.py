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
images_base_url_hires="https://www.kb.nl/kbhtml/bout/"

homepageNL = "https://www.kb.nl/themas/middeleeuwen/bout-psalter-getijdenboek"
homepageEN = "https://www.kb.nl/en/themes/middle-ages/bout-psalter-hours"
browse_entry = "https://galerij.kb.nl/kb.html#/en/bout/page/16/zoom/3/lat/-70.17020068549206/lng/-118.30078125"
sourcetemplate = "{{Koninklijke Bibliotheek}}"
institution = "Koninklijke Bibliotheek"

calendar_dic_long ={'002_000v-001r':'Calendar for the month of January - Folio 1r',
              '003_001v-002r':'Calendar for the month of February - Folio 2r',
              '004_002v-003r':'Calendar for the month of March - Folio 3r',
              '005_003v-004r':'Calendar for the month of April - Folio 4r',
              '006_004v-005r':'Calendar for the month of May - Folio 5r',
              '007_005v-006r':'Calendar for the month of June - Folio 6r (Sinte aelbrecht confessoir = St. Albrecht, confessor, 25th June)',
              '008_006v-007r':'Calendar for the month of July - Folio 7r',
              '009_007v-008r':'Calendar for the month of August - Folio 8r (Sinte ieroen = St. Jerome, 17th August)',
              '010_008v-009r':'Calendar for the month of September - Folio 9r',
              '011_009v-010r':'Calendar for the month of October - Folio 10r (Sinte bave confessoir = St. Bavo, confessor, written in red on 1st October; Bavo is the patron of the main church in Haarlem',
              '012_010v-011r':'Calendar for the month of November - Folio 11r',
              '013_011v-012r':'Calendar for the month of December - Folio 12r',
              '014_012v-013r':'The right folio (13r) show a computational table for calculating the day of Easter. It begins with the year 1453 (CCCC ende liii). We can therefore assume that the manuscript was made in 1453',
              '015_015v-016r':'Computational tables for calculating the day of Easter (folios 15v and 16r)',
              }

calendar_dic_short ={'002_000v-001r':'Calendar for the month of January - Folio 1r',
              '003_001v-002r':'Calendar for the month of February - Folio 2r',
              '004_002v-003r':'Calendar for the month of March - Folio 3r',
              '005_003v-004r':'Calendar for the month of April - Folio 4r',
              '006_004v-005r':'Calendar for the month of May - Folio 5r',
              '007_005v-006r':'Calendar for the month of June - Folio 6r',
              '008_006v-007r':'Calendar for the month of July - Folio 7r',
              '009_007v-008r':'Calendar for the month of August - Folio 8r',
              '010_008v-009r':'Calendar for the month of September - Folio 9r',
              '011_009v-010r':'Calendar for the month of October - Folio 10r',
              '012_010v-011r':'Calendar for the month of November - Folio 11r',
              '013_011v-012r':'Calendar for the month of December - Folio 12r',
              '014_012v-013r':'Computational table for calculating the day of Easter (right folio 13r)',
              '015_015v-016r':'Computational tables for calculating the day of Easter (folios 15v and 16r)',
                     }


# {{Artwork}} template on Commons, as stated in GWToolset # https://commons.wikimedia.org/wiki/Template:Artwork
# accessionnumber =	"" (=ppn)
# artist =	"" (miniaturist)
# author =	"" (scribe)
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
#Generic stuff, for all images
ppn = "311783821"
permission = "{{PD-art|PD-old-70-1923}}"
source = "["+ browse_entry + " Browse this manuscript] on the website of the KB. Or read [" + homepageNL + " backgroud information in Dutch] and in ["+ homepageEN + " English]<br/>"+ sourcetemplate
date = "1453"
placeofcreation = "[https://www.kb.nl/en/themes/middle-ages/bout-psalter-hours/haarlem Haarlem], [https://www.kb.nl/en/themes/middle-ages/bout-psalter-hours/utrecht Utrecht]"
artist = "Illuminators: [[:w:nl:Meester_van_Gijsbrecht_van_Brederode|Masters of Gijsbrecht van Brederode]], Masters of the Haarlem Bible, [[:w:nl:Meester_van_Otto_van_Moerdrecht|Masters of Otto van Moerdrecht]] (circa 1420 - circa 1460), unknown Utrecht miniaturist"
size_folio= "{{Size|mm|158|116}}"
size_block= "{{Size|mm|101|64}}, 1 column, 24 lines"
medium = "Manuscript with illuminations on parchment, littera textualis"
base_title = "Bout Psalter-Hours - KB 79 K 11"
objecthistory =	"Acquired by the KB from the antiquarian bookshop of J&#xf6;rn G&#xfc;nther in Hamburg, Germany in 2007. For earlier provenance information see the [http://opc4.kb.nl/PPN?PPN="+ ppn + " KB catalogue]"
#Hex codes: http://www.codetable.net/unicodecharacters

XMLoutputfile = open("boutpsalter.xml", "w")

xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname=infile.replace(imagedir_hires, "") #"004_001v-002r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"004_001v-002r"
    # split in 3 parts: 010 + 002v + 003r
    imagenumber = picname_trunc.split("_")[0] #004
    folio_left = picname_trunc.split("_")[1].split("-")[0]  # 001v
    folio_right = picname_trunc.split("-")[1] #002r
    print(imagenumber + " -- " + folio_left + " -- " + str(folio_right))
    xmlstring += "<record>\n"
    xmlstring += "<accessionnumber>Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN="+ ppn +"</accessionnumber> (in Dutch)\n"
    xmlstring += "<Institution>" + institution + "</Institution>\n"
    xmlstring += "<permission>"+permission+"</permission>\n"
    xmlstring += "<source>"+source+"</source>\n"
    xmlstring += "<folio>"+str(picname_trunc)+"</folio>\n"
#   xmlstring += "<wikidata>"+str(wikidata)+"</wikidata>\n"

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
    if picname_trunc == "001_voorplat-achterplat":
        xmlstring += "<description>Front and back side of late 16th-century (1590-1600) brown leather binding with Caritas blocks and decorative rolls in gold</description>\n"
        xmlstring += "<URLtothemediafile>"+images_base_url_hires+str(picname)+"</URLtothemediafile>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - Front and back side of late 16th-century brown leather binding with Caritas blocks and decorative rolls in gold</GWToolsettitle>\n"
        xmlstring += "<title>"+ base_title + " - Front and back side of late 16th-century (1590-1600) brown leather binding with Caritas blocks and decorative rolls in gold</title>\n"
        xmlstring += "<medium>Brown leather binding with Caritas blocks and decorative rolls in gold</medium>\n"
        xmlstring += "<dimensions>Circa " + size_folio + " (per side)</dimensions>\n"
        xmlstring += "<date>" + "Late 16th century (1590-1600)" + "</date>\n"
        xmlstring += "<placeofcreation>" + "Not known" + "</placeofcreation>\n"

    elif picname_trunc in calendar_dic_long.keys(): # special sections of the book
        xmlstring += "<description>" + calendar_dic_long[picname_trunc] +"</description>\n"
        xmlstring += "<URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - "+ calendar_dic_short[picname_trunc] +"</GWToolsettitle>\n"
        xmlstring += "<title>" + base_title + " - "+ calendar_dic_short[picname_trunc] +"</title>\n"
        xmlstring += "<medium>" + str(medium) + "</medium>\n"
        xmlstring += "<dimensions>Folia: " + size_folio + "; Text block: " + size_block + "</dimensions>\n"
        xmlstring += "<objecthistory>" + str(objecthistory) + "</objecthistory>\n"
    #     xmlstring += "<author>" + str(author) + "</author>\n"
        xmlstring += "<artist>" + str(artist) + "</artist>\n"
        xmlstring += "<date>" + str(date) + "</date>\n"
        xmlstring += "<placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"

    elif picname_trunc == "016_016v-017r":
        xmlstring += "<description>The left folio (16v) shows a [[:w:en:Phlebotomy|phlebotomy]] table, where we learn that the constellation Gemini is responsible for shoulders, arms, and hands. Gemini must lie correctly in the sky before bloodletting is performed to cure these body parts. On the bottom right on folio 17r: the [https://www.kb.nl/en/themes/middle-ages/bout-psalter-hours/amsterdam coat of arms of the Bout family] (three arrows) which has been overpainted; see the front on folio 17v</description>\n"
        xmlstring += "<URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - Folio 016v - Phlebotomy table (left) and 017r (right) </GWToolsettitle>\n"
        xmlstring += "<title>" + base_title + " - [[:w:en:Phlebotomy|phlebotomy]] table (left) and coat of arms of the Bout family (three arrows, bottom right)</title>\n"
        xmlstring += "<medium>" + str(medium) + "</medium>\n"
        xmlstring += "<dimensions>Folia: " + size_folio + "; Text block: " + size_block + "</dimensions>\n"
        #     xmlstring += "<author>" + str(author) + "</author>\n"
        xmlstring += "<artist>" + str(artist) + "</artist>\n"
        xmlstring += "<date>" + str(date) + "</date>\n"
        xmlstring += "<placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
        xmlstring += "<objecthistory>" + str(objecthistory) + "</objecthistory>\n"

    else: # all the 'normal' folia
        xmlstring += "<description>Lefthand side folio " + folio_left + "; righthand side folio " + folio_right + " from the " + base_title +"</description>\n"
        xmlstring += "<URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "<GWToolsettitle>"+ base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"
        xmlstring += "<title>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
        xmlstring += "<medium>" + str(medium) + "</medium>\n"
        xmlstring += "<dimensions>Folia: " + size_folio + "; Text block: " + size_block + "</dimensions>\n"
    #     xmlstring += "<author>" + str(author) + "</author>\n"
        xmlstring += "<artist>" + str(artist) + "</artist>\n"
        xmlstring += "<date>" + str(date) + "</date>\n"
        xmlstring += "<placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
        xmlstring += "<objecthistory>" + str(objecthistory) + "</objecthistory>\n"
        if picname_trunc == "017_017v-018r":
            xmlstring += "<notes>Bottom left on folio 17v: the [https://www.kb.nl/en/themes/middle-ages/bout-psalter-hours/amsterdam coat of arms of the Bout family] (three arrows) has been overpainted; see the back on folio 17r</notes>\n"
    xmlstring += "</record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()

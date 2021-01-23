# coding=utf-8
import os, os.path, glob
import json
from pprint import pprint
from lxml import html
import requests

# {{Book}} template on Commons, as stated in GWToolset # https://commons.wikimedia.org/wiki/Template:Book ## DO NOT EDIT
# Author =
# Translator =
# Editor =
# Illustrator =
# Title =
# Subtitle =
# Series
# Volume =
# Edition =
# Publisher =
# Printer =
# Date =
# City =
# Language =
# Description =
# License =
# Image =
# Page =
# Pageoverview =
# Wikisource =
# Homecat =
# Other_versions =
# References = references =
# BNF =
# ISBN =
# LCCN =
# OCLC =
# Other_fields =
# Other_fields_1 =
# Other_fields_2 =
# Other_fields_3 =
# Accession number =
# Institution =
# Gallery =
# Department =
# Linkback =
# Wikidata =
# GWToolsettitle =	""
# URLtothemediafile =""

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
images_base_url_hires="https://www.kb.nl/kbhtml/liberpantegni/"

homepageNL = "https://www.kb.nl/themas/middeleeuwen/liber-pantegni"
homepageEN = "https://www.kb.nl/en/themes/medieval-manuscripts/liber-pantegni"
browse_entry = "https://galerij.kb.nl/kb.html#/en/liberpantegni/page/5/zoom/3/lat/75.6504309974655/lng/49.74609374999999"
base_title = "Liber pantegni - KB 73 J 6"

chapter_dic ={'Chapter I':'5/zoom/2/lat/30.90222470517144/lng/66.09375','Chapter II':'11/zoom/2/lat/39.50404070558415/lng/3.1640625','Chapter III':'17/zoom/2/lat/37.85750715625203/lng/64.6875','Chapter IV':'25/zoom/2/lat/34.74161249883172/lng/-53.4375','Chapter V':'30/zoom/2/lat/34.74161249883172/lng/-53.4375','Chapter VI':'41/zoom/2/lat/34.74161249883172/lng/-53.4375','Chapter VII':'48/zoom/2/lat/43.45291889355465/lng/81.5625','Chapter VIII':'57/zoom/2/lat/43.45291889355465/lng/81.5625','Chapter IX':'64/zoom/2/lat/43.45291889355465/lng/81.5625','Chapter X':'82/zoom/2/lat/43.45291889355465/lng/81.5625'}

chapteroverviewstring = ""
for chapter in chapter_dic:
    chapteroverviewstring += "[https://galerij.kb.nl/kb.html#/nl/liberpantegni/page/" + str(chapter_dic[chapter]) + " " + str(chapter) + "]"
    if chapter == "Chapter X": # if it's the last pagenumber, don't print the divider "--"
        chapteroverviewstring += ""
    else:
        chapteroverviewstring += " - "
#print(chapteroverviewstring)
pageoverview  = "*["+ str(browse_entry) + " Browse this manuscript] on the website of the KB.\n*Browse by chapter: " + str(chapteroverviewstring)

source = "{{Koninklijke Bibliotheek}}"
institution = "Koninklijke Bibliotheek"
ppn = "311778224"
permission = "{{PD-art|PD-old-70-1923}}"
wikidata ="Q748421"

date1= "Late 11th century"
date2= "12th/13th century"
date3 = "The binding is from the period 1750-1810"

placeofcreation = "[[:w:en:Monte Cassino|Monte Cassino]], Italy"
size_folio = "{{Size|mm|235|128}}"
size_block = "{{Size|mm|189|98}}"
block_layout = "2 columns, 62 lines, littera pregothica"

medium1 = "Manuscript on parchment"
medium2 = "Red velvet" # for front/back cover

language1 = "Latin, translated from Arabic"
language2 =  "Latin" # for 12/13th c. sections

author1 = "[[:w:en:Constantine_the_African|Constantine the African]] (ca. 1010-1098/9)"
author2 = "[[:w:en:Trota_of_Salerno|Trotula de Salerno]] (11th/12th century), [[:w:en:Gilbertus_Anglicus|Gilbertus Anglicus]] (ca. 1180-ca. 1250) and [[:w:es:Juan_Gil_de_Zamora|Johannes Egidius Zamorensis]] (ca. 1240-1320)" # for 12/13th c. sections

edition1 = "This manuscript is in large parts a translation from the Arabic of the ''[[:w:en:Kitab al-Malaki|Kitab al-Malaki]]'' (''Royal Book'') of [[:w:en:Ali ibn Abbas al-Magusi|Ali ibn al-Abbas al-Majusi]] (Ali Abbas, died ca. 994)"
edition2 = "In the 12th and 13th century various recepies and other medical texts were added to the front (folios Ir-IIv) and back (folios 87v-89r) of the manuscript. Among others, these additions were based on (or also used by) " + author2

description1 = "This is the earliest known copy (prior to 1086) of the [[:w:en:Liber_pantegni|Liber pantegni]], made at Monte Cassino under the supervision of [[:w:en:Constantine_the_African|Constantine the African]]"
description2 = "It is dedicated to [[:w:en:Abbot|Abbot]] [[:w:en:Desiderius,_Abbot_of_Monte_Cassino|Desiderius]] of [[:w:en:Monte Cassino|Monte Cassino]] (1027-1087), before he became [[:w:en:Pope_Victor_III|Pope Victor III]]"
description3 = "Folio 1r, middle of left column: ''Cum totius pater scientiae generalitas tres principales partes habeat [...]''"
description4 = "Folio 87v: ''Explicit prima pars pantegni scilicet theorica. Amen''"
description5 = "Read [" + homepageNL + " backgroud information in Dutch] and in ["+ homepageEN + " English]"


XMLoutputfile = open("liberpantegni.xml", "w")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname=infile.replace(imagedir_hires, "") #"010_002v-003r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"010_002v-003r"
    if  picname_trunc != "001_voorplat" and picname_trunc != "096_achterplat":
        #split in 3 parts: 010 + 002v + 003r
        imagenumber = picname_trunc.split("_")[0] #010
        folio_left = picname_trunc.split("_")[1].split("-")[0]  # 002v
        folio_right = picname_trunc.split("-")[1] #003r
        print(imagenumber + " -- " + folio_left + " -- " + str(folio_right))
    else: #voorplat en achterplat
        imagenumber = picname_trunc.split("_")[0] #001 of 096
        cover = picname_trunc.split("_")[1] #voorplat of achterplat
        print(imagenumber + " -- " + str(cover))

    xmlstring += "<record>\n"
# Generic stuff for all images
    xmlstring += "<accessionnumber>Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN="+ ppn +"</accessionnumber>\n"
    xmlstring += "<Institution>" + institution + "</Institution>\n"
    xmlstring += "<permission>"+permission+"</permission>\n"
    xmlstring += "<source>"+source+"</source>\n"
    xmlstring += "<folio>"+str(picname_trunc)+"</folio>\n"
    xmlstring += "<wikidata>"+str(wikidata)+"</wikidata>\n"
    xmlstring += "<pageoverview>" + str(pageoverview) + "</pageoverview>\n"
    xmlstring += "<URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"

#Exceptions for non-typical pages
    if picname_trunc == "001_voorplat": #front of binding
        xmlstring += "<title>Pantegni pars prima theorica (lib. I-X) - Front side of red velvet binding from 1750-1810</title>\n"
        xmlstring += "<author>Unknown</author>\n"
        xmlstring += "<date>" + str(date3) + "</date>\n"
        xmlstring += "<description>Front side of red velvet binding from the period 1750-1810 containing an 11th century copy of the [[:w:en:Liber_pantegni|Liber pantegni]]</description>\n"
        xmlstring += "<other_fields>{{Information field|name=Dimensions|value=Approx. " + str(size_folio) + "}}</other_fields>\n"
        xmlstring += "<other_fields_1>{{Information field|name=Medium|value=" + str(medium2) + "}}</other_fields_1>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - Front side of red velvet binding from 1750-1810</GWToolsettitle>\n"

    elif picname_trunc == "096_achterplat": #back of binding
        xmlstring += "<title>Pantegni pars prima theorica (lib. I-X) - Back side of red velvet binding from 1750-1810</title>\n"
        xmlstring += "<date>" + str(date3) + "</date>\n"
        xmlstring += "<author>Unknown</author>\n"
        xmlstring += "<description>Back side of red velvet binding from the period 1750-1810 containing an 11th century copy of the [[:w:en:Liber_pantegni|Liber pantegni]]</description>\n"
        xmlstring += "<other_fields>{{Information field|name=Dimensions|value=Approx. " + str(size_folio) + "}}</other_fields>\n"
        xmlstring += "<other_fields_1>{{Information field|name=Medium|value=" + str(medium2) + "}}</other_fields_1>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - Back side of red velvet binding from 1750-1810</GWToolsettitle>\n"

    elif picname_trunc == "002_schutblad-i": # cover sheet front
        xmlstring += "<title>Pantegni pars prima theorica (lib. I-X) - Front cover sheet</title>\n"
        xmlstring += "<date>" + str(date3) + "</date>\n"
        xmlstring += "<author>Unknown</author>\n"
        xmlstring += "<description>Front cover sheet of an 11th century copy of the [[:w:en:Liber_pantegni|Liber pantegni]]</description>\n"
        xmlstring += "<other_fields>{{Information field|name=Dimensions|value=Approx. " + str(size_folio) + "}}</other_fields>\n"
        xmlstring += "<other_fields_1>{{Information field|name=Medium|value=Parchment}}</other_fields_1>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - Front cover sheet</GWToolsettitle>\n"

    elif picname_trunc == "095_089v-090r": # cover sheet back
        xmlstring += "<title>Pantegni pars prima theorica (lib. I-X) - Back cover sheet</title>\n"
        xmlstring += "<date>" + str(date3) + "</date>\n"
        xmlstring += "<author>Unknown</author>\n"
        xmlstring += "<description>Back cover sheet of an 11th century copy of the [[:w:en:Liber_pantegni|Liber pantegni]]</description>\n"
        xmlstring += "<other_fields>{{Information field|name=Dimensions|value=Approx. " + str(size_folio) + "}}</other_fields>\n"
        xmlstring += "<other_fields_1>{{Information field|name=Medium|value=Parchment}}</other_fields_1>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - Back cover sheet</GWToolsettitle>\n"

    elif picname_trunc in ["003_ii-iii", "004_iv-v", "005_vi-vii"]: # 12/13th century part in front of the manuscript
        xmlstring += "<title>Pantegni pars prima theorica (lib. I-X) - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
        xmlstring += "<author>" + str(author2) + "</author>\n"
        xmlstring += "<date>" + str(date2) + "</date>\n"
        #xmlstring += "<placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
        xmlstring += "<other_fields>{{Information field|name=Dimensions|value=Folio: " + size_folio + "}}</other_fields>\n"
        xmlstring += "<other_fields_1>{{Information field|name=Medium|value=" + str(medium1) + "}}</other_fields_1>\n"
        xmlstring += "<description>*Lefthand side folio " + folio_left + "; righthand side folio " + folio_right + " from a copy of the [[:w:en:Liber_pantegni|Liber pantegni]]\n" + "*" + str(description1) + "\n*" + str(description2) + "\n*" + str(description5) + "</description>\n"
        xmlstring += "<edition>*" + str(edition1) + "\n*" + str(edition2) + "</edition>\n"
        xmlstring += "<language>" + str(language2) + "</language>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"

    elif picname_trunc == "006_viii-001r": # 12/13th century part in front of the manuscript
        xmlstring += "<title>Pantegni pars prima theorica (lib. I-X) - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
        xmlstring += "<author>" + str(author1) + "</author>\n"
        xmlstring += "<date>" + str(date1) + "</date>\n"
        xmlstring += "<placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
        xmlstring += "<other_fields>{{Information field|name=Dimensions|value=Folio: " + size_folio + "; Text block: " + size_block + ", " + block_layout + "}}</other_fields>\n"
        xmlstring += "<other_fields_1>{{Information field|name=Medium|value=" + str(medium1)+ "}}</other_fields_1>\n"
        xmlstring += "<description>*Lefthand side folio " + folio_left + "; righthand side folio " + folio_right + " from an 11th century copy of the [[:w:en:Liber_pantegni|Liber pantegni]]\n" + "*" + str(description1) + "\n*" + description2 + "\n*" + str(description3) + "\n*" + description5 + "</description>\n"
        xmlstring += "<edition>" + str(edition1) + "</edition>\n"
        xmlstring += "<language>" + str(language2) + "</language>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"

    elif picname_trunc in ["093_087v-088r", "094_088v-089r"]: # 12/13th century part in back of the manuscript
        xmlstring += "<title>Pantegni pars prima theorica (lib. I-X) - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
        xmlstring += "<author>" + str(author2) + "</author>\n"
        xmlstring += "<date>End of the 12th century</date>\n"
        #xmlstring += "<placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
        xmlstring += "<other_fields>{{Information field|name=Dimensions|value=Folio: " + size_folio + "}}</other_fields>\n"
        xmlstring += "<other_fields_1>{{Information field|name=Medium|value=" + str(medium1) + "}}</other_fields_1>\n"
        xmlstring += "<description>*Lefthand side folio " + folio_left + "; righthand side folio " + folio_right + " from a copy of the [[:w:en:Liber_pantegni|Liber pantegni]]\n*"+description1 + "\n*" + description2 + "\n*" + description4 + "\n*" + description5 + "</description>\n"
        xmlstring += "<edition>*" + str(edition1) + "\n*" + str(edition2) + "</edition>\n"
        xmlstring += "<language>" + str(language2) + "</language>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"

    else:  # all the 'normal' folia from the 11th c. part of the Liber
        xmlstring += "<title>Pantegni pars prima theorica (lib. I-X) - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
        xmlstring += "<date>" + str(date1) + "</date>\n"
        xmlstring += "<author>" + str(author1) + "</author>\n"
        xmlstring += "<placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
        xmlstring += "<language>" + str(language1) + "</language>\n"
        xmlstring += "<description>*Lefthand side folio " + folio_left + "; righthand side folio " + folio_right + " from an 11th century copy of the [[:w:en:Liber_pantegni|Liber pantegni]].\n*"+str(description1)+".\n*"+str(description2)+".\n*"+str(description5)+".</description>\n"
        xmlstring += "<other_fields>{{Information field|name=Dimensions|value=Folio: " + size_folio + "; Text block: " + size_block + ", " + block_layout + "}}</other_fields>\n"
        xmlstring += "<other_fields_1>{{Information field|name=Medium|value=" + str(medium1)+ "}}</other_fields_1>\n"
        xmlstring += "<edition>"+ str(edition1) + "</edition>\n"
        xmlstring += "<GWToolsettitle>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"

    xmlstring += "</record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()

#GENERIC fields
# License =
# Pageoverview =
# Source
# Accession number =
# Institution =
# Wikidata =

#Page specific fields
# Title =
# Author =
# GWToolsettitle =	""
# URLtothemediafile =""
# Date =
# City =
# Description =
# Other_fields = dimensions
# Other_fields_1 = medium
# Other_versions =
# Page = folio
# Translator = c de afrikaan
# Editor = de 3 andere schrijvers bij voor-deel en na-deel
# Language =
# Edition =


#Unused fields for this manuscript
# Volume =
# Illustrator =
# Subtitle =
# Series
# Publisher =
# Printer =
# Image =
# Wikisource =
# Homecat =
# References =
# BNF =
# ISBN =
# LCCN =
# OCLC =
# Other_fields_2 =
# Other_fields_3 =
# Gallery =
# Department =
# Linkback =
# Translator = c de afrikaan
# Editor = de 3 andere schrijvers bij voor-deel en na-deel
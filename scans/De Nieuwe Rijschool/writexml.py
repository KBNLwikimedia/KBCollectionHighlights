
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
imagedir= current_dir + "\\images\\"
images_base_url="https://www.kb.nl/kbhtml/rijschool/"


homepage = "https://www.kb.nl/themas/kinderboeken-en-strips/klassieke-kinderboeken/de-nieuwe-rijschool"
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
#DUMP uit KB-cat PPN = 305451642
#          Titel: De nieuwe rijschool : een beweegbaar prenteboek met rijmen /
#                 van A. van der Hoop Jr'szoon
#         Auteur: Adriaan van der Hoop Juniorszoon (1827-1863)
#           Jaar: [1856]
#       Uitgever: Schiedam : H.A.M. Roelants
#      Annotatie: Omslagtitel: De nieuwe rijschool : beweegbaar prentenboek
#                 Omslag vermeldt: Steendr. v. H.L. van Hoogstraten te Zwolle
#                 De keerzijde der afbeeldingen is niet bedrukt
#                 Vermelding op titelpagina: De kameel. De buffel. Het paard.
#                 De bok. De leeuw. De kat
#                 Boek met 6 in kleur gedrukte platen, waarvan onderdelen van
#                 de afbeelding door middel van strookjes kunnen worden
#                 verwisseld of bewogen. In 'Lust & Leering' (p. 397) wordt het
#                 boek genoemd als eerste beweegbare Nederlandse kinderboek
#         Omvang: [12] p., [6] bl. pl
#    Illustratie: gekl. lith
#        Formaat: 25x32 cm
#           ISBN:  (Geb.) : f 1,80
# Aanvraagnummer: KW 2281 A 136
#----------------------

accessionnumber = "305451642"
institution = provider
medium = "Paper and colored lithographs"
dimensions = "{{Size|cm|25|32}}"
permission = "{{PD-art|PD-old-70-1923}}"
source = sourcetemplate # +homepage
date = "1856"
artist = "Lithograph by [[:w:nl:Hendrik Scheeve|Hendrik Scheeve]] (1826-1870)"
author = "[[:w:nl:Adriaan_van_der_Hoop_jrsz.|Adriaan van der Hoop Juniorszoon]] (1827-1863)"
notes = "Publisher: H.A.M. Roelants, Schiedam"
title = "[[:w:nl:De nieuwe rijschool|De nieuwe rijschool : een beweegbaar prenteboek met rijmen]]"
placeofcreation = "[[:w:en:Netherlands|Netherlands]]"
otherversions =	"Facsimile edition from 2016: http://opc4.kb.nl/PPN?PPN=406858071"
#-wikidata = "Q3372028"
# inscriptions = "The inscriptions are explained (transcribed) in the orginal armorial, see [https://galerij.kb.nl/kb.html#/nl/wapenboek/ the digitised manuscript] on the website of the KB"

#f = open('transcriptions.txt','w')
XMLoutputfile = open("denieuwerijschool.xml", "w")

XMLoutputfile.write("<?xml version='1.0' encoding='UTF-8'?>\n")
XMLoutputfile.write("<records>\n")

for infile in glob.glob(os.path.join(imagedir, '*.jpg')):
    picname=infile.replace(imagedir, "") #"003_001v-002r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"003_001v-002r"
# split in 3 parts: 003 + 001v + 002r - where applicable formatwise
    if picname_trunc != "001_voorplat" and picname_trunc != "016_achterplat":
        imagenumber = picname_trunc.split("_")[0] #003
        folio_left = picname_trunc.split("_")[1].split("-")[0]  # 001v
        folio_right = picname_trunc.split("-")[1] #002r
        print(imagenumber + " -- " + folio_left + " -- " + str(folio_right))
    else: #voorplat en achterplat
        imagenumber = picname_trunc.split("_")[0] #001 of 016
        cover = picname_trunc.split("_")[1] #voorplat of achterplat

    XMLoutputfile.write("   <record>\n")
    XMLoutputfile.write("       <author>"+ str(author) + "</author>\n")
    XMLoutputfile.write("       <artist>"+ str(artist) + "</artist>\n")
    XMLoutputfile.write("       <notes>"+ notes + "</notes>\n")   #Publisher
    XMLoutputfile.write("       <accessionnumber>Description of this book in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN="+ accessionnumber +"</accessionnumber>\n")
    XMLoutputfile.write("       <dimensions>" + dimensions + "</dimensions>\n")
    XMLoutputfile.write("       <Institution>" + institution + "</Institution>\n")
    XMLoutputfile.write("       <permission>"+permission+"</permission>\n")
    # XMLoutputfile.write("       <page>"+str(picname_trunc)+"</page>\n")
    XMLoutputfile.write("       <homepage>See this book on the website of the KB: "+ str(homepage) + " (page in Dutch)</homepage>\n")
    XMLoutputfile.write("       <source>"+source+"</source>\n")
    XMLoutputfile.write("       <date>" + str(date) + "</date>\n")
    XMLoutputfile.write("       <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n")
    XMLoutputfile.write("       <medium>"+ medium +"</medium>\n")
    # XMLoutputfile.write("       <wikidata>"+str(wikidata)+"</wikidata>\n")
    XMLoutputfile.write("       <otherversions>"+ otherversions +"</otherversions>\n")


    if picname_trunc == "001_voorplat":
        XMLoutputfile.write("       <description>Front cover of ''De nieuwe rijschool'' (the new riding school) from " + date + "</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>Front cover of De nieuwe rijschool ("+date+") - KW 2281 A 136</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>Front cover of ''"+ title + "'' ("+date+")</title>\n")

    elif picname_trunc == "016_achterplat":
        XMLoutputfile.write("       <description>Back cover of ''De nieuwe rijschool'' (the new riding school) from "+date+"</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>Back cover of De nieuwe rijschool ("+date+") - KW 2281 A 136</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>Back cover of ''"+ title + "'' ("+date+")</title>\n")

    else:
        XMLoutputfile.write("       <description>Lefthand page "+folio_left+"; righthand page "+folio_right +" from De nieuwe rijschool' (the new riding school) from "+ date + "</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>De nieuwe rijschool - KW 2281 A 136 - pages " + folio_left + " and " + folio_right + "</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>Pages " + folio_left + " and " + folio_right + " from "+ title + "("+date+") </title>\n")

    XMLoutputfile.write("   </record>\n")
XMLoutputfile.write("</records>\n")

XMLoutputfile.close()

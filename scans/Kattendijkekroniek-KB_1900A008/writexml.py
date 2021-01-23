
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
images_base_url_hires="https://www.kb.nl/kbhtml/kattendijkekroniek/"

homepageNL = "https://www.kb.nl/themas/middeleeuwse-handschriften/kattendijkekroniek-ca-1491"
#homepageEN = "https://www.kb.nl/en/themes/middle-ages/beatrijs"

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
ppn = "40239772X"
signature = "KB KW 1900 A 008"
institution = "Koninklijke Bibliotheek"
medium = "Paper"
dimensions = "Folium size: {{Size|mm|200|140}} - Text block size: circa {{Size|mm|140|87}} with 1 column and 26 lines"
binding="Brown leather binding with blind embossing from ca. 1560-1580"
permission = "{{PD-art|PD-old-70-1923}}"
#wikidata = "Q1929931"
source =  "{{Koninklijke Bibliotheek}}"
date = "1491-1493"
placeofcreation = "[[:en:North Holland|North Holland]], [[:en:Haarlem|Haarlem]]?"
language = "Dutch"
script = "mainly [[:nl:Littera hybrida|littera hybrida]], on occasion [[:nl:Littera_textualis|littera textualis]]"
notes= "Text in "+str(language)+ ". Script is " + str(script)
nfolios = "viii + 561 + xii (1.122 pages)"

artist = "Unknown"
author = "Unknown"

title_short = "Kattendijkekroniek"
title = "Die historie of die cronicke van Hollant, van Zeelant ende van Vrieslant ende van den stichte van Uutrecht ende van veel landen die men hierna nomen sal"
title_GWT = "Kattendijkekroniek (ca. 1491)"

objecthistory ="The Kattendijkekroniek was possibly made for [[:en:Yolande van Lalaing|Yolande van Lalaing]] (1422-1497), wife of [[:en:Reinoud II van Brederode|Reinoud II van Brederode]] (1415-1473). Former owners include [[:nl:Pieter_Cornelisz._Bockenberg|Pieter Cornelisz. Bockenberg]] (1548-1617), Pieter Hanneman (1544-1593) and his son Jan Pietersz. Hanneman (ca. 1565-before 1607). In 1614 it was acquired by Johan [[:nl:Huyssen_van_Kattendijke|Huyssen van Kattendijke]] (1566-1634) and it remains in this family to this day. Hugo Huyssen van Kattendijke (1948-) gave it on permanent loan to the Koninklijke Bibliotheek in 2016."

#illuminations = "27 full-page miniatures (possibly 15 missing); 16 historiated initials; decorated initials with border decoration; penwork initials"

references = "For more elaborate background information and full-text transcriptions with annotations, see [http://resources.huygens.knaw.nl/retroboeken/kattendycke  Kroniek van Kattendijke tot 1490], published by Antheun Janse, with cooperation from Ingrid Biesheuvel, [[:en:Huygens Institute for the History of the Netherlands|Institute for the History of the Netherlands]] (ING), The Hague, 2005. This publication is in Dutch."

#de default browse entry, for pages not part of the sections below
browse_entry = "https://galerij.kb.nl/kb.html#/nl/kattendijke/page/9/zoom/3/lat/-58.859223547066584/lng/-44.6484375"

#===================================================================

XMLoutputfile = open("kattendijke.xml", "w")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname = infile.replace(imagedir_hires, "") #"002r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"002r"
    # split in 3 parts: 006 + 76e5 + fl002v
    #imagenumber = picname_trunc.split("_")[0] #006
    #folio_left = picname_trunc.split("_")[1]  # 76e5- we can further ignore this part, this is always the same
    #folio = picname_trunc.split("_")[2] #fl002v
    folio = picname_trunc  # 002r
    #print(imagenumber + " -- " + str(folio) + " -- " + str(hasIlluminations(folio)) + " -- " + str(findIlluminations(folio)))
    #print(imagenumber + " -- " + str(folio) + " -- " + str(hasIlluminations(folio)))# + " -- " + str(findIlluminations(folio)))
    print('"'+str(folio)+'",')# + " -- " + str(findIlluminations(folio)))

    xmlstring += "  <record>\n"
    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(picname_trunc)+"</folio>\n"
    xmlstring += "    <objecthistory>"+ str(objecthistory)+"</objecthistory>\n"
    xmlstring += "    <accessionnumber>*[" + browse_entry + " View this manuscript] on the website of the KB, including a full-text transcription of each page." + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch]" + "\n*" + "Description of the manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" +ppn + "</accessionnumber>\n"
    xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
    # xmlstring += "    <artist>" + "Lucie M. Gimbr&#xe8;re" + "</artist>\n"
    xmlstring += "    <references>" + str(references) + "</references>\n"
    #xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"
    #xmlstring += "    <otherversions>"+ str(otherversions) +"</otherversions>\n"

    if folio == "moderneband-voor":
        xmlstring += ""
        # xmlstring += "    <description>Front of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
        # xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        # xmlstring += "    <GWToolsettitle>"+ signature+ " - Front of brown leather binding from 1993. Inside is the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
        # xmlstring += "    <title>Front of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
        # xmlstring += "    <medium>Brown leather binding</medium>\n"
        # xmlstring += "    <date>" + "1993" + "</date>\n"
        # xmlstring += "    <artist>" + "Lucie M. Gimbr&#xe8;re" + "</artist>\n"
        # xmlstring += "    <placeofcreation>" + "[[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]" + "</placeofcreation>\n"
        # xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"

    else: #all the normal folio
        xmlstring += "    <description>Folium " + str(folio) + " from the " + str(title_GWT) + " from the collection of the [[:en:National Library of the Netherlands|National Library of the Netherlands]].</description>\n"
        xmlstring += "    <GWToolsettitle>" + str(title_GWT)+ " - " + signature + ", folium "+ str(folio) + "</GWToolsettitle>\n"
        xmlstring += "    <title>"+str(title_short)+ " - " + str(title) + " - " + signature + ", folium "+ str(folio)+"</title>\n"
        xmlstring += "    <medium>" + str(medium) + "</medium>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <notes>" + str(notes) + "</notes>\n"
        xmlstring += "    <dimensions>" + str(dimensions) + "</dimensions>\n"

    xmlstring += "  </record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()
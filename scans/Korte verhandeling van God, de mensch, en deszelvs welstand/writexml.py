
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
images_base_url_hires="https://www.kb.nl/kbhtml/spinoza/"

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
ppn = "310835097"
institution = "Koninklijke Bibliotheek"
medium = "Manuscript on paper"
dimensions = "Folium size: {{Size|mm|210|163}}"
permission = "{{PD-art|PD-old-70-1923}}"
#wikidata = "Q1929931"
source =  "{{Koninklijke Bibliotheek}}"
date = "Circa 1675-1700"
placeofcreation = "Netherlands"
#placeofcreation = "[[:en:Fecamp|Fecamp]]"
author ="{{Creator:Baruch Spinoza}}"
#Manuscript on paper with 433 folios, ca. 210x163 mm
language="'Dutch"

#language = "Dutch"
#script = "[[:nl:Littera textualis|Littera textualis]]"
#notes= "Script is " + str(script)
#nfolios = "80"

binding = "Contemporary half parchment binding from circa 1700"



#otherversions = ""

objecthistory = "This text is considered to be a precursor of Spinozas [[:en:Ethics_(Spinoza)|Ethics]]. This text in Dutch is a copy from a lost 17th century translation of the original Latin text. It contains titles and annotations written at a later date by [[:nl:Johannes Monnikhoff|Johannes Monnikhoff]] (1707-1787)"


#former_owners = "This manuscript was formerly owned by [[:en:Gérard de Dainville|Gérard de Dainville]] (-1378), Jeanne des Planches (a nun in the convent of Étrun in the diocese of Arras) and [[:fr:Georges-Joseph Gérard|Georges-Joseph Gérard]] (1767). Read the [https://www.kb.nl/en/themes/medieval-manuscripts/psalter-of-eleanor-of-aquitaine-ca-1185 whereabouts of the psalter]"

#illuminations = "27 full-page miniatures (possibly 15 missing); 16 historiated initials; decorated initials with border decoration; penwork initials"

base_title = "Korte verhandeling van God, de mensch, en deszelvs welstand - KB 75 G15"
base_title_GWT = "Korte verhandeling van God, de mensch, en deszelvs welstand - KB 75 G15"
browse_entry = "https://galerij.kb.nl/kb.html#/nl/spinoza/page/8/zoom/4/lat/-67.05030412177986/lng/-30.9814453125"
homepageNL = "https://www.kb.nl/themas/filosofiethemas/filosofie/benedictus-de-spinoza/spinoza-korte-verhandeling-van-god-de-mensch-en-deszelvs-welstand"



#===================================================================

XMLoutputfile = open("spinoza.xml", "w", encoding="UTF-8")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname=infile.replace(imagedir_hires, "") #"010_002v-003r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"010_002v-003r"
    # split in 3 parts: 010 + 002v + 003r
    imagenumber = picname_trunc.split("_")[0] #010
    folio_left = picname_trunc.split("_")[1].split("-")[0]  # 002v
    folio_right = picname_trunc.split("-")[1] #003r
    print(imagenumber + " -- " + folio_left + " -- " + str(folio_right))

    xmlstring += "  <record>\n"
    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(picname_trunc)+"</folio>\n"
    xmlstring += "    <medium>" + str(medium) + "</medium>\n"
    xmlstring += "    <dimensions>" + str(dimensions) + "</dimensions>\n"
    xmlstring += "    <accessionnumber>*[" + browse_entry + " View this manuscript] on the website of the KB" + "\n*" + "Read an [" + homepageNL + " introduction to the manuscript in Dutch]"+ "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn +"</accessionnumber>\n"
    xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname)+"</URLtothemediafile>\n"
    xmlstring += "    <date>" + str(date) + "</date>\n"
    xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
    xmlstring += "    <author>" + str(author) + "</author>\n"
    xmlstring += "    <description>[[:en:Baruch Spinoza|Benedictus de Spinoza]], Korte verhandeling van God, de mensch, en deszelvs welstand. Godgeleerde staatkundige verhandelinge. Nauwkeurige en nootsakelyke aenmerkingen tot beeter verstant van dit boek - Lefthand side folium " + folio_left + "; righthand side folium " + folio_right + ".</description>\n"
    xmlstring += "    <title>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
    xmlstring += "    <GWToolsettitle>"+ base_title_GWT + " - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"
    xmlstring += "    <objecthistory>"+ str(objecthistory)+"</objecthistory>\n"

    #xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"
    #xmlstring += "    <otherversions>"+ str(otherversions) +"</otherversions>\n"
    #xmlstring += "    <notes>"+ str(notes) +"</notes>\n"
    #xmlstring += "    <artist>" + str(artist) + "</artist>\n"
    #xmlstring += "    <language>" + str(language) + "</language>\n"

    xmlstring += "  </record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()



    # if folio == "moderneband-voor":
    #     xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    #     xmlstring += "    <description>Front of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
    #     xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ signature+ " - Front of brown leather binding from 1993. Inside is the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
    #     xmlstring += "    <title>Front of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
    #     xmlstring += "    <medium>Brown leather binding</medium>\n"
    #     xmlstring += "    <date>" + "1993" + "</date>\n"
    #     xmlstring += "    <artist>" + "Lucie M. Gimbr&#xe8;re" + "</artist>\n"
    #     xmlstring += "    <placeofcreation>" + "[[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]" + "</placeofcreation>\n"
    #     xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    # elif folio == "moderneband-achter":
    #     xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    #     xmlstring += "    <description>Back of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing " + title_overall + " - " + signature + "</description>\n"
    #     xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>" + signature + " - Back of brown leather binding from 1993. Inside is the manuscript containing " + title_overall_GWT + "</GWToolsettitle>\n"
    #     xmlstring += "    <title>Back of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing " + title_overall + " - " + signature + "</title>\n"
    #     xmlstring += "    <medium>Brown leather binding</medium>\n"
    #     xmlstring += "    <date>" + "1993" + "</date>\n"
    #     xmlstring += "    <artist>" + "Lucie M. Gimbr&#xe8;re" + "</artist>\n"
    #     xmlstring += "    <placeofcreation>" + "[[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]" + "</placeofcreation>\n"
    #     xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    # elif folio == "oudeband-voor":
    #     xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    #     xmlstring += "    <description>Front of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
    #     xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ signature+ " - Front of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
    #     xmlstring += "    <title>Front of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
    #     xmlstring += "    <medium>Gilded vellum binding</medium>\n"
    #     xmlstring += "    <date>" + "18th century" + "</date>\n"
    #     xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    # elif folio == "oudeband-achter":
    #     xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    #     xmlstring += "    <description>Back of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
    #     xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ signature+ " - Back of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
    #     xmlstring += "    <title>Back of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
    #     xmlstring += "    <medium>Gilded vellum binding</medium>\n"
    #     xmlstring += "    <date>" + "18th century" + "</date>\n"
    #     xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    # elif folio == "078r":
    #     xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    #     xmlstring += "    <description>Handwritten table of contents for the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
    #     xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ signature+ " - Handwritten table of contents for the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
    #     xmlstring += "    <title>Handwritten table of contents for the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
    #     xmlstring += "    <medium>"+str(medium)+"</medium>\n"
    #     xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    #     xmlstring += "    <date>" + "Between 1779 and 1809" + "</date>\n"
    #     xmlstring += "    <author>" + "[http://www.boekprentverzamelaars.info/jacob-visser-1724-1804 Jacob Visser] (1724-1804)" + "</author>\n"
    # elif folio == "binnenzijde1":
    #     xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    #     xmlstring += "    <description>Inside of 18th century vellum binding of the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
    #     xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ signature+ " - Inside of 18th century vellum binding of the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
    #     xmlstring += "    <title>Inside of 18th century vellum binding of the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
    #     xmlstring += "    <medium>"+str(medium)+"</medium>\n"
    #     xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    #     xmlstring += "    <date>" + "18th century" + "</date>\n"
    # elif folio == "binnenzijde2":
    #     xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    #     xmlstring += "    <description>Message by [[:nl:Willem_Jonckbloet|Willem Jonckbloet]] and a library check-out card (period 1930-1933) from the [[:nl:Koninklijke_Bibliotheek_(Nederland)|Koninklijke Bibliotheek]]. These are part of the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
    #     xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>"+ signature+ " - Message by Willem Jonckbloet and library check-out card. Part of manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
    #     xmlstring += "    <title>Message by [[:nl:Willem_Jonckbloet|Willem Jonckbloet]] and a library check-out card (period 1930-1933) from the [[:nl:Koninklijke_Bibliotheek_(Nederland)|Koninklijke Bibliotheek]]. These are part of the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
    #     xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}} (the entire page)" + "</dimensions>\n"
    #     xmlstring += "    <date>" + "1930-1933 (check-out card)" + "</date>\n"
    #     xmlstring += "    <author>" + "[[:nl:Willem_Jonckbloet|Willem Jonckbloet]] (message)" + "</author>\n"
    # elif folio in paaslist: #Paastabel
    #     xmlstring += "    <accessionnumber>*[" + browse_entry_1 + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    #     xmlstring += "    <description>Paschal table, folium "+ str(folio) +". This table is part of the manuscript containing " + title_overall + " - " + signature + "</description>\n"
    #     xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "    <GWToolsettitle>" + signature + " - Paschal table, folium "+ str(folio) + "</GWToolsettitle>\n"
    #     xmlstring += "    <title>Paschal table, folium "+ str(folio) +". This table is part of the manuscript containing " + title_overall + " - " + signature + "</title>\n"
    #     xmlstring += "    <date>" + str(date) + "</date>\n"
    #     xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
    #     xmlstring += "    <medium>"+str(medium)+"</medium>\n"
    #     xmlstring += "    <dimensions>" + str(dimensions) + "</dimensions>\n"
    #     xmlstring += "    <notes>" + str(notes) + "</notes>\n"
    #
    # elif folio in illumlist_1: #or folio in illumlist_1 or folio in illumlist_2:
    #     xmlstring += "    <accessionnumber>*[" + browse_entry_3 + " View this text] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript (KB 76 E 5) in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
    #     xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
    #     xmlstring += "    <date>" + str(date) + "</date>\n"
    #     xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"

        # if folio in illumlist_1: #separate illuminations (cut-outs, cropped)
        #     xmlstring += "    <description>"+ str(ullim_descrioption form json) + ". This illumination is part of folium " +str(folio)+ " from  "+ str(base_title_2) + "</description>\n"
        #     xmlstring += "    <title>"+ str(base_title_2)+", folium "+ str(folio) +". This illumination is  part of folium..... the manuscript containing " + title_overall + " - " + signature + "</title>\n"
        #     xmlstring += "    <GWToolsettitle>" + signature + " - " + str(base_titleGWT_2)+", folium "+ str(folio) + "</GWToolsettitle>\n"
        #     xmlstring += "    <medium>"+"Illumination on parchment"+"</medium>\n"
        #     xmlstring += "    <dimensions>" + str(KB76E5_illum.json) + "</dimensions>\n" # Dimensions of illum from KB76E5_illum.json
        #     #xmlstring += "    <notes>" + str(notes) + "</notes>\n"
        #     #xmlstring += "    <author>" + str(author_2) + "</author>\n" #The illum. has no disctinct author

        # xmlstring += "    <description>Folio " + folio + " from Beatrijsssssss\n"
        #          if hasIlluminations(folio_left):
        #              xmlstring += "=====Illuminations on this folio " + str(folio_left) + "=====" + "\n"
        #              xmlstring += findIlluminations(folio) + "\n"
        #          if hasIlluminations(folio_right):
        #              xmlstring += "=====Illuminations on the right folio " + str(folio_right) + "=====" + "\n"
        #              xmlstring += findIlluminations(folio_right) + "\n"
        # #         xmlstring += "</description>\n"
        #
        # elif folio in illumlist_2:  #illuminations are part of folium
        #     xmlstring += "    <description>"+ str(base_title_2)+", folium "+ str(folio) +". This text is part of a manuscript containing " + title_overall + " - " + signature + "</description>\n"
        #     xmlstring += "    <GWToolsettitle>" + signature + " - " + str(base_titleGWT_2)+", folium "+ str(folio) + "</GWToolsettitle>\n"
        #     xmlstring += "    <medium>"+str(medium)+"</medium>\n"
        #     xmlstring += "    <dimensions>" + str(dimensions) + "</dimensions>\n" #Full folium
        #     xmlstring += "    <notes>" + str(notes) + "</notes>\n"
        #     xmlstring += "    <author>" + str(author_2) + "</author>\n"


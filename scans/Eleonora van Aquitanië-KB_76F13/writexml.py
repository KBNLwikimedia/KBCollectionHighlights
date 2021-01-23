
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

def hasIlluminations(folium):
#In : folium (string)
#Returns: Boolan True is folium has illuminations, otherwise False
    hasIllums = False
    jsonfile = "illums-KB76F13.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["root"]["row"])):
        if data["root"]["row"][i]["folium"] == folium:
            hasIllums = True
    data_file.close()
    return hasIllums

def DescribeIlluminatedFolio(folium):
#In : folium (string)
#Returns: illumString: string with info about illuminations on this particular folio
    illumString = ""
    jsonfile = "illums-KB76F13.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["root"]["row"])):
        if data["root"]["row"][i]["folium"] == folium:
            print("-----------------"+str(folium)+"-------------------------")
            descriptionEN = finditem(data["root"]["row"][i], "descriptionEN")
            descriptionNL = finditem(data["root"]["row"][i], "descriptionNL")
            print(descriptionEN + " - " + descriptionNL)
    data_file.close()
    return descriptionEN, descriptionNL

#config paths/ urls
current_dir = os.path.dirname(os.path.realpath(__file__))
imagedir_hires= current_dir + "\\images\\bladerboek\\"
images_base_url_hires="https://www.kb.nl/kbhtml/eleonora/"

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
ppn = "311779549"
institution = "Koninklijke Bibliotheek"
medium = "Manuscript with [[:en:Illuminated_manuscript|illuminations]] on [[:en:Vellum|vellum]]"
dimensions = "Folium size: {{Size|mm|232|169}} - Block size: {{Size|mm|173|109}} with 1 column and 22 lines"
permission = "{{PD-art|PD-old-70-1923}}"
#wikidata = "Q1929931"
source =  "{{Koninklijke Bibliotheek}}"
date = "Circa 1180-1185"
placeofcreation = "[[:en:F&#233;camp|F&#233;camp]], Normandy, France"
#placeofcreation = "[[:en:Fecamp|Fecamp]]"


#language = "Dutch"
script = "[[:nl:Littera textualis|Littera textualis]]"
notes= "Script is " + str(script)
#nfolios = "80"

binding = "Brown leather binding with gilt stamped, made in France in circa 1770"

#otherversions = ""

#objecthistory = "In de zeventiende eeuw is het handschrift eigendom van de geleerde diplomaat Nicolaas Heinsius. Na diens dood wordt het in 1683 in Leiden geveild, om pas weer in 1764 in Den Haag op te duiken. In 1779 wordt het boek opnieuw verkocht, vermoedelijk aan Jacob Visser, de Haagse jurist die het bezit in 1784 (dat weten we zeker). Op aandringen van koning Lodewijk Napoleon komt de rijke boekenverzameling van landsadvocaat Visser in 1809 terecht in de Koninklijke Bibliotheek. Pas dan en daar begint de zegetocht van dit kostbare boek door het land der letteren: ‘de Beatrijs’ is nu onbetwist het bekendste middeleeuwse handschrift in de collectie van de KB."

fol001rdesc = "Ex bibliotheca G.J. Gerard 1767"

fol176vdescr="Nos Gerardus de Dainvilla, episcopus quondam Atrebatensis et nunc Morinensis, concessimus Johanne de Plancquis, moniali de Strumis Atrebatensis dyocesis, consanguinee nostre, quod nostro psalterio presenti quoadiuxerit, uti et gaudere possit. Et si dicta consanguinea nostra ante nos decesserit, illud ad nos vel heredes nostro proprietarie revertetur. Et si ante eam nos decedere contingat, dicta Johanna de eo disponere valeat secundum devocionem suam, in personam talem que pro nobis orare perpetuo teneatur. Actum anno Domini millesimo CCCo sexagesimo nono, die XIIIa junii, presente Stephano de Matheny, apostolica et imperiali auctoritate notario. St. de Matheny"

former_owners = "This manuscript was formerly owned by [[:en:Gérard de Dainville|Gérard de Dainville]] (-1378), Jeanne des Planches (a nun in the convent of Étrun in the diocese of Arras) and [[:fr:Georges-Joseph Gérard|Georges-Joseph Gérard]] (1767). Read the [https://www.kb.nl/en/themes/medieval-manuscripts/psalter-of-eleanor-of-aquitaine-ca-1185 whereabouts of the psalter]"

#illuminations = "27 full-page miniatures (possibly 15 missing); 16 historiated initials; decorated initials with border decoration; penwork initials"

base_titleEN = "Psalter of [[:en:Eleanor of Aquitaine|Eleanor of Aquitaine]] (ca. 1185)"
base_titleNL = "Psalter van [[:nl:Eleonora van Aquitanië|Eleonora van Aquitanië]] (ca. 1185)"
base_title_GWT = "Psalter of Eleanor of Aquitaine (ca. 1185)"
signature = "KB 76 F 13"

browse_entry = "https://galerij.kb.nl/kb.html#/en/psalter/page/3/zoom/3/lat/-58.95000823335702/lng/-37.79296875"
homepageNL = "https://www.kb.nl/themas/middeleeuwse-handschriften/psalter-van-eleonora-van-aquitanie-ca-1185"
detailpageNL = "https://www.kb.nl/psalter-van-eleonora-van-aquitanie-de-beschrijving-en-inhoud"
homepageEN = "https://www.kb.nl/en/themes/medieval-manuscripts/psalter-of-eleanor-of-aquitaine-ca-1185"
detailpageEN = "https://www.kb.nl/en/themes/medieval-manuscripts/psalter-of-eleanor-of-aquitaine-ca-1185/psalter-of-eleanor-of-aquitaine-description-and-contents"

#===================================================================

XMLoutputfile = open("eleonora.xml", "w", encoding="UTF-8")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname = infile.replace(imagedir_hires, "") #"008-002r.jpg"
    picname_trunc=picname.replace(".jpg", "") #"008-002r"
    # split in 2 parts: 008 + 002r
    imagenumber = picname_trunc.split("-")[0] #008
    folium = picname_trunc.split("-")[1] #002r
    #print('"'+str(folium)+'",')# + " -- " + str(findIlluminations(folio)))

    xmlstring += "  <record>\n"
    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(picname_trunc)+"</folio>\n"
    xmlstring += "    <medium>" + str(medium) + "</medium>\n"
    xmlstring += "    <dimensions>" + str(dimensions) + "</dimensions>\n"
    xmlstring += "    <accessionnumber>*[" + browse_entry + " View this manuscript] on the website of the KB" + "\n*" + "Read an [" + homepageNL + " introduction to the manuscript in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Read a [" + detailpageNL + " detailed description of the contents in Dutch] and in [" + detailpageEN + " English]" "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn +"</accessionnumber>\n"
    xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(folium)+".jpg</URLtothemediafile>\n"
    xmlstring += "    <date>" + str(date) + "</date>\n"
    xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
    xmlstring += "    <notes>"+ str(notes) +"</notes>\n"
    xmlstring += "    <objecthistory>"+ str(former_owners)+"</objecthistory>\n"
    if hasIlluminations(folium) == True:
        xmlstring += "    <description lang='en'>Folium " + str(folium) + " from the "+ str(base_titleEN) + " from the collection of the [[:en:National Library of the Netherlands|National Library of the Netherlands]]. The illumination shows " + DescribeIlluminatedFolio(folium)[0] + ".</description>\n"
        xmlstring += "    <description lang='nl'>Folium " + str(folium) + " van het "+ str(base_titleNL) + " uit de collectie van de [[:nl:Koninklijke_Bibliotheek_(Nederland)|Koninklijke Bibliotheek]]. De verluchting toont " + DescribeIlluminatedFolio(folium)[1] + ".</description>\n"
        xmlstring += "    <title lang='en'>" + DescribeIlluminatedFolio(folium)[0] + " - " + str(base_titleEN) + " - " + signature + ", folium " + str(folium)+ "</title>\n"
        xmlstring += "    <title lang='nl'>" + DescribeIlluminatedFolio(folium)[1] + " - " + str(base_titleNL) + " - " + signature + ", folium " + str(folium)+ "</title>\n"
        xmlstring += "    <GWToolsettitle>" + DescribeIlluminatedFolio(folium)[0] + " - " + str(base_title_GWT) + " - " + signature + ", folium " + str(folium)+ "</GWToolsettitle>\n"
    else: #no illums
        xmlstring += "    <description lang='en'>Folium " + str(folium) + " from the "+ str(base_titleEN) + " from the collection of the [[:en:National Library of the Netherlands|National Library of the Netherlands]].</description>\n"
        xmlstring += "    <description lang='nl'>Folium " + str(folium) + " van het "+ str(base_titleNL) + " uit de collectie van de [[:nl:Koninklijke_Bibliotheek_(Nederland)|Koninklijke Bibliotheek]].</description>\n"
        xmlstring += "    <title lang='en'>" + str(base_titleEN) + " - " + signature + ", folium " + str(folium)+ "</title>\n"
        xmlstring += "    <title lang='nl'>" + str(base_titleNL) + " - " + signature + ", folium " + str(folium)+ "</title>\n"
        xmlstring += "    <GWToolsettitle>" + str(base_title_GWT) + " - " + signature + ", folium " + str(folium)+ "</GWToolsettitle>\n"

        #xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"
    #xmlstring += "    <otherversions>"+ str(otherversions) +"</otherversions>\n"

    # xmlstring += "    <author>" + str(author_3) + "</author>\n"

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


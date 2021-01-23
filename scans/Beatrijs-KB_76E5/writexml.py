
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
    jsonfile = "KB76E5_illum.json"
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
    jsonfile = "KB76E5_illum.json"
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    for i in range(len(data["records"]["record"])):
        if data["records"]["record"][i]["folio"] == folio:
            print("-----------------"+str(folio)+"-------------------------")
            illumType = finditem(data["records"]["record"][i], "type")
            illumDesc = finditem(data["records"]["record"][i], "description")
            illumIconclassCode = finditem(data["records"]["record"][i], "iconClass")
            illumDimensions = finditem(data["records"]["record"][i], "dimensions")
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
imagedir_hires= current_dir + "\\images\\bladerboek\\test\\"
images_base_url_hires="https://www.kb.nl/kbhtml/beatrijs/"

homepageNL = "https://www.kb.nl/themas/middeleeuwen/beatrijs"
homepageEN = "https://www.kb.nl/en/themes/middle-ages/beatrijs"

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
ppn = "311779255"
institution = "Koninklijke Bibliotheek"
medium = "Manuscript on parchment"
dimensions = "Folium size: {{Size|mm|257|190}} - Block size: {{Size|mm|185|150}} with 2 columns and 37 lines"
permission = "{{PD-art|PD-old-70-1923}}"
wikidata = "Q1929931"
source =  "{{Koninklijke Bibliotheek}}"
date = "Circa 1374"
placeofcreation = "Brabant, Southern Netherlands (Brussels?)"
language = "Dutch"
script = "Littera textualis"
notes= "Text in "+str(language)+ ". Script is " + str(script)
nfolios = "80"


#otherversions = ""

#objecthistory = "In de zeventiende eeuw is het handschrift eigendom van de geleerde diplomaat Nicolaas Heinsius. Na diens dood wordt het in 1683 in Leiden geveild, om pas weer in 1764 in Den Haag op te duiken. In 1779 wordt het boek opnieuw verkocht, vermoedelijk aan Jacob Visser, de Haagse jurist die het bezit in 1784 (dat weten we zeker). Op aandringen van koning Lodewijk Napoleon komt de rijke boekenverzameling van landsadvocaat Visser in 1809 terecht in de Koninklijke Bibliotheek. Pas dan en daar begint de zegetocht van dit kostbare boek door het land der letteren: ‘de Beatrijs’ is nu onbetwist het bekendste middeleeuwse handschrift in de collectie van de KB."

#illuminations = "27 full-page miniatures (possibly 15 missing); 16 historiated initials; decorated initials with border decoration; penwork initials"

title_overall = "[[:nl:Dietsche doctrinale|Die Dietsche Doctrinale]] by [[:nl:Jan van Boendale|Jan van Boendale]], [[:nl:Beatrijs|Beatrijs]], Dit es vanden aflate van Rome, Die heimelicheit der heimelicheden by [[:nl:Jacob van Maerlant|Jacob van Maerlant]] and other texts"
title_overall_GWT = "Die Dietsche Doctrinale by Jan van Boendale, Beatrijs, Die heimelicheit der heimelicheden by Jacob van Maerlant and other texts"
signature = "KB 76 E 5"
#de default browse entry, for pages not part of the sections below
browse_entry_default = "https://galerij.kb.nl/kb.html#/nl/beatrijs/page/4/zoom/3/lat/-39.43619299931407/lng/87.275390625"

#===================================================================

#fol. Iv: paastabel
base_titleGWT_1 = "Paschal table"
base_title_1    = "Paschal table"
author_1= ""
browse_entry_1 = "https://galerij.kb.nl/kb.html#/nl/beatrijs/page/3/zoom/3/lat/-37.92686760148134/lng/-45.17578125"
paaslist = ["fl001r","fl002v","fl003r","fl003v"]

#fol. 1r t/m 47r: Die Dietsche doctrinale / [Jan van Boendale (ca. 1280-1351)]
base_titleGWT_2 = "Die Dietsche Doctrinale"
base_title_2    = "Die Dietsche Doctrinale"
author_2= "{{Creator:Jan van Boendale}}"
browse_entry_2 = "https://galerij.kb.nl/kb.html#/nl/beatrijs/page/4/zoom/3/lat/-51.124212757826875/lng/88.06640625"
dietselist = ["001r","001v","002r","002v","003r","003v","004r","004v","005r","005v","006r","006v","007r","007v","008r","008v","009r","009v","010r","010v","011r","011v","012r","012v","013r","013v","014r","014v","015r","015v","016r","016v","017r","017v","018r","018v","019r","019v","020r","020v","021r","021v","022r","022v","023r","023v","024r","024v","025r","025v","026r","026v","027r","027v","028r","028v","029r","029v","030r","030v","031r","031v","032r","032v","033r","033v","034r","034v","035r","035v","036r","036v","037r","037v","038r","038v","039r","039v","040r","040v","041r","041v","042r","042v","043r","043v","044r","044v","045r","045v","046r","046v","047r"]

#fol. 47v t/m 54r: Beatrijs
base_titleGWT_3 = "Beatrijs"
base_title_3    = "[[:nl:Beatrijs|Beatrijs]]"
author_3= ""
browse_entry_3 = "https://galerij.kb.nl/kb.html#/nl/beatrijs/page/51/zoom/3/lat/-37.92686760148134/lng/-45.17578125"
beatlist=["047v","048r","048v","049r","049v","050r","050v","051r","051v","052r","052v","053r","053v","054r"]
modern_translation = "[https://www.kb.nl/themas/middeleeuwen/beatrijs/beatrijs-moderne-vertaling-door-willem-wilmink Moderne translation] by [[:nl:Willem Wilmink|Willem Wilmink]]"

#fol. 54v: Ave Maria, Pater noster en Credo uit Der leken spieghel van Jan van Boendale (ca. 1280-1351)
base_titleGWT_4 = "Hail Mary, Lord's_Prayer and Credo from Der leken spieghel"
base_title_4    = "[[:en:Hail_Mary|Ave Maria]], [[:en:Lord's_Prayer|Pater noster]] and [[:en:Credo|Credo]] from [https://nl.wikipedia.org/wiki/Jan_van_Boendale#Der_leken_spiegel_.28ca._1325-1330.29 Der leken spieghel]"
author_4= "{{Creator:Jan van Boendale}}"
browse_entry_4 = "https://galerij.kb.nl/kb.html#/nl/beatrijs/page/58/zoom/3/lat/-69.8698915662856/lng/-51.328125"
avelist=["054v"]

#fol. 55r t/m 57r: catechetische teksten
base_titleGWT_5 = "Catechetical texts about the Ten Commandments, the Seven Sacraments and about the Seven Corporal Works of Mercy (excerpts)"
base_title_5    = "[[:en:Catechesis|Catechetical]] texts about the [[:en:Ten Commandments|Ten Commandments]], about the Seven [[:en:Sacrament|Sacraments]] and about the Seven [[:en:Works of mercy|Corporal Works of Mercy]] (excerpts from [[:nl:Jan van Ruusbroec|Jan van Ruusbroec]] (ca. 1293-1381))"
author_5= "{{Creator:Jan van Ruusbroec}}"
browse_entry_5 = "https://galerij.kb.nl/kb.html#/nl/beatrijs/page/58/zoom/3/lat/-53.80065082633021/lng/82.96875"
catlist=["055r","055v","056r","056v","057r"]

#fol. 57v t/m 61r: de aflaten van de zeven kerken van Rome
base_titleGWT_6 = "Dit es vanden aflate van Rome (The indulgences of the seven church of Rome)"
base_title_6    = "Dit es vanden aflate van Rome (The indulgences of the seven church of Rome)"
author_6= ""
browse_entry_6 = "https://galerij.kb.nl/kb.html#/nl/beatrijs/page/61/zoom/3/lat/-48.98021698537499/lng/-10.72265625"
aflist=["057v","058r","058v","059r","059v","060r","060v","061r"]

#fol. 61v t/m 76r: Heimelicheit der heimelicheden / Jacob van Maerlant (ca. 1235-1300)
base_titleGWT_7 = "Die Heimelicheit der heimelicheden"
base_title_7    = "Die Heimelicheit der heimelicheden"
author_7= "{{Creator:Jacob van Maerlant}}"
browse_entry_7 = "https://galerij.kb.nl/kb.html#/nl/beatrijs/page/65/zoom/3/lat/-37.5097258429375/lng/-52.734375"
heimlist=["061v","062r","062v","063r","063v","064r","064v","065r","065v","066r","066v","067r","067v","068r","068v","069r","069v","070r","070v","071r","071v","072r","072v","073r","073v","074r","074v","075r","075v","076r"]

#all illuminations
illumlist_1 =["001r-init","007v-init","033v-init","047v-init","057v-init","061v-init"]
illumlist_2 =["001r","007v","033v","047v","057v","061v"]

#===================================================================

XMLoutputfile = open("beatrijs.xml", "w")
xmlstring=""
xmlstring += "<?xml version='1.0' encoding='UTF-8'?>\n"
xmlstring += "<records>\n"

for infile in glob.glob(os.path.join(imagedir_hires, '*.jpg')):
    picname = infile.replace(imagedir_hires, "") #"006_76e5_fl002v.jpg"
    picname_trunc=picname.replace(".jpg", "") #"006_76e5_fl002v"
    # split in 3 parts: 006 + 76e5 + fl002v
    imagenumber = picname_trunc.split("_")[0] #006
    #folio_left = picname_trunc.split("_")[1]  # 76e5- we can further ignore this part, this is always the same
    folio = picname_trunc.split("_")[2] #fl002v
    #print(imagenumber + " -- " + str(folio) + " -- " + str(hasIlluminations(folio)) + " -- " + str(findIlluminations(folio)))
    #print(imagenumber + " -- " + str(folio) + " -- " + str(hasIlluminations(folio)))# + " -- " + str(findIlluminations(folio)))
    print('"'+str(folio)+'",')# + " -- " + str(findIlluminations(folio)))

    xmlstring += "  <record>\n"
    xmlstring += "    <Institution>" + institution + "</Institution>\n"
    xmlstring += "    <permission>"+permission+"</permission>\n"
    xmlstring += "    <source>"+source+"</source>\n"
    xmlstring += "    <folio>"+str(picname_trunc)+"</folio>\n"
    xmlstring += "    <wikidata>"+str(wikidata)+"</wikidata>\n"
    #xmlstring += "    <otherversions>"+ str(otherversions) +"</otherversions>\n"
    #xmlstring += "    <objecthistory>"+ str(objecthistory)+"</objecthistory>\n"

    if folio == "moderneband-voor":
        xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
        xmlstring += "    <description>Front of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ signature+ " - Front of brown leather binding from 1993. Inside is the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
        xmlstring += "    <title>Front of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
        xmlstring += "    <medium>Brown leather binding</medium>\n"
        xmlstring += "    <date>" + "1993" + "</date>\n"
        xmlstring += "    <artist>" + "Lucie M. Gimbr&#xe8;re" + "</artist>\n"
        xmlstring += "    <placeofcreation>" + "[[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]" + "</placeofcreation>\n"
        xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    elif folio == "moderneband-achter":
        xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
        xmlstring += "    <description>Back of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing " + title_overall + " - " + signature + "</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>" + signature + " - Back of brown leather binding from 1993. Inside is the manuscript containing " + title_overall_GWT + "</GWToolsettitle>\n"
        xmlstring += "    <title>Back of brown leather binding from 1993 made by the nun Lucie M. Gimbr&#xe8;re from the [[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]. Inside is the manuscript containing " + title_overall + " - " + signature + "</title>\n"
        xmlstring += "    <medium>Brown leather binding</medium>\n"
        xmlstring += "    <date>" + "1993" + "</date>\n"
        xmlstring += "    <artist>" + "Lucie M. Gimbr&#xe8;re" + "</artist>\n"
        xmlstring += "    <placeofcreation>" + "[[:nl:Onze-Lieve-Vrouweabdij|Onze-Lieve-Vrouweabdij]] in [[:nl:Oosterhout (Noord-Brabant)|Oosterhout]]" + "</placeofcreation>\n"
        xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    elif folio == "oudeband-voor":
        xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
        xmlstring += "    <description>Front of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ signature+ " - Front of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
        xmlstring += "    <title>Front of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
        xmlstring += "    <medium>Gilded vellum binding</medium>\n"
        xmlstring += "    <date>" + "18th century" + "</date>\n"
        xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    elif folio == "oudeband-achter":
        xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
        xmlstring += "    <description>Back of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ signature+ " - Back of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
        xmlstring += "    <title>Back of gilded vellum binding from the 18th century. Inside is the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
        xmlstring += "    <medium>Gilded vellum binding</medium>\n"
        xmlstring += "    <date>" + "18th century" + "</date>\n"
        xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
    elif folio == "078r":
        xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
        xmlstring += "    <description>Handwritten table of contents for the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ signature+ " - Handwritten table of contents for the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
        xmlstring += "    <title>Handwritten table of contents for the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
        xmlstring += "    <medium>"+str(medium)+"</medium>\n"
        xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
        xmlstring += "    <date>" + "Between 1779 and 1809" + "</date>\n"
        xmlstring += "    <author>" + "[http://www.boekprentverzamelaars.info/jacob-visser-1724-1804 Jacob Visser] (1724-1804)" + "</author>\n"
    elif folio == "binnenzijde1":
        xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
        xmlstring += "    <description>Inside of 18th century vellum binding of the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ signature+ " - Inside of 18th century vellum binding of the manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
        xmlstring += "    <title>Inside of 18th century vellum binding of the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
        xmlstring += "    <medium>"+str(medium)+"</medium>\n"
        xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}}" + "</dimensions>\n"
        xmlstring += "    <date>" + "18th century" + "</date>\n"
    elif folio == "binnenzijde2":
        xmlstring += "    <accessionnumber>*[" + browse_entry_default + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
        xmlstring += "    <description>Message by [[:nl:Willem_Jonckbloet|Willem Jonckbloet]] and a library check-out card (period 1930-1933) from the [[:nl:Koninklijke_Bibliotheek_(Nederland)|Koninklijke Bibliotheek]]. These are part of the manuscript containing "+ title_overall + " - " + signature +"</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>"+ signature+ " - Message by Willem Jonckbloet and library check-out card. Part of manuscript containing "+ title_overall_GWT+"</GWToolsettitle>\n"
        xmlstring += "    <title>Message by [[:nl:Willem_Jonckbloet|Willem Jonckbloet]] and a library check-out card (period 1930-1933) from the [[:nl:Koninklijke_Bibliotheek_(Nederland)|Koninklijke Bibliotheek]]. These are part of the manuscript containing "+ title_overall+" - " + signature +"</title>\n"
        xmlstring += "    <dimensions>" + "Approx. {{Size|mm|257|190}} (the entire page)" + "</dimensions>\n"
        xmlstring += "    <date>" + "1930-1933 (check-out card)" + "</date>\n"
        xmlstring += "    <author>" + "[[:nl:Willem_Jonckbloet|Willem Jonckbloet]] (message)" + "</author>\n"
    elif folio in paaslist: #Paastabel
        xmlstring += "    <accessionnumber>*[" + browse_entry_1 + " View this manuscript] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
        xmlstring += "    <description>Paschal table, folium "+ str(folio) +". This table is part of the manuscript containing " + title_overall + " - " + signature + "</description>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <GWToolsettitle>" + signature + " - Paschal table, folium "+ str(folio) + "</GWToolsettitle>\n"
        xmlstring += "    <title>Paschal table, folium "+ str(folio) +". This table is part of the manuscript containing " + title_overall + " - " + signature + "</title>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
        xmlstring += "    <medium>"+str(medium)+"</medium>\n"
        xmlstring += "    <dimensions>" + str(dimensions) + "</dimensions>\n"
        xmlstring += "    <notes>" + str(notes) + "</notes>\n"

    elif folio in illumlist_1: #or folio in illumlist_1 or folio in illumlist_2:
        xmlstring += "    <accessionnumber>*[" + browse_entry_3 + " View this text] on the website of the KB" + "\n*" + "Read [" + homepageNL + " backgroud information in Dutch] and in [" + homepageEN + " English]" + "\n*" + "Description of the entire manuscript (KB 76 E 5) in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN=" + ppn + "</accessionnumber>\n"
        xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
        xmlstring += "    <date>" + str(date) + "</date>\n"
        xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"

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

        #else: #regular folio, without illuminations
        xmlstring += "    <description>" + str(base_title_3) + ". This text is folium " + str(folio)+ " of the manuscript "+ str(signature) +" containing " + title_overall + "</description>\n"



        xmlstring += "    <title>" + str(base_title_3) + "</title>\n"
        xmlstring += "    <GWToolsettitle>" + str(base_titleGWT_3)+ " - " + signature + ", folium "+ str(folio) + "</GWToolsettitle>\n"
        xmlstring += "    <medium>" + str(medium) + "</medium>\n"
        xmlstring += "    <dimensions>" + str(dimensions) + "</dimensions>\n"
        xmlstring += "    <notes>" + str(notes) + "</notes>\n"
        #xmlstring += "    <author>" + str(author_3) + "</author>\n"
        #xmlstring += "    <otherversions>" + str(modern_translation) + "</otherversions>\n"

        xmlstring += "    <description>Folio " + folio + " from Beatrijsssssss\n"
        if hasIlluminations(folio):
            xmlstring += "=====Illuminations on this folio " + str(folio) + "=====" + "\n"
            xmlstring += findIlluminations(folio) + "\n"
        xmlstring += "</description>\n"


    #   elif folio in beatlist:
    #       if picname_trunc in illumlist:
    #   elif folio in  avelist:
    #       if picname_trunc in illumlist:
    #   elif folio in catlist:
    #       if picname_trunc in illumlist:
    #   elif folio in aflist:
    #       if picname_trunc in illumlist:
    #   elif folio in heimlist:
    #       if picname_trunc in illumlist:




#
#     elif picname_trunc == "160_achterplat":
#         xmlstring += "    <description>Back of red velvet binding from 18th century with silver locks and gilded edges. Inside is the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]</description>\n"
#         xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
#         xmlstring += "    <GWToolsettitle>" + base_titleGWT + " - Back of red velvet binding from 18th century with silver locks  and gilded edges</GWToolsettitle>\n"
#         xmlstring += "    <title>" + base_title + " - Back of red velvet binding from 18th century with silver locks and gilded edges</title>\n"
#         xmlstring += "    <medium>Red velvet binding with silver locks and gilded edges</medium>\n"
#         xmlstring += "    <dimensions>" + "Approx. {{Size|mm|116|84}}" + "</dimensions>\n"
#         xmlstring += "    <date>" + "18th century" + "</date>\n"
#
#     elif picname_trunc == "003_fl001v-001r":  # Calendar - month of January
#         xmlstring += "    <description>Folio 001r from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]. Calendar of the diocese of Utrecht, month of January, first half</description>\n"
#         xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
#         xmlstring += "    <GWToolsettitle>" + base_titleGWT + " - Folio 001r - Calendar of the diocese of Utrecht, month of January, first half</GWToolsettitle>\n"
#         xmlstring += "    <title>" + base_title + " - Folio 001r - Calendar of the diocese of Utrecht, month of January, first half</title>\n"
#         xmlstring += "    <artist>" + str(artist) + "</artist>\n"
#         xmlstring += "    <notes>" + str(notes) + "</notes>\n"
#         xmlstring += "    <dimensions>" + dimensions_calendar + "</dimensions>\n"
#         xmlstring += "    <medium>" + str(medium) + "</medium>\n"
#         xmlstring += "    <date>" + str(date) + "</date>\n"
#         xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
#
#     elif picname_trunc in illumlist
#         xmlstring += "<description>Lefthand side folio " + folio_left + " and righthand side folio " + folio_right + " from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]] - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</description>\n"
#         xmlstring += "<URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
#         xmlstring += "<GWToolsettitle>" + base_titleGWT + " - folios " + folio_left + " (left) and " + folio_right + " (right) - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</GWToolsettitle>\n"
#         xmlstring += "<title>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right) - Calendar of the diocese of Utrecht for the months of " + calendar_dic[picname_trunc] + "</title>\n"
#         xmlstring += "    <artist>" + str(artist) + "</artist>\n"
#         xmlstring += "    <notes>" + str(notes) + "</notes>\n"
#         xmlstring += "    <dimensions>" + dimensions_calendar + "</dimensions>\n"
#         xmlstring += "    <medium>" + str(medium) + "</medium>\n"
#         xmlstring += "    <date>" + str(date) + "</date>\n"
#         xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
#
#     elif picname_trunc == "158_155v-ep001r":
#         xmlstring += "    <description>Folio 155v from the Book of hours by the [[w:en:Master_of_Zweder_van_Culemborg|Master(s) of Zweder van Culemborg]]</description>\n"
#         xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
#         xmlstring += "    <GWToolsettitle>" + base_titleGWT + " - Folio 155v</GWToolsettitle>\n"
#         xmlstring += "    <title>" + base_title + " - Folio 155v</title>\n"
#         xmlstring += "    <artist>" + str(artist) + "</artist>\n"
#         xmlstring += "    <notes>" + str(notes) + "</notes>\n"
#         xmlstring += "    <dimensions>" + dimensions + "</dimensions>\n"
#         xmlstring += "    <medium>" + str(medium) + "</medium>\n"
#         xmlstring += "    <date>" + str(date) + "</date>\n"
#         xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
#
#     else:  # all the normal pages
#         xmlstring += "    <artist>" + str(artist) + "</artist>\n"
#         xmlstring += "    <notes>" + str(notes) + "</notes>\n"
#         xmlstring += "    <dimensions>" + dimensions + "</dimensions>\n"
#         xmlstring += "    <medium>" + str(medium) + "</medium>\n"
#         xmlstring += "    <date>" + str(date) + "</date>\n"
#         xmlstring += "    <placeofcreation>" + str(placeofcreation) + "</placeofcreation>\n"
#         xmlstring += "    <URLtothemediafile>" + images_base_url_hires + str(picname) + "</URLtothemediafile>\n"
#         xmlstring += "    <title>" + base_title + " - folios " + folio_left + " (left) and " + folio_right + " (right)</title>\n"
#         xmlstring += "    <GWToolsettitle>" + base_titleGWT + " - folios " + folio_left + " (left) and " + folio_right + " (right)</GWToolsettitle>\n"



    xmlstring += "  </record>\n"
xmlstring += "</records>\n"

XMLoutputfile.write(xmlstring)
XMLoutputfile.close()
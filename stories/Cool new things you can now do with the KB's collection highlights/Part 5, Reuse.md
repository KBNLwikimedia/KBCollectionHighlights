![Banner](../images/banners/KBTopstukkenBannerWikimedia_EN.jpg)
# 50 cool new things you can now do with KB's collection highlights - Part 5, Reuse

<img src="images/KBtopstukkenMemeEN.jpg" width="70%" align="right"/>

*In this [series of 5 articles](index.md) I show the added value of putting images and metadata of [digitised collection highlights](https://www.kb.nl/galerij/digitale-topstukken) of the KB, national library of the Netherlands, into the Wikimedia infrastructure. By putting our collection highlights into Wikidata, Wikimedia Commons and Wikipedia, dozens of new functionalities have been added. As a result of Wikifying this collection, you can now do things with these highlights that were not possible before.*

In het vorige (vierde) deel van deze vijfdelige Plein-serie heb ik 11 hulpstukken van het rechter mes uitgeklapt. We bekeken welke vernieuwende functionaliteiten er voor losse Topstukafbeeldingen beschikbaar zijn gekomen; we lieten o.a. het kunnen downloaden van afbeeldingen in meerdere resoluties, metadatering per beeld met manifeste bronvermelding en rechtenstatus, geo-coördinaten , gestructureerde data, meertalige ontsluiting en nieuwe zoekmogelijkheden op basis van inhoud (‘wat staat erop?’) de revue passeren.

In dit vijfde deel ga ik het laatste groepje gereedschappen van het rechter mes uitklappen. Ik ga uitleggen hoe je op basis van de Wikimedia-infrastructuur onze topstukken buiten de Wikimedia-context kunt hergebruiken. Hoe je de topstukken als technisch LEGO kunt gebruiken t.b.v. je eigen websites, diensten, apps, hackathons en projecten.

 In Part 5, Reuse I will explain how you can reuse KB's collection highlights outside of the Wikimedia context, that is, for/in your own websites, services, apps, hackathons and projects. I'm going to talk about REST APIs, SPARQL, data dumps, Python scripts and machine interactions with our highlights.

<kbd><img src="images/image-p1-024.png" height="220" align="right"/></kbd>

Ik ga het m.a.w. hebben over APIs, SPARQL, datadumps, Python en script- en machinematige interacties met onze topstukken. Toffe dingen voor onze doelgroep van ontwikkelaars, appbouwers, digital humanists, data scientists, LOD-afficionados en andere leuke nerds.

<hr>

### About the author
<img align="left" src="../images/800px-Olaf_Janssen_at_GLAM_WIKI_Tel_Aviv_Conference_2018.JPG" width="50"/>

Olaf Janssen is the Wikimedia coordinator of the KB, the national library of the Netherlands. He contributes to
[Wikipedia](https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief), [Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:Koninklijke_Bibliotheek) and [Wikidata](https://www.wikidata.org/wiki/Wikidata:GLAM/Koninklijke_Bibliotheek_Nederland) as [User:OlafJanssen](https://nl.wikipedia.org/wiki/Gebruiker:OlafJanssen)<br>

### Reusing this article
This text of this article is available under the [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) license. 
<kbd><img src="../images/cc-by.png" width="80"/></kbd>

### Image sources & credits
* [Swiss_army_knife_open,_2012-(01)](https://commons.wikimedia.org/wiki/File:Swiss_army_knife_open,_2012-(01).jpg) -- Joe Loong, [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0), via Wikimedia Commons
* [Victorinox_Swiss_Army_SwissChamp_XAVT](https://commons.wikimedia.org/wiki/File:Victorinox_Swiss_Army_SwissChamp_XAVT.jpg) -- Dave Taylor from Boulder, CO, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0>), via Wikimedia Commons

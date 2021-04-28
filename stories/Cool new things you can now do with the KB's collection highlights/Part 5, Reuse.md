![Banner](../images/banners/KBTopstukkenBannerWikimedia_EN.jpg)
# 50 cool new things you can now do with KB's collection highlights - Part 5, Reuse

<img src="images/KBtopstukkenMemeEN.jpg" width="70%" align="right"/>

*In this [series of 5 articles](index.md) I show the added value of putting images and metadata of [digitised collection highlights](https://www.kb.nl/galerij/digitale-topstukken) of the KB, national library of the Netherlands, into the Wikimedia infrastructure. By putting our collection highlights into Wikidata, Wikimedia Commons and Wikipedia, dozens of new functionalities have been added. As a result of Wikifying this collection, you can now do things with these highlights that were not possible before.*

In het vorige (vierde) deel van deze vijfdelige Plein-serie heb ik 11 hulpstukken van het rechter mes uitgeklapt. We bekeken welke vernieuwende functionaliteiten er voor losse Topstukafbeeldingen beschikbaar zijn gekomen; we lieten o.a. het kunnen downloaden van afbeeldingen in meerdere resoluties, metadatering per beeld met manifeste bronvermelding en rechtenstatus, geo-coördinaten , gestructureerde data, meertalige ontsluiting en nieuwe zoekmogelijkheden op basis van inhoud (‘wat staat erop?’) de revue passeren.

In dit vijfde deel ga ik het laatste groepje gereedschappen van het rechter mes uitklappen. Ik ga uitleggen hoe je op basis van de Wikimedia-infrastructuur onze topstukken buiten de Wikimedia-context kunt hergebruiken. Hoe je de topstukken als technisch LEGO kunt gebruiken t.b.v. je eigen websites, diensten, apps, hackathons en projecten.

<kbd><img src="images/image-p1-024.png" height="200"/></kbd><kbd><img src="images/image-p1-020.png" height="200"/></kbd><kbd><img src="images/image-p1-025.png" height="200"/></kbd>


 In Part 5, Reuse I will explain how you can reuse KB's collection highlights outside of the Wikimedia context, that is, for/in your own websites, services, apps, hackathons and projects. I'm going to talk about REST APIs, SPARQL, data dumps, Python scripts and machine interactions with our highlights.

Ik ga het m.a.w. hebben over APIs, SPARQL, Python en script- en machinematige interacties met onze topstukken. Toffe dingen voor onze doelgroep van ontwikkelaars, appbouwers, digital humanists, data scientists, LOD-afficionados en andere leuke nerds.

I'll Try to Follow the same orfer as in parts 2, 3 and 4, so 
- all highlights
- indivdial highlghts
- individual highlght images
and explain how you can retrieve some of the images, data, and texts we requested requested via the GUI (so in HTML)  in the previos parts now in their machine readable fromats(json, rdf, xnl, csv) via API and sparql services in the wikimedia infra, giving more controll & felixibilty over the excat ouptut, cutom made for ypour needs


## Reuse - all highlights

38) Let's start with recreating the [image grid](https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken/Galerij) we started out with in [Part 2](Part%202%2C%20Overviews%20of%20all%20highlights.html) using the [Wikidata SPARQL query service](https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service). A short [SPARQL query](https://w.wiki/3E8w) does the job: 

```sparql
# Thumbnail gallery of KB collection highlights
#defaultView:ImageGrid
SELECT DISTINCT ?item ?itemLabel ?image WHERE {
  # the thing is part of the KB collection, and has role 'collection highlight' within that collection
  ?item (p:P195/ps:P195) wd:Q1526131; p:P195 [pq:P2868 wd:Q29188408]. 
  OPTIONAL{?item wdt:P18 ?image.}
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} ORDER BY ?itemLabel
```
<sub>*[Try it](https://w.wiki/3E8w) in the Wikidata query service*</sub>

This query results into a **[SPARQL driven thumbnail gallery](https://w.wiki/3E8z)** of KB highlights.

 <kbd><img src="images/image-p5-002.png" width="100%"/></kbd><br/><sub>*The [image grid](https://w.wiki/3E8z) of KB highlights for the above SPARQL query. Screenshot Wikidata query service d.d. 23-04-2021*</sub>

39) Next, let's look at lists and tables. The [list of highlights](https://www.kb.nl/galerij/digitale-topstukken) on the KB website is only availabe as HTML. For effective reuse you'd prefer it in a structured and open format such as JSON, XML or RDF. Let's look how we can request **structured lists of KB highlights, both simple and more elaborate** from the Wikidata query service: 

   a) *[Simple list](https://w.wiki/3FWz)*, using this query:

```sparql
# Simple list of KB collection highlights 
SELECT DISTINCT ?highlight ?highlightLabel ?highlightDescription
WHERE {
  # the thing is part of the KB collection, and has role 'collection highlight' within that collection
  ?highlight (p:P195/ps:P195) wd:Q1526131; p:P195 [pq:P2868 wd:Q29188408]. 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?highlightLabel
```
<sub>*[Try it](https://w.wiki/3FWz) in the Wikidata query service*</sub>

It results into a [simple list](https://w.wiki/3FW$) of KB collection highlights, with the names, labels and descriptions in English.

<kbd><img src="images/image-p5-003.png" width="100%"/></kbd><br/><sub>*Result of the query, a [simple list](https://w.wiki/3FW$) of KB collection highlights, with the names, labels and descriptions in English. Screenshots Wikidata query service d.d. 28-04-2021*</sub>

You can also request the [result as JSON](https://query.wikidata.org/sparql?query=%23%20Simple%20list%20of%20KB%20collection%20highlights%20%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3FhighlightDescription%0AWHERE%20%7B%0A%20%20%23%20the%20thing%20is%20part%20of%20the%20KB%20collection%2C%20and%20has%20role%20'collection%20highlight'%20within%20that%20collection%0A%20%20%3Fhighlight%20(p%3AP195%2Fps%3AP195)%20wd%3AQ1526131%3B%20p%3AP195%20%5Bpq%3AP2868%20wd%3AQ29188408%5D.%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%0AORDER%20BY%20%3FhighlightLabel&format=json) and as an [XML download](https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%23%20Simple%20list%20of%20KB%20collection%20highlights%20%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3FhighlightDescription%0AWHERE%20%7B%0A%20%20%23%20the%20thing%20is%20part%20of%20the%20KB%20collection%2C%20and%20has%20role%20'collection%20highlight'%20within%20that%20collection%0A%20%20%3Fhighlight%20(p%3AP195%2Fps%3AP195)%20wd%3AQ1526131%3B%20p%3AP195%20%5Bpq%3AP2868%20wd%3AQ29188408%5D.%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%0AORDER%20BY%20%3FhighlightLabel)

   b) *[Elaborate list](https://w.wiki/3FXe)*, recreating the [overview table of KB collection highlights](https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken/Listeria) from [Part 2](Part%202%2C%20Overviews%20of%20all%20highlights.html) via SPARQL 

<kbd><img src="images/image-p5-004.png" height="220"/></kbd><kbd><img src="images/image-p5-005.png" height="220"/></kbd><br/>
<sub>*Left: [SPARQL query](https://w.wiki/3FXe) to create an elaborate list of KB collection highlights. Right: Result of the query, an [elaborate list](https://w.wiki/3FXg) of KB collection highlights. Please note the results have not been aggregated by the [GROUP_CONCAT function](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial#Aggregate_functions_summary), hence the higher number of results compared to the simple query. Screenshots Wikidata query service d.d. 28-04-2021*</sub>

You can also request the [result as JSON](https://query.wikidata.org/sparql?query=%23%20Elaborated%20list%20of%20KB%20collection%20highlights%2C%20recreating%0A%23%20https%3A%2F%2Fnl.wikipedia.org%2Fwiki%2FWikipedia%3AGLAM%2FKoninklijke_Bibliotheek_en_Nationaal_Archief%2FTopstukken%2FListeria%0A%23%20using%20SPARQL%0A%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3Ftitle%20%3FhighlightDescription%20%3Fimage%20%3FhighlightIsALabel%20%3FinventoryNr%20%0A%3Fkbcat%20%3Fkburl%20%3Fbrowsebook%20%3Fgallery%20%3FcopyrightLabel%20%0A%0AWHERE%20%7B%0A%20%20%3Fhighlight%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408.%0A%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP18%20%3Fimage.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP1476%20%3Ftitle.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP31%20%3FhighlightIsA.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP217%20%3FinventoryNr.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP528%20%3Fppn.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fresolver.kb.nl%2Fresolve%3Furn%3DPPN%3A%22%2C%3Fppn)%20AS%20%3Fkbcat).%7D%20%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP973%20%3Fkburl.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fkburl)%2C%20%22https%3A%2F%2Fwww.kb.nl%2Fthemas%2F%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP953%20%3Fbrowsebook.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fbrowsebook)%2C%20%22https%3A%2F%2Fgalerij.kb.nl%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP935%20%3Fgal.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2F%22%2CREPLACE(%3Fgal%2C%22%20%22%2C%22_%22))%20AS%20%3Fgallery).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP6216%20%3Fcopyright.%7D%0A%20%20%20%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%20ORDER%20BY%20%3FhighlightLabel%0A%0A%0A%0A%0A%0A%0A%0A&format=json) and as an [XML download](https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%23%20Elaborated%20list%20of%20KB%20collection%20highlights%2C%20recreating%0A%23%20https%3A%2F%2Fnl.wikipedia.org%2Fwiki%2FWikipedia%3AGLAM%2FKoninklijke_Bibliotheek_en_Nationaal_Archief%2FTopstukken%2FListeria%0A%23%20using%20SPARQL%0A%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3Ftitle%20%3FhighlightDescription%20%3Fimage%20%3FhighlightIsALabel%20%3FinventoryNr%20%0A%3Fkbcat%20%3Fkburl%20%3Fbrowsebook%20%3Fgallery%20%3FcopyrightLabel%20%0A%0AWHERE%20%7B%0A%20%20%3Fhighlight%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408.%0A%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP18%20%3Fimage.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP1476%20%3Ftitle.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP31%20%3FhighlightIsA.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP217%20%3FinventoryNr.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP528%20%3Fppn.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fresolver.kb.nl%2Fresolve%3Furn%3DPPN%3A%22%2C%3Fppn)%20AS%20%3Fkbcat).%7D%20%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP973%20%3Fkburl.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fkburl)%2C%20%22https%3A%2F%2Fwww.kb.nl%2Fthemas%2F%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP953%20%3Fbrowsebook.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fbrowsebook)%2C%20%22https%3A%2F%2Fgalerij.kb.nl%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP935%20%3Fgal.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2F%22%2CREPLACE(%3Fgal%2C%22%20%22%2C%22_%22))%20AS%20%3Fgallery).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP6216%20%3Fcopyright.%7D%0A%20%20%20%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%20ORDER%20BY%20%3FhighlightLabel%0A%0A%0A%0A%0A%0A%0A%0A)

  <kbd><img src="images/image-p5-006.png" height="400"/></kbd><kbd><img src="images/image-p5-007.png" height="400"/></kbd><br/>
  <sub>*Left: JSON result of the query. Right: XML result of the query. Screenshots Wikidata query service d.d. 28-04-2021*</sub>

40) You might want to **programatically check for Wikipedia articles about KB highlights** [in Dutch](https://w.wiki/3FbF), using this query:

```sparql
#Articles about KB collection highlights on Dutch Wikipedia
select ?item ?itemLabel ?articleNL where {
  ?item (p:P195/ps:P195) wd:Q1526131; p:P195 [pq:P2868 wd:Q29188408]. 
  OPTIONAL {
    ?articleNL schema:about ?item.
    ?articleNL schema:isPartOf <https://nl.wikipedia.org/>.
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,nl". }
}
```
<sub>*[Try it](https://w.wiki/3FbF) in the Wikidata query service*</sub>

As before, the results are available in [JSON](https://query.wikidata.org/sparql?query=%23Articles%20about%20KB%20collection%20highlights%20on%20Dutch%20Wikipedia%0Aselect%20%3Fitem%20%3FitemLabel%20%3FarticleNL%20where%20%7B%0A%20%20%3Fitem%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408%20.%0A%20%20OPTIONAL%20%7B%0A%20%20%20%20%3FarticleNL%20schema%3Aabout%20%3Fitem.%0A%20%20%20%20%3FarticleNL%20schema%3AisPartOf%20%3Chttps%3A%2F%2Fnl.wikipedia.org%2F%3E.%0A%20%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%2Cnl%22.%20%7D%0A%7D%0A%0A%0A%0A%0A%0A%0A&format=json) and [in XML](https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%23Articles%20about%20KB%20collection%20highlights%20on%20Dutch%20Wikipedia%0Aselect%20%3Fitem%20%3FitemLabel%20%3FarticleNL%20where%20%7B%0A%20%20%3Fitem%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408%20.%0A%20%20OPTIONAL%20%7B%0A%20%20%20%20%3FarticleNL%20schema%3Aabout%20%3Fitem.%0A%20%20%20%20%3FarticleNL%20schema%3AisPartOf%20%3Chttps%3A%2F%2Fnl.wikipedia.org%2F%3E.%0A%20%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%2Cnl%22.%20%7D%0A%7D%0A%0A%0A%0A%0A%0A%0A)

## Reuse - individual highlights

Wikimedia Commons API documentation:
https://commons.wikimedia.org/w/api.php?action=help&modules=main - General, with 
https://commons.wikimedia.org/w/api.php?action=help&modules=query - Fetch data from and about Wikimedia Commons. Mostly used, with here some 
https://commons.wikimedia.org/wiki/Commons:API/MediaWiki - Examples of using the MediaWiki API to request Commons content. 

=============================================================
41) Request the images from [Armorial de Beyeren](https://commons.wikimedia.org/wiki/Category:Armorial_de_Beyeren) as a JSON/XML file

a) Shoert list, names only
as json 
* https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmtitle=Category:Armorial%20de%20Beyeren&format=json&gcmnamespace=6
* https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmtitle=Category%3ADe+Nieuwe+Rijschool&format=json&gcmnamespace=6

as xml 
* https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmtitle=Category:Armorial%20de%20Beyeren&format=xml&gcmnamespace=6
* https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmtitle=Category:De%20Nieuwe%20Rijschool&format=xml&gcmnamespace=6

b) Longer lists, URLs
Request URLS: List of file titles, file page URLs and direct image URLs (json, via Commons API)
* https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Reward%20letter%20of%20King%20Filip%20II%20of%20Spain%20to%20family%20of%20Balthasar%20Gerards,%201590&gcmlimit=500&gcmtype=file&prop=imageinfo&iiprop=url&format=json
* https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Reward%20letter%20of%20King%20Filip%20II%20of%20Spain%20to%20family%20of%20Balthasar%20Gerards,%201590&gcmlimit=500&gcmtype=file&prop=imageinfo&iiprop=url&format=xml

* https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Album_amicorum_van_Jacobus_Heyblocq&gcmlimit=500&gcmtype=file&prop=imageinfo&iiprop=url&format=json
* https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Album_amicorum_van_Jacobus_Heyblocq&gcmlimit=500&gcmtype=file&prop=imageinfo&iiprop=url&format=xml

=============================================================
42) Dingen afgebeeld in Atlas de Wit - via WMC sparql
https://tinyurl.com/yzp3xy8l
https://wcqs-beta.wmflabs.org/sparql?query=SELECT%20%3Ffile%20(GROUP_CONCAT(DISTINCT%20%3FdepictionLabel%20%3B%20separator%20%3D%20%22%20--%20%22)%20as%20%3FThingsDepicted)%0AWHERE%20%7b%0A%20%20%3Ffile%20wdt%3AP6243%20wd%3AQ2520345%20.%0A%20%20%3Ffile%20wdt%3AP180%20%3Fdepiction%20.%0A%20%20SERVICE%20%3Chttps%3A%2F%2Fquery.wikidata.org%2Fsparql%3E%20%7b%20%20%0A%20%20%20%20SERVICE%20wikibase%3Alabel%20%7b%0A%20%20%20%20%20%20%20%20bd%3AserviceParam%20wikibase%3Alanguage%20%22nl%22%20.%0A%20%20%20%20%20%20%20%20%3Fdepiction%20rdfs%3Alabel%20%3FdepictionLabel.%0A%20%20%20%20%20%20%20%20%3Ffile%20rdfs%3Alabel%20%3FfileLabel.%0A%20%20%20%20%7d%0A%20%20%7d%0A%7d%0AGROUP%20BY%20%3Ffile&format=json

#Captions of files depicting roses
SELECT ?file ?fileLabel WHERE {
  ?file wdt:P180 wd:Q80973 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}

=============================================================
43) Embedded AAJH contributos gallerey in KB website
https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken/Hergebruik/Voorbeelden/Smoelenboek_bijdragers_AAJH#Vormgeving_kb.nl

=====================================================
44)Requrst which WP aricles (in all langiages) are avialable for a given highlightd, in json
https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q42&props=sitelinks

=======================================================
45) De kenmerken van elke topstukk opvragen in xml, rdf, json

For cases in which it is inconvenient to use content negotiation (e.g. to view non-HTML content in a web browser), you can also access data about an entity in a specific format by extending the data URL with an extension suffix to indicate the content format that you want, such as .json, .rdf, .ttl, .nt or .jsonld. For example, https://www.wikidata.org/wiki/Special:EntityData/Q42.json 
https://www.wikidata.org/wiki/Special:EntityData/Q5.json
https://www.wikidata.org/wiki/Special:EntityData/Q1018644
https://www.wikidata.org/wiki/Special:EntityData/Q1018644.rdf

https://www.wikidata.org/w/api.php?action=help&modules=wbgetentities
https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q372|Q44&format=json
https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q372&format=xml

========================================
46) Een overicht opvragen in XML bij de Topstrukken betrokken entiteien:  (makers, bijdragers, vertalers, uitgevers, drukkers, illustratoren, eigenaren 

==============================
47) Examples of **Python scripts** to request & process highlight data
https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken/Hergebruik/Wikidata

==============================
48) linjkngto eexternal identfiers – europeana, rkd… AAJH

==============================

## Reuse - individual highlight images

==================================================
49) SDoC Dingen afgebeeld in 1 bepaald bestand uit Atlas de Wit - via WMC api: 
https://commons.wikimedia.org/wiki/Commons:Depicts#Access

===================================
50) https://tools.wmflabs.org/magnus-toolserver/commonsapi.php - request image info

https://tools.wmflabs.org/magnus-toolserver/commonsapi.php?image=Album%20amicorum%20Jacob%20Heyblocq%20KB131H26%20-%20p010%20-%20Franciscus%20Snellinx%20-%20Poem%20part2.jpg&thumbwidth=150&thumbheight=150&versions&meta&format=json
https://commons.wikimedia.org/w/api.php?action=query&titles=Image:Album%20amicorum%20Jacob%20Heyblocq%20KB131H26%20-%20p010%20-%20Franciscus%20Snellinx%20-%20Poem%20part2.jpg&prop=imageinfo&iiprop=extmetadata

## Summary
OK, that's it for this fifth and last article.  For convenience and overview, let me summarize all the cool new things for KB's collection highlights we have seen in this article:

38) A [SPARQL driven thumbnail gallery](https://w.wiki/3E8z) of KB highlights<br/>
39) Structured lists of all KB highlights, both [simple](https://w.wiki/3FWz) and [more elaborate](https://w.wiki/3FXe) in [JSON](https://query.wikidata.org/sparql?query=%23%20Elaborated%20list%20of%20KB%20collection%20highlights%2C%20recreating%0A%23%20https%3A%2F%2Fnl.wikipedia.org%2Fwiki%2FWikipedia%3AGLAM%2FKoninklijke_Bibliotheek_en_Nationaal_Archief%2FTopstukken%2FListeria%0A%23%20using%20SPARQL%0A%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3Ftitle%20%3FhighlightDescription%20%3Fimage%20%3FhighlightIsALabel%20%3FinventoryNr%20%0A%3Fkbcat%20%3Fkburl%20%3Fbrowsebook%20%3Fgallery%20%3FcopyrightLabel%20%0A%0AWHERE%20%7B%0A%20%20%3Fhighlight%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408.%0A%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP18%20%3Fimage.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP1476%20%3Ftitle.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP31%20%3FhighlightIsA.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP217%20%3FinventoryNr.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP528%20%3Fppn.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fresolver.kb.nl%2Fresolve%3Furn%3DPPN%3A%22%2C%3Fppn)%20AS%20%3Fkbcat).%7D%20%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP973%20%3Fkburl.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fkburl)%2C%20%22https%3A%2F%2Fwww.kb.nl%2Fthemas%2F%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP953%20%3Fbrowsebook.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fbrowsebook)%2C%20%22https%3A%2F%2Fgalerij.kb.nl%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP935%20%3Fgal.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2F%22%2CREPLACE(%3Fgal%2C%22%20%22%2C%22_%22))%20AS%20%3Fgallery).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP6216%20%3Fcopyright.%7D%0A%20%20%20%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%20ORDER%20BY%20%3FhighlightLabel%0A%0A%0A%0A%0A%0A%0A%0A&format=json) and [XML](https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%23%20Simple%20list%20of%20KB%20collection%20highlights%20%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3FhighlightDescription%0AWHERE%20%7B%0A%20%20%23%20the%20thing%20is%20part%20of%20the%20KB%20collection%2C%20and%20has%20role%20'collection%20highlight'%20within%20that%20collection%0A%20%20%3Fhighlight%20(p%3AP195%2Fps%3AP195)%20wd%3AQ1526131%3B%20p%3AP195%20%5Bpq%3AP2868%20wd%3AQ29188408%5D.%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%0AORDER%20BY%20%3FhighlightLabel)<br/>
40) Programatically check for [Wikipedia articles about KB highlights in Dutch](https://w.wiki/3FbF)<br/>
41) <br/>
42) <br/>
43) <br/>
44) <br/>
45) <br/>
46) <br/>
47) <br/>
48) <br/>
49) <br/>
50) <br/>

## Summary of summaries
As a bonus, amd for overview., part 6 is a summary of all 50 new cool things


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

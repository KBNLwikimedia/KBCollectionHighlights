![Banner](../images/banners/KBTopstukkenBannerWikimedia_EN.jpg)
# 50 cool new things you can now do with KB's collection highlights - Part 5, Reuse

<img src="images/KBtopstukkenMemeEN.jpg" width="70%" align="right"/>

*In this [series of 5 articles](index.md) I show the added value of putting images and metadata of [digitised collection highlights](https://www.kb.nl/galerij/digitale-topstukken) of the KB, national library of the Netherlands, into the Wikimedia infrastructure. By putting our collection highlights into Wikidata, Wikimedia Commons and Wikipedia, dozens of new functionalities have been added. As a result of Wikifying this collection, you can now do things with these highlights that were not possible before.*

In the previous (fourth) part of this series I discussed 11 tools of the right hand knife. We looked at [which new functionalities](Part%204%2C%20Images.html) have become available for individual highlight images. We talked about the ability to download images in multiple resolutions, [file level descriptive metadata](https://commons.wikimedia.org/wiki/File:Atlas_Van_der_Hagen-KW1049B12_002-HISPANIAE_ET_PORTUGALIAE_REGNA.jpeg#Summary) with manifest attributions and copyrights status, geo coordinates linking images to [various map services](https://geohack.toolforge.org/geohack.php?pagename=File:Den_Haag,_gezicht_bij_de_Doelen_over_de_Korte_Vijverberg,_tot_aan_het_Plein_(7985085070).jpg&params=052.081352_N_0004.313528_E_globe:Earth_type:camera_source:Flickr_&language=nl), [linking images to Wikidata](https://commons.wikimedia.org/wiki/Commons:Structured_data), as well as enabling [multilingual search by content](https://hay.toolforge.org/sdsearch/#q=incategory:%22Media%20contributed%20by%20Koninklijke%20Bibliotheek%22%20haswbstatement:P180) (*What is depicted in the images?*)

In this fifth part I am going to unfold the last group of tools. I am going to illustrate how you can *reuse KB's collection highlights outside of the Wikimedia context*, that is, for/in your own websites, services, apps, hackathons and projects. I'm going to talk about SPARQL, APIs, Python scripts, data dumps and machine interactions with our highlights. Cool LEGO Technic® blocks for KB's target group of developers, app builders, digital humanists, data scientists, LOD afficionados and other nice nerds. 

<kbd><img src="images/image-p1-024.png" height="200"/></kbd><kbd><img src="images/image-p1-020.png" height="200"/></kbd><kbd><img src="images/image-p1-025.png" height="200"/></kbd>

I'll try to follow the same order as in [Part 2](Part%202%2C%20Overviews%20of%20all%20highlights.html) , [3](Part%203%2C%20Overviews%20per%20highlight.html) and [4](Part%204%2C%20Images.html), so 
* all highlights together
* indivudual highlights
* individual highlight images.

I'll illustrate how you can retrieve the same images, data and texts we requested via the GUI (so in HTML) in these previous parts, but now in their raw, machine readable formats (JSON, XML etc.) using Wikimedia's APIs and SPARQL services. This will give you more control & flexibilty over the exact outputs, custom made for your needs.

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
This query results into a **[SPARQL driven thumbnail gallery](https://w.wiki/3E8z)** of KB highlights.

 <kbd><img src="images/image-p5-002.png" width="100%"/></kbd><br/><sub>*The [image grid](https://w.wiki/3E8z) of KB highlights for the above SPARQL query. Screenshot Wikidata query service d.d. 23-04-2021*</sub>

39) Next, let's look at lists and tables. The [list of highlights](https://www.kb.nl/galerij/digitale-topstukken) on the KB website is only availabe as HTML. For effective reuse you'd prefer it in a structured and open format such as JSON, XML or RDF. Let's look how we can request **structured lists of KB highlights, both simple and more elaborate** from the Wikidata query service: 

- *Simple list*, using [this query](https://w.wiki/3FWz):
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
  It results into a [simple list](https://w.wiki/3FW$) of KB collection highlights, with the names, labels and descriptions in English.

  <kbd><img src="images/image-p5-003.png" width="100%"/></kbd><br/><sub>*Result of the query, a [simple list](https://w.wiki/3FW$) of KB collection highlights, with the names, labels and descriptions in English. Screenshots Wikidata query service d.d. 28-04-2021*</sub>

  You can request the [result as JSON](https://query.wikidata.org/sparql?query=%23%20Simple%20list%20of%20KB%20collection%20highlights%20%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3FhighlightDescription%0AWHERE%20%7B%0A%20%20%23%20the%20thing%20is%20part%20of%20the%20KB%20collection%2C%20and%20has%20role%20'collection%20highlight'%20within%20that%20collection%0A%20%20%3Fhighlight%20(p%3AP195%2Fps%3AP195)%20wd%3AQ1526131%3B%20p%3AP195%20%5Bpq%3AP2868%20wd%3AQ29188408%5D.%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%0AORDER%20BY%20%3FhighlightLabel&format=json) and as an [XML download](https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%23%20Simple%20list%20of%20KB%20collection%20highlights%20%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3FhighlightDescription%0AWHERE%20%7B%0A%20%20%23%20the%20thing%20is%20part%20of%20the%20KB%20collection%2C%20and%20has%20role%20'collection%20highlight'%20within%20that%20collection%0A%20%20%3Fhighlight%20(p%3AP195%2Fps%3AP195)%20wd%3AQ1526131%3B%20p%3AP195%20%5Bpq%3AP2868%20wd%3AQ29188408%5D.%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%0AORDER%20BY%20%3FhighlightLabel) as well.

-  *Elaborate list*, recreating the [overview table of KB collection highlights](https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken/Listeria) from [Part 2](Part%202%2C%20Overviews%20of%20all%20highlights.html) via [this SPARQL query](https://w.wiki/3FXe): 

   <kbd><img src="images/image-p5-004.png" height="210"/></kbd><kbd><img src="images/image-p5-005.png" height="210"/></kbd><br/><sub>*Left: [SPARQL query](https://w.wiki/3FXe) to create an elaborate list of KB collection highlights. Right: Result of the query, an [elaborate list](https://w.wiki/3FXg) of KB collection highlights. Please note the results have not been aggregated by the [GROUP_CONCAT function](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial#Aggregate_functions_summary), hence the higher number of results compared to the simple query. Screenshots Wikidata query service d.d. 28-04-2021*</sub>

   You can also request the [result as JSON](https://query.wikidata.org/sparql?query=%23%20Elaborated%20list%20of%20KB%20collection%20highlights%2C%20recreating%0A%23%20https%3A%2F%2Fnl.wikipedia.org%2Fwiki%2FWikipedia%3AGLAM%2FKoninklijke_Bibliotheek_en_Nationaal_Archief%2FTopstukken%2FListeria%0A%23%20using%20SPARQL%0A%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3Ftitle%20%3FhighlightDescription%20%3Fimage%20%3FhighlightIsALabel%20%3FinventoryNr%20%0A%3Fkbcat%20%3Fkburl%20%3Fbrowsebook%20%3Fgallery%20%3FcopyrightLabel%20%0A%0AWHERE%20%7B%0A%20%20%3Fhighlight%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408.%0A%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP18%20%3Fimage.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP1476%20%3Ftitle.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP31%20%3FhighlightIsA.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP217%20%3FinventoryNr.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP528%20%3Fppn.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fresolver.kb.nl%2Fresolve%3Furn%3DPPN%3A%22%2C%3Fppn)%20AS%20%3Fkbcat).%7D%20%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP973%20%3Fkburl.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fkburl)%2C%20%22https%3A%2F%2Fwww.kb.nl%2Fthemas%2F%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP953%20%3Fbrowsebook.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fbrowsebook)%2C%20%22https%3A%2F%2Fgalerij.kb.nl%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP935%20%3Fgal.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2F%22%2CREPLACE(%3Fgal%2C%22%20%22%2C%22_%22))%20AS%20%3Fgallery).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP6216%20%3Fcopyright.%7D%0A%20%20%20%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%20ORDER%20BY%20%3FhighlightLabel%0A%0A%0A%0A%0A%0A%0A%0A&format=json) and as an [XML download](https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%23%20Elaborated%20list%20of%20KB%20collection%20highlights%2C%20recreating%0A%23%20https%3A%2F%2Fnl.wikipedia.org%2Fwiki%2FWikipedia%3AGLAM%2FKoninklijke_Bibliotheek_en_Nationaal_Archief%2FTopstukken%2FListeria%0A%23%20using%20SPARQL%0A%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3Ftitle%20%3FhighlightDescription%20%3Fimage%20%3FhighlightIsALabel%20%3FinventoryNr%20%0A%3Fkbcat%20%3Fkburl%20%3Fbrowsebook%20%3Fgallery%20%3FcopyrightLabel%20%0A%0AWHERE%20%7B%0A%20%20%3Fhighlight%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408.%0A%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP18%20%3Fimage.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP1476%20%3Ftitle.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP31%20%3FhighlightIsA.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP217%20%3FinventoryNr.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP528%20%3Fppn.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fresolver.kb.nl%2Fresolve%3Furn%3DPPN.%3A%22%2C%3Fppn)%20AS%20%3Fkbcat).%7D%20%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP973%20%3Fkburl.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fkburl)%2C%20%22https%3A%2F%2Fwww.kb.nl%2Fthemas%2F%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP953%20%3Fbrowsebook.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fbrowsebook)%2C%20%22https%3A%2F%2Fgalerij.kb.nl%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP935%20%3Fgal.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2F%22%2CREPLACE(%3Fgal%2C%22%20%22%2C%22_%22))%20AS%20%3Fgallery).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP6216%20%3Fcopyright.%7D%0A%20%20%20%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%20ORDER%20BY%20%3FhighlightLabel%0A%0A%0A%0A%0A%0A%0A%0A).

    <kbd><img src="images/image-p5-006.png" height="400"/></kbd><kbd><img src="images/image-p5-007.png" height="400"/></kbd><br/><sub>*Left: JSON result of the query. Right: XML result of the query. Screenshots Wikidata query service d.d. 28-04-2021*</sub>

40) You might want to **programatically check for Wikipedia articles about KB highlights**, for instance in Dutch, using [this query](https://w.wiki/3FbF):
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
As before, the results can be requested in [JSON](https://query.wikidata.org/sparql?query=%23Articles%20about%20KB%20collection%20highlights%20on%20Dutch%20Wikipedia%0Aselect%20%3Fitem%20%3FitemLabel%20%3FarticleNL%20where%20%7B%0A%20%20%3Fitem%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408%20.%0A%20%20OPTIONAL%20%7B%0A%20%20%20%20%3FarticleNL%20schema%3Aabout%20%3Fitem.%0A%20%20%20%20%3FarticleNL%20schema%3AisPartOf%20%3Chttps%3A%2F%2Fnl.wikipedia.org%2F%3E.%0A%20%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%2Cnl%22.%20%7D%0A%7D%0A%0A%0A%0A%0A%0A%0A&format=json) and [in XML](https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%23Articles%20about%20KB%20collection%20highlights%20on%20Dutch%20Wikipedia%0Aselect%20%3Fitem%20%3FitemLabel%20%3FarticleNL%20where%20%7B%0A%20%20%3Fitem%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408%20.%0A%20%20OPTIONAL%20%7B%0A%20%20%20%20%3FarticleNL%20schema%3Aabout%20%3Fitem.%0A%20%20%20%20%3FarticleNL%20schema%3AisPartOf%20%3Chttps%3A%2F%2Fnl.wikipedia.org%2F%3E.%0A%20%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%2Cnl%22.%20%7D%0A%7D%0A%0A%0A%0A%0A%0A%0A) as well.

## Reuse - individual highlights

41) In [Part 3](Part%203%2C%20Overviews%20per%20highlight.html) we looked at individual pages (14), double page openings (15) and miniatures/page details (16) that are available for public domain highlights. Let's see how we can **request image URLs from the [Wikimedia Commons query API](https://commons.wikimedia.org/w/api.php?action=help&modules=query)** using [this documentation](https://www.mediawiki.org/wiki/API:Categorymembers).

- **Individual pages**<br/> 
  For [Armorial de Beyeren](https://commons.wikimedia.org/wiki/Category:Armorial_de_Beyeren) we can request a simple list of images
  - in JSON: [https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmtitle=Category:Armorial%20de%20Beyeren&*format=json&gcmnamespace=6*](https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmtitle=Category:Armorial%20de%20Beyeren&format=json&gcmnamespace=6) and 
  - in XML: [https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmtitle=Category:Armorial%20de%20Beyeren&*format=xml&gcmnamespace=6*](https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmtitle=Category:Armorial%20de%20Beyeren&format=xml&gcmnamespace=6). 

  Here we are filtering on [namespace=6](https://commons.wikimedia.org/wiki/Help:Namespaces#Standard_Namespaces) (ns=6), so we are looking for files only (ie. no categories (ns=14) or galleries (ns=0)).   

  <kbd><img src="images/image-p5-008.png" width="100%"/></kbd><br/><sub>*XML list of files from [Armorial de Beyeren](https://commons.wikimedia.org/wiki/Category:Armorial_de_Beyeren) using [this API call](https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmtitle=Category:Armorial%20de%20Beyeren&format=xml&gcmnamespace=6). Screenshot Wikimedia Commons API, d.d. 29-04-2021*</sub>

- **Double page openings**<br/> 
  The downside of the above reponses is that they do not contain URLs (starting with https://), but only Wikimedia Commons file names. To request https URLs we need to modify our API call. When we apply the modified call to the [double page openings of Visboek Coenen](https://commons.wikimedia.org/wiki/Category:Visboeck_Coenen_(openings)), 

  [https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Visboeck_Coenen_(openings)&gcmlimit=500&gcmtype=file&prop=imageinfo&iiprop=url&format=xml](https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Visboeck_Coenen_(openings)&gcmlimit=500&gcmtype=file&prop=imageinfo&iiprop=url&format=xml)

  we get this XML reponse

  <kbd><img src="images/image-p5-009.png" width="100%"/></kbd><br/><sub>*XML reponse containing https URLs to the [double page openings of Visboek Coenen](https://commons.wikimedia.org/wiki/Category:Visboeck_Coenen_(openings)) using [this API call](https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Visboeck_Coenen_(openings)&gcmlimit=500&gcmtype=file&prop=imageinfo&iiprop=url&format=xml). Screenshot Wikimedia Commons API, d.d. 29-04-2021*</sub>

  Please note that this reponse contains both direct URLs to the hires images ([example](https://upload.wikimedia.org/wikipedia/commons/e/ed/Adriaen_Coenen%27s_Visboeck_-_KB_78_E_54_-_Folio_001r.jpg)), as well as two forms of URLs to the Wikimedia Commons files page ([example](https://commons.wikimedia.org/wiki/File:Adriaen_Coenen%27s_Visboeck_-_KB_78_E_54_-_Folio_001r.jpg)).
  
- **Miniatures and page details**<br/>
  Besides calling the API by a URL query string (as done above), it is also possible to do this via a Python script. For instance, we can request the [miniatures](https://commons.wikimedia.org/wiki/Category:Chroniques_de_Froissart,_vol_1_-_Den_Haag,_KB_:_72_A_25_(details)) from [Chroniques de Froissart](https://commons.wikimedia.org/wiki/Category:Chroniques_de_Froissart,_vol_1_-_Den_Haag,_KB_:_72_A_25_(c.1410)):

```python
	#!/usr/bin/python3
	import requests, json
	S = requests.Session()
	URL = "https://commons.wikimedia.org/w/api.php"
	PARAMS = {
	   "action": "query",
	   "gcmtitle":"Category:Chroniques_de_Froissart,_vol_1_-_Den_Haag,_KB_:_72_A_25_(details)",
	   "gcmlimit":"500",
	   "generator":"categorymembers",
	   "format":"json",
	   "gcmtype":"file",
	   "prop":"imageinfo",
	   "iiprop":"url"
	}
	R = S.get(url=URL, params=PARAMS)
	DATA = R.json()
	PAGES = DATA['query']['pages']
	print(json.dumps(PAGES, indent=2))
```
  Running this script in my [Python IDE](https://www.jetbrains.com/pycharm/) gives the following output: 

  <kbd><img src="images/image-p5-010.png" width="100%"/></kbd><br/><sub>*Titles and URLs of [miniatures](https://commons.wikimedia.org/wiki/Category:Chroniques_de_Froissart,_vol_1_-_Den_Haag,_KB_:_72_A_25_(details)) from [Chroniques de Froissart](https://commons.wikimedia.org/wiki/Category:Chroniques_de_Froissart,_vol_1_-_Den_Haag,_KB_:_72_A_25_(c.1410)) formatted as JSON. Screenshot [Pycharm IDE](https://www.jetbrains.com/pycharm/), d.d. 29-04-2021*</sub>

42) Every KB highlight is described by a Wikidata item (Qnumber). Let's see how we can request **highlight information from the Wikidata API** directly from that Qnumber. We can use the [*wbgetentities* action](https://www.wikidata.org/w/api.php?action=help&modules=wbgetentities) for that.

* Get *all information* ('the entire Qnumber') from the [Beatrijs manuscript](https://www.wikidata.org/wiki/Q1929931) (Q1929931) in all available languages, as JSON: [https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q1929931](https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q1929931)

* Get *only the labels* of the [Egmond Gospels](https://www.wikidata.org/wiki/Q759256) (Q759256) in all available languages, as XML: [https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q759256&props=labels&format=xml](https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q759256&props=labels&format=xml) 

  <kbd><img src="images/image-p5-011.png" width="100%"/></kbd><br/><sub>*Comparison between the multilingual labeling of the Egmond Gospels (Q759256) from the [Wikidata web interface](https://www.wikidata.org/wiki/Q759256) and from the [Wikidata API](https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q759256&props=labels&format=xml). Screenshot Wikidata GUI & Wikidata API, d.d. 30-04-2021*</sub>

* Get the *aliases* of [Atlas Ortelius 1571](https://www.wikidata.org/wiki/Q67465742) (Q67465742) in German, Czech, Polish and Ukrainian, as JSON: [https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q67465742&props=aliases&languages=de%7Ccs%7Cpl%7Cuk&format=json](https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q67465742&props=aliases&languages=de%7Ccs%7Cpl%7Cuk&format=json)

* Get the *Wikipedia articles* for both [Liber Pantegni](https://www.wikidata.org/wiki/Q748421) (Q748421) and the [Beyeren armorial](https://www.wikidata.org/wiki/Q3372028) (Q3372028) in all available languages, as XML: [https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q748421%7CQ3372028&props=sitelinks&format=xml](https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q748421%7CQ3372028&props=sitelinks&format=xml)

43) An alternative way is to **request full Wikidata items directly from the Qnumber via a [Special:EntityData](https://www.mediawiki.org/wiki/Wikibase/EntityData) URL.** The ouput can be obtained in no fewer than seven different formats:

 - Get all information from the [Haags liederenhandschrift](https://www.wikidata.org/wiki/Q16641064) (Q16641064, *The Hague song manuscript*) as HTML: [https://www.wikidata.org/wiki/Special:EntityData/Q16641064](https://www.wikidata.org/wiki/Special:EntityData/Q16641064). This uses [content negotiation](https://en.wikipedia.org/wiki/content_negotiation) to return HTML in your browser. 
 - If you don't want to depend on content negotiation (e.g. view non-HTML content in a web browser), you can actively request alternative formats by appendig a *format suffix* to the URL, eg. to retrieve JSON: [https://www.wikidata.org/wiki/Special:EntityData/Q16641064.json](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.json). 
 - Other available formats are [JSON-LD](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.jsonld), [RDF](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.rdf), [NT](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.nt), [TTL or N3](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.ttl) and [PHP](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.php). 
 - Equivalant URLs for these requests use the *format argument*, e.g. : [Special:EntityData?id=Q16641064](https://www.wikidata.org/wiki/Special:EntityData?id=Q16641064&format=rdf)[*&format=rdf*](https://www.wikidata.org/wiki/Special:EntityData?id=Q16641064&format=rdf).

    <kbd><img src="images/image-p5-012.png" width="66%"/></kbd><br/><sub>*Seven different output formats for the [Special:EntityData](https://www.mediawiki.org/wiki/Wikibase/EntityData) URL for the [Haags liederenhandschrift](https://www.wikidata.org/wiki/Q16641064) (Q16641064): [HTML](https://www.wikidata.org/wiki/Special:EntityData/Q16641064), [JSON](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.json), [JSON-LD](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.jsonld), [RDF](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.rdf), [NT](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.nt), [TTL or N3](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.ttl) and [PHP](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.php). Compilation of screenshot d.d. 03-05-2021*</sub>

For exploring the JSON response in further detail we can tweak [this Python script](https://gist.github.com/thisismattmiller/42c9d5981ee233c6288194af234ac6e4) that [Matt Miller](https://gist.github.com/thisismattmiller) from the Library of Congress explains in *[Demo: Programmatic Wikidata](https://www.youtube.com/watch?v=SzfC3KFqmPs)* from his YouTube series *[Programming for Cultural Heritage](https://www.youtube.com/playlist?list=PL9Oe03cT2WhwMsSZLsUg6ej-5imNzhgBX)*.

For instance, we can make a list of all Wikidata properties that are used in [Q16641064](https://www.wikidata.org/wiki/Q16641064)

```python
  import requests
  import json
  url = "https://www.wikidata.org/wiki/Special:EntityData/"
  qnumbers = ['Q16641064'] # Haags liederenhandschrift // The Hague song manuscript
  all_properties = {}
  for qnum in qnumbers:
      useurl = url + qnum + '.json'
      headers = {
  	'Accept' : 'application/json',
  	'User-Agent': 'User OlafJanssen - Haags liederenhandschrift'
      }
      r = requests.get(useurl, headers=headers)
      data = json.loads(r.text)
      properties = list(data['entities'][qnum]['claims'].keys())
      print(properties)
```
returning a list in Python

```
  ['P31', 'P18', 'P195', 'P217', 'P571', 'P973', 'P953', 'P373', 'P5008', 'P276', 'P1476', 'P170', 'P127', 'P767', 'P291', 'P2670', 'P2048', 'P2049', 'P186', 'P1104', 'P935', 'P8791', 'P1343', 'P528', 'P6216', 'P2671']
```

If we modify the last couple of code lines into

```python
  .... # as previous
  data = json.loads(r.text)
  nlen= len(data['entities'][qnum]['claims']['P170'])
  for i in range(0, nlen):
      creatorid = data['entities'][qnum]['claims']['P170'][i]['mainsnak']['datavalue']['value']['id']
      creatorurl= "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + str(creatorid) + "&props=labels&languages=en&format=json"
      creatorresponse = requests.get(creatorurl, headers=headers)
      creatordata = json.loads(creatorresponse.text)
      print(str(i+1)+": "+creatordata['entities'][creatorid]['labels']['en']['value'])
```
we can retrieve the English names (labels) of the three creators ([P170](https://www.wikidata.org/wiki/Property:P170)) of this manuscript: 

```
  1: Noydekijn
  2: Augustijnken
  3: Freidank
```

========================================
44) Een overicht opvragen in XML bij een topstuk betrokken entiteien:  (makers, bijdragers, vertalers, uitgevers, drukkers, illustratoren, eigenaren 

=============================================================
43) Embedded AAJH contributos gallerey in KB website
https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken/Hergebruik/Voorbeelden/Smoelenboek_bijdragers_AAJH#Vormgeving_kb.nl

=============================================================
42) Dingen afgebeeld in Atlas de Wit - via WMC sparql
https://tinyurl.com/yzp3xy8l
https://wcqs-beta.wmflabs.org/sparql?query=SELECT%20%3Ffile%20(GROUP_CONCAT(DISTINCT%20%3FdepictionLabel%20%3B%20separator%20%3D%20%22%20--%20%22)%20as%20%3FThingsDepicted)%0AWHERE%20%7b%0A%20%20%3Ffile%20wdt%3AP6243%20wd%3AQ2520345%20.%0A%20%20%3Ffile%20wdt%3AP180%20%3Fdepiction%20.%0A%20%20SERVICE%20%3Chttps%3A%2F%2Fquery.wikidata.org%2Fsparql%3E%20%7b%20%20%0A%20%20%20%20SERVICE%20wikibase%3Alabel%20%7b%0A%20%20%20%20%20%20%20%20bd%3AserviceParam%20wikibase%3Alanguage%20%22nl%22%20.%0A%20%20%20%20%20%20%20%20%3Fdepiction%20rdfs%3Alabel%20%3FdepictionLabel.%0A%20%20%20%20%20%20%20%20%3Ffile%20rdfs%3Alabel%20%3FfileLabel.%0A%20%20%20%20%7d%0A%20%20%7d%0A%7d%0AGROUP%20BY%20%3Ffile&format=json

#Captions of files depicting roses
SELECT ?file ?fileLabel WHERE {
  ?file wdt:P180 wd:Q80973 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}


==============================
47) Examples of **Python scripts** to request & process highlight data
https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken/Hergebruik/Wikidata

```python
# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
endpoint_url = "https://query.wikidata.org/sparql"
query = """# Vind topstukken uit de collectie van de Koninklijke Bibliotheek Nederland
 SELECT DISTINCT ?topstuk ?topstukLabel 
 WHERE {
   # het ding is onderdeel van de collectie van de KB, en heeft daarbinnen de rol 'topstuk'
   ?topstuk (p:P195/ps:P195) wd:Q1526131; p:P195 [pq:P2868 wd:Q29188408]. 
   SERVICE wikibase:label { bd:serviceParam wikibase:language "nl". }
 }
 ORDER BY ?topstukLabel"""

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # User-Agent policy, see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

results = get_results(endpoint_url, query)
for result in results["results"]["bindings"]:
    print(result)
```
==============================
48) linjkngto eexternal identfiers – europeana, rkd… AAJH

==============================

## Reuse - individual highlight images

==================================================
49) SDoC Dingen afgebeeld in 1 bepaald bestand uit Atlas de Wit - via WMC api: 
https://commons.wikimedia.org/wiki/Commons:Depicts#Access

===================================
50) https://tools.wmflabs.org/magnus-toolserver/commonsapi.php - request image info

https://commons.wikimedia.org/wiki/Commons:API/MediaWiki

https://tools.wmflabs.org/magnus-toolserver/commonsapi.php?image=Album%20amicorum%20Jacob%20Heyblocq%20KB131H26%20-%20p010%20-%20Franciscus%20Snellinx%20-%20Poem%20part2.jpg&thumbwidth=150&thumbheight=150&versions&meta&format=json
https://commons.wikimedia.org/w/api.php?action=query&titles=Image:Album%20amicorum%20Jacob%20Heyblocq%20KB131H26%20-%20p010%20-%20Franciscus%20Snellinx%20-%20Poem%20part2.jpg&prop=imageinfo&iiprop=extmetadata

## Summary
OK, that's it for this fifth and last article.  For convenience and overview, let me summarize all the cool new things for KB's collection highlights we have seen in this article:

38) A [SPARQL driven thumbnail gallery](https://w.wiki/3E8z) of KB highlights<br/>
39) Structured lists of all KB highlights, both [simple](https://w.wiki/3FWz) and [more elaborate](https://w.wiki/3FXe) in [JSON](https://query.wikidata.org/sparql?query=%23%20Elaborated%20list%20of%20KB%20collection%20highlights%2C%20recreating%0A%23%20https%3A%2F%2Fnl.wikipedia.org%2Fwiki%2FWikipedia%3AGLAM%2FKoninklijke_Bibliotheek_en_Nationaal_Archief%2FTopstukken%2FListeria%0A%23%20using%20SPARQL%0A%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3Ftitle%20%3FhighlightDescription%20%3Fimage%20%3FhighlightIsALabel%20%3FinventoryNr%20%0A%3Fkbcat%20%3Fkburl%20%3Fbrowsebook%20%3Fgallery%20%3FcopyrightLabel%20%0A%0AWHERE%20%7B%0A%20%20%3Fhighlight%20p%3AP195%20%3Fst%20.%0A%20%20%3Fst%20ps%3AP195%20wd%3AQ1526131%20.%0A%20%20%3Fst%20pq%3AP2868%20wd%3AQ29188408.%0A%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP18%20%3Fimage.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP1476%20%3Ftitle.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP31%20%3FhighlightIsA.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP217%20%3FinventoryNr.%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP528%20%3Fppn.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fresolver.kb.nl%2Fresolve%3Furn%3DPPN%3A%22%2C%3Fppn)%20AS%20%3Fkbcat).%7D%20%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP973%20%3Fkburl.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fkburl)%2C%20%22https%3A%2F%2Fwww.kb.nl%2Fthemas%2F%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP953%20%3Fbrowsebook.%0A%20%20%20%20%20FILTER(STRSTARTS(STR(%3Fbrowsebook)%2C%20%22https%3A%2F%2Fgalerij.kb.nl%22)).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP935%20%3Fgal.%0A%20%20%20%20%20BIND(CONCAT(%22https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2F%22%2CREPLACE(%3Fgal%2C%22%20%22%2C%22_%22))%20AS%20%3Fgallery).%7D%0A%20%20OPTIONAL%7B%3Fhighlight%20wdt%3AP6216%20%3Fcopyright.%7D%0A%20%20%20%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%20ORDER%20BY%20%3FhighlightLabel%0A%0A%0A%0A%0A%0A%0A%0A&format=json) and [XML](https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%23%20Simple%20list%20of%20KB%20collection%20highlights%20%0ASELECT%20DISTINCT%20%3Fhighlight%20%3FhighlightLabel%20%3FhighlightDescription%0AWHERE%20%7B%0A%20%20%23%20the%20thing%20is%20part%20of%20the%20KB%20collection%2C%20and%20has%20role%20'collection%20highlight'%20within%20that%20collection%0A%20%20%3Fhighlight%20(p%3AP195%2Fps%3AP195)%20wd%3AQ1526131%3B%20p%3AP195%20%5Bpq%3AP2868%20wd%3AQ29188408%5D.%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22.%20%7D%0A%7D%0AORDER%20BY%20%3FhighlightLabel)<br/>
40) Programatically check for [Wikipedia articles about KB highlights in Dutch](https://w.wiki/3FbF)<br/>
41) Request multiple image URLs from the [Wikimedia Commons query API](https://commons.wikimedia.org/w/api.php?action=help&modules=query) for a specific highlight, both via URL query strings and Python scripts<br/>
42) Request highlight information from the [Wikidata API](https://www.wikidata.org/w/api.php?action=help&modules=wbgetentities) in multiple formats, directly from the highlight's Qnumber<br/>
43) Request full Wikidata items in seven different formats via a [Special:EntityData](https://www.mediawiki.org/wiki/Wikibase/EntityData) URL, directly from the Qnumber: [HTML](https://www.wikidata.org/wiki/Special:EntityData/Q16641064), [JSON](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.json), [JSON-LD](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.jsonld), [RDF](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.rdf), [NT](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.nt), [TTL or N3](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.ttl) and [PHP](https://www.wikidata.org/wiki/Special:EntityData/Q16641064.php) <br/>
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

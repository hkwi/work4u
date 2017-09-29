import rdflib

WD = rdflib.Namespace("http://www.wikidata.org/entity/")
WDT = rdflib.Namespace("http://www.wikidata.org/wiki/Property:")
RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")

# https://query.wikidata.org
a = rdflib.ConjunctiveGraph(store="SPARQLStore")
a.store.endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
info = a.query('''
SELECT ?s ?w ?name ?wname WHERE {
 ?s wdt:P39 ?w ; # 公職
    wdt:P27 wd:Q17 ; # 国籍 日本
    rdfs:label ?name .
 ?w rdfs:label ?wname .
 FILTER ( lang(?name)="ja" )
 FILTER ( lang(?wname)="ja" )
} ORDER BY ?name
''')

b = rdflib.Graph()
b.bind("wd", WD)
b.bind("wdt", WDT)
for s,w,name,wname in info:
	b.add((s, WDT["P39"], w))
	b.add((s, RDFS["label"], name))
	b.add((w, RDFS["label"], wname))
open("docs/people.ttl","w").write(b.serialize(format="turtle").decode("UTF-8"))

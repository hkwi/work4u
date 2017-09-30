import rdflib
import csv

WD = rdflib.Namespace("http://www.wikidata.org/entity/")
WDT = rdflib.Namespace("http://www.wikidata.org/wiki/Property:")
RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")

# https://query.wikidata.org
a = rdflib.ConjunctiveGraph(store="SPARQLStore")
a.store.endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"

b = rdflib.Graph()
b.bind("wd", WD)
b.bind("wdt", WDT)

q = '''
SELECT ?s ?name WHERE {
 ?s rdfs:label ?name .
} ORDER BY ?name
'''
for name, in csv.reader(open("docs/names.csv")):
	r = a.query(q, initBindings={"name":rdflib.Literal(name, lang="ja")})
	hit = False
	for s,name in r:
		b.add((s, RDFS["label"], name))
		hit = True
	if not hit:
		print(name)

open("docs/people.ttl","w").write(b.serialize(format="turtle").decode("UTF-8"))

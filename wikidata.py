import rdflib
import csv

WD = rdflib.Namespace("http://www.wikidata.org/entity/")
WDT = rdflib.Namespace("http://www.wikidata.org/wiki/Property:")
RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")

def normalize_party(party):
	m = {
		"自民党":"自民",
		"日本維新の会":"維新",
		"公明党":"公明",
		"共産党":"共産",
		"希望の党":"希望",
		"民進党":"民進",
		"社民党":"社民",
		"自由党":"自由",
	}
	return m.get(party, party)

nps = {}
for name,area,party in csv.reader(open("docs/seiji_yahoo.csv")):
	party = normalize_party(party)
	nps[(name,party)] = (area, "現職", "")

for name,area,party in csv.reader(open("docs/senkyo_dotcom.csv")):
	party = normalize_party(party)
	k = (name, party)
	if k in nps:
		continue
	if name in [name for name,party in nps.keys()]:
		nps[k] = (area, "", "重複注意")
	else:
		nps[k] = (area, "", "")

# https://query.wikidata.org
a = rdflib.ConjunctiveGraph(store="SPARQLStore")
a.store.endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"

b = rdflib.Graph()
b.bind("wd", WD)
b.bind("wdt", WDT)

rows = []
q = '''
SELECT ?s ?name ?sex ?dt WHERE {
 ?s rdfs:label ?name ;
    wdt:P21/rdfs:label ?sex ;
    wdt:P569 ?dt .
  FILTER(lang(?sex)="ja")
} ORDER BY ?name
'''
for k,v in nps.items():
	name, party = k
	area, info, dup = v
	
	r = a.query(q, initBindings={"name":rdflib.Literal(name, lang="ja")})
	hit = False
	rs = [d for d in r]
	if len(rs) == 1:
		s,n,sex,dt = rs[0]
		rows += [(s[len(WD):], name, party, info, area, sex.value, dt.value, dup)]
		print(s[len(WD):], name, party, info, area, sex.value, dt.value, dup)
	elif len(rs) == 0:
		rows += [("", name, party, info, area, "", "", dup)]
	else:
		for r in rs:
			s,n,sex,dt = r
			rows += [(s[len(WD):], name, party, info, area, sex.value, dt.value, "重複注意")]
			print(s[len(WD):], name, party, info, area, sex.value, dt.value, "重複注意")

csv.writer(open("docs/wikidata.csv","w")).writerows(rows)

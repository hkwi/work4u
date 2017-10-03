import csv
import json

d = json.load(open("ep-popolo-v1.0.json"))

def person(qid):
	for p in d["persons"]:
		for i in p.get("identifiers", []):
			if i["scheme"] == "wikidata" and i["identifier"]==qid:
				return p

def twitter(qid):
	p = person(qid)
	if p:
		for c in p.get("contact_details", []):
			if c["type"] == "twitter":
				return c["value"]

def facebook(qid):
	p = person(qid)
	if p:
		for l in p.get("links", []):
			url = l["url"]
			pre = "https://facebook.com/"
			if url.startswith(pre):
				return url

prefs = '''北海道
青森県
岩手県
宮城県
秋田県
山形県
福島県
茨城県
栃木県
群馬県
埼玉県
千葉県
東京都
神奈川県
新潟県
富山県
石川県
福井県
山梨県
長野県
岐阜県
静岡県
愛知県
三重県
滋賀県
京都府
大阪府
兵庫県
奈良県
和歌山県
鳥取県
島根県
岡山県
広島県
山口県
徳島県
香川県
愛媛県
高知県
福岡県
佐賀県
長崎県
熊本県
大分県
宮崎県
鹿児島県
沖縄県'''.split()
pref = {}
for i, p in enumerate(prefs):
	pref[p] = i+1

rows = []
for qid, name, party, info, area, sex, birth, dup in csv.reader(open("docs/wikidata.csv")):
	if birth:
		birth = birth.split()[0]
	area_num = None
	for k,v in pref.items():
		if area.startswith(k):
			area_num = v
	
	rows += [(qid, name, party, info, area_num, area, sex, birth, twitter(qid), facebook(qid), "", dup)]

csv.writer(open("docs/main.tsv", "w"), delimiter="\t").writerows(rows)

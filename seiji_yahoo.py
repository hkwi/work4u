import lxml.html
import urllib.request
import csv
rows = []
for i in range(1, 49):
	url = "https://seiji.yahoo.co.jp/giin/?pl=1&p=%d" % i
	doc = lxml.html.parse(urllib.request.urlopen(url))
	
	prows = []
	for li in doc.xpath(".//tr"):
		names = [s.strip() for s in li.xpath('./td[@class="colName"]/a/text()') if s.strip()]
		zones = li.xpath('./td[@class="colZone"]/text()')
		parties = li.xpath('./td[@class="colParty"]/text()')
		if len(names) == 0 and len(zones) == 0 and len(parties)==0:
			continue
		assert len(names) == 1 and len(zones) == 1 and len(parties) == 1, "%s %s %s" % (names, zones, parties)
		prows += [(names[0].replace(" ",""), zones[0].strip(), parties[0].strip())]
	
	print("%d from %s" % (len(prows),url))
	rows += prows

csv.writer(open("docs/seiji_yahoo.csv", "w")).writerows((rows))

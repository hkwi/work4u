import lxml.html
import urllib.request
import csv
rows = []
for i in range(1, 49):
	url = "https://seiji.yahoo.co.jp/giin/?pl=1&p=%d" % i
	names = lxml.html.parse(urllib.request.urlopen(url)).xpath('.//td[@class="colName"]/a/text()')
	names = [n.strip() for n in names if n.strip()]
	rows += [(name,) for name in names]
	print("%d from %s" % (len(names),url))

csv.writer(open("docs/seiji_yahoo.csv", "w")).writerows((rows))

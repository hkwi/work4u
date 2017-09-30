import lxml.etree
import lxml.html
import csv
t=lxml.etree.parse("http://shugiin.go2senkyo.com/sitemap.xml")
rows = []
for url in t.xpath(".//s:loc/text()", namespaces={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}):
	if not url.endswith("/"):
		url += "/"
	names = lxml.html.parse(url).xpath('.//p[@class="list_peason_name"]/text()')
	rows += [(name,) for name in names]
	print("%d from %s" % (len(names),url))

csv.writer(open("docs/senkyo_dotcom.csv", "w")).writerows((rows))

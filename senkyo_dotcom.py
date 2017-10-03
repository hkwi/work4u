import lxml.etree
import lxml.html
import csv
t=lxml.etree.parse("http://shugiin.go2senkyo.com/sitemap.xml")
rows = []
for url in t.xpath(".//s:loc/text()", namespaces={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}):
	if not url.endswith("/"):
		url += "/"
	url = url.replace("/aomor/", "/aomori/")
	
	doc = lxml.html.parse(url)
	
	areas = doc.xpath('.//span[@class="ttl_txt"]/text()')
	assert len(areas)==1, url
	
	prows = []
	for txt in doc.xpath('.//div[@class="txts"]'):
		names = txt.xpath('.//p[@class="list_peason_name"]/text()')
		parties = txt.xpath('.//span[@class="pname"]/text()')
		assert len(names) == 1 and len(parties) == 1
		prows += [(names[0].replace("　",""), areas[0].strip(), parties[0].strip())]
	print("%d from %s" % (len(prows),url))
	rows += prows

csv.writer(open("docs/senkyo_dotcom.csv", "w")).writerows((rows))

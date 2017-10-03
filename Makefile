docs/senkyo_dotcom.csv:
	python3 senkyo_dotcom.py

docs/seiji_yahoo.csv:
	python3 seiji_yahoo.py

docs/wikidata.csv: docs/seiji_yahoo.csv docs/senkyo_dotcom.csv
	python3 wikidata.py

docs/main.tsv: docs/wikidata.csv
	python3 everypolitican.py

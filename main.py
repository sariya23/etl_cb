import datetime
from urllib.request import urlopen, urlretrieve
import requests
from lxml import etree

date_format = "%d/%m/%y"

def get_currency_date_xml(date: datetime.date):
    parsed_date = datetime.datetime.strftime(date, date_format)


curr_date = "07/06/2025"
URL = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={curr_date}"

response = urlopen(URL)
xml_data = response.read()
with open("response.xml", "wb") as f:
    f.write(xml_data)
tree = etree.fromstring(xml_data)
for v in tree.xpath("/ValCurs/Valute"):
    print(v.xpath("./NumCode")[0].text)
    print(v.xpath("./CharCode")[0].text)
    print(v.xpath("./Nominal")[0].text)
    print(v.xpath("./Name")[0].text)
    print(v.xpath("./Value")[0].text)
    print(v.xpath("./VunitRate")[0].text)
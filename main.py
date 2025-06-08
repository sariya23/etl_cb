import datetime
import requests
from lxml import etree

date_format = "%d/%m/%Y"
base_url = "http://www.cbr.ru/scripts/XML_daily.asp"

def get_xml_currency(date: datetime.date):
    parsed_date = datetime.datetime.strftime(date, date_format)
    response = requests.get(f"{base_url}?date_req={parsed_date}")
    print(response.url)
    return response

xml_data = get_xml_currency(datetime.date.today()).content
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
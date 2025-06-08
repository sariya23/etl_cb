import datetime
import requests
from lxml import etree
import pandas as pd
import os


static_dir = "static"
static_dir_xml = "static/xml"
static_dir_csv = "static/csv"
date_format = "%d/%m/%Y"
base_url = "http://www.cbr.ru/scripts/XML_daily.asp"
root_tag = "ValCurs"
item_tag = "Valute"
data_tags = ("NumCode", "CharCode", "Nominal", "Name", "Value", "VunitRate")


def get_xml_data(date: datetime.date) -> bytes:
    parsed_date = datetime.datetime.strftime(date, date_format)
    response = requests.get(f"{base_url}?date_req={parsed_date}")
    return response.content

def write_data_in_xml(data: bytes) -> None:
    file_name = f"{datetime.datetime.now()}_currency.xml"
    with open(os.path.join(static_dir_xml, file_name), "wb") as f:
        f.write(data)

def build_dataframe(xml_data: bytes) -> pd.DataFrame:
    currency = {}

    tree = etree.fromstring(xml_data)
    for v in tree.xpath(f"/{root_tag}/{item_tag}"):
        for t in data_tags:
            if t not in currency:
                currency[t] = [v.xpath(f"./{t}")[0].text]
            else:
                currency[t].append(v.xpath(f"./{t}")[0].text)

    df = pd.DataFrame(currency)
    df["NumCode"] = df["NumCode"].astype(str)
    df["Value"] = pd.to_numeric(df["Value"].str.replace(",", "."), errors="coerce")
    df["VunitRate"] = pd.to_numeric(df["VunitRate"].str.replace(",", "."), errors="coerce")
    return df


if __name__ == "__main__":
    xml_data = get_xml_data(datetime.date.today())
    write_data_in_xml(xml_data)
    df = build_dataframe(xml_data)
    print(df)
    p = os.path.join(static_dir_csv, f"{datetime.datetime.now()}_currency.csv")
    df.to_csv(p, index=False)

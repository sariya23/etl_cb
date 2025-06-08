import datetime

import requests
from lxml import etree
import pandas as pd
import os
from dotenv import load_dotenv

from storage.postgres.postgres import Postgres

load_dotenv(".env")


static_dir = "static"
static_dir_xml = "static/xml"
static_dir_csv = "static/csv"
date_format = "%d/%m/%Y"
base_url = "http://www.cbr.ru/scripts/XML_daily.asp"
root_tag = "ValCurs"
item_tag = "Valute"
data_tags = ("NumCode", "CharCode", "Nominal", "Name", "Value", "VunitRate")

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

def get_xml_data(date: datetime.date) -> bytes:
    parsed_date = datetime.datetime.strftime(date, date_format)
    response = requests.get(f"{base_url}?date_req={parsed_date}")
    return response.content


def write_data_in_xml(data: bytes) -> None:
    file_name = f"{datetime.datetime.now()}_currency.xml"
    with open(os.path.join(static_dir_xml, file_name), "wb") as f:
        f.write(data)


def build_dataframe(xml_data: bytes, date: datetime.date) -> pd.DataFrame:
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
    df["Nominal"] = df["Nominal"].astype(int)
    df["Value"] = pd.to_numeric(df["Value"].str.replace(",", "."), errors="coerce")
    df["VunitRate"] = pd.to_numeric(
        df["VunitRate"].str.replace(",", "."), errors="coerce"
    )
    df["CourseDate"] = date
    return df


if __name__ == "__main__":
    xml_data = get_xml_data(datetime.date.today())
    write_data_in_xml(xml_data)
    df = build_dataframe(xml_data, datetime.date.today())
    print(df)
    p = os.path.join(static_dir_csv, f"{datetime.datetime.now()}_currency.csv")
    print(df.to_records(index=False))
    pos = Postgres(
        dbname=POSTGRES_DB,
        user=POSTGRES_USERNAME,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    pos.insert_currency_course(df)
import datetime

import requests
from lxml import etree
import pandas as pd
import os

from storage.postgres.postgres import Postgres
from constants.constants import Constants
from constants.db_config import DbConfig


def get_xml_data(date: datetime.date) -> bytes:
    parsed_date = datetime.datetime.strftime(date, Constants.DATE_FORMAT)
    response = requests.get(f"{Constants.BASE_URL}?date_req={parsed_date}")
    return response.content


def write_data_in_xml(data: bytes) -> None:
    file_name = f"{datetime.datetime.now()}_currency.xml"
    with open(os.path.join(Constants.STATIC_DIR_XML, file_name), "wb") as f:
        f.write(data)


def build_dataframe(xml_data: bytes, date: datetime.date) -> pd.DataFrame:
    currency = {}

    tree = etree.fromstring(xml_data)
    for v in tree.xpath(f"/{Constants.ROOT_TAG}/{Constants.ITEM_TAG}"):
        for t in Constants.DATA_TAGS:
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
    p = os.path.join(Constants.STATIC_DIR_CSV, f"{datetime.datetime.now()}_currency.csv")
    print(df.to_records(index=False))
    pos = Postgres(DbConfig())
    pos.insert_currency_course(df)
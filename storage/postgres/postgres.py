import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

from constants.db_config import DbConfig


class Postgres:
    def __init__(self, db_config: DbConfig):
        self.__conn = psycopg2.connect(
            dbname=db_config.POSTGRES_DB,
            user=db_config.POSTGRES_USERNAME,
            password=db_config.POSTGRES_PASSWORD,
            host=db_config.POSTGRES_HOST,
            port=db_config.POSTGRES_PORT,
        )

    def insert_currency_course(self, data: pd.DataFrame):
        with self.__conn.cursor() as cur:
            rows = data.to_records(index=False).tolist()
            query = """
                    INSERT INTO currency_rate (num_code, char_code, nominal, name, value, vunit_value, rate_date)
                    VALUES %s
                    """
            execute_values(cur, query, rows)
        self.__conn.commit()

    def close(self):
        self.__conn.close()

    def __del__(self):
        try:
            self.__conn.close()
        except:
            pass



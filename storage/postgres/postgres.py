import datetime

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

class Postgres:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.__conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )

    def insert_currency_course(self, data: pd.DataFrame):
        with self.__conn.cursor() as cur:
            rows = data.to_records(index=False).tolist()
            query = """
                    INSERT INTO currency_course (num_code, char_code, nominal, name, value, vunit_value, course_date)
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



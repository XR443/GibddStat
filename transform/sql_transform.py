import json
import sqlite3
from pathlib import Path

from tqdm import tqdm

from transform import ddl_sql, dml_sql


class SqlTransformer:

    def __init__(self, dtp_db_name="dtp.db"):
        self.__sqlite_connect = None
        self.__dtp_db_name = dtp_db_name

    def connect_to_db(self):
        self.__sqlite_connect = sqlite3.connect(self.__dtp_db_name)
        cursor = self.__sqlite_connect.cursor()
        self.__execute_queries(cursor, ddl_sql.all_ddl_sql())
        self.__sqlite_connect.commit()

    def get_connection(self):
        return self.__sqlite_connect

    def transform_card(self, card):
        cursor = self.__sqlite_connect.cursor()
        self.__execute_queries(cursor, dml_sql.insert_dtp(card))
        self.__execute_queries(cursor, dml_sql.insert_objects(card))
        self.__execute_queries(cursor, dml_sql.insert_factors(card))
        self.__execute_queries(cursor, dml_sql.insert_ndu(card))
        self.__execute_queries(cursor, dml_sql.insert_weather(card))
        self.__execute_queries(cursor, dml_sql.insert_road_sections(card))
        self.__execute_queries(cursor, dml_sql.insert_vehicles_with_participants(card))
        self.__execute_queries(cursor, dml_sql.insert_participants(card))
        self.__sqlite_connect.commit()

    @staticmethod
    def __execute_queries(cursor, generator):
        for sql in generator:
            try:
                cursor.execute(sql)
            except Exception as e:
                print(f"Возникла ошибка при выполнении запроса:\n{sql}")
                raise e

    def execute(self, sql):
        print(f"Исполнение запроса: {sql}")
        return self.__sqlite_connect.cursor().execute(sql).fetchall()

    def close(self):
        self.__sqlite_connect.close()


def load_data(transformer, data_path="dtpdata"):
    transformer.connect_to_db()

    if not transformer.execute("SELECT EXISTS(SELECT * FROM dtp LIMIT 1)") or True:
        dtp_data = Path(data_path)
        print(f"Данных в базе не обнаружено. Начинается загрузка данных из {dtp_data}")
        for year_folder in dtp_data.iterdir():
            for dtp_file in tqdm(year_folder.iterdir(), desc=f"Загрузка данных из каталога '{year_folder}'"):
                try:
                    for card in get_cards(dtp_file):
                        transformer.transform_card(card)
                except Exception as e:
                    print(f"При обработке '{dtp_file}' возникла ошибка '{e}'")
                    transformer.close()
                    raise e

    try:
        assert len(transformer.execute("SELECT * FROM dtp LIMIT 1")) == 1
        print("Данные загружены")
    except AssertionError:
        print("Данные не загрузились")
        raise Exception("Данные не были загружены, повторите попытку.")


def get_cards(path):
    with open(path, 'r', encoding='utf-8') as file:
        file_data = file.read()
        data = json.loads(file_data)
        cards = data["cards"]
        for card in cards:
            yield card

import json
import re

import pymysql
import hbzk_show.settings


class Get_data():
    def __init__(self, cursor):
        self.cursor = cursor

    def select_per_year(self):
        table_sql = "SELECT table_name FROM table_name"
        self.cursor.execute(table_sql)
        tables = self.cursor.fetchall()
        for table in tables:
            table = re.findall('\((.*?)\)', str(table), re.I)
            sql = f"SELECT {table}, year, sum FROM year_data_sum"
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            rows = []
            row_data = []



    def count_per_mouth(self):
        pass

    @classmethod
    def db(cls,settings):
        DB = settings.get['DB']
        mysql_db = pymysql.connect(host=eval(DB)['MYSQL_HOST'], user=DB['USER'], password=DB['PASSWORD'], port=DB['port'], charset='utf8',
                                        database=DB['DB'])
        cursor = mysql_db.cursor()
        return cls(cursor)

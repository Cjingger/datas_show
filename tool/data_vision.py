import json
import time
import pymysql
from hbzk_show.settings import DB

MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306


class Get_data(object):
    def __init__(self,offset,pagesize,tim,clss_code,control_term):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                        database=DB)
        self.cursor = self.mysql_db.cursor()
        self.offset = offset
        self.pagesize = pagesize
        self.tim = tim
        self.clss_code = clss_code
        self.control_term = control_term

    def get_data(self):
        period = 'create_date >= {} and create_date <= {}'
        sql = 'select count(id) as daily_data' + period

    def __del__(self):
        self.mysql_db.close()
        self.cursor.close()

    @classmethod
    def get_db(cls,DB):
        conn = pymysql.connect(cls,host=DB['MYSQL_HOST'],user=DB['USER'],password=DB['PASSWORD'],charset='utf8',database=DB['DB'],port=3306)



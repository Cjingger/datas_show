from dbutils.pooled_db import PooledDB

from hbzk_show.settings import DB
import pymysql


MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306


#  更新show表数据
class Update_show(object):
    def __init__(self, table_name):
        self.pool = PooledDB(pymysql, 10, host=MYSQL_HOST, user=USER, passwd=PASSWORD, db=DB, port=PORT)  # 5为连接池里的最少连接数
        self.db = self.pool.connection()
        self.cursor = self.db.cursor()
        self.table_name = table_name

    def select_info(self):
        sql = "select discipline , subdiscipline, classify from {} group by discipline , subdiscipline, classify".format(self.table_name)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.insert_info(res)

    def insert_info(self, map_l):
        sql1 = 'truncate table {}_show'.format(self.table_name)
        self.cursor.execute(sql1)
        self.db.commit()

        sql = "insert into {}_show (discipline,subdiscipline,classify) values(%s,%s,%s)".format(self.table_name)
        self.cursor.executemany(sql, map_l)  # 执行插入数据
        self.db.commit()

    def __delete__(self):
        self.db.close()
        self.cursor.close()


















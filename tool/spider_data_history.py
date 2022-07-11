import json

import pymysql
from hbzk_show.settings import DB

MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306

# 插入爬虫爬取信息
class Insert_spider():
    def __init__(self):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                        database=DB)
        self.cursor = self.mysql_db.cursor()

    def insert_spider(self,l):
        sql = "insert into spider_history (time,uri,data_from,subdiscipline,classify,keywords,discipline,statu,name) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # 要插入的数据
        self.cursor.execute(sql, l)
        self.mysql_db.commit()

    def update_spider(self,statu,time):
        sql = "update spider_history set `statu` = {} where time = {}".format(statu,time)  # 要插入的数据
        self.cursor.execute(sql)  # 执行插入数据
        self.mysql_db.commit()

    def __delete__(self, instance):
        self.mysql_db.close()
        self.cursor.close()

class Query_spider():
    def __init__(self,name,offset,pagesize):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                        database=DB)
        self.cursor = self.mysql_db.cursor()
        self.name = name
        self.offset = offset
        self.pagesize = pagesize

    def select_spider_history(self):
        sql = 'select * from spider_history where name= "{}" limit {}, {}'.format(self.name,self.offset*self.pagesize,self.pagesize)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        a = ('id','time','uri','data_from','subdiscipline','classify','keywords','discipline','statu','name')
        rows = []
        for i in res:
            b = zip(a, i)
            c = dict(b)
            rows.append(c)

        sql_ = 'select count(id) from spider_history where name= "{}"'.format(self.name)
        self.cursor.execute(sql_)
        total = self.cursor.fetchall()[0][0]
        varsd=json.dumps({'total': total, 'rows': rows})
        return varsd

    def __delete__(self, instance):
        self.mysql_db.close()
        self.cursor.close()

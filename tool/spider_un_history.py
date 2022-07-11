import json

import pymysql
from hbzk_show.settings import DB


MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306


# 插入抓取高校信息历史记录
class Insert_un():
    def __init__(self):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                   database=DB)
        self.cursor = self.mysql_db.cursor()

    def insert_un(self,l):
        sql = "insert into spider_un_history (time,name,data_from,subdiscipline,classify,statu) values(%s,%s,%s,%s,%s,%s)"  # 要插入的数据
        self.cursor.execute(sql, l)  # 执行插入数据
        self.mysql_db.commit()

    def update_un(self,statu,time):
        sql = "update spider_un_history set statu = '{}' where time = '{}'".format(statu,time)
        self.cursor.execute(sql)
        self.mysql_db.commit()

    def __delete__(self, instance):
        self.mysql_db.close()
        self.cursor.close()


#  查询高校抓取信息历史记录
class Select_un_history():

    def __init__(self,name,offset,pagesize):

        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                        database=DB)
        self.cursor = self.mysql_db.cursor()
        self.name = name
        self.offset = offset
        self.pagesize = pagesize

    def select_un_history(self):
        sql = 'select * from spider_un_history where name= "{}" limit {}, {}'.format(self.name,self.offset*self.pagesize,self.pagesize)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        a = ('id','time','name','data_from','subdiscipline','classify','statu')
        rows = []
        for i in res:
            b = zip(a, i)
            c = dict(b)
            rows.append(c)

        sql_ = 'select count(id) from spider_un_history where name= "{}"'.format(self.name)
        self.cursor.execute(sql_)
        total = self.cursor.fetchall()[0][0]
        varsd=json.dumps({'total': total, 'rows': rows})
        return varsd

    def __delete__(self, instance):
        self.mysql_db.close()
        self.cursor.close()


















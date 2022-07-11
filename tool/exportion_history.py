import datetime
import json

import pymysql
from hbzk_show.settings import DB


MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306

# 将导出或推送记录写入数据库
class Insert_exportion_history():
    def __init__(self):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                   database=DB)
        self.cursor = self.mysql_db.cursor()

    def insert_exportion_history(self,l):
        sql = "insert into exportion_history (name,table_name,discipline,subdiscipline,classify,time,send_type,start_num,end_num,num) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # 要插入的数据
        self.cursor.execute(sql, l)  # 执行插入数据
        self.mysql_db.commit()

    def __delete__(self, instance):
        self.mysql_db.close()
        self.cursor.close()

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

#  查询推送或导出历史
class Select_exportion_history():
    def __init__(self,name,offset,pagesize):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                   database=DB)
        self.cursor = self.mysql_db.cursor()
        self.name = name
        self.offset = offset
        self.pagesize = pagesize


    def select_exportion_history(self):
        sql = 'select * from exportion_history where name= "{}" limit {}, {}'.format(self.name,self.offset*self.pagesize,self.pagesize)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        a = ('id','name','table_name','discipline','subdiscipline','classify','time','send_type','start_num','end_num','num')
        rows = []
        for i in res:
            b = zip(a, i)
            c = dict(b)
            rows.append(c)

        sql_ = 'select count(id) from exportion_history where name= "{}"'.format(self.name)
        self.cursor.execute(sql_)
        total = self.cursor.fetchall()[0][0]
        dic = {'total': total, 'rows': rows}
        varsd=json.dumps(dic,cls=DateEncoder)
        return varsd


    def __delete__(self, instance):
        self.mysql_db.close()
        self.cursor.close()
























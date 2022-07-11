import json
import time

import pymysql

from hbzk_show.settings import  DB

MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306


# 插入sci解析状态

class Sci_history():
    def __init__(self,user,subject,mark,status):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                        database=DB)
        self.cursor = self.mysql_db.cursor()
        self.user = user
        self.subject = subject
        self.mark = mark
        self.time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        self.status = status

    # 插入数据库
    def insert_sci_history(self):
        try:
            sql = "insert into sci_history (user,subject,mark,time,status) values(%s,%s,%s,%s,%s)"
            self.cursor.execute(sql,(self.user,self.subject,self.mark,self.time,self.status))
            self.mysql_db.commit()
        except:
            self.mysql_db.rollback()

    # 更改状态
    def update_sci_history(self,status):
        try:
            sql = "update sci_history set status = '{}' where mark = '{}'".format(status,self.mark)
            self.cursor.execute(sql)
            self.mysql_db.commit()
            # 更改数量
            self.update_sci_num()

        except Exception as e:
            print(e)
            self.mysql_db.rollback()

    # 记录总数
    def update_sci_num(self):
        num = self.select_num()

        try:
            sql = "update sci_history set num = '{}' where mark = '{}'".format(num,self.mark)

            self.cursor.execute(sql)
            self.mysql_db.commit()
        except Exception as e:
            print(e)
            self.mysql_db.rollback()

    # 查询总数
    def select_num(self):
        num = ''
        try:
            sql = 'select count(id) from new_sci where mark = "{}"'.format(self.mark)
            self.cursor.execute(sql)
            num = self.cursor.fetchall()[0][0]
        except Exception as e:
            print(e)
            self.mysql_db.rollback()
            num = ''
        finally:
            return num

    def __del__(self):
        self.mysql_db.close()
        self.cursor.close()


# 查询sci历史记录
class Select_sci_history():

    def __init__(self,name,offset,pagesize):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                        database=DB)
        self.cursor = self.mysql_db.cursor()
        self.name = name
        self.offset = offset
        self.pagesize = pagesize

    def select_sci_history(self):
        sql = 'select * from sci_history where user= "{}" limit {}, {}'.format(self.name,self.offset*self.pagesize,self.pagesize)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        a = ('id','user','subject','mark','time','status','num')
        rows = []
        for i in res:
            b = zip(a, i)
            c = dict(b)
            rows.append(c)

        sql_ = 'select count(id) from sci_history where user= "{}"'.format(self.name)
        self.cursor.execute(sql_)
        total = self.cursor.fetchall()[0][0]
        varsd=json.dumps({'total': total, 'rows': rows})
        return varsd

    def __del__(self):
        self.mysql_db.close()
        self.cursor.close()


# 到处查询记录
class Exportion_sci():
    def __init__(self,name,mark):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                        database=DB)
        self.cursor = self.mysql_db.cursor()
        self.name = name
        self.mark = mark

    def select_sci(self):
        l = []
        a = ('create_date','time','data_from','keyword','is_qikan','article','area','is_ch','name','email','classify','url','discipline','subdiscipline')

        sql = 'select create_date,time,data_from,keyword,is_qikan,article,area,is_ch,name,email,classify,url,discipline,subdiscipline from new_sci where user= "{}" and mark = "{}"'.format(self.name,self.mark)
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            for i in res:
                b = zip(a,i)
                c = dict(b)
                l.append(c)

        except Exception as e:
            print(e)
        finally:
            return l

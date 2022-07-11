import json
import time
import pymysql
from hbzk_show.settings import DB

MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306



# 查询ei
class Select_ei():

    def __init__(self,offset,pagesize,tim,clss_code,control_term):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                        database=DB)
        self.cursor = self.mysql_db.cursor()
        self.offset = offset
        self.pagesize = pagesize
        self.tim = tim
        self.clss_code = clss_code
        self.control_term = control_term

    def select_ei(self):
        tim = ' and time={} '.format(self.tim) if self.tim else ''
        clss_code = ' and LOCATE("{}", clss_code)>0 '.format(self.clss_code) if self.clss_code else ''
        control_term = ' and LOCATE("{}", control_term)>0 '.format(self.control_term) if self.control_term else ''

        sql = 'SELECT article,name,email,is_ch,time,clss_code,control_term FROM ei WHERE 1 = 1'  +tim + clss_code + control_term  + ' limit {}, {} '.format(self.offset*self.pagesize,self.pagesize)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        a = ('article','name','email','is_ch','time','clss_code','control_term')
        rows = []
        for i in res:
            b = zip(a, i)
            c = dict(b)
            rows.append(c)

        sql_ = 'select count(id) from ei where 1 = 1' + tim + clss_code + control_term
        self.cursor.execute(sql_)
        total = self.cursor.fetchall()[0][0]
        varsd=json.dumps({'total': total, 'rows': rows})
        return varsd

    def __del__(self):
        self.mysql_db.close()
        self.cursor.close()


# 到处查询记录
class Exportion_ei():
    def __init__(self,start_num,end_num,tim,clss_code,control_term):
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                        database=DB)
        self.cursor = self.mysql_db.cursor()
        self.start_num = start_num-1
        self.end_num = end_num
        self.tim = tim
        self.clss_code = clss_code
        self.control_term = control_term

    def select_ei(self):
        tim = ' and time={} '.format(self.tim) if self.tim else ''
        clss_code = ' and LOCATE("{}", clss_code)>0 '.format(self.clss_code) if self.clss_code else ''
        control_term = ' and LOCATE("{}", control_term)>0 '.format(self.control_term) if self.control_term else ''

        l = []
        a = ('article','name','email','is_ch','time','affils','abstracty','clss_code','control_term')

        sql = 'SELECT article,name,email,is_ch,time,affils,abstracty,clss_code,control_term FROM ei WHERE 1 = 1'  +tim + clss_code + control_term  + ' limit {}, {} '.format(self.start_num,self.end_num-self.start_num)
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            for i in res:
                b = zip(a, i)
                c = dict(b)
                l.append(c)

        except Exception as e:
            print(e)
        finally:
            return l

    def __del__(self):
        self.mysql_db.close()
        self.cursor.close()


# coding:utf-8

import datetime
import os
import re
import time
from threading import Thread
import pymysql
from dbutils.pooled_db import PooledDB
from hbzk_show.settings import DB
from tool.get_name import Get_name
from queue import Queue

MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306


# sci解析
class Sci_extrat():
    def __init__(self, path, name, mark):
        self.queue1 = Queue()
        self.path = path
        self.pool = PooledDB(pymysql, 20, host=MYSQL_HOST, user=USER, passwd=PASSWORD, db=DB, port=PORT)  # 5为连接池里的最少连接数
        self.db = self.pool.connection()
        self.cursor = self.db.cursor()
        self.name = name
        self.mark = mark
        self.dic_class = self.get_discipline()

    def get_sci(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            data = f.read()
            content_list = re.findall(r'(PT [A-Z]\n.*?DA .*?\nER\n)', data, re.S)
            for content in content_list:
                if 'EM ' and '@' in content:
                    # 出版社
                    classify_ = re.findall('SO (.*?)\nLA ', content, re.S)
                    classify = classify_[0] if classify_ else ''

                    nam_ = re.findall('AF (.*?)\nTI ', content, re.S)
                    # 作者
                    if nam_:
                        name_ = nam_[0].split('\n')
                    else:
                        name_ = ''

                    # 摘要
                    object_ = re.findall('AB (.*?)\nC1 ', content, re.S)
                    object = object_[0] if object_ else ''

                    # 标题
                    article_ = re.findall('TI (.*?)\nSO ', content, re.S)
                    if article_:
                        article = article_[0].replace('\n', '').strip()
                    else:
                        article = 'N/A'

                    # 出版时间
                    tim_ = re.findall('PD .*?\nPY (.*?)\nVL ', content, re.S)
                    if tim_:
                        tim = tim_[0]
                    else:
                        tim = ''
                    # 关键字
                    sub = re.findall('ID (.*?)\n[AB |CI ]', content, re.S)
                    if sub:
                        subject = sub[0]
                    else:
                        subject = 'N/A'

                    # 邮箱
                    email_ = re.findall('[a-z0-9A-Z-+_.]+[a-z0-9A-Z-+_]*@[a-z0-9\-+_.]+[a-z0-9A-Z-+_]+', content, re.S)
                    if email_:

                        for email in email_:

                            if '.uk' == email[-3:] or ".ca" == email[-3:] or ".au" == email[-3:] or ".nz" == email[
                                                                                                             -3:] or ".ie" == email[
                                                                                                                              -3:] or '.de' == email[
                                                                                                                                               -3:]:
                                is_ch = 2
                            elif "163.com" == email[-7:] or ".cn" == email[-3:] or ".hk" == email[
                                                                                            -3:] or "qq.com" in email or "126.com" in email or "189.com" in email or "21cn.com" in email or "tom.com" in email or "sohu.com" in email or "aliyun.com" in email or "188.com" in email or "139.com" in email or "foxmail.com" in email or "jsinm.org" in email or "hecpharm.com" in email or "sina.com" in email or "njucm.com" in email or "bloomagefreda.com" in email or "263.net" in email or "edu.tw" in email or "yeah.net" in email or ".mo" == email[
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     -3:]:
                                is_ch = 1
                            else:
                                is_ch = 0
                            area_ = re.findall('LA (.*?)\nDT ', content, re.S)
                            if area_:
                                area = area_[0]
                            else:
                                area = ''

                            discipline = self.get_discipline1(classify)

                            subdiscipline = ''

                            if name_:
                                name = Get_name().get_name(name_, email).strip()
                                print(name)

                            newlist = [
                                str(datetime.datetime.now()),
                                tim,
                                'SCI',
                                subject,
                                '1',
                                article,
                                area,
                                is_ch,
                                name,
                                email,
                                classify,
                                object,
                                discipline,
                                subdiscipline,
                                self.name,
                                self.mark
                            ]
                            self.queue1.put(newlist)

        # 删除文件
        os.remove(self.path)


    def insert_sci(self):
        while not self.queue1.empty():
            newlist = self.queue1.get()
            try:
                sql = "insert into new_sci(create_date,time,data_from,keyword,is_qikan,article,area,is_ch,name,email,classify,url,discipline,subdiscipline,user,mark) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # 要插入的数据
                self.cursor.execute(sql, newlist)  # 执行插入数据
                self.db.commit()
            except Exception as e:
                pass

    def get_discipline(self):
        try:
            sql = "select classify,discipline from sci_classify"
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            dic_class = dict((x, y) for x, y in res)
            return dic_class

        except Exception as e:
            return ''

    def get_discipline1(self,classify):
        try:
            discipline = self.dic_class[classify]
            return discipline
        except:
            return ''

    def main(self):
        self.get_sci()
        self.insert_sci()

    def __del__(self):
        self.cursor.close()
        self.db.close()




if __name__ == '__main__':
    s = Sci_extrat(1,1,1)
    s.main()







import re
import time

import pymysql
import requests
from lxml import etree
from hbzk_show.settings import DB


MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306



class Get_un():
    def __init__(self,data_from,dicsipline,subdiscipline,url):
        self.data_from = data_from
        self.discipline = dicsipline
        self.subdiscipline = subdiscipline
        self.url = url
        self.mysql_db = pymysql.connect(host=MYSQL_HOST, user=USER, password=PASSWORD, port=PORT, charset='utf8',
                                   database=DB)
        self.cursor = self.mysql_db.cursor()


    def parse(self):
        data_from = self.data_from
        discipline = self.data_from
        url = self.url
        html = requests.get(url)
        html.encoding = html.apparent_encoding

        data = etree.HTML(html.text)
        res = data.xpath('//a')

        subdiscipline = self.discipline
        classify = self.subdiscipline
        url_split = url.split("//")
        for i in res:
            name = ''.join(i.xpath('.//text()')).strip()
            if name:
                time.sleep(0.2)
                try:
                    if 'http' in i.xpath('./@href')[0]:
                        two_url = i.xpath('./@href')[0].replace('../','')
                    else:

                        two_url = url_split[0] + "//" + url_split[-1].split("/")[0] + "/" +  i.xpath('./@href')[0].replace('../','')
                    res = self.two_parse(two_url)
                    if res:
                        for email in res:
                            self.save_db(name,email,data_from,discipline,two_url,subdiscipline,classify)
                    else:
                        three_url = url_split[0] + "//" + url_split[-1].split("/")[0] + "/" + url_split[-1].split("/")[1] + "/" + i.xpath('./@href')[0].replace('../','')
                        res1 = self.two_parse(three_url)
                        if res1:
                            for email in res1:
                                self.save_db(name, email, data_from, discipline, three_url, subdiscipline, classify)

                except Exception as e:
                    print(e)
                    pass


    def two_parse(self,two_url):
        try:
            html = requests.get(two_url,timeout=10)
            if html.status_code == 200:
                html.encoding = html.apparent_encoding
                text = etree.HTML(html.text)
                text = ','.join(text.xpath(".//text()"))
                email_ = re.findall("[a-z0-9A-Z-+_.]*[a-z0-9A-Z-+_]+@[a-z0-9\-+_.]+[a-z0-9A-Z-+_]+",text, re.S)
                if email_:
                    return email_
                else:
                    return
            else:
                return

        except Exception as e:
            print(e)
            pass

    #  抓取数据入库
    def save_db(self,name,email,data_from,discipline,url,subdiscipline,classify):

        l = (name,email,data_from,discipline,url,subdiscipline,classify)
        try:
            sql = "insert into university (name,email,data_from,discipline,url,subdiscipline,classify) values(%s,%s,%s,%s,%s,%s,%s)"  # 要插入的数据
            self.cursor.execute(sql, l)  # 执行插入数据
            self.mysql_db.commit()
        except Exception as e:
            print(e)
            pass

























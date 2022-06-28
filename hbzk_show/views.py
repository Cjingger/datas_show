import datetime
import gzip
import json
import time
import urllib
import requests
from django.http import HttpResponse, Http404
from django.shortcuts import render
# 首页  查询数据库名
import pymysql
from dbutils.pooled_db import PooledDB
from tool.exportion_history import Insert_exportion_history,Select_exportion_history

import aiohttp
import asyncio
# CONCURRENCY = 5
# semaphore = asyncio.Semaphore(CONCURRENCY)

from hbzk_show.settings import DB

MYSQL_HOST = DB['MYSQL_HOST']
USER = DB['USER']
PASSWORD = DB['PASSWORD']
DB = DB['DB']
PORT = 3306

pool = PooledDB(pymysql, 10, host=MYSQL_HOST, user=USER, passwd=PASSWORD, db=DB, port=PORT)  # 5为连接池里的最少连接数


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user = request.POST.get('name', '')
        password = request.POST.get('password', '')
        db = pool.connection()
        cursor = db.cursor()
        try:
            sql = 'select password,name from user where user = "{}"'.format(user)
            print(sql)
            cursor.execute(sql)
            password1,name= cursor.fetchall()[0]
            cursor.close()
            db.close()
            if password == password1:
                request.session['name'] = name
                return HttpResponse('200')
            else:
                return HttpResponse('400')
        except:
            return HttpResponse('400')


# 退出登录
def logout(request):
    request.session.flush()
    if not request.session.get('nickname'):
        return render(request,'login.html')


def query(request):
    if request.method == 'GET':
        name = request.session.get('name')
        return render(request, 'select.html',locals())


def get_count(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            db = pool.connection()
            cursor = db.cursor()
            tablename = request.GET['data']
            keyword = request.GET['keyword']
            tim = request.GET['time']
            period = request.GET['time_period']
            discipline = request.GET['discipline']
            subdiscipline = request.GET['subdiscipline']
            is_ch = request.GET['is_ch']
            classify = request.GET['classify']
            if discipline:
                discipline_ = " and discipline in ('" + urllib.parse.unquote_plus(discipline.replace('check_box_discipline=','').replace("&","','")) + "') "
            else:
                discipline_ = ''

            if subdiscipline:
                subdiscipline_ = " and subdiscipline in ('" + urllib.parse.unquote_plus(subdiscipline.replace('check_box_subdiscipline=','').replace("&","','")) + "') "
            else:
                subdiscipline_ = ''

            if classify:
                classify_ = " and classify in ('" + urllib.parse.unquote_plus(classify.replace('check_box_classify=','').replace("&","','")) + "') "
            else:
                classify_ = ''
            if period:
                print("period",period)
                start = str(period).split("-")[0:3]
                s_tim = ""
                for times,i in enumerate(start):
                    s_tim += i.strip() if times == 2 else i.strip()+"-"
                print("start",s_tim)
                end = str(period).split("-")[-3:]
                e_tim = ""
                for times,j in enumerate(end):
                    e_tim += j.strip() if times == 2 else j.strip()+"-"
                print("end", e_tim)
                period_ = 'and create_date >= "{}" and create_date <= "{}"'.format(s_tim,e_tim)
            else:
                period_ = ''

            is_ch_ = ' and is_ch = ' + '"'+ is_ch + '"' if is_ch else ''
            keyword_ = ' and ( keyword like "%{}%" or article like "%{}%" ) '.format(keyword,keyword) if keyword else ''
            tim_ = ' and time =  '+ '"'+ tim +'"' if tim else ''

            _sql = 'SELECT  count(id) from ' + tablename + ' where 1=1 ' + discipline_ + is_ch_ + classify_ + subdiscipline_ + keyword_ + tim_ + period_
            print(_sql)
            cursor.execute(_sql)
            # total = len(cursor.fetchall())
            total = cursor.fetchall()[0]
            return HttpResponse(total)


#  返回查询数据列表
def data(request):
    global a,sql,_sql
    name = request.session.get('name')
    if name:
        if request.method == 'GET':

            tablename = request.GET['data']
            keyword = request.GET['keyword']
            tim = request.GET['time']
            period = request.GET['time_period']
            discipline = request.GET['discipline']
            subdiscipline = request.GET['subdiscipline']
            is_ch = request.GET['is_ch']
            classify = request.GET['classify']
            pagesize = int(request.GET['offset']) - 1
            pagenumber = int(request.GET['pagesize'])
            if discipline:
                discipline_ = " and discipline in ('" + urllib.parse.unquote_plus(discipline.replace('check_box_discipline=','').replace("&","','")) + "') "
            else:
                discipline_ = ''

            if subdiscipline:
                subdiscipline_ = " and subdiscipline in ('" + urllib.parse.unquote_plus(subdiscipline.replace('check_box_subdiscipline=','').replace("&","','")) + "') "
            else:
                subdiscipline_ = ''

            if classify:
                classify_ = " and INSTR(classify, '" + urllib.parse.unquote_plus(classify.replace('check_box_classify=','').replace("&","','")) + "') "
            else:
                classify_ = ''
            if period:
                print("peropd",period)
                start = str(period).split("-")[0:3]
                s_tim = ""
                for times,i in enumerate(start):
                    s_tim += i.strip() if times == 2 else i.strip()+"-"
                print("start",s_tim)
                end = str(period).split("-")[-3:]
                e_tim = ""
                for times,j in enumerate(end):
                    e_tim += j.strip() if times == 2 else j.strip()+"-"
                print("end", e_tim)
                period_ = 'and create_date >= "{}" and create_date <= "{}"'.format(s_tim,e_tim)
            else:
                period_ = ''

            is_ch_ = ' and is_ch = ' + '"'+ is_ch + '"' if is_ch else ''
            keyword_ = ' and ( keyword like "%{}%" or article like "%{}%" ) '.format(keyword,keyword) if keyword else ''
            tim_ = ' and time =  '+ '"'+ tim +'"' if tim else ''

            db = pool.connection()
            cursor = db.cursor()
            sql_judge = f"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{DB}' AND TABLE_NAME = '{tablename}'"
            cursor.execute(sql_judge)
            data = cursor.fetchall()
            # print(data)
            a = ('discipline', 'subdiscipline', 'classify', 'email', 'name', 'article', 'is_ch', 'is_qikan',
                     'keyword', 'conference', 'time') if "conference" in str(data[-1]) else ('discipline', 'subdiscipline', 'classify', 'email','name','article','is_ch','is_qikan','keyword','','time')
            sql = 'SELECT  discipline,subdiscipline,classify,email,name,article,is_ch,is_qikan,keyword,conference,time from ' + tablename + ' where 1=1 ' + discipline_ + is_ch_ + classify_ + subdiscipline_ + keyword_ + tim_ + period_ +' limit {},{}'.format(
                pagesize * pagenumber, pagenumber) if "conference" in str(data[-1]) else 'SELECT  discipline,subdiscipline,classify,email,name,article,is_ch,is_qikan,keyword,NULL,time from '+tablename +' where 1=1 ' + discipline_ + is_ch_ + classify_ + subdiscipline_ + keyword_ + tim_ + period_ +' limit {},{}'.format(pagesize*pagenumber,pagenumber)
            _sql = 'SELECT  count(id) from ' + tablename + ' where 1=1 ' + discipline_ + is_ch_ + classify_ + subdiscipline_ + keyword_ + tim_ + period_
            print(sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            rows = []
            for i in data:
                b = zip(a, i)
                c = dict(b)
                rows.append(c)
            cursor.execute(_sql)
            total = cursor.fetchall()[0][0]
            if int(total) > 50000:
                total1 = 50000
            else:
                total1 = total
            varsd=json.dumps({
                'total': total1,
                'rows': rows,
                # 'nums':total
            })
            cursor.close()
            db.close()
            return HttpResponse(varsd)
    else:
        raise Http404


# 选择数据来源刷新期刊名,根据期刊名刷新大小学科
def get_content(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            tablename = request.GET['tablename']
            db = pool.connection()
            cursor = db.cursor()
            sql1 = 'select classify from ' + tablename + '_show group by classify'
            print("sql1",sql1)
            cursor.execute(sql1)
            data1 = cursor.fetchall()
            classify_list = []
            for classify in data1:
                classify_list.append(classify[0])

            data = {
                'classify_list':classify_list,
            }
            cursor.close()
            db.close()
            return HttpResponse(json.dumps(data))
    else:
        raise Http404


# 选择期刊名更新大学科
def get_discipline(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            tablename = request.GET['tablename']
            classify_list = request.GET['classify_list']
            db = pool.connection()
            cursor = db.cursor()
            if classify_list :
                classify = ' and classify in ' + str(tuple(classify_list.split('@')))
                # print("classify",classify)
                if classify[-2:-1] == ',':
                    classify = classify[:-2] + classify[-1]
            else:
                classify = ''

            sql = 'select discipline from ' + tablename + '_show where 1=1 ' + classify + ' group by discipline'

            cursor.execute(sql)
            data1 = cursor.fetchall()
            discipline_list_ = []
            for discipline_ in data1:
                discipline_list_.append(discipline_[0])

            sql3 = 'select subdiscipline from ' + tablename + '_show where 1=1 ' + classify +  ' group by subdiscipline'

            cursor.execute(sql3)
            data3 = cursor.fetchall()
            subdiscipline_list_ = []
            for subdiscipline_ in data3:
                subdiscipline_list_.append(subdiscipline_[0])
            data = {
                'discipline_list': discipline_list_,
                'subdiscipline_list': subdiscipline_list_,
            }
            cursor.close()
            db.close()
            return HttpResponse(json.dumps(data))
    else:
        raise Http404


# 选择大学科更新小学科
def get_subdiscipline(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            tablename = request.GET['tablename']
            classify_list = request.GET['classify_list']
            discipline_list = request.GET['discipline_list']

            db = pool.connection()
            cursor = db.cursor()
            if discipline_list:
                discipline = ' and discipline in ' + str(tuple(discipline_list.split('@')))
                if discipline[-2:-1] == ',':
                    discipline = discipline[:-2] + discipline[-1]
            else:
                discipline = ''

            if classify_list:
                classify = " and discipline in ('" + urllib.parse.unquote_plus(classify_list.replace('check_box_classify=','').replace("&","','")) + "') "
            else:
                classify = ''
            sql = 'select subdiscipline from ' + tablename + '_show where 1=1 ' + classify + discipline + ' group by subdiscipline'

            cursor.execute(sql)
            data3 = cursor.fetchall()
            subdiscipline_list_ = []
            for subdiscipline_ in data3:
                subdiscipline_list_.append(subdiscipline_[0])
            cursor.close()
            db.close()
            # print("subdiscipline_list_",subdiscipline_list_)
            return HttpResponse(json.dumps(subdiscipline_list_))
    else:
        raise Http404


#  数据导出接口
def get_code(server,title):
    data = {
        'title': title,
        'unid': 1,
        'statusFlag': '0'
    }
    url = server +'v1/api/EmailGroup/new.xos'
    data = requests.post(url, data=data).json()['emailGroup']
    id = data['id']
    code = data['code']
    return id,code


# 推送邮箱
def send_email(server,id,code,l):
    print(datetime.datetime.now())
    start_ = time.time()
    s = requests.session()
    json_p ={
        "groupid": id,
        "code": code,
        "list": l
    }
    headers = {'Content-type': 'application/json',
               'Accept-Encoding': 'gzip'}

    html = s.post(server + 'v1/api/EmailAd/batchNew.xos',headers=headers,json=json_p)
    print(html.status_code,'========================',datetime.datetime.now())
    print(time.time()-start_)

def run_time(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        end_time = time.time()
        print("运行时间---->",end_time-start_time)
        return result
    return wrapper

# @run_time
# 导出数据
def get_exportion(request):
    name_ = request.session.get('name')
    if name_:
        if request.method == 'GET':
            start_tim = time.time()
            insert_exportion_history = Insert_exportion_history()
            start_num = request.GET['start_num']
            end_num = request.GET['end_num']
            server = request.GET['server']
            tablename = request.GET['data']
            keyword = request.GET['keyword']
            tim = request.GET['time']
            period = request.GET['time_period']
            discipline = request.GET['discipline']
            subdiscipline = request.GET['subdiscipline']
            is_ch = request.GET['is_ch']
            classify = request.GET['classify']

            if discipline:
                discipline_ = " and discipline in ('" + urllib.parse.unquote_plus(discipline.replace('check_box_discipline=','').replace("&","','")) + "') "
            else:
                discipline_ = ''

            if subdiscipline:
                subdiscipline_ = " and subdiscipline in ('" + urllib.parse.unquote_plus(subdiscipline.replace('check_box_subdiscipline=','').replace("&","','")) + "') "
            else:
                subdiscipline_ = ''

            if classify:
                classify_ = " and classify in ('" + urllib.parse.unquote_plus(classify.replace('check_box_classify=','').replace("&","','")) + "') "
            else:
                classify_ = ''
            if period:
                print("peropd",period)
                start = str(period).split("-")[0:3]
                s_tim = ""
                for times,i in enumerate(start):
                    s_tim += i.strip() if times == 2 else i.strip()+"-"
                print("start",s_tim)
                end = str(period).split("-")[-3:]
                e_tim = ""
                for times,j in enumerate(end):
                    e_tim += j.strip() if times == 2 else j.strip()+"-"
                print("end", e_tim)
                period_ = 'and create_date >= "{}" and create_date <= "{}"'.format(s_tim,e_tim)
            else:
                period_ = ''

            is_ch_ = ' and is_ch = ' + '"'+ is_ch + '"' if is_ch else ''
            keyword_ = ' and ( keyword like "%{}%" or article like "%{}%" ) '.format(keyword,keyword) if keyword else ''
            tim_ = ' and time =  '+ '"'+ tim +'"' if tim else ''
            db = pool.connection()
            cursor = db.cursor()

            # 获取大学科
            sql1 = 'SELECT  discipline from '+tablename +' where 1=1 ' + discipline_ + is_ch_ + classify_ + subdiscipline_ + keyword_ + tim_ + ' group by discipline'
            cursor.execute(sql1)
            get_discipline = cursor.fetchall()
            print("get_discipline", get_discipline)
            if len(get_discipline)!=0:
                title = name_ +  tablename + '-'+ get_discipline[-1][0] + '-'+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                title = name_ + tablename + '-' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # 获取email 和 article
            l = []
            # 查询email
            sql_judge = f"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{DB}' AND TABLE_NAME = '{tablename}'"
            cursor.execute(sql_judge)
            data = cursor.fetchall()
            if "conference" in str(data[-1]):
                sql3 = 'SELECT name, article ,email, area, classify, discipline, subdiscipline, time, conference from '+tablename +' where 1=1 ' + discipline_ + is_ch_ + classify_ + subdiscipline_ + keyword_ + tim_ + period_ + ' group by email '  + ' limit {},{} '.format(int(start_num),int(end_num)-int(start_num))
                print(sql3)
                cursor.execute(sql3)
                email_list = cursor.fetchall()
                print('查询成功', sql3)
                for i in email_list:
                    d = {"name": i[0], "article": i[1], "email": i[2], "area": i[3], "classify": i[4],
                         "discipline": i[5], "subdiscipline": i[6],"year": i[7], "conference": i[8]}
                    l.append(d)
            else:
                sql3 = 'SELECT  name, article ,email, area, classify, discipline, subdiscipline, time from '+tablename +' where 1=1 ' + discipline_ + is_ch_ + classify_ + subdiscipline_ + keyword_ + tim_ + period_ +' group by email '  + ' limit {},{} '.format(int(start_num),int(end_num)-int(start_num))
                print(sql3)
                cursor.execute(sql3)
                email_list = cursor.fetchall()
                print('查询成功',sql3)
                # 获取标题
                for i in email_list:
                    d = {"name": i[0], "article": i[1], "email": i[2], "area": i[3], "classify": i[4],
                         "discipline": i[5], "subdiscipline": i[6],"year": i[7]}
                    l.append(d)
            if server == 'export':
                send_type = '下载'
            else:
                send_type = '推送'

            # 插入历史发送记录
            insert_exportion_history_l = [
                name_,
                tablename,
                urllib.parse.unquote_plus(discipline.replace('check_box_discipline=','').replace("&",",")),
                urllib.parse.unquote_plus(subdiscipline.replace('check_box_subdiscipline=','').replace("&",",")),
                urllib.parse.unquote_plus(classify.replace('check_box_classify=','').replace("&",",")),
                str(datetime.datetime.now()),
                send_type,
                start_num,
                end_num,
                len(l)
            ]
            insert_exportion_history.insert_exportion_history(insert_exportion_history_l)
            end_tim = time.time()
            if server == 'export':
                print('下载')
                print("download_time",end_tim-start_tim)
                return HttpResponse(json.dumps(l))
            else:
                id, code = get_code(server, title)
                send_email(server,id,code,l)
                print(name_,'成功=============================================')
                return HttpResponse('200')
    else:
        raise Http404


# 查询大学科
def query_discipline(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            tablename = request.GET['data']
            discipline_name = request.GET['discipline_name']
            if discipline_name:
                db = pool.connection()
                cursor = db.cursor()
                sql = 'select DISTINCT discipline from '+tablename + '_show where  INSTR(discipline,"'+ discipline_name +'")>0'
                cursor.execute(sql)
                data= cursor.fetchall()

                discipline_list = []
                for discipline_ in data:
                    discipline_list.append(discipline_[0])

                cursor.close()
                db.close()
                return HttpResponse(json.dumps(discipline_list))
    else:
        raise Http404


# 查询小学科
def query_subdiscipline(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            tablename = request.GET['data']
            subdiscipline_name = request.GET['subdiscipline_name']
            if subdiscipline_name:
                db = pool.connection()
                cursor = db.cursor()
                sql = 'select DISTINCT subdiscipline from '+tablename + '_show where  INSTR(subdiscipline,"'+ subdiscipline_name +'")>0'
                cursor.execute(sql)
                data= cursor.fetchall()
                subdiscipline_list = []
                for subdiscipline_ in data:
                    subdiscipline_list.append(subdiscipline_[0])
                cursor.close()
                db.close()
                return HttpResponse(json.dumps(subdiscipline_list))
    else:
        raise Http404


# 查询期刊名
def query_classify(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            tablename = request.GET['data']
            classify_name = request.GET['classify_name']
            if classify_name:
                db = pool.connection()
                cursor = db.cursor()
                sql = 'select classify from '+tablename + '_show where  INSTR(classify,"'+ classify_name +'")>0 group by classify'
                print(sql)
                cursor.execute(sql)
                data= cursor.fetchall()
                classify_list = []
                for classify_ in data:
                    classify_list.append(classify_[0])

                cursor.close()
                db.close()
                return HttpResponse(json.dumps(classify_list))
    else:
        raise Http404


#  个人中心
def person(request):
    name = request.session.get('name')

    if request.method == 'GET':
        if name:
            return render(request,'person.html',locals())
        else:
            raise Http404


# 渲染数据库名称
def table_name(request):
    name = request.session.get('name')
    if request.method == 'GET':
        if name:
            db = pool.connection()
            cursor = db.cursor()
            sql = 'select table_name from table_name'
            cursor.execute(sql)
            res = cursor.fetchall()

            table_name_l = []

            for i in res:
                table_name_l.append(i[0])

            cursor.close()
            db.close()
            return HttpResponse(json.dumps(table_name_l))


#  渲染获取导出或推送记录页面
def exportion_history(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            return render(request,'exportion_history.html',locals())

    else:
        raise Http404


# 获取导出或推送记录数据
def get_exportion_history(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            offset = int(request.GET['offset']) - 1
            pagesize = int(request.GET['pagesize'])
            select_exportion_history = Select_exportion_history(name,offset,pagesize)
            data = select_exportion_history.select_exportion_history()
            return HttpResponse(data)
    else:
        raise Http404

# def data_visible(request):
#     name = request.session.get('name')
#     if name:
#         render()
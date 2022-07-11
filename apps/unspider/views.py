import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse,Http404
# Create your views here.
from django.shortcuts import render
from tool.spider_university import Get_un
from tool.spider_un_history import Insert_un,Select_un_history
from tool.update_show import Update_show



def index(request):
    table_name = 'university'
    name = request.session.get('name')
    if request.method == 'GET':
        return render(request,'unspider_index.html',locals())
    elif request.method == 'POST':
        try:
            data = json.loads(request.POST.get('data', ''))['data']
            insert_un = Insert_un()
            for i in data[1:]:
                if i[0]:
                    tim = str(datetime.datetime.now())
                    statu = '正在抓取'
                    l = [tim,name,i[0],i[1],i[2],statu]
                    # 插入抓取记录
                    insert_un.insert_un(l)
                    try:
                        Get_un(i[0],i[1],i[2],i[3]).parse()
                        # 更改抓取状态
                        statu = '成功'
                        insert_un.update_un(statu,tim)
                    except Exception as e:
                        statu = e
                        #  更改抓取状态
                        insert_un.update_un(statu, tim)
            #  更新show表数据
            Update_show(table_name).select_info()
            return HttpResponse(1)
        except Exception as e:
            raise Http404



def show_un_history(request):
    name = request.session.get('name')
    if request.method == 'GET':
        offset = int(request.GET['offset']) - 1
        pagesize = int(request.GET['pagesize'])
        data = Select_un_history(name,offset,pagesize).select_un_history()
        return HttpResponse(data)












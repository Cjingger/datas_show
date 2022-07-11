import datetime
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render
from tool.get_ei import Select_ei
from tool.get_ei import Exportion_ei
from tool.exportion_history import Insert_exportion_history

# Create your views here.


# 首页渲染
def index(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            return render(request,'ei_index.html',locals())
    else:
        raise Http404


def get_ei(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            try:
                offset = int(request.GET['offset'])
                pagesize = int(request.GET['pagesize'])
                tim = request.GET['time']
                clss_code = request.GET['clss_code']
                control_term = request.GET['control_term']
                select_ei = Select_ei(offset,pagesize,tim,clss_code,control_term)
                data = select_ei.select_ei()
                return HttpResponse(data)
            except Exception as e:
                print(e)
                raise Http404
    else:
        raise Http404


def exportion(request):
    name = request.session.get('name')
    if name:
        if request.method == 'POST':
            try:
                his = Insert_exportion_history()
                start_num = int(request.POST.get('start_num',''))
                end_num = int(request.POST.get('end_num',''))
                tim = request.POST.get('tim','')
                clss_code = request.POST.get('clss_code','')
                control_term = request.POST.get('control_term','')
                data = Exportion_ei(start_num,end_num,tim,clss_code,control_term).select_ei()
                his.insert_exportion_history((name,'ei',clss_code,control_term,'',str(datetime.datetime.now()),'下载',start_num,end_num,end_num-start_num+1))
                return HttpResponse(json.dumps({"data": data}))


            except Exception as e:
                print(e)
                raise Http404

        else:
            return HttpResponse(status=404)
            # raise Http404











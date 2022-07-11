import json
import os
import time

from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
from hbzk_show.settings import BASE_DIR
from tool.sci_extract import Sci_extrat
from tool.sci_history import Sci_history, Select_sci_history, Exportion_sci


def index(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            return render(request,'scispider_index.html',locals())


        elif request.method == 'POST':
            subject = request.POST.get('subject','')
            # 保存上传文件
            mark = int(time.time()*1000)
            status = '正在解析'

            # 将解析记录插入数据库
            sci_history = Sci_history(name,subject,mark,status)
            sci_history.insert_sci_history()


            try:
                file_obj = request.FILES.items()

                path = os.path.join(BASE_DIR, 'file', '{}.text'.format(mark))

                sci_extract = Sci_extrat(path,name,mark)

                for (k, v) in file_obj:
                    file_data = request.FILES.getlist(k)
                    for fl in file_data:
                        for chunk in fl.chunks():
                            with open(path, 'ab+') as f:
                                f.write(chunk + '\n\n'.encode())
                sci_extract.main()

                sci_history.update_sci_history('解析成功')
                return HttpResponse(1)
            except Exception as e:
                sci_history.update_sci_history('解析失败')
                raise Http404

    else:
        raise Http404



# 展示sci抓取记录

def show_sci_history(request):
    name = request.session.get('name')
    if request.method == 'GET':
        offset = int(request.GET['offset']) - 1
        pagesize = int(request.GET['pagesize'])
        data = Select_sci_history(name,offset,pagesize).select_sci_history()
        return HttpResponse(data)

# 导出sci数据
def expro_sci(request):
    name = request.session.get('name')
    if request.method == 'POST':
        mark = request.POST.get('mark','')
        # 导出数据
        l = Exportion_sci(name,mark).select_sci()
        if l:
            return HttpResponse(json.dumps({"data":l}))
        else:
            return HttpResponse()





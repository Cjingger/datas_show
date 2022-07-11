import xlrd
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from tool.spider_data_history import Query_spider
# Create your views here.

def index(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            return render(request, 'dataspider_index.html', locals())

        # elif request.method == 'POST':
        #     request.POST.get('data')
    else:
        return HttpResponse(status=404)

def show_spider_history(request):
    name = request.session.get('name')
    if request.method == 'GET':
        offset = int(request.GET['offset']) - 1
        pagesize = int(request.GET['pagesize'])
        data = Query_spider(name, offset, pagesize).select_spider_history()
        return HttpResponse(data)


def import_file(request):
    template = loader.get_template('dataspider_index.html')
    context = {}
    stat = {'status': False, 'data': None, 'msg': ""}
    if request.method == 'POST':
        try:
            excel_file = request.FILES.get('excelFile')
            wb = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
            table = wb.sheets()[0]
            paper_name = table.cell_value(0, 1)
            section_count = table.cell_value(1, 1)
            nrows = table.nrows  # 行数
            ncole = table.ncols  # 列数
            sec_start_line = 3
            sec_end_line = sec_start_line + int(section_count)
            for x in range(sec_start_line, sec_end_line):
                print(table.cell_value(x, 1))
            # 用完记得删除
            wb.release_resources()
            del wb
        except Exception as e:
            return e,501
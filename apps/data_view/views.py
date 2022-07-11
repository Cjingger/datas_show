from django.shortcuts import render
import datetime
import json
from django.http import HttpResponse, Http404
# Create your views here.


def index(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            return render(request, 'data_view.html', locals())
    else:
        return HttpResponse(status=404)


def count_discipline_classify(request):
    name = request.session.get('name')
    if name:
        if request.method == 'GET':
            tablenames = request.GET('data')
            for tablename in tablenames:
                data = tablename
                insert_sql = ""
                return HttpResponse(data)


    else:
        return HttpResponse(status=404)

def count_pie_year(request):
    pass

def ocunt_line_mouth(request):
    pass
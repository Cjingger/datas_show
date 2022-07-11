"""hbzk_show URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from hbzk_show import views
from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home$', views.query),
    url(r'^data$', views.data),
    url(r'^content$', views.get_content),
    url(r'^discipline$', views.get_discipline),
    url(r'^subdiscipline$', views.get_subdiscipline),
    url(r'^exportion$', views.get_exportion),
    url(r'^query_classify$', views.query_classify),
    url(r'^query_discipline$', views.query_discipline),
    url(r'^query_subdiscipline$', views.query_subdiscipline),
    url(r'^$',views.login),
    url(r'^loginout$', views.logout),
    url(r'^person$', views.person),
    url(r'^table_name$', views.table_name),
    url(r'^exportion_history$', views.exportion_history),
    url(r'^get_exportion_history$', views.get_exportion_history),
    url(r'^get_count$', views.get_count),
    url(r'^unspider/', include('unspider.urls')),
    url(r'^scispider/', include('scispider.urls')),
    url(r'^ei/', include('ei_app.urls')),
    url(r'^data_view/', include('data_view.urls')),
    url(r'^dataspider/', include('dataspider.urls')),



]

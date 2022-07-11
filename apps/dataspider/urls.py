from apps.dataspider import views
from django.urls import path
from django.conf.urls import url,include


urlpatterns = [
    url('^$', views.index),
    url('^show_spider_history', views.show_spider_history),
    url('^import_paper', views.import_file),

]

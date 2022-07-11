from apps.ei_app import views
from django.urls import path
from django.conf.urls import url,include


urlpatterns = [
    url('^$', views.index),
    url('^get_ei', views.get_ei),
    url('^exportion', views.exportion),

]
from apps.unspider import views
from django.urls import path
from django.conf.urls import url,include


urlpatterns = [
    url('^$', views.index),
    url('^show_un_history', views.show_un_history)

]
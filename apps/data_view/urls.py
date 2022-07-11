from apps.data_view import views
from django.urls import path
from django.conf.urls import url,include


urlpatterns = [
    url('^$', views.index)
    # url('^', views.get_ei),
    # url('^exportion', views.exportion),

]
from apps.scispider import views
from django.urls import path
from django.conf.urls import url,include


urlpatterns = [
    url('^$', views.index),
    url('^show_sci_history', views.show_sci_history),
    url('^expro_sci', views.expro_sci),

]
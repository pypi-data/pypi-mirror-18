from django.conf.urls import url
from . import views

urlpatterns = [
       url(r'^$', views.logs_page, name='logs'),
       url(r'^filter/$', views.logs_filter, name='logs_filter')
]

# coding:utf-8
from django.conf.urls import url
from .views import get_information

urlpatterns = [
    url(r'^$', get_information, name='get_information'),
]

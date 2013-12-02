# -*- coding:utf-8 -*- 
from django.conf.urls  import patterns,url
import service

urlpatterns = patterns('',
    url('^service/expertRegister',service.expertRegister,name='service.expertRegister'),
)






# -*- coding:utf-8 -*- 
from django.conf.urls  import patterns,url
import service

urlpatterns = patterns('',
    url('^service/ExpertRegister',service.expertRegister,name='service.ExpertRegister'),
    url('^service/ExpertUnregister',service.expertUnregister,name='service.ExpertUnregister'),
)






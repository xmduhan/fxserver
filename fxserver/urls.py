# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, include, url
from fxserver import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fxserver.views.home', name='home'),
    # url(r'^fxserver/', include('fxserver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # 映射上传文件目录
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    
    # 映射expert应用
    url(r'^experts/',include('experts.urls',namespace="experts")),
)

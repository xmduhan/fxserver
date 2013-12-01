# -*- coding:utf-8 -*- 
from django.contrib import admin
from models import *


class ExpertAdmin(admin.ModelAdmin):
    list_display=["code","name"]
admin.site.register(Expert,ExpertAdmin)

class ExpertInstanceAdmin(admin.ModelAdmin):
    list_display=["id","expert","account","tradingAllowed","lotSize"]    
admin.site.register(ExpertInstance,ExpertInstanceAdmin)






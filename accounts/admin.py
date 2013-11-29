# -*- coding: utf-8 -*-

from django.contrib import admin
from accounts.models import *



class AccountAdmin(admin.ModelAdmin):
    list_display=["loginId","investor","companyListDisplay","accountBillType","demo","tradingAllowed","lotSize"]
admin.site.register(Account,AccountAdmin)
    
class AccountServerAdmin(admin.ModelAdmin):
    list_display = ["companyListDisplay","name","address"]
admin.site.register(AccountServer,AccountServerAdmin)

class AccountBillTypeAdmin(admin.ModelAdmin):
    list_display = ["code","name"]
admin.site.register(AccountBillType,AccountBillTypeAdmin)

class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ["companyListDisplay","name"]
admin.site.register(AccountType,AccountTypeAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display=["logoIcoListDisplay","name","timeZone"]
admin.site.register(Company,CompanyAdmin)

class CurrencyAdmin(admin.ModelAdmin):
    list_display=["code","name"]
admin.site.register(Currency,CurrencyAdmin)

class InvestorAdmin(admin.ModelAdmin):
    list_display=["name","email","phone"]
admin.site.register(Investor,InvestorAdmin)
    
class TimeZoneAdmin(admin.ModelAdmin):
    list_display=["code","name","offset"]
admin.site.register(TimeZone,TimeZoneAdmin)



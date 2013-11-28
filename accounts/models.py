## -*- coding: utf-8 -*-
from django.db import models



# Create your models here.


class TimeZone(models.Model):
	code = models.CharField("代码",max_length=256)
	name = models.CharField("时区",max_length=256)
	timeOffset = models.IntegerField("时差")


class Company(models.Model):
	name = models.CharField("公司名称",max_length=256)
	timeZone = models.ForeignKey(TimeZone,verbose_name="时区")            # 后需要改为对应的类型


class Account(models.Model):
	userId = models.IntegerField("账户号")	
	traderPassword =  models.CharField("交易密码",max_length=256)
	investorPassword = models.CharField("投资人密码",max_length=256)
	phonePassword = models.CharField("手机密码",max_length=256)	
	company = models.CharField("交易商",max_length=256)         # 需要改为配置
	currency = models.CharField("资金类型",max_length=256)      # 需要改配置
	leverage = models.IntegerField("杠杆倍数")   # 需要改为配置
	server = models.CharField("服务器地址",max_length=256)
        accountType = models.CharField("账户类型",max_length=256)   # 后续需要改称可配置
	lotSzie = models.IntegerField("交易手数")    
	tradingAllowed = models.IntegerField("是否允许交易") # 需要改为布尔型
	





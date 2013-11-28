## -*- coding: utf-8 -*-
from django.db import models



# Create your models here.


class TimeZone(models.Model):
	code = models.CharField("代码",max_length=256)
	name = models.CharField("时区",max_length=256)
	timeOffset = models.IntegerField("时差")


class Company(models.Model):
	name = models.CharField("公司名称",max_length=256)
	logoIco = models.ImageField("商标",upload_to="logoico")
	timeZone = models.ForeignKey(TimeZone,verbose_name="时区")           
	terminalUrl = models.CharField("交易终端下载地址",max_length=512)
	
class AccountType(models.Model):
	company = models.ForeignKey(Company,verbose_name="交易商")
	name = models.CharField("名称",max_length=256)


class Currency(models.Model):
	code = models.CharField("代码",max_length=256)
	name = models.CharField("名称",max_length=256)

class Account(models.Model):
	userId = models.IntegerField("账户号")	
	traderPassword =  models.CharField("交易密码",max_length=256)
	investorPassword = models.CharField("投资人密码",max_length=256)
	phonePassword = models.CharField("手机密码",max_length=256)	
	company = models.ForeignKey(Company,verbose_name="交易商")         
	currency = models.ForeignKey(Currency,verbose_name="资金类型")      
	leverage = models.IntegerField("杠杆倍数")   
	server = models.CharField("服务器地址",max_length=512)
        accountType = models.ForeignKey(AccountType,verbose_name="账户类型")  
	tradingAllowed = models.BooleanField("是否允许交易") 
	lotSzie = models.IntegerField("交易手数")    
	





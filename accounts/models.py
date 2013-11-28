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


class AccountBillType(models.Model):
	name = models.CharField("名称",max_length=256)	



class Currency(models.Model):
	code = models.CharField("代码",max_length=256)
	name = models.CharField("名称",max_length=256)

class Investor(models.Model):
	name = models.CharField("姓名",max_length=256)
	email = models.CharField("电子邮件",max_length=256)
	phone = models.CharField("电话",max_length=256)
	address = models.CharField("通讯地址",max_length=256)
	im = models.CharField("即时通讯",max_length=256)
	identityInfo = models.CharField("证件信息",max_length=256)
	bankcard = models.CharField("银行卡号",max_length=256)


class Account(models.Model):
	loginId = models.IntegerField("账户号")	
	company = models.ForeignKey(Company,verbose_name="交易商")         
	traderPassword =  models.CharField("交易密码",max_length=256)
	investorPassword = models.CharField("投资人密码",max_length=256)
	phonePassword = models.CharField("手机密码",max_length=256)	
	currency = models.ForeignKey(Currency,verbose_name="资金类型")      
	leverage = models.IntegerField("杠杆倍数")   
	server = models.CharField("服务器地址",max_length=512)
        accountType = models.ForeignKey(AccountType,verbose_name="账户类型")  
	rebatePerLot = models.IntegerField("手均返佣")
	tradingAllowed = models.BooleanField("是否允许交易") 
	lotSzie = models.IntegerField("交易手数")   
	investor = models.ForeignKey(Investor,verbose_name="投资人")
	accountBillType = models.ForeignKey(AccountBillType,verbose_name="结算类型")
	
	





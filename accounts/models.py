#  -*- coding: utf-8 -*-
from django.db import models

# 交易账户管理相关数据模型定义



class TimeZone(models.Model):
    def __unicode__(self):
        return self.name
    code = models.CharField("代码",max_length=256)
    name = models.CharField("时区",max_length=256)
    offset = models.IntegerField("时差")
    class Meta:
        verbose_name = "时区表"
        verbose_name_plural = "(01)时区表"

class Company(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField("公司名称",max_length=256)
    logoIco = models.ImageField("商标",upload_to="company/logoico")
    timeZone = models.ForeignKey(TimeZone,verbose_name="时区")           
    terminalUrl = models.CharField("交易终端下载地址",max_length=512)
    def logoIcoListDisplay(self):
        return  u"<img src='%s' height='30' width='30'  />" %  self.logoIco.url
    logoIcoListDisplay.allow_tags = True
    class Meta:
        verbose_name = "交易商"
        verbose_name_plural = "(02)交易商"

class AccountType(models.Model):
    def __unicode__(self):
        return "%s--%s" % (self.company,self.name)
    company = models.ForeignKey(Company,verbose_name="交易商")
    name = models.CharField("名称",max_length=256)
    class Meta:
        verbose_name = "账户类型"
        verbose_name_plural = "(03)账户类型"
    def companyListDisplay(self):
        return  u"<img src='%s' height='15' width='15'  /> %s" % (self.company.logoIco.url,self.company)
    companyListDisplay.allow_tags = True
    companyListDisplay.short_description = "交易商"

class AccountServer(models.Model):
    def __unicode__(self):
        return "%s--%s" % (self.company,self.name)
    company = models.ForeignKey(Company,verbose_name="交易商")
    name = models.CharField("名称",max_length=256)
    address = models.CharField("地址",max_length=512)
    class Meta:
        verbose_name = "服务器"
        verbose_name_plural = "(04)服务器"        
    def companyListDisplay(self):
        return  u"<img src='%s' height='15' width='15'  /> %s" % (self.company.logoIco.url,self.company)
    companyListDisplay.allow_tags = True
    companyListDisplay.short_description = "交易商"


class AccountBillType(models.Model):
    def __unicode__(self):
        return self.name
    code = models.CharField("代码",max_length=30)
    name = models.CharField("名称",max_length=256)	
    class Meta:
        verbose_name = "结算类型"
        verbose_name_plural = "(05)结算类型"
    

class Currency(models.Model):
    def __unicode__(self):
        return "%s(%s)" % (self.name,self.code)
    code = models.CharField("代码",max_length=256)
    name = models.CharField("名称",max_length=256)
    class Meta:
        verbose_name = "资金类型"
        verbose_name_plural = "(06)资金类型"

class Investor(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField("姓名",max_length=256)
    email = models.CharField("电子邮件",max_length=256)
    phone = models.CharField("电话",max_length=256)
    address = models.CharField("通讯地址",max_length=256)
    im = models.CharField("即时通讯",max_length=256)
    identityInfo = models.CharField("证件信息",max_length=256)
    bankcard = models.CharField("银行卡号",max_length=256)
    class Meta:
        verbose_name = "投资人"
        verbose_name_plural = "(07)投资人"

class Account(models.Model):
    def __unicode__(self):
        return u"%d(%s,%s)" % (self.loginId,self.investor,self.company)
    loginId = models.IntegerField("账户号")	
    company = models.ForeignKey(Company,verbose_name="交易商")         
    traderPassword =  models.CharField("交易密码",max_length=256)
    investorPassword = models.CharField("投资人密码",max_length=256)
    phonePassword = models.CharField("手机密码",max_length=256)	
    currency = models.ForeignKey(Currency,verbose_name="资金类型")      
    leverage = models.IntegerField("杠杆倍数")   
    server = models.ForeignKey(AccountServer,verbose_name="服务器地址")
    accountType = models.ForeignKey(AccountType,verbose_name="账户类型")  
    rebatePerLot = models.FloatField("手均返佣($)")
    tradingAllowed = models.BooleanField("是否允许交易") 
    lotSize = models.FloatField("交易手数")   
    investor = models.ForeignKey(Investor,verbose_name="投资人")
    accountBillType = models.ForeignKey(AccountBillType,verbose_name="结算类型")
    demo = models.BooleanField("模拟账户")
    accountLevel = models.IntegerField("账户级别($)")
    def companyListDisplay(self):
        return  u"<img src='%s' height='15' width='15'  /> %s" % (self.company.logoIco.url,self.company)
    companyListDisplay.allow_tags = True
    companyListDisplay.short_description = "交易商"
    class Meta:
        verbose_name = "交易账户"
        verbose_name_plural = "(08)交易账户"


    		





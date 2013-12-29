# -*- coding:utf-8 -*- 
from django.db import models
from accounts.models import *

class Expert(models.Model):
    def __unicode__(self):
        return self.code
    code = models.CharField("代码",max_length=256)
    name = models.CharField("名称",max_length=256)
    class Meta:
        verbose_name = "(01)智能交易"
        verbose_name_plural = "(01)智能交易"

class ExpertInstance(models.Model):
    def __unicode__(self):
        return unicode("%s(%s)[%d]" % (self.expert.name,self.expert.code,self.id))
    token = models.CharField("更新令牌",max_length=256)
    # machine = models.ForeignKey(Machine,"挂线机")    代挂线机模块完成后加入
    expert = models.ForeignKey(Expert,verbose_name="智能交易")
    account = models.ForeignKey(Account,verbose_name="账户")
    accountType = models.ForeignKey(AccountType,verbose_name="账户类型")  # new field 
    tradingAllowed = models.BooleanField("是否允许交易")
    lotSize = models.FloatField("交易手数")
    positionCount = models.IntegerField("当前头寸数")
    floatProfit = models.FloatField("浮动盈亏")
    state = models.BooleanField("运行")
    createTime = models.DateTimeField("创建时间")             # new field 
    stateTime = models.DateTimeField("状态更新时间")
    endTime = models.DateTimeField("结束时间",blank=True,null=True)       # new field
    class Meta:
        verbose_name = "(02)交易实例"
        verbose_name_plural = "(02)交易实例"

class OrderType(models.Model):
    orderTypeId = models.IntegerField(verbose_name="类型标识")
    orderTypeName = models.CharField("类型名称",max_length="256")

class TradingOrder(models.Model):
    expertInstance = models.ForeignKey(ExpertInstance,verbose_name="交易实例")
    ticket = models.IntegerField("订单号")
    symbol = models.CharField("交易品种",max_length="256")
    orderType = models.ForeignKey(OrderType,verbose_name="订单类型")
    openTime = models.DateTimeField("开仓时间")
    openPrice = models.FloatField("开仓价格")
    closeTime = models.DateTimeField("平仓价格")
    closePrice = models.FloatField("平仓价格")
    lots = models.FloatField("交易手数")
    stopLoss = models.FloatField("止损水平")
    takeProfit = models.FloatField("止赢水平")
    comment = models.FloatField("订单注释")
    commission = models.FloatField("手续费")
    swap = models.FloatField("库存费")
    expiration = models.DateTimeField("过期时间")
    magicNumber = models.IntegerField("订单标识")
    profit = models.FloatField("获利")





# -*- coding:utf-8 -*- 
from django.db import models
from accounts.models import Account

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
    tradingAllowed = models.BooleanField("是否允许交易")
    lotSize = models.DecimalField("交易手数",max_digits=4,decimal_places=2)
    positionCount = models.IntegerField("当前头寸数")
    floatProfit = models.DecimalField("浮动盈亏",max_digits=12,decimal_places=2)
    stateTime = models.DateTimeField("状态更新时间")
    class Meta:
        verbose_name = "(02)交易实例"
        verbose_name_plural = "(02)交易实例"



# -*- coding:utf-8 -*- 
from django.db import models

# Create your models here.
class DFX_FinanceEvent(models.Model):
    def __unicode__(self):
        return self.event
    time = models.DateTimeField("时间")    
    currency = models.CharField("货币",max_length=256)
    event = models.CharField("事件",max_length=1000)
    class Meta:
        verbose_name = "财经事件"
    verbose_name_plural = "(01)财经事件"

class DFX_Holiday(models.Model):
    def __unicode__(self):
        return self.holiday
    date = models.DateField("日期")
    currency = models.CharField("货币",max_length=256)
    holiday = models.CharField("假期",max_length=256)
    class Meta:
        verbose_name = "各国假期"
    verbose_name_plural = "(02)各国假期"

class DFX_FinanceData(models.Model):
    def __unicode__(self):
        return self.event
    time = models.DateTimeField("时间")
    event = models.CharField("事件",max_length=1000)
    grade = models.CharField("重要性",max_length=50)
    previous = models.CharField("前值",max_length=256)
    forecast = models.CharField("市场预测",max_length=256)
    result = models.CharField("结果",max_length=256)
    class Meta:
        verbose_name = "财经数据"
    verbose_name_plural = "(03)财经数据"







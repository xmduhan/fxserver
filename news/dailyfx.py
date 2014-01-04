# -*- coding: utf-8 -*-

import urllib,urllib2,chardet
from HTMLParser import HTMLParser
from datetime import datetime,timedelta
from models import *


class FinanceDataParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.div = 0
        self.fdata = 0
        self.table = 0
        self.tr = 0
        self.td = 0
        self.row = []
        self.dataset = []
        self.tddata = ""
    def handle_starttag(self, tag, attrs):
        if tag.upper() == "DIV":
            self.div += 1
        if tag.upper() == "TABLE":
            self.table += 1
        if tag.upper() == "TR":
            self.tr += 1
        if tag.upper() == "TD":
            self.td += 1
            if self.fdata == 1 and self.td == 2:
                self.tddata = ""

    def handle_endtag(self, tag):
        if tag.upper() == "DIV":
            self.div -= 1
        if tag.upper() == "TABLE":
            self.table -= 1
        if tag.upper() == "TR":
            if self.fdata == 1 and self.tr == 2:      # 数据在第2层的嵌套表中
                if len(self.row) == 7 :
                    self.dataset.append(self.row)
                self.row=[]
            self.tr -= 1
        if tag.upper() == "TD":
            if self.fdata == 1 and self.td == 2:      # 数据在第2层的嵌套表中            
                self.row.append(self.tddata)
            self.td -= 1

    def handle_data(self, data):
        if self.div > 1 :
            if data == "财经数据":
                self.fdata = 1
        if self.fdata == 1 and self.td == 2:          # 数据在第2层嵌套表
            self.tddata += data

class FinanceEventParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.div = 0
        self.fdata = 0
        self.table = 0
        self.tr = 0
        self.td = 0
        self.row = []
        self.nrow = 0
        self.dataset = []
        self.tddata = ""

    def handle_starttag(self, tag, attrs):
        if tag.upper() == "DIV":
            self.div += 1
        if tag.upper() == "TABLE":
            self.table += 1
        if tag.upper() == "TR":
            self.tr += 1
        if tag.upper() == "TD":
            self.td += 1            
            if self.fdata == 1 and self.td == 1:
                self.tddata = ""
    def handle_endtag(self, tag):
        if tag.upper() == "DIV":
            self.div -= 1
        if tag.upper() == "TABLE":
            self.table -= 1
        if tag.upper() == "TR":
            if self.fdata == 1 and self.tr == 1:
                if self.nrow != 0 :
                    if len(self.row) == 4:
                        self.dataset.append(self.row)
                    self.row=[]
                self.nrow += 1
            self.tr -= 1
        if tag.upper() == "TD":
            if self.fdata == 1 and self.td == 1:
                self.row.append(self.tddata)                
            self.td -= 1
    def handle_data(self, data):
        if self.div > 1 :
            if data == "财经事件":
                self.fdata = 1
            if data == "世界各国假期":
                self.fdata = 0
        if self.fdata == 1 and self.td == 1:
            self.tddata += data


class HolidayParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.div = 0
        self.fdata = 0
        self.table = 0
        self.tr = 0
        self.td = 0
        self.row = []
        self.nrow = 0
        self.dataset = []
        self.tddata = ""

    def handle_starttag(self, tag, attrs):
        if tag.upper() == "DIV":
            self.div += 1
        if tag.upper() == "TABLE":
            self.table += 1
        if tag.upper() == "TR":
            self.tr += 1
        if tag.upper() == "TD":
            self.td += 1
            if self.fdata == 1 and self.td == 1:
                self.tddata = ""

    def handle_endtag(self, tag):
        if tag.upper() == "DIV":
            self.div -= 1
        if tag.upper() == "TABLE":
            self.table -= 1
        if tag.upper() == "TR":
            if self.fdata == 1 and self.tr == 1:
                if self.nrow != 0 :
                    self.dataset.append(self.row)
                    self.row=[]
                self.nrow += 1
            self.tr -= 1
        if tag.upper() == "TD":            
            if self.fdata == 1 and self.td == 1:
                self.row.append(self.tddata)                
            self.td -= 1
    def handle_data(self, data):
        if self.div > 1 :
            if data == "世界各国假期":
                self.fdata = 1
            if data == "财经数据":
                self.fdata = 0
        if self.fdata == 1 and self.td == 1:
            self.tddata += data



def printDataset(dataset):
    for i in range(0,len(dataset)):
        row = dataset[i]
        cols=[]
        for j in range(0,len(row)):
            cols.append(row[j])
        print(str(i) + ":" + (",".join(cols)))


def getData(day):
    data = {"type":"calendar","date":day}
    postData = urllib.urlencode(data)
    url = "http://cdn.dailyfx.com.hk/inc/process.php"
    req = urllib2.Request(url, postData)
    response = urllib2.urlopen(req)
    content = response.read()
    result = {}
    # 读取金融数据发布信息
    financeDataParser = FinanceDataParser()
    financeDataParser.feed(content)
    financeData = financeDataParser.dataset
    if len(financeData) == 1 and financeData[0][0].find("没有财经数据") != -1:
        result["FinanceData"] = []
    else:
        result["FinanceData"] = financeData    
    
    # 读取金融事件信息
    financeEventParser = FinanceEventParser()
    financeEventParser.feed(content)       
    financeEvent = financeEventParser.dataset
    if len(financeEvent) == 1 and financeEvent[0][0].find("没有财经事件") != -1:
        result["FinanceEvent"] = []
    else:
        result["FinanceEvent"] = financeEvent
    # 读取假期信息
    holidayParser = HolidayParser()
    holidayParser.feed(content)
    holiday = holidayParser.dataset
    if len(holiday) == 1 and holiday[0][0].find("没有假期") != -1:
        result["Holiday"] = [] 
    else:    
        result["Holiday"] = holiday
    # 返回数据
    return result

def update(day):
    res = getData(day)
    
    # 读取金融数据
    financeData = res["FinanceData"]
    for i in range(0,len(financeData)):
        row = financeData[i]        
        if len(row[1]) == 0 :            
            hh24 = "00:00"
        else:
            hh24 = row[1]
        time = datetime.strptime(row[0] + " " + hh24,"%Y-%m-%d %H:%M")
        event = row[2]
        grade = row[3]
        previous = row[4]
        forecast = row[5]
        result = row[6]
        
        # 检查数据是否存在
        listDFX_FinanceData = DFX_FinanceData.objects.filter(time=time,event=event)
        if len(listDFX_FinanceData) == 0 :
            # 不存在，新建数据
            dfx_FinanceData = DFX_FinanceData()        
        else:
            # 已经存在，将其更新
            dfx_FinanceData = listDFX_FinanceData[0]

        # 保存数据
        dfx_FinanceData.time = time
        dfx_FinanceData.event = event
        dfx_FinanceData.grade = grade
        dfx_FinanceData.previous = previous
        dfx_FinanceData.forecast = forecast
        dfx_FinanceData.result = result
        dfx_FinanceData.save()

    # 读取金融事件   
    financeEvent = res["FinanceEvent"]
    for i in range(0,len(financeEvent)):        
        row = financeEvent[i]
        if len(row[1]) == 0 :            
            hh24 = "00:00"
        else:
            hh24 = row[1]
        time = datetime.strptime(row[0] + " " + hh24,"%Y-%m-%d %H:%M")
        currency = row[2]
        event = row[3]

        # 检查数据是否存在
        listDFX_FinanceEvent = DFX_FinanceEvent.objects.filter(time=time,event=event)
        if len(listDFX_FinanceEvent) == 0:
            # 不存在，新建数据
            dfx_FinanceEvent = DFX_FinanceEvent()
        else:
            # 已经存在，将其更新
            dfx_FinanceEvent = listDFX_FinanceEvent[0]

        # 保存数据
        dfx_FinanceEvent.time = time
        dfx_FinanceEvent.currency = currency
        dfx_FinanceEvent.event = event
        dfx_FinanceEvent.save()


    # 读取各国假期
    Holiday = res["Holiday"]
    for i in range(0,len(Holiday)):
        row = Holiday[i]
        date = datetime.strptime(row[0],"%Y-%m-%d")
        currency =  row[1]
        holiday = row[2]
        
        # 检查数据是否存在
        listDFX_Holiday = DFX_Holiday.objects.filter(
            date=date,currency=currency,holiday=holiday
        )
        if len(listDFX_Holiday) == 0 :
            # 不存在添加数据
            dfx_Holiday = DFX_Holiday()
        else:
            dfx_Holiday = listDFX_Holiday[0]

        # 保存数据
        dfx_Holiday.date = date
        dfx_Holiday.currency = currency
        dfx_Holiday.holiday = holiday
        dfx_Holiday.save()
        
def updateBetween(beginDay,endDay):
    beginDate = datetime.strptime(beginDay,"%Y-%m-%d")
    endDate = datetime.strptime(endDay,"%Y-%m-%d")
    for i in range(0,(endDate-beginDate).days + 1) :
        day = (beginDate + timedelta(i)).strftime("%Y-%m-%d")
        try:
            update(day)
            print(day+" : ok")
        except Exception as e:            
            print(day+" : failed",e)
            raise
            

    
    




#data = {"type":"calendar","date":"2014-01-01",}
#postData = urllib.urlencode(data)
#url = "http://cdn.dailyfx.com.hk/inc/process.php"
#req = urllib2.Request(url, postData)
#response = urllib2.urlopen(req)
#content = response.read()
#print(chardet.detect(content))
#print("-----------------------------------")
#fdp = FinanceDataParser()
#fdp.feed(content)
#printDataset(fdp.dataset)
#print("-----------------------------------")
#fep = FinanceEventParser()
#fep.feed(content)
#printDataset(fep.dataset)
#print("-----------------------------------")
#hp = HolidayParser()
#hp.feed(content)
#printDataset(hp.dataset)



#res = getData("2013-12-05")
#printDataset(res["FinanceData"])
#print("-----------------------------------")
#printDataset(res["FinanceEvent"])
#print("-----------------------------------")
#printDataset(res["Holiday"])








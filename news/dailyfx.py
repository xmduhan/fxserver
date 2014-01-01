# -*- coding: utf-8 -*-

import urllib,urllib2,chardet
from HTMLParser import HTMLParser


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

    def handle_starttag(self, tag, attrs):
        if tag.upper() == "DIV":
            self.div += 1
        if tag.upper() == "TABLE":
            self.table += 1
        if tag.upper() == "TR":
            self.tr += 1
        if tag.upper() == "TD":
            self.td += 1

    def handle_endtag(self, tag):
        if tag.upper() == "DIV":
            self.div -= 1
        if tag.upper() == "TABLE":
            self.table -= 1
        if tag.upper() == "TR":
            if self.fdata == 1 and self.tr == 2:      # 数据在第2层的嵌套表中
                self.dataset.append(self.row)
                self.row=[]
            self.tr -= 1
        if tag.upper() == "TD":
            self.td -= 1

    def handle_data(self, data):
        if self.div > 1 :
            if data == "财经数据":
                self.fdata = 1
        if self.fdata == 1 and self.td == 2:          # 数据在第2层嵌套表
            self.row.append(data)


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

    def handle_starttag(self, tag, attrs):
        if tag.upper() == "DIV":
            self.div += 1
        if tag.upper() == "TABLE":
            self.table += 1
        if tag.upper() == "TR":
            self.tr += 1
        if tag.upper() == "TD":
            self.td += 1
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
            self.td -= 1
    def handle_data(self, data):
        if self.div > 1 :
            if data == "财经事件":
                self.fdata = 1
            if data == "世界各国假期":
                self.fdata = 0
        if self.fdata == 1 and self.td == 1:
            self.row.append(data)


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

    def handle_starttag(self, tag, attrs):
        if tag.upper() == "DIV":
            self.div += 1
        if tag.upper() == "TABLE":
            self.table += 1
        if tag.upper() == "TR":
            self.tr += 1
        if tag.upper() == "TD":
            self.td += 1
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
            self.td -= 1
    def handle_data(self, data):
        if self.div > 1 :
            if data == "世界各国假期":
                self.fdata = 1
            if data == "财经数据":
                self.fdata = 0
        if self.fdata == 1 and self.td == 1:
            self.row.append(data)




def printDataset(dataset):
    for i in range(0,len(dataset)):
        row = dataset[i]
        cols=[]
        for j in range(0,len(row)):
            cols.append(row[j])
        print(str(i) + ":" + (",".join(cols)))


def getDailyfxData(day):
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
    if len(financeData) == 1 and financeData[0][2].find("没有财经数据") != -1:
        result["FinanceData"] = []
    else:
        result["FinanceData"] = financeData    
    
    # 读取金融事件信息
    financeEventParser = FinanceEventParser()
    financeEventParser.feed(content)       
    financeEvent = financeEventParser.dataset
    if len(financeEvent) == 1 and financeEvent[0][2].find("没有财经事件") != -1:
        result["FinanceEvent"] = []
    else:
        result["FinanceEvent"] = financeEvent
    # 读取假期信息
    holidayParser = HolidayParser()
    holidayParser.feed(content)
    holiday = holidayParser.dataset
    if len(holiday) == 1 and holiday[0][2].find("没有假期") != -1:
        result["Holiday"] = [] 
    else:    
        result["Holiday"] = holiday
    # 返回数据
    return result


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



res = getDailyfxData("2013-12-05")
printDataset(res["FinanceData"])
print("-----------------------------------")
printDataset(res["FinanceEvent"])
print("-----------------------------------")
printDataset(res["Holiday"])








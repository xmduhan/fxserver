# -*- coding:utf-8 -*-
from django.http import HttpResponse
from models import *
import json

def packResult(errcode=0, errmsg="", data={}):
    result = {}
    result["errcode"] = errcode
    result["errmsg"] = errmsg
    result["data"] = data 
    return json.dumps(result)

def expertRegister(request):

    # 读取智能交易代码
    try:
        expertCode = request.POST("ExpertCode")
    except:
        return HttpResponse(packResult(-1,"需要提供智能交易代码(ExpertCode)",{}))
    
    # 读取当前登录账户号
    try:
        accountLoginId = request.POST("AccountLoginId")
    except:
        return HttpResponse(packResult(-1,"需要提供账户号(AccountLoginId)",{}))
        
    # 读取服务器名称 
    try:
        accountServerName = request.POST("AccountServerName")
    except: 
        return HttpResponse(packResult(-1,"需要提供服务器名称(AccountServerName)",{}))

    # 准备读取和生成相关数据    
    expertInstance = ExpertInstance()

    # 生成更新令牌
    expertInstance.token = "".join(random.sample(string.uppercase+string.digits,8))
        
    # 读取智能交易配置数据
    expertList = Expert.objects.filter(code=expertCode)
    if len(expertList) <> 0 :       
       expert = expertList[0]
    else:
         # 不存在则新建
        expert = Expert()
        expert.code = expertCode
        expert.name = "未命名(%)" % expertCode
    expertInstance.expert = expert

    # 读取交易账户信息
    accountList = Account.objects.filter(loginId=accountLoginId,server__name=accountServerName)
    if len(accountList) <> 0 :
       account = accountList[0]
    else:
        return HttpResponse(packResult(-1,"账户配置不存在",{}))    
    expertInstance.account = account

    # 保存实例信息
    expertInstance.tradingAllowed = account.tradingAllowed
    expertInstance.lotSzie = account.lotSize
    expertInstance.positionCount = 0
    expertInstance.floatProfit = 0    
    expertInstance.save()
    
    # 准备返回给客户端的信息
    data = {}
    data["ExpertInstanceId"] = expertInstance.id
    data["token"] = expertInstance.token
    data["AccountType"] = expertInstance.account.accountType
    data["TrandingAllowed"] = expertInstance.tradingAllowed
    data["LotSize"] = expertInstance.losSize    
        
    return HttpResponse(packResult(0,"成功",data))


# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.utils import timezone
from django.db import transaction
from models import *
import json,random,string


def packResult(errcode=0, errmsg="", data={}):
    result = {}
    result["errcode"] = errcode
    result["errmsg"] = errmsg
    result["data"] = data 
    #print(result)
    return json.dumps(result)

@transaction.atomic
def expertRegister(request):
    
    # 读取智能交易代码
    try:
        expertCode = request.POST["ExpertCode"]
        if len(expertCode) == 0:
            raise
    except:
        return HttpResponse(packResult(-1,"Need to provide ExpertCode.",{}))
    
    # 读取当前登录账户号
    try:
        accountLoginId = request.POST["AccountLoginId"]
        if len(accountLoginId) == 0:
            raise
    except:
        return HttpResponse(packResult(-1,"Need to provide AccountLoginId.",{}))
        
    # 读取交易商名称
    try:
        accountCompanyName = request.POST["AccountCompanyName"]
        if len(accountCompanyName) == 0:
            raise
    except:
        return HttpResponse(packResult(-1,"Need to provide AccountCompanyName.",{}))           
    
    # 读取服务器名称 
    try:
        accountServerName = request.POST["AccountServerName"]
        if len(accountServerName) == 0:
            raise
    except: 
        return HttpResponse(packResult(-1,"Need to provide AccountServerName.",{}))

    # 准备读取和生成相关数据    
    expertInstance = ExpertInstance()

    # 生成更新令牌
    expertInstance.token = "".join(random.sample(string.uppercase+string.digits,8))
    
    # 数据库事务开始
    sp = transaction.savepoint()    
    # 读取智能交易配置数据
    expertList = Expert.objects.filter(code=expertCode)
    if len(expertList) <> 0 :       
        expert = expertList[0]
    else:
         # 不存在则新建
        expert = Expert()
        expert.code = expertCode
        expert.name = u"未命名(%s)"  % expertCode        
        expert.save()             
    expertInstance.expert = expert

    # 读取交易账户信息
    accountList = Account.objects.filter(
        loginId=accountLoginId,
        server__name=accountServerName,
        company__name=accountCompanyName
    )
    if len(accountList) <> 0 :
       account = accountList[0]
    else:
        transaction.savepoint_rollback(sp)    # 回滚可能已经写入的expert对象
        return HttpResponse(packResult(-1,"Account information or config is invalid.",{}))    
    expertInstance.account = account

    # 保存实例信息
    #print("account.losSzie=",account.lotSize)
    expertInstance.tradingAllowed = account.tradingAllowed
    expertInstance.lotSize = account.lotSize
    expertInstance.accountType = account.accountType
    expertInstance.positionCount = 0
    expertInstance.floatProfit = 0    
    expertInstance.state = "A"  
    expertInstance.createTime = timezone.now()
    expertInstance.stateTime = timezone.now()
    expertInstance.save()
        
    # 数据库事务结束

    # 准备返回给客户端的信息
    data = {}
    data["ExpertInstanceId"] = expertInstance.id
    data["Token"] = expertInstance.token
    data["AccountTypeName"] = expertInstance.account.accountType.name
    data["TradingAllowed"] = expertInstance.tradingAllowed
    data["LotSize"] = expertInstance.lotSize    
    #print(data)        
    return HttpResponse(packResult(0,"Succeed!",data))


@transaction.atomic
def expertUnregister(request):
    
    # 读取Eexpert实例标识
    try:
        expertInstanceId = request.POST["ExpertInstanceId"]
        if len(expertInstanceId) == 0:
            raise
    except:
        return HttpResponse(packResult(-1,"Need to provide ExpertInstanceId.",{}))
    
    # 读取Expert Instance更新令牌
    try:
        token = request.POST["Token"]
        if len(token) == 0:
            raise    
    except:
        return HttpResponse(packResult(-1,"Need to provide Token.",{}))
    
    # 检查实例是否存在
    expertInstanceList = ExpertInstance.objects.filter(id = expertInstanceId)
    if len(expertInstanceList) == 0:
        return HttpResponse(packResult(-1,"ExpertInstance is not exist",{}))
    expertInstance = expertInstanceList[0]

    # 检查令牌是否正确
    if expertInstance.token != token:
        return HttpResponse(packResult(-1,"ExpertInstanceId and Token is not matched.",{}))
    
    # 检查Expert Instance是否失效
    if expertInstance.state != True:
        #print("expertInstance.state=",expertInstance.state)
        return HttpResponse(packResult(-1,"ExpertInstance is not active",{}))     
    
    # 更新ExpertInstance状态未失效
    expertInstance.state = False
    expertInstance.stateTime = timezone.now()   
    expertInstance.save()
    
    return HttpResponse(packResult(0,"Succeed!",{}))

'''

@transaction.atomic
def expertInfomation(request):
    pass

'''

@transaction.atomic
def tradingOrder(request):
    print(request.POST)
    print(request.BODY)
    return HttpResponse(packResult(0,"Succeed!",{}))









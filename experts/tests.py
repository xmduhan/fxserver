# -*- coding:utf-8 -*- 
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json,random,string
from django.test import TestCase
from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from django.db import transaction
from accounts.models import Account
from experts.models import Expert

class ExpertIntanceTest(TransactionTestCase):
    # (1)账户和智能交易配置都存在的情况
    def test_expertRegister_1(self):

        # 尝试获取一个测试账户配置
        accountList = Account.objects.all()
        self.assertNotEqual(len(accountList),0)
        account = accountList[0]
       
        # 尝试获取一个智能交易配置
        expertList = Expert.objects.all()
        self.assertNotEqual(len(expertList),0)
        expert = expertList[0]   

        # 提交数据给服务
        url = reverse("experts:service.expertRegister")
        postData = {}
        postData["ExpertCode"] = expert.code
        postData["AccountLoginId"] = account.loginId
        postData["AccountServerName"] = account.server.name
        response = self.client.post(url,postData)
        
        # 检查返回状态               
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertIn("errcode",result)
        self.assertEqual(result["errcode"],0)
        
        # 检查数据完整性
        self.assertIn("data",result)
        data = result["data"]        
        self.assertIn("ExpertInstanceId",data)
        self.assertIn("Token",data)
        self.assertEqual(len(data["Token"]),8)
        self.assertIn("TradingAllowed",data)
        self.assertEqual(data["TradingAllowed"],account.tradingAllowed)
        self.assertIn("LotSize",data)
        self.assertEqual(data["LotSize"],account.lotSize)
        self.assertIn("AccountTypeName",data)
        self.assertEqual(data["AccountTypeName"],account.accountType.name)      
    
    # 交易账户存在，智能交易配置不存在的情况
    def test_expertRegister_2(self):
          
        # 尝试获取一个测试账户配置
        accountList = Account.objects.all()
        self.assertNotEqual(len(accountList),0)
        account = accountList[0]
       
        # 随机生成一个expert代码
        expertCode = "".join(random.sample(string.ascii_letters,20))
       
        # 提交数据给服务
        url = reverse("experts:service.expertRegister")
        postData = {}
        postData["ExpertCode"] = expertCode
        postData["AccountLoginId"] = account.loginId
        postData["AccountServerName"] = account.server.name
        response = self.client.post(url,postData)

        # 检查返回状态               
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertIn("errcode",result)
        self.assertEqual(result["errcode"],0)
        
        # 检查数据完整性
        self.assertIn("data",result)
        data = result["data"]        
        self.assertIn("ExpertInstanceId",data)
        self.assertIn("Token",data)
        self.assertEqual(len(data["Token"]),8)
        self.assertIn("TradingAllowed",data)
        self.assertEqual(data["TradingAllowed"],account.tradingAllowed)
        self.assertIn("LotSize",data)
        self.assertEqual(data["LotSize"],account.lotSize)
        self.assertIn("AccountTypeName",data)
        self.assertEqual(data["AccountTypeName"],account.accountType.name)      

        # 检查Expert对象是否保存在数据库
        expertList = Expert.objects.filter(code=expertCode)
        self.assertEqual(len(expertList),1)

    # 交易账户不存在,智能交易配置也不存在
    def test_expertRegister_3(self):
        
        # 生成一个不存在的acount信息
        accountLoginId = string.atoi("".join(random.sample(string.digits,10)))
        accountServerName = "".join(random.sample(string.ascii_letters,30))
        
        # 随机生成一个expert代码
        expertCode = "".join(random.sample(string.ascii_letters,20))   

        # 提交数据给服务
        url = reverse("experts:service.expertRegister")
        postData = {}
        postData["ExpertCode"] = expertCode
        postData["AccountLoginId"] = accountLoginId
        postData["AccountServerName"] = accountServerName
        response = self.client.post(url,postData)

        # 检查返回状态               
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertIn("errcode",result)
        self.assertEqual(result["errcode"],-1)

        # 检查事务的完整性，expert配置是否回滚
        expertList=Expert.objects.filter(code=expertCode)
        self.assertEqual(len(expertList),0)

    #@transaction.atomic()
    def test_transaction_1(self):        
        with transaction.commit_manually():
            expert = Expert()
            expert.code = "code"
            expert.name = "name"
            expert.save()
            transaction.rollback()
        expertList = Expert.objects.filter(code="code")
        self.assertEqual(len(expertList),0)

        



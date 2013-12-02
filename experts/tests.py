# -*- coding:utf-8 -*- 
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json,random,string
from django.test import TestCase
from django.core.urlresolvers import reverse
from accounts.models import Account
from experts.models import Expert

class ExpertIntanceTest(TestCase):
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
        #print(expertCode)
       
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



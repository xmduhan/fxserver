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
        url = reverse("experts:service.ExpertRegister")
        postData = {}
        postData["ExpertCode"] = expert.code
        postData["AccountLoginId"] = account.loginId
        postData["AccountCompanyName"] = account.company.name
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
        url = reverse("experts:service.ExpertRegister")
        postData = {}
        postData["ExpertCode"] = expertCode
        postData["AccountLoginId"] = account.loginId
        postData["AccountCompanyName"] = account.company.name
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
        accountCompanyName = "".join(random.sample(string.ascii_letters,30))
        accountServerName = "".join(random.sample(string.ascii_letters,30))
        

        # 随机生成一个expert代码
        expertCode = "".join(random.sample(string.ascii_letters,20))   

        # 提交数据给服务
        url = reverse("experts:service.ExpertRegister")
        postData = {}
        postData["ExpertCode"] = expertCode
        postData["AccountLoginId"] = accountLoginId
        postData["AccountCompanyName"] = accountCompanyName
        postData["AccountServerName"] = accountServerName
        response = self.client.post(url,postData)

        # 检查返回状态               
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertIn("errcode",result)
        self.assertEqual(result["errcode"],-1)

        # 检查事务的完整性，expert配置是否回滚
        expertList=Expert.objects.filter(code=expertCode)
        self.assertEqual(len(expertList),0)        # 事务是否成功回滚

    def test_expertRegister_4(self):
        # 提交数据给服务
        url = reverse("experts:service.ExpertRegister")
        postData = {}
        # 所有数据都填空的情况
        postData["ExpertCode"] = ""
        postData["AccountLoginId"] = ""
        postData["AccountCompanyName"] = ""
        postData["AccountServerName"] = ""
        response = self.client.post(url,postData)

        # 检查返回状态               
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertIn("errcode",result)
        self.assertEqual(result["errcode"],-1)




class DatabaseTransactionTest(TransactionTestCase):

    #@transaction.atomic()
    def test_transaction_1(self):       
        #print("autocommit=",transaction.get_autocommit())        
        testcode = "".join(random.sample(string.letters,20))
        testname = "".join(random.sample(string.letters,20))        
        expert = Expert()
        expert.code = testcode
        expert.name = testname
        expert.save()

           
    def test_transaction_2(self):        
        #transaction.set_autocommit(False)
        expert = Expert()
        expert.code = "code"
        expert.name = "name"
        expert.save()
        #transaction.set_autocommit(True)

        #transaction.rollback()
        #expertList = Expert.objects.filter(code="code")
        #self.assertEqual(len(expertList),0)

    # 默认情况下调用save()，数据就写到数据库中并提交
    def test_transaction_3(self):
        testcode = "".join(random.sample(string.letters,20))
        testname = "".join(random.sample(string.letters,20))
        step = 0
        try:
            expert = Expert()
            expert.code = testcode
            expert.name = testname
            expert.save()
            step = 1
            raise
        except:  
            pass
        expertList = Expert.objects.filter(code=testcode)
        self.assertEqual(step,1)                                #  确认执行到了raise
        self.assertEqual(len(expertList),1)                     #  确认数据已经提交了
    
    # 如果使用了transaction.atiom
    def test_transaction_4(self):
        testcode = "".join(random.sample(string.letters,20))
        testname = "".join(random.sample(string.letters,20))
        step = 0
        try:
           with transaction.atomic():
                expert = Expert()
                expert.code = testcode
                expert.name = testname
                expert.save()                
                #transaction.commit()
                step = 1
                raise
        except:
            pass            
        expertList = Expert.objects.filter(code=testcode)
        self.assertEqual(step,1)                                # 确认执行到了raise
        self.assertEqual(len(expertList),0)                     # 确认数据已经被回滚了

    # 测试使用函数的事务修饰符
    def test_transaction_5(self):        
        
        testcode = "".join(random.sample(string.letters,20))
        testname = "".join(random.sample(string.letters,20))
        self.step = 0
        def test_transaction_5_1():
            expert = Expert()
            expert.code = testcode
            expert.name = testname
            expert.save()
            self.step = 1
            raise Exception()
        try:
            test_transaction_5_1()
        except:
            pass
        expertList = Expert.objects.filter(code=testcode)
        self.assertEqual(self.step,1)                                #  确认执行到了raise
        self.assertEqual(len(expertList),1)                     #  确认数据已经提交了

        testcode = "".join(random.sample(string.letters,20))
        testname = "".join(random.sample(string.letters,20))
        self.step = 0
        @transaction.atomic
        def test_transaction_5_2():            
            expert = Expert()
            expert.code = testcode
            expert.name = testname
            expert.save()            
            self.step = 1
            raise Exception()       
        try:
            test_transaction_5_2()        
        except:
            pass
        self.assertEqual(self.step,1)
        expertList = Expert.objects.filter(code = testcode)
        self.assertEqual(len(expertList),0)                     #  确认数据已经回滚了
    # 测试使用savepoint
    def test_transaction_6(self):
        testcode1 = "".join(random.sample(string.letters,20))
        testname1 = "".join(random.sample(string.letters,20))
        testcode2 = "".join(random.sample(string.letters,20))
        testname2 = "".join(random.sample(string.letters,20))
        @transaction.atomic
        def test_transaction_6_1():            
            # 插入第1个对象
            expert1 = Expert()
            expert1.code = testcode1
            expert1.name = testname1
            expert1.save()
            sp = transaction.savepoint()               #  设置事务保存点            
            
            # 插入第2个对象
            expert2 = Expert()
            expert2.code = testcode2
            expert2.name = testname2
            expert2.save()
            transaction.savepoint_rollback(sp)         # 回滚到插入第2个对象之前的状态
        
        test_transaction_6_1()
        expertList1 = Expert.objects.filter(code=testcode1)
        self.assertEqual(len(expertList1),1)
        expertList2 = Expert.objects.filter(code=testcode2)
        self.assertEqual(len(expertList2),0)
    
    # 测试关闭自动提交
    def test_transaction_7(self):
        transaction.set_autocommit(False)
        try:            
            testcode = "".join(random.sample(string.letters,20))
            testname = "".join(random.sample(string.letters,20))
            step = 0
            expert = Expert()
            expert.code = testcode
            expert.name = testname
            expert.save()
            transaction.rollback()
        finally:
            transaction.set_autocommit(True)
        
        expertList = Expert.objects.filter(code=testcode)
        self.assertEqual(len(expertList),0)
    
    # 测试在atomic事务中进行回滚
    def test_transaction_8(self):
        testcode = "".join(random.sample(string.letters,20))
        testname = "".join(random.sample(string.letters,20))
        step = 0
        try:
            with transaction.atomic():
                expert = Expert()
                expert.code = testcode
                expert.name = testname
                expert.save()
                step = 1
                transaction.rollback()             # 这原子事务中rollback是要抛异常的
        except:
            self.assertEqual(step,1)
            step=2
        self.assertEqual(step,2)
        expertList = Expert.objects.filter(code=testcode)
        self.assertEqual(len(expertList),0)
                
    
    # 测试在atomic事务中进行回滚(使用savepoint变通)
    def test_transaction_9(self):
        testcode = "".join(random.sample(string.letters,20))
        testname = "".join(random.sample(string.letters,20))
        step = 0
        try:
            with transaction.atomic():
                sp = transaction.savepoint()
                expert = Expert()
                expert.code = testcode
                expert.name = testname
                expert.save()
                transaction.savepoint_rollback(sp)           # 回滚到保存点就不抛异常了
                step = 1
        except:
            step=2
        self.assertEqual(step,1)
        expertList = Expert.objects.filter(code=testcode)
        self.assertEqual(len(expertList),0)
                
    






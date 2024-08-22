# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-7-19
# Description: 静安健康档案数据治理页面自动化更新脚本
# https://chromedriver.storage.googleapis.com/index.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.
import sys

from BasePO import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import psutil

options = Options()
options.add_argument("--start-maximized")
s = Service("d:\project\web\chromedriver.exe")
driver = webdriver.Chrome(service=s, options=options)
# print(driver.capabilities['browserVersion'])
# print(driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])
Base_PO = BasePO(driver)

class JinganPO():


    def closeApp(self, varApp):
        """关闭应用程序"""
        # closeApp("chrome.exe")
        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()

    def login(self, varUrl, varUser, varPass):
        # 登录
        driver.get(varUrl)
        Base_PO.inputId("username", varUser)
        Base_PO.inputId("password", varPass)
        Base_PO.clickId("loginBtn", 1)

    # Base_PO.clickXpath('/html/body/div/div[2]/div[2]/ul/li[1]/a', 1)
    # Base_PO.switchLabel(1)
    # sleep(2)

    # 健康档案
    # Base_PO.clickXpath('/html/body/div[1]/div/div/div[2]/ul/li[3]/a', 1)
    # Base_PO.inputId("keyword",r'310107194812044641') # 魏梅娣
    # Base_PO.clickXpath('/html/body/div[5]/div/div[1]/table/tbody/tr/td[1]/div/div', 2)
    # Base_PO.clickXpath('/html/body/div[5]/div/div[2]/div/div[2]/div[4]/div[2]/div/table/tbody/tr[3]/td[2]/div/input[1]',1)
    # 健康档案 - 基本信息



    def basicInfo(self, idCard):
        # 2，通过身份证打开用户页
        driver.get('http://172.16.209.10:9071/cdc/a/doctor/archive/detail?personcard=' + str(idCard))
        # Base_PO.switchLabel(1)
        Base_PO.clickId('one2', 1)  # 基本信息

        # todo 基本信息
        # # 姓名
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[1]/td[2]/span/span/input', '魏梅娣')
        # 民族
        Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[2]/span/span/input')
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[2]/span/span/input', '苗族')
        # 文化程度
        Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[4]/span/span/input')
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[4]/span/span/input', '小学教育')
        # 职业
        Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[4]/td[2]/span/span/input')
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[4]/td[2]/span/span/input', '军人')
        # 就业状态
        Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[5]/td[2]/span/span/input')
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[5]/td[2]/span/span/input', '其他')
        # 婚姻状况
        Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[2]/span/span/input')
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[2]/span/span/input', '离婚')
        # 工作单位
        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[4]/span/span/input', '北京科美有限公司')
        # 手机号
        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[8]/td[2]/span/span/input', '13011234567')
        # 固定电话
        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[9]/td[2]/span/span/input', '58776543')
        # 联系人姓名
        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[10]/td[2]/span/span/input', '魏梅名')
        # 联系人电话
        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[10]/td[4]/span/span/input', '13356789098')
        # 血型 ？？
        Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[2]/span/span/input')
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[2]/span/span/input', 'B型')
        # Rh血型
        Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[4]/span/span/input')
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[4]/span/span/input', '不详')
        # 医疗费用支付方式
        Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[12]/td[2]/span/span/input')
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[12]/td[2]/span/span/input', '全自费')

        # 残疾情况
        varStatus = True
        var = {"视力残疾": "2222", "语言残疾": "3333", "其他残疾": "121212"}
        currStatus = Base_PO.isCheckbox('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]/span/input')  # 无残疾是否勾选
        # cj1,默认无残疾，要求无残疾，不操作
        if currStatus == True:
            if varStatus == True:
                ...
            else:
                # cj2,默认无残疾，要求视力残疾，翻勾选无，勾选视力残疾。
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
                # 遍历勾选
                for k, v in var.items():
                    if k == '视力残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '听力残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '语言残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '肢体残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input',1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '智力残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[6]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '精神残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[7]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '其他残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]', 1)
                        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[4]/span/span/input', v)  # 残疾说明
        if currStatus == False:
            # cj3,默认视力残疾，要求无残疾，勾选无残疾。
            if varStatus == False:
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
            # cj4，默认视力残疾，要求精神残疾，操作取消所有勾选，勾选精神残疾。
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input') # 视力残疾
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input') # 听力残疾
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input') # 语言残疾
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input') # 肢体残疾
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[1]/span/input') # 智力残疾
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[2]/span/input') # 精神残疾
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]/span/input') # 其他残疾
                # 遍历勾选
                for k, v in var.items():
                    if k == '视力残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '听力残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '语言残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '肢体残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '智力残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[6]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '精神残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[7]/span/input', 1)
                        Base_PO.inputXpathClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '其他残疾':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]', 1)
                        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[4]/span/span/input', v)  # 残疾说明
        # todo 户籍地址
        var = ['北京市', '市辖区', '丰台区', '南苑街道办事处', '机场社区居委会', '洪都拉斯100号']
        # 省（自治区、直辖市）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[2]/span/span/input', var[0])
        # 市（地区/州）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[4]/span/span/input', var[1])
        # 县（区）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[6]/span/span/input', var[2])
        # 街道（镇）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[2]/span/span/input', var[3])
        # 居委（村）
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[4]/span/span/input', var[4])
        # 详细地址
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[3]/td[2]/span/span/input', var[5])

        # todo 居住地址
        # 同户籍地址
        varStatus = True
        var = ['北京市', '市辖区', '丰台区', '南苑街道办事处', '机场社区居委会', '洪都拉斯100号']
        currStatus = Base_PO.isCheckbox('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input')
        if currStatus == True:
            # cj1, 默认是勾选同户籍地址，要求也是勾选同户籍地址，不操作
            if varStatus == True:
                ...
            else:
                # cj2，默认是勾选同户籍地址，要求不勾选同户籍地址，操作反勾选同户籍地址，同时填入一下信息
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input', 1)  # 不勾选同户籍地址
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]/span/span/input', var[0])  # 省（自治区、直辖市）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[4]/span/span/input', var[1])  # 市（地区/州）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[6]/span/span/input', var[2])  # 县（区）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]/span/span/input', var[3])  # 街道（镇）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[4]/span/span/input', var[4])  # 居委（村）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]/span/span/input', var[5])  # 详细地址
        else:
            # cj3，默认是不勾选同户籍地址，要求勾选同户籍地址
            if varStatus == True:
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input', 1)
            else:
                # cj4,默认是不勾选同户籍地址，要求更新以下信息。
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]/span/span/input', var[0])   # 省（自治区、直辖市）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[4]/span/span/input', var[1])  # 市（地区/州）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[6]/span/span/input', var[2])  # 县（区）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]/span/span/input', var[3])  # 街道（镇）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[4]/span/span/input', var[4])  # 居委（村）
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]/span/span/input', var[5])  # 详细地址


        # todo 其他信息
        # # 家庭厨房排风设施标识
        # Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[2]/span/span/input')
        # Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[2]/span/span/input','烟囱')
        # # 家庭燃料类别
        # Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[4]/span/span/input')
        # Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[4]/span/span/input', '煤')
        # # 家庭饮用水类别
        # Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[6]/span/span/input')
        # Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[6]/span/span/input', '井水')
        # # 家庭厕所类别
        # Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[2]/span/span/input')
        # Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[2]/span/span/input','马桶')
        # # 家庭禽畜栏类别
        # Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[4]/span/span/input')
        # Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[4]/span/span/input','室内')

        # # 药物过敏史
        varStatus = '有'
        var = ['头孢类抗生素', '酒精', {"其他药物过敏原": '3333'}]
        # 判断默认勾选的是无还是有
        currStatus = Base_PO.getXpathAttr(u'//div[@id="signAllergy"]/table/tbody/tr/td/div/div[1]', '类与实例')
        if currStatus == "mini-radiobuttonlist-item":
            currStatus = '无'
        else:
            currStatus = '有'
        if currStatus == '无':
            # cj1,默认无，要求无，不操作
            if varStatus == '无':
                ...
            else:
                # cj2，默认无，要求有，勾选有，勾选酒精
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)
                for i in range(len(var)):
                    if var[i] == '青霉素抗生素':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[1]/input', 1)
                    if var[i] == '磺胺类抗生素':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[2]/input', 1)
                    if var[i] == '头孢类抗生素':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[3]/input', 1)
                    if var[i] == '含碘药品':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[1]/input', 1)
                    if var[i] == '酒精':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[2]/input', 1)
                    if var[i] =='镇静麻醉剂':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[3]/input', 1)
                    if isinstance(var[i], dict) == True:
                        for k1, v1 in var[i].items():
                            if k1 == '其他药物过敏原':
                                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[4]/input', 1)
                                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[5]/span/input', v1)
        else:
            # cj3,默认有，要求无，勾选无
            if varStatus == '无':
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)
            else:
                # cj4，默认有，取消所有复选框，勾选酒精
                for i in range(1, 3):
                    Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[' + str(i) + ']/input')
                for i in range(1, 4):
                    Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[' + str(i) + ']/input')
                for i in range(len(var)):
                    if var[i] == '青霉素抗生素':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[1]/input', 1)
                    if var[i] == '磺胺类抗生素':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[2]/input', 1)
                    if var[i] == '头孢类抗生素':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[3]/input', 1)
                    if var[i] == '含碘药品':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[1]/input', 1)
                    if var[i] == '酒精':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[2]/input', 1)
                    if var[i] =='镇静麻醉剂':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[3]/input', 1)
                    if isinstance(var[i], dict) == True:
                        for k1, v1 in var[i].items():
                            if k1 == '其他药物过敏原':
                                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[4]/input', 1)
                                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[5]/span/input', v1)


        # 环境危险因素暴露类别
        varStatus = False
        var = ['毒物', '化学品', {'其他': "11111"}]

        # 判断是否勾选了无
        currStatus = Base_PO.isCheckbox('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input')
        if currStatus == True:
            # cj1,默认勾选无，要求勾选无，不操作。
            if varStatus == True:
                ...
            # cj2，默认勾选无，要求勾选其他，操作取消无勾选，勾选其他
            elif varStatus == False:
                # 取消无勾选
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)
                for i in range(len(var)):
                    if var[i] == '化学品':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
                    if var[i] == '毒物':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
                    if var[i] == '射线':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
                    if var[i] == '不详':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
                    if isinstance(var[i], dict) == True:
                        for k1, v1 in var[i].items():
                            if k1 == '其他':
                                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
                                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[3]/span/span/input', v1)
        else:
            # cj3，默认不勾选无，要求勾选无，直接勾选无。
            if varStatus == True:
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)
            else:
                # cj4，默认不勾选无，要求勾选化学，操作取消所有勾选，勾选化学。
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input')  # 化学品
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input')  # 毒物
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input')  # 射线
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input')  # 不详
                Base_PO.checkboxXpathsClear('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input')  # 其他
                for i in range(len(var)):
                    if var[i] == '化学品':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
                    if var[i] == '毒物':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
                    if var[i] == '射线':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
                    if var[i] == '不详':
                        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
                    if isinstance(var[i], dict) == True:
                        for k1, v1 in var[i].items():
                            if k1 == '其他':
                                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
                                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[3]/span/span/input', v1)



        # todo 疾病信息
        # 疾病史
        # 风险1：不知道当前用户有多少疾病史，默认最多5个，全部关闭。???
        varQty = 5
        var = {'脑卒中': '2010-12-01', '其他法定传染病': ['baidu', '2020-12-10'], '高血压': '2010-12-02', '其他': ['12121', '2020-12-12']}
        for i in range(varQty):
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[2]/td[2]/input', 1)  # -
            Base_PO.clickXpath(u"//a[@href='javascript:void(0)']", 2)  # 弹框确认
        x = 1
        for k, v in var.items():
            x = x + 1
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[1]/td[2]/input[1]')  # +
            if k == '其他' or k == '其他法定传染病':
                Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input')
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input', k)
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[2]/span/input', v[0])
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v[1])
            else:
                Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input')
                Base_PO.inputXpathClearEnter('//html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input', k)
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v)


        # 手术史
        varStatus = '有'
        var = {'手术1': '2010-12-01', '手术2': '2010-12-02'}
        # cj1，要求无，点击无，弹出框确认
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)  # 无
        Base_PO.clickXpath(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        # cj2,默认无，要求有，点击有，输入内容
        # cj3，默认有，要求有，修改原有数据
        if varStatus == '有':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)  # 有
            x = 1
            for k, v in var.items():
                x = x + 1
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/input', 1)  # +
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr[' + str(x) + ']/td[3]/span/span/input', k)  # 名称
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v)  # 手术日期


        # 外伤史
        varStatus = '有'
        var = {'外伤3': '2020-12-01', '外伤4': '2020-12-02'}
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)  # 无
        Base_PO.clickXpath(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        if varStatus == '有':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)  # 有
            x = 1
            for k, v in var.items():
                x = x + 1
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/input', 1)  # +
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr[' + str(x) + ']/td[3]/span/span/input', k)  # 名称
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v)  # 发生日期


        # 输血史
        varStatus = '有'
        var = {'输血4': '2020-12-12', '输血5': '2020-12-13'}
        Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)  # 无
        Base_PO.clickXpath(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        if varStatus == '有':
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[1]/input',1)  # 有
            x = 1
            for k, v in var.items():
                x = x + 1
                Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/input', 1)  # +
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr[' + str(x) + ']/td[3]/span/span/input', k)  # 数学原因
                Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v)  # 输血日期


        # 家族史 {家庭关系：疾病种类}
        var = {"母亲": ['高血压', '糖尿病', {'其他法定传染病':'123'}], "父亲": ['性阻塞性肺疾病', '脑卒中', {'其他': '4444123'}]}
        for k, v in var.items():
            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr/td[2]/input', 1)  # +
            Base_PO.jsXpathReadonly('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[3]/span/span/input')  # 家庭关系
            Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[3]/span/span/input', k)  # mother
            for i in range(len(v)):
                if v[i] == '高血压':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[2]/input',1) # 高血压
                if v[i] == '糖尿病':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[3]/input',1) # 糖尿病
                if v[i] == '冠心病':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[4]/input',1) # 冠心病
                if v[i] == '慢性阻塞性肺疾病':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[5]/input',1) # 慢性阻塞性肺疾病
                if v[i] == '恶性肿瘤':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[6]/input',1) # 恶性肿瘤
                if v[i] == '脑卒中':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[7]/input',1) # 脑卒中
                if v[i] == '重性精神疾病':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[8]/input',1) # 重性精神疾病
                if v[i] == '结核病':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[9]/input',1) # 结核病
                if v[i] == '肝炎':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[10]/input',1) # 肝炎
                if v[i] == '先天畸形':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[11]/input',1) # 先天畸形
                if v[i] == '职业病':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[12]/input',1) # 职业病
                if v[i] == '肾脏疾病':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[13]/input',1) # 肾脏疾病
                if v[i] == '贫血':
                    Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[14]/input',1) # 贫血
                if isinstance(v[i], dict) == True:
                    for k1, v1 in v[i].items():
                        if k1 == '其他法定传染病':
                            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[15]/input',1)  # 其他法定传染病
                            Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[16]/span/input', v1)
                        if k1 == '其他':
                            Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[17]/input',1)  # 其他
                            Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[18]/span/input', v1)


        # 遗传性疾病史
        var = '121212'
        Base_PO.inputXpathClearEnter('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[6]/tbody/tr/td[2]/span/span/textarea', var)

        # 保存
        # Base_PO.clickId('button1', 1)


        # Base_PO.clickXpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[4]/a/input', 1)  #关闭


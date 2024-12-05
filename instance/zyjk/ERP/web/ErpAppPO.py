# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-7-19
# Description: ERP 对象库
# *****************************************************************


import string, numpy
from string import digits
from PO.ListPO import *
from PO.TimePO import *
from PO.ColorPO import *
from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.FilePO import *
from PO.StrPO import *
from PO.WebPO import *
# from PO.DomPO import *


class ErpAppPO(object):

    def __init__(self):
        self.List_PO = ListPO()
        self.Time_PO = TimePO()
        self.Color_PO = ColorPO()
        self.List_PO = ListPO()
        self.Str_PO = StrPO()
        # self.Dom_PO = DomPO()



    def login(self, varURL, varUser, varPass):
        self.Web_PO = WebPO("appChrome")
        self.Web_PO.openURL(varURL)
        self.Web_PO.setTextByX('/html/body/div[1]/div/div[1]/div/div[2]/form/div[1]/div[1]/div[2]/div/input', varUser)
        self.Web_PO.setTextByX('/html/body/div[1]/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div[2]/div/input', varPass)
        self.Web_PO.clkByX('/html/body/div[1]/div/div[1]/div/div[2]/form/div[3]/button', 2)
        self.Web_PO.clkByX('/html/body/div[3]/div[2]/div[3]/button[2]', 2)

    def getMenuUrl(self):

        self.Web_PO.clksByX("//div[@class='el-sub-menu__title']", 1)
        d_menu_url = self.Web_PO.getDictTextAttrByAttrByX("//a", "href")
        return (d_menu_url)

    def newLabel(self,varUrl, varNo):
        self.Web_PO.opnLabel(varUrl, 2)
        self.Web_PO.swhLabel(varNo)

    def swhLabel(self, varNo):
        self.Web_PO.swhLabel(varNo)

    def _attitude(self, varValue):

        d = {"支持":"1", "中立":"2", "反对":"3"}
        if varValue in d:
            return (d[varValue])



    def _hospital_verifyDateTime(self, varTD, varActual, varExpected, varLoc):
        # verifyDateTime(6, d_['药事会实际召开时间'][2], defaultDay, varDay, 3)
        if varActual != varExpected:
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
            if varActual > varExpected:
                var_ = (varActual - varExpected) * -20
            else:
                var_ = (varExpected - varActual) * 20
            self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
            sleep(3)
            varExpected = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
            self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")
            if varActual != varExpected:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
                if varActual > varExpected:
                    var_ = (varActual - varExpected) * -20
                else:
                    var_ = (varExpected - varActual) * 20
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                varExpected = int(self.Web_PO.getTextByX(
                    "//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(
                        varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")
            if varActual != varExpected:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
                if varActual > varExpected:
                    var_ = (varActual - varExpected) * -20
                else:
                    var_ = (varExpected - varActual) * 20
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                varExpected = int(self.Web_PO.getTextByX(
                    "//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(
                        varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")
            if varActual != varExpected:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
                if varActual > varExpected:
                    var_ = (varActual - varExpected) * -20
                else:
                    var_ = (varExpected - varActual) * 20
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                varExpected = int(self.Web_PO.getTextByX(
                    "//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(
                        varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")


    def _hospital_getStep(self, l_expected, l_default):

        if l_expected[0] > l_default[0]:
            varYear = (l_expected[0] - l_default[0]) * -20  # 鼠标往上滚动，取大值（预期值大于当前值）
        else:
            varYear = (l_default[0] - l_expected[0]) * 20  # 鼠标往下滚动，取小值（预期值小于当前值）
        # print("药事会实际召开时间year: " + str(varYear))

        if l_expected[1] > l_default[1]:
            varMonth = (l_expected[1] - l_default[1]) * -20
        else:
            varMonth = (l_default[1] - l_expected[1]) * 20
        # print("药事会实际召开时间month: " + str(varMonth))

        if l_expected[2] > l_default[2]:
            varDay = (l_expected[2] - l_default[2]) * -20
        else:
            varDay = (l_default[2] - l_expected[2]) * 20
        # print("药事会实际召开时间day: " + str(varDay))

        if l_expected[3] > l_default[3]:
            varHour = (l_expected[3] - l_default[3]) * -20
        else:
            varHour = (l_default[3] - l_expected[3]) * 20
        # print("药事会实际召开时间hour: " + str(varHour))

        if l_expected[4] > l_default[4]:
            varMinutes = (l_expected[4] - l_default[4]) * -20
        else:
            varMinutes = (l_default[4] - l_expected[4]) * 20
        # print("药事会实际召开时间minutes: " + str(varMinutes))

        return (varYear, varMonth, varDay, varHour, varMinutes)


    def _hospital_getDateTimeList(self):

        # 开发跟进信息 - 获取日期和时间
        sleep(2)
        defaultYear = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        defaultMonth = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        defaultDay = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        defaultHour = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[4]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        defaultMinutes = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[5]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")
        print("defaultYear,defaultMonth,defaultDay,defaultHour,defaultMinutes =>", defaultYear,defaultMonth,defaultDay,defaultHour,defaultMinutes)
        l_default = []
        l_default.append(defaultYear)
        l_default.append(defaultMonth)
        l_default.append(defaultDay)
        l_default.append(defaultHour)
        l_default.append(defaultMinutes)
        return l_default

    def _hospital_dataTime(self, varTD, d_ ):
        # _hospital_dataTime(6, d_['药事会实际召开时间'])
        # _hospital_dataTime(9, d_['过会日期'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
        l_ = self._hospital_getStep(d_, self._hospital_getDateTimeList())

        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[0])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[1])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[2])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[4]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[3])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[5]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[4])
        l_revise = self._hospital_getDateTimeList()

        # 校验年月日时分(varTD 对应 div[6])
        self._hospital_verifyDateTime(varTD, d_[0], l_revise[0], 1)
        self._hospital_verifyDateTime(varTD, d_[1], l_revise[1], 2)
        self._hospital_verifyDateTime(varTD, d_[2], l_revise[2], 3)
        self._hospital_verifyDateTime(varTD, d_[2], l_revise[2], 3)  # 重复跑
        self._hospital_verifyDateTime(varTD, d_[3], l_revise[3], 4)
        self._hospital_verifyDateTime(varTD, d_[3], l_revise[3], 4)
        self._hospital_verifyDateTime(varTD, d_[4], l_revise[4], 5)
        self._hospital_verifyDateTime(varTD, d_[4], l_revise[4], 5)
        self._hospital_verifyDateTime(varTD, d_[4], l_revise[4], 5)

        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
        l_result = self._hospital_getDateTimeList()
        if d_ == l_result:
            return 1
        else:
            return 0



    # todo 医院管理
    def hospital(self, d_):

        self.Web_PO.clkByX("//a[@href='#/hospital?title=%E5%8C%BB%E9%99%A2%E7%AE%A1%E7%90%86']")
        # 搜索
        # self.Web_PO.appentTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div[1]/div[1]/div/div/div/div[2]/div/input", d_["搜索"])
        self.Web_PO.appentTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div[1]/div[1]/div/div/div/div[2]/div/input", "奉贤区青村南路")
        sleep(2)
        self.Web_PO.appentTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div[1]/div[1]/div/div/div/div[2]/div/input", "182号")
        # 开发医院
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[3]/div[1]/div/div[3]/button")

        # todo 医院开发信息
        # 产品信息
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/input")
        # 选择指定的产品
        # 获取li的数量
        count = self.Web_PO.getQtyByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[3]/div/div[2]/div[2]/div[1]/ul/li")
        for i in range(count):
            if self.Web_PO.getTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[3]/div/div[2]/div[2]/div[1]/ul/li[" + str(i+1) + "]/div") == d_["产品信息"]:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[3]/div/div[2]/div[2]/div[1]/ul/li[" + str(i+1) + "]")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[3]/div/div[2]/div[1]/button[2]", 2)

        # 1 todo 拜访及态度
        # todo 药事会计划时间
        # 科室主任 - 主要成员
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[2]/td[1]/div/div/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input", list(d_['科室主任'].keys())[0])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[3]/div[1]/button[2]")
        # # 科室主任 - 态度
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[2]/td[3]/div/div/div/input", 2)
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[2]/div[1]/ul/li[" + str(self._attitude(d_['科室主任'][list(d_['科室主任'].keys())[0]])) + "]")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[1]/button[2]")
        #
        # # 药剂科主任 - 主要成员
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[3]/td[1]/div/div/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input", list(d_['药剂科主任'].keys())[0])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[3]/div[1]/button[2]")
        # # 药剂科主任 - 态度
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[3]/td[3]/div/div/div/input", 2)
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[2]/div[1]/ul/li[" + str(self._attitude(d_['药剂科主任'][list(d_['药剂科主任'].keys())[0]])) + "]")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[1]/button[2]")
        #
        # # 医务处长 - 主要成员
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[4]/td[1]/div/div/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input", list(d_['医务处长'].keys())[0])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[3]/div[1]/button[2]")
        # # 医务处长 - 态度
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[4]/td[3]/div/div/div/input", 2)
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[2]/div[1]/ul/li[" + str(self._attitude(d_['医务处长'][list(d_['医务处长'].keys())[0]])) + "]")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[1]/button[2]")
        #
        # # 业务院长 - 主要成员
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[5]/td[1]/div/div/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input", list(d_['业务院长'].keys())[0])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[3]/div[1]/button[2]")
        # # 业务院长 - 态度
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[5]/td[3]/div/div/div/input", 2)
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[2]/div[1]/ul/li[" + str(self._attitude(d_['业务院长'][list(d_['业务院长'].keys())[0]])) + "]")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[1]/button[2]")
        #
        # # # 院长 - 主要成员
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[6]/td[1]/div/div/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input", list(d_['院长'].keys())[0])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[3]/div[1]/button[2]")
        # # 院长 - 态度
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[6]/td[3]/div/div/div/input", 2)
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[2]/div[1]/ul/li[" + str(self._attitude(d_['院长'][list(d_['院长'].keys())[0]])) + "]")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[1]/button[2]")

        # 判断是否其他药事会成员
        otherMemberCount = len(d_['其他药事会成员'])
        # print(otherMemberCount)

        # 删除第一条
        self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/div", 2)
                                 # /html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[2]/div/tr/td[1]/div/div/div/input
        self.Web_PO.scrollToLeft("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div", -50)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div/div/div/button")
                          # /html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[2]/div/div/div/button
        # self.Web_PO.scrollToLeft("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div/tr/td[1]/div/div/div", 444)
        sys.exit(0)

        if otherMemberCount > 0:
            # 定位元素为可见
            self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/div", 2)

            # 其他药事会成员
            # 编辑第一条 成员
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div/tr/td[1]/div/div/div/input")
            self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input", list(d_['其他药事会成员'].keys())[0])
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[3]/div[1]/button[2]")
            # # 编辑第一条 态度
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div/div/tr/td[4]/div/div/div", 2)
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[2]/div[1]/ul/li[" + str(self._attitude(d_['其他药事会成员'][list(d_['其他药事会成员'].keys())[0]])) + "]")
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[1]/button[2]")

            if otherMemberCount > 1:
                del d_['其他药事会成员'][list(d_['其他药事会成员'].keys())[0]]
                for i, k in enumerate(d_['其他药事会成员']):
                    # 定位元素为可见
                    self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/div", 2)

                    # 点击增加一行新纪录
                    self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/div")
                    # 新建成员
                    self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[" + str(i+2) + "]/div/tr/td[1]/div/div/div/input")
                    self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input", k)
                    self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[3]/div[1]/button[2]")
                    # 新建态度
                    self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[" + str(i+2) + "]/div/tr/td[4]/div/div/div")
                    self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[2]/div[1]/ul/li[" + str(self._attitude(d_['其他药事会成员'][k])) + "]")
                    self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[1]/button[2]")

            # 删除第一条
            self.Web_PO.scrollToLeft("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div/tr/td[1]/div/div/div")




        # 2 todo 开发跟进反馈
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[1]/div/div[2]", 2)

        # # # todo 1 开发跟进信息 - 提单科室
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/input", 2)
        # self.Web_PO.eleSetTextClkByX(self.Web_PO.getDivTextUpEle('提单科室', '..'), "//div[2]/div/div/div[2]/div/input", d_['提单科室'],"//div[3]/div[1]/button[2]")
        #
        # # # todo 2 开发跟进信息 - 提单规则
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[2]/div[2]/div/input", 2)
        # self.Web_PO.eleSetTextClkByX(self.Web_PO.getDivTextUpEle('提单规则', '..'), "//div[2]/div/div/div[2]/div/input", d_['提单规则'], "//div[3]/div[1]/button[2]")
        #
        # # # todo 3 开发跟进信息 - 提单状态
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[3]/div[2]/div/input", 2)
        # self.Web_PO.eleSetTextClkByX(self.Web_PO.getDivTextUpEle('提单状态', '..'), "//div[2]/div/div/div[2]/div/input", d_['提单状态'], "//div[3]/div[1]/button[2]")
        #
        # # # todo 4 开发跟进信息 - 过会规则
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[4]/div[2]/div/input", 2)
        # self.Web_PO.eleSetTextClkByX(self.Web_PO.getDivTextUpEle('过会规则', '..'), "//div[2]/div/div/div[2]/div/input", d_['过会规则'], "//div[3]/div[1]/button[2]")

        # 定位元素为可见
        # self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[11]", 2)

        # todo 5 开发跟进信息 - 药剂科会前确认信息
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[5]/div[2]/div/input", 2)
        # self.Web_PO.eleSetTextClkByX(self.Web_PO.getDivTextUpEle('药剂科会前确认信息', '..'), "//div[2]/div/div/div[2]/div/input", d_['药剂科会前确认信息'], "//div[3]/div[1]/button[2]")

        # todo 6 开发跟进信息 - 药事会实际召开时间
        # conveningTime = self._hospital_dataTime(6, d_['药事会实际召开时间'])

        # # todo 7 开发跟进信息 - 会前评估能否过会
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[7]/div[2]/div/input", 2)
        # self.Web_PO.eleSetTextClkByX(self.Web_PO.getDivTextUpEle('会前评估能否过会', '..'), "//div[2]/div/div/div[2]/div/input", d_['会前评估能否过会'], "//div[3]/div[1]/button[2]")
        #
        # # todo 8 开发跟进信息 - 经改进后能否过会
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[8]/div[2]/div/input", 2)
        # self.Web_PO.eleSetTextClkByX(self.Web_PO.getDivTextUpEle('经改进后能否过会', '..'), "//div[2]/div/div/div[2]/div/input", d_['经改进后能否过会'], "//div[3]/div[1]/button[2]")

        # # todo 9 开发跟进信息 - 过会日期
        # afterMetting = self._hospital_dataTime(9, d_['过会日期'])


        # # todo 10 提交
        # if conveningTime == 1 and afterMetting == 1:
        #     ...
        #     # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[3]/button[2]")
        # else:
        #     if conveningTime == 0:
        #         self.Color_PO.outColor([{"31": "药事会实际召开时间值不对！"}])
        #     elif afterMetting == 0:
        #         self.Color_PO.outColor([{"31": "过会日期值不对！"}])

        # 取消
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[3]/button[1]")



    # todo 客户管理
    def customer(self):
        self.Web_PO.clkByX("//a[@href='#/customer?title=%E5%AE%A2%E6%88%B7%E7%AE%A1%E7%90%86']")

        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")


    # todo 拜访管理
    def visit(self):
        self.Web_PO.clkByX("//a[@href='#/visit']")

        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")


    # todo 拜访管理
    def withVisit(self):
        self.Web_PO.clkByX("//a[@href='#/withVisit']")

        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")

    # todo 会议管理
    def meeting(self):
        self.Web_PO.clkByX("//a[@href='#/meeting']")

        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")


    # todo 产品开发
    def product(self):
        self.Web_PO.clkByX("//a[@href='#/product']")

        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")


   # todo 审批中心
    def approve(self):
        self.Web_PO.clkByX("//a[@href='#/approve']")
        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")


 # todo 工作计划
    def jobPlan(self):
        self.Web_PO.clkByX("//a[@href='#/jobPlan']")
        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")


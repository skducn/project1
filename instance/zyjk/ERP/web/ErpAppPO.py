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


    def login(self, varURL, varUser, varPass, varPost=None):
        self.Web_PO = WebPO("appChrome")
        self.Web_PO.openURL(varURL)
        self.Web_PO.setTextByX('/html/body/div[1]/div/div[1]/div/div[2]/form/div[1]/div[1]/div[2]/div/input', varUser)
        self.Web_PO.setTextByX('/html/body/div[1]/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div[2]/div/input', varPass)
        self.Web_PO.clkByX('/html/body/div[1]/div/div[1]/div/div[2]/form/div[3]/button', 2)
        if varPost == None:
            self.Web_PO.clkByX('/html/body/div[3]/div[2]/div[3]/button[2]', 2)  # 确认
        else:
            self.Web_PO.scrollToView("/html/body/div[3]/div[2]/div[3]/button[2]")
            l_ = (self.Web_PO.getTextsByX("//div"))
            l_1 = self.List_PO.deduplication(l_)
            # print(l_1)
            l_2 = self.List_PO.split(l_1, "注：当一个人拥有多个岗位时，需要选择对应的岗位进行登录，将会影响到所对应岗位的数据权限及功能权限的展示;", 1)
            # print(l_2[0])
            l_3 = l_2[0].split("\n")
            # print(l_3)
            l_4 = self.List_PO.delDuplicateElement(l_3)
            # print(l_4)
            d_5 = dict(enumerate(l_4, start=1))
            # print(d_5)
            d_6 = {v:k for k,v in d_5.items()}
            # print(d_6)

            self.Web_PO.clkByX("/html/body/div[3]/div[2]/div[2]/div/div/div[2]/div/div[" + str(d_6[varPost]) + "]")
            self.Web_PO.clkByX('/html/body/div[3]/div[2]/div[3]/button[2]', 2)  # 确认


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




    def _topRank_getDate(self):
        # 获取日期
        sleep(2)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
        l_1 = self.Web_PO.getTextsByX("//li[@class='van-picker-column__item van-picker-column__item--selected']/div")
        l_date = []
        for i in l_1:
            i = i.replace("年", "").replace("月", "").replace("日", "")
            l_date.append(int(i))
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")
        return l_date

    def _scrollUpDown_date(self, l_expected, l_actual):

        # 模拟鼠标上下滚动
        # 负数，鼠标往上滚动，取大值（预期值大于当前值）
        # 正数，鼠标往下滚动，取小值（预期值小于当前值）
        if l_expected[0] > l_actual[0]:
            varYear = (l_expected[0] - l_actual[0]) * -20
        else:
            varYear = (l_actual[0] - l_expected[0]) * 20

        if l_expected[1] > l_actual[1]:
            varMonth = (l_expected[1] - l_actual[1]) * -20
        else:
            varMonth = (l_actual[1] - l_expected[1]) * 20

        if l_expected[2] > l_actual[2]:
            varDay = (l_expected[2] - l_actual[2]) * -20
        else:
            varDay = (l_actual[2] - l_expected[2]) * 20

        return [varYear, varMonth, varDay]

    def _topRank_verifyDate(self, varExpected, varActual, varLoc):
        # 校验日期
        sleep(2)
        if varExpected != varActual:
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
            if varExpected > varActual:
                var_ = (varExpected - varActual) * -20
            else:
                var_ = (varActual - varExpected) * 20
            self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
            sleep(3)
            varActual = self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
            varActual = int(varActual[:-1])
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")
            if varExpected != varActual:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(3)
                varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")
            if varExpected != varActual:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(3)
                varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")
            if varExpected != varActual:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(3)
                varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")

    
    


    # todo 首页

    # 看板辖区
    def switchArea(self, manager, representative):
        # 切换
        # 定位元素为可见
        self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[1]/div[2]", 2)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[1]/div[2]")

        # 经理辖区
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div[2]/div[2]",2)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[2]/div/div/div[2]/div/input", manager)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[4]/button[2]")

        # 代表辖区
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div[2]/div[3]", 2)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[2]/div/div/div[2]/div/input", representative)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[4]/button[2]")

        # 确定
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[3]/div[2]")



    def _topRank_getDate(self):
        # 获取日期
        sleep(2)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
        l_1 = self.Web_PO.getTextsByX("//li[@class='van-picker-column__item van-picker-column__item--selected']/div")
        l_date = []
        for i in l_1:
            i = i.replace("年", "").replace("月", "").replace("日", "")
            l_date.append(int(i))
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")
        return l_date

    def _scrollUpDown_date(self, l_expected, l_actual):
        # 模拟鼠标上下滚动
        # 负数，鼠标往上滚动，取大值（预期值大于当前值）
        # 正数，鼠标往下滚动，取小值（预期值小于当前值）
        if l_expected[0] > l_actual[0]:
            varYear = (l_expected[0] - l_actual[0]) * -20
        else:
            varYear = (l_actual[0] - l_expected[0]) * 20

        if l_expected[1] > l_actual[1]:
            varMonth = (l_expected[1] - l_actual[1]) * -20
        else:
            varMonth = (l_actual[1] - l_expected[1]) * 20

        if l_expected[2] > l_actual[2]:
            varDay = (l_expected[2] - l_actual[2]) * -20
        else:
            varDay = (l_actual[2] - l_expected[2]) * 20

        return (varYear, varMonth, varDay)

    def _topRank_verifyDate(self, varExpected, varActual, varLoc):
        # 校验日期
        sleep(2)
        if varExpected != varActual:
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
            if varExpected > varActual:
                var_ = (varExpected - varActual) * -20
            else:
                var_ = (varActual - varExpected) * 20
            self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
                varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
            sleep(3)
            varActual = self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
                varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
            varActual = int(varActual[:-1])
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")
            if varExpected != varActual:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
                    varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(3)
                varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
                    varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")
            if varExpected != varActual:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
                    varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(3)
                varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
                    varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")
            if varExpected != varActual:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
                    varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(3)
                varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
                    varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")

    def _topRank_date(self, l_expected):

        # 选择年月日（封装）

        # 默认系统日期
        l_sysDate = []
        l_sysDate.append(int(Time_PO.getYear()))
        l_sysDate.append(int(Time_PO.getMonth()))
        l_sysDate.append(int(Time_PO.getDay()))
        print("l_sysDate => ", l_sysDate)  # [2024, 12, 6]

        # 模拟鼠标上下滚动，修改日期
        l_ = self._scrollUpDown_date(l_expected, l_sysDate)
        # print(l_)  # (40, 220, 100)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
        self.Web_PO.scrollUpDown(
            "//div[@class='van-picker van-datetime-picker']/div/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
            l_[0])
        self.Web_PO.scrollUpDown(
            "//div[@class='van-picker van-datetime-picker']/div/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
            l_[1])
        self.Web_PO.scrollUpDown(
            "//div[@class='van-picker van-datetime-picker']/div/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
            l_[2])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")

        # 获取修改后的日期
        l_getModuleDate = self._topRank_getDate()
        print("l_getModuleDate =>", l_getModuleDate)  # [2022, 4, 1]

        # 校验日期
        self._topRank_verifyDate(l_expected[0], l_getModuleDate[0], 1)
        self._topRank_verifyDate(l_expected[1], l_getModuleDate[1], 2)
        self._topRank_verifyDate(l_expected[2], l_getModuleDate[2], 3)

        l_actual = self._topRank_getDate()
        print("l_actual =>", l_actual)  # [2022, 1, 1]

        if l_expected == l_actual:
            print(1)
            return 1
        else:
            print(0)
            return 0


    # 今日团队综合排名
    def topRank(self, l_expected, varOrg):
        # 今日团队综合排名 - Top排名 - 拜访达成统计排名

        # 首页点击top排名
        self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[2]/div[1]/div[2]")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[2]/div[1]/div[2]")

        # # todo 选择日期
        if self._topRank_date(l_expected) == 1:

            # todo 选择排名
            s_date = ("-".join(["".join(str(x)) for x in l_expected]))  # 2024-1-1
            d_team = {}
            if varOrg == "团队排名":
                # 点击团队排名
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[1]")
                l_ = self.Web_PO.getTextsByX("//span")
                l_2 = self.List_PO.split(l_, "个人排名", 1)
                l_3 = self.List_PO.dels(l_2, "")
                l_3 = self.List_PO.dels(l_3, "团队")
                for i in range(8):
                    l_3 = self.List_PO.dels(l_3, str(i+3))
                l_5 = self.List_PO.dels(l_3, "\n", varMode="mohu")
                l_6 = self.List_PO.group(l_5, 10)
                # print(l_6)
                # 获取各指标达成分数
                l_7 = self.Web_PO.getTextsByX("//div/div[2]/div")
                c = len(l_7[0].split("指标达成分数")) - 1
                l_8 = []
                for i in range(c):
                    s_8 = l_7[0].split("指标达成分数：")[1+i].split("\n")[0]
                    l_8.append(s_8)
                # print(l_8) # ['0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
                l_9 = []
                for i in range(len(l_6)):
                    l_6[i].append('指标达成分数')
                    l_6[i].append(l_8[i])
                    l_9.append(self.List_PO.pair2dict(l_6[i]))
                # print(l_9)  # [{'薛伟团队': '浦东/闵行/徐汇', '实地工作拜访完成率': '0.00%', '定位匹配率': '0.00%', '双A客户达成率': '0.00%', '高潜客户达成率': '0.00%', '指标达成分数': '0.00'},...
                d_team[s_date] = l_9
                print(d_team)  # {'2014-1-1': [{'薛伟团队': '浦东/闵行/徐汇', '实地工作拜访完成率': '0.00%', '定位匹配率': '0.00%', '双A客户达成率': '0.00%', '高潜客户达成率': '0.00%', '指标达成分数': '0.00'}

            else:
                # 个人排名
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]")
                sleep(2)
                l_ = self.Web_PO.getTextsByX("//span")
                # print(l_)
                l_2 = self.List_PO.split(l_, "个人排名", 1)
                l_3 = self.List_PO.dels(l_2, "")
                for i in range(30):
                    l_3 = self.List_PO.dels(l_3, str(i+3))
                l_5 = self.List_PO.dels(l_3, "\n", varMode="mohu")
                l_6 = self.List_PO.group(l_5, 10)
                # print(l_6)
                # # 获取各指标达成分数
                l_7 = self.Web_PO.getTextsByX("//div/div[2]/div")
                c = len(l_7[0].split("指标达成分数")) - 1
                l_8 = []
                for i in range(c):
                    s_8 = l_7[0].split("指标达成分数：")[1 + i].split("\n")[0]
                    l_8.append(s_8)
                # print(l_8) # ['0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00']
                l_9 = []
                for i in range(len(l_6)):
                    l_6[i].append('指标达成分数')
                    l_6[i].append(l_8[i])
                    l_9.append(self.List_PO.pair2dict(l_6[i]))
                # print(l_9)  # [{'薛伟团队': '浦东/闵行/徐汇', '实地工作拜访完成率': '0.00%', '定位匹配率': '0.00%', '双A客户达成率': '0.00%', '高潜客户达成率': '0.00%', '指标达成分数': '0.00'},...
                d_team[s_date] = l_9
                print(d_team)  # {'2014-1-1': [{'薛伟团队': '浦东/闵行/徐汇', '实地工作拜访完成率': '0.00%', '定位匹配率': '0.00%', '双A客户达成率': '0.00%', '高潜客户达成率': '0.00%', '指标达成分数': '0.00'}

    def todayRank(self):
        # 今日团队综合排名 - 列表数据

        self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[2]/div[2]")
        s = self.Web_PO.getTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[2]/div[2]")
        l_ = s.split("\n")
        # print(l_)
        l_1 = self.List_PO.group(l_, 3)
        # print(l_1)
        d_ = {}
        for i in l_1:
            k = i.pop(0)
            d_[k] = i
        # print(d_)
        return d_



    # 行为分析
    def behaviorAnalysis(self):
        # 行为分析 - 团队拜访、团队会议、团队开发数据

        self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[3]/div[2]")
        s = self.Web_PO.getTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[3]/div[2]")
        l_ = s.split("\n")
        l_1 = self.List_PO.pair2dict(l_)
        del l_1['1']
        return (l_1)



    # 业绩分析
    def getProduct(self, varProduct):
        # 业绩分析 - 选择产品

        # 点击选择产品
        self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[4]/div[1]/div[2]", 2)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[4]/div[1]/div[2]")
        # 获取li的数量
        count = self.Web_PO.getQtyByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[4]/div[3]/div[2]/div[3]/div/div[1]/ul/li")
        for i in range(count):
            if self.Web_PO.getTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[4]/div[3]/div[2]/div[3]/div/div[1]/ul/li[" + str(i+1) + "]/div") == varProduct:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[4]/div[3]/div[2]/div[3]/div/div[1]/ul/li[" + str(i+1) + "]")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[4]/div[3]/div[2]/div[4]/button[2]")


    def _hospital_getDateTime(self):

        # 开发跟进信息 - 获取日期和时间
        sleep(2)
        defaultYear = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        defaultMonth = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        defaultDay = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        defaultHour = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[4]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        defaultMinutes = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[5]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")
        # print("defaultYear,defaultMonth,defaultDay,defaultHour,defaultMinutes =>", defaultYear,defaultMonth,defaultDay,defaultHour,defaultMinutes)
        l_default = []
        l_default.append(defaultYear)
        l_default.append(defaultMonth)
        l_default.append(defaultDay)
        l_default.append(defaultHour)
        l_default.append(defaultMinutes)
        return l_default

    def _scrollUpDown_dateTime(self, l_expected, l_actual):
        # 模拟鼠标上下滚动
        # 负数，鼠标往上滚动，取大值（预期值大于当前值）
        # 正数，鼠标往下滚动，取小值（预期值小于当前值）
        if l_expected[0] > l_actual[0]:
            varYear = (l_expected[0] - l_actual[0]) * -20
        else:
            varYear = (l_actual[0] - l_expected[0]) * 20
        # print("药事会实际召开时间year: " + str(varYear))

        if l_expected[1] > l_actual[1]:
            varMonth = (l_expected[1] - l_actual[1]) * -20
        else:
            varMonth = (l_actual[1] - l_expected[1]) * 20
        # print("药事会实际召开时间month: " + str(varMonth))

        if l_expected[2] > l_actual[2]:
            varDay = (l_expected[2] - l_actual[2]) * -20
        else:
            varDay = (l_actual[2] - l_expected[2]) * 20
        # print("药事会实际召开时间day: " + str(varDay))

        if l_expected[3] > l_actual[3]:
            varHour = (l_expected[3] - l_actual[3]) * -20
        else:
            varHour = (l_actual[3] - l_expected[3]) * 20
        # print("药事会实际召开时间hour: " + str(varHour))

        if l_expected[4] > l_actual[4]:
            varMinutes = (l_expected[4] - l_actual[4]) * -20
        else:
            varMinutes = (l_actual[4] - l_expected[4]) * 20
        # print("药事会实际召开时间minutes: " + str(varMinutes))

        return (varYear, varMonth, varDay, varHour, varMinutes)

    def _hospital_verifyDateTime(self, varTD, varActual, varExpected, varLoc):
        # verifyDateTime(6, d_['药事会实际召开时间'][2], defaultDay, varDay, 3)
        if varActual != varExpected:
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
            if varActual > varExpected:
                var_ = (varActual - varExpected) * -20
            else:
                var_ = (varExpected - varActual) * 20
            self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
            sleep(3)
            varExpected = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
            self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")
            if varActual != varExpected:
                self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
                if varActual > varExpected:
                    var_ = (varActual - varExpected) * -20
                else:
                    var_ = (varExpected - varActual) * 20
                self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
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
                self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
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
                self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                varExpected = int(self.Web_PO.getTextByX(
                    "//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(
                        varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")


    def __hospital_dataTime(self, varTD, l_dateTime ):
        # __hospital_dataTime(6, d_['药事会实际召开时间'])
        # __hospital_dataTime(9, d_['过会日期'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)

        l_ = self._scrollUpDown_dateTime(l_dateTime, self._hospital_getDateTime())
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
        self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[0])
        self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[1])
        self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[2])
        self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div[2]/div[4]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[3])
        self.Web_PO.scrollUpDown("//div[@class='van-picker van-datetime-picker']/div[2]/div[5]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[4])
        l_revise = self._hospital_getDateTime()

        # 校验年月日时分(varTD 对应 div[6])
        self._hospital_verifyDateTime(varTD, l_dateTime[0], l_revise[0], 1)
        self._hospital_verifyDateTime(varTD, l_dateTime[1], l_revise[1], 2)
        self._hospital_verifyDateTime(varTD, l_dateTime[2], l_revise[2], 3)
        self._hospital_verifyDateTime(varTD, l_dateTime[2], l_revise[2], 3)  # 重复跑
        self._hospital_verifyDateTime(varTD, l_dateTime[3], l_revise[3], 4)
        self._hospital_verifyDateTime(varTD, l_dateTime[3], l_revise[3], 4)
        self._hospital_verifyDateTime(varTD, l_dateTime[4], l_revise[4], 5)
        self._hospital_verifyDateTime(varTD, l_dateTime[4], l_revise[4], 5)
        self._hospital_verifyDateTime(varTD, l_dateTime[4], l_revise[4], 5)

        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
        l_result = self._hospital_getDateTime()
        if l_dateTime == l_result:
            return 1
        else:
            return 0


    # 功能
    # todo 医院管理
    def hospital(self, d_):
        # 医院管理

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
        self.Web_PO.scrollLeftRight("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div", -50)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div/div/div/button")
                          # /html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[2]/div/div/div/button
        # self.Web_PO.scrollLeftRight("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div/tr/td[1]/div/div/div", 444)
        # sys.exit(0)

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
            self.Web_PO.scrollLeftRight("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div/tr/td[1]/div/div/div")




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
        # conveningTime = self.__hospital_dataTime(6, d_['药事会实际召开时间'])

        # # todo 7 开发跟进信息 - 会前评估能否过会
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[7]/div[2]/div/input", 2)
        # self.Web_PO.eleSetTextClkByX(self.Web_PO.getDivTextUpEle('会前评估能否过会', '..'), "//div[2]/div/div/div[2]/div/input", d_['会前评估能否过会'], "//div[3]/div[1]/button[2]")
        #
        # # todo 8 开发跟进信息 - 经改进后能否过会
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[8]/div[2]/div/input", 2)
        # self.Web_PO.eleSetTextClkByX(self.Web_PO.getDivTextUpEle('经改进后能否过会', '..'), "//div[2]/div/div/div[2]/div/input", d_['经改进后能否过会'], "//div[3]/div[1]/button[2]")

        # # todo 9 开发跟进信息 - 过会日期
        afterMetting = self.__hospital_dataTime(9, d_['过会日期'])


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





    def _common_date__xpath(self, varXpathDiv, varDiv):
        return varXpathDiv + "/div[" + str(varDiv) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"
    def _common_date__verify(self, ele, varXpathIn, i_expected, i_getModuleDate, varXpathDiv, varLoc, varXpathConfirm):
        if i_expected != i_getModuleDate:
            self.Web_PO.clkByX(varXpathIn)
            if i_expected > i_getModuleDate:
                var_ = (i_expected - i_getModuleDate) * -20
            else:
                var_ = (i_getModuleDate - i_expected) * 20
            self.Web_PO.scrollUpDown(ele, self._common_date__xpath(varXpathDiv, varLoc), var_)
            s_getModuleDate = self.Web_PO.eleGetTextByX(ele, self._common_date__xpath(varXpathDiv, varLoc))
            if self.Str_PO.isContainChinese(s_getModuleDate):
                i_getModuleDate = int(s_getModuleDate[:-1])
            else:
                i_getModuleDate = int(s_getModuleDate)
            self.Web_PO.eleClkByX(ele, varXpathConfirm)
            return self._common_date__verify(ele, varXpathIn, i_expected, i_getModuleDate, varXpathDiv, varLoc, varXpathConfirm)
        else:
            return 1
    def _common_date__get(self, varXpathIn, varTitle, varXpathDiv, varXpathConfirm):

        # 获取年月日
        self.Web_PO.clkByX(varXpathIn, 2)
        ele = self.Web_PO.getDivTextUpEle(varTitle)
        l_1 = []
        l_1.append(self.Web_PO.eleGetTextByX(ele, self._common_date__xpath(varXpathDiv, 1)))
        l_1.append(self.Web_PO.eleGetTextByX(ele, self._common_date__xpath(varXpathDiv, 2)))
        l_1.append(self.Web_PO.eleGetTextByX(ele, self._common_date__xpath(varXpathDiv, 3)))
        l_getModuleDate = []
        for i in l_1:
            i = i.replace("年", "").replace("月", "").replace("日", "")
            l_getModuleDate.append(int(i))
        self.Web_PO.eleClkByX(ele, varXpathConfirm)
        return (ele, l_getModuleDate)
    def _common_date(self, d_expected, varField, varTitle, varXpathDiv, varXpathConfirm):
        # 选择年月日（公共封装）
        # 如：药事会计划开始日期，药事会计划结束日期

        # 开发跟进信息
        ele = self.Web_PO.getLabelTextUpEle2("span", "开发次数", "../../../..")
        l_field = self.Web_PO.eleGetTextsByX(ele, ".//span")
        dd_ = dict(enumerate(l_field, start=1))
        d_field = {v: k for k, v in dd_.items()}
        ele2 = self.Web_PO.getLabelTextUpEle2("span", varField, "../..")
        l_actual = self.Web_PO.eleGetShadowRoots(ele2, ".//input", "div")

        # 判断补0
        if d_expected[varField][1] < 10:
            varMonth = "0" + str(d_expected[varField][1])
        else:
            varMonth = str(d_expected[varField][1])
        if d_expected[varField][2] < 10:
            varDay = "0" + str(d_expected[varField][2])
        else:
            varDay = str(d_expected[varField][2])
        s_expected = str(d_expected[varField][0]) + "-" + varMonth + "-" + varDay
        if s_expected != str(l_actual[0]):
            for i in range(len(d_expected[varField])):
                # 获取组件年月日
                ele, l_getModuleDate = self._common_date__get(self._product_devFollowUp__common_xpath(d_field[varField]), varTitle, varXpathDiv, varXpathConfirm)
                # 获取预期值与组件值之步长并校验比对年月日
                self._common_date__verify(ele, self._product_devFollowUp__common_xpath(d_field[varField]), d_expected[varField][i], l_getModuleDate[i], varXpathDiv, i+1, varXpathConfirm)


    def _common_dateTime__xpath(self, varXpathDiv, varDiv):
        return varXpathDiv + "/div[" + str(varDiv) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"
    def _common_dateTime__verify(self, ele, varXpathIn, i_expected, i_getModuleDate, varXpathDiv, varLoc, varXpathConfirm):
        if i_expected != i_getModuleDate:
            self.Web_PO.clkByX(varXpathIn)
            if i_expected > i_getModuleDate:
                var_ = (i_expected - i_getModuleDate) * -20
            else:
                var_ = (i_getModuleDate - i_expected) * 20
            self.Web_PO.scrollUpDown(ele, self._common_dateTime__xpath(varXpathDiv, varLoc), var_)
            s_getModuleDate = self.Web_PO.eleGetTextByX(ele, self._common_dateTime__xpath(varXpathDiv, varLoc))
            if self.Str_PO.isContainChinese(s_getModuleDate):
                i_getModuleDate = int(s_getModuleDate[:-1])
            else:
                i_getModuleDate = int(s_getModuleDate)
            self.Web_PO.eleClkByX(ele, varXpathConfirm)
            return self._common_dateTime__verify(ele, varXpathIn, i_expected, i_getModuleDate, varXpathDiv, varLoc, varXpathConfirm)
        else:
            return 1
    def _common_dateTime__get(self, varXpathIn, varTitle, varXpathDiv, varXpathConfirm):

        # 获取年月日
        self.Web_PO.clkByX(varXpathIn, 2)
        ele = self.Web_PO.getDivTextUpEle(varTitle)
        l_1 = []
        l_1.append(self.Web_PO.eleGetTextByX(ele, self._common_dateTime__xpath(varXpathDiv, 1)))
        l_1.append(self.Web_PO.eleGetTextByX(ele, self._common_dateTime__xpath(varXpathDiv, 2)))
        l_1.append(self.Web_PO.eleGetTextByX(ele, self._common_dateTime__xpath(varXpathDiv, 3)))
        l_1.append(self.Web_PO.eleGetTextByX(ele, self._common_dateTime__xpath(varXpathDiv, 4)))
        l_1.append(self.Web_PO.eleGetTextByX(ele, self._common_dateTime__xpath(varXpathDiv, 5)))
        # print("日期 => ", l_1)
        l_getModuleDate = []
        for i in l_1:
            i = i.replace("年", "").replace("月", "").replace("日", "")
            l_getModuleDate.append(int(i))
        self.Web_PO.eleClkByX(ele, varXpathConfirm)
        return (ele, l_getModuleDate)
    def _common_dateTime(self, d_expected, varField, varTitle, varXpathDiv, varXpathConfirm):

        # 选择年月日时分（公共封装）
        # 如：药事会实际召开时间

        # 开发跟进信息
        ele = self.Web_PO.getLabelTextUpEle2("span", "开发次数", "../../../..")
        l_field = self.Web_PO.eleGetTextsByX(ele, ".//span")
        dd_ = dict(enumerate(l_field, start=1))
        d_field = {v: k for k, v in dd_.items()}
        ele2 = self.Web_PO.getLabelTextUpEle2("span", varField, "../..")
        l_actual = self.Web_PO.eleGetShadowRoots(ele2, ".//input", "div")

        # 判断补0
        if d_expected[varField][1] < 10:
            varMonth = "0" + str(d_expected[varField][1])
        else:
            varMonth = str(d_expected[varField][1])
        if d_expected[varField][2] < 10:
            varDay = "0" + str(d_expected[varField][2])
        else:
            varDay = str(d_expected[varField][2])
        s_expected = str(d_expected[varField][0]) + "-" + varMonth + "-" + varDay
        if s_expected != str(l_actual[0]):
            for i in range(len(d_expected[varField])):
                # 获取组件年月日
                ele, l_getModuleDate = self._common_dateTime__get(self._product_devFollowUp__common_xpath(d_field[varField]), varTitle, varXpathDiv, varXpathConfirm)
                # 获取预期值与组件值之步长并校验比对年月日
                self._common_dateTime__verify(ele, self._product_devFollowUp__common_xpath(d_field[varField]), d_expected[varField][i], l_getModuleDate[i], varXpathDiv, i + 1, varXpathConfirm)



    def __getVisitor(self):

        # 拜访及态度
        # {'主要成员': {'科室主任': ['陈海群', '中立'], '药剂科主任': ['杨忠英', '中立'], '医务处长': ['王久文', '支持'], '业务院长': ['陈健', '中立'], '院长': ['王旭辉', '支持']},
        # '其他药事会成员': [['郭震', '支持'], ['杨忠英', '反对'], ['陈健', '中立'], ['张金春', '支持'], ['石来新', '反对'], ['沈亚雯', '中立']]}

        d_visitor = {}
        # 主要成员
        ele = self.Web_PO.getLabelTextUpEle2("th", "主要成员", "../..")
        l_shadow = self.Web_PO.eleGetShadowRoots(ele, './/input', 'div:nth-last-of-type(1)')
        l_shadow = self.List_PO.group(l_shadow, 2)
        l_post = ['科室主任', '药剂科主任', '医务处长', '业务院长', '院长']
        d_visitor['主要成员'] = dict(zip(l_post, l_shadow))

        # 其他药事会成员
        ele = self.Web_PO.getLabelTextUpEle2("th", "其他药事会成员", "../..")
        l_shadow = self.Web_PO.eleGetShadowRoots(ele, './/input', 'div:nth-last-of-type(1)')
        d_visitor['其他药事会成员'] = self.List_PO.group(l_shadow, 2)

        return d_visitor





    # todo 产品开发

    def _product_devFollowUp__common_xpath(self, varDiv):
        # 公共表单（产品开发 - 开发跟进反馈）
        # 第一层
        return "/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[" + str(varDiv) + "]/div/div[2]/div/input"
    def _product_devFollowUp__common(self, d_expected, varField):
        # 公共表单（产品开发 - 开发跟进反馈）

        # 开发跟进信息
        ele = self.Web_PO.getLabelTextUpEle2("span", "开发次数", "../../../..")
        l_field = self.Web_PO.eleGetTextsByX(ele, ".//span")
        dd_ = dict(enumerate(l_field, start=1))
        d_field = {v: k for k, v in dd_.items()}
        ele2 = self.Web_PO.getLabelTextUpEle2("span", varField, "../..")
        l_actual = self.Web_PO.eleGetShadowRoots(ele2, ".//input", "div")
        if l_actual[0] != d_expected[varField]:
            self.Web_PO.clkByX(self._product_devFollowUp__common_xpath(d_field[varField]))
            self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[2]/div/div/div[2]/div/input", d_expected[varField])
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/button[2]")  # 确认
    def set_product_devFollowUp(self, d_expected):
        # 开发跟进

        self._product_devFollowUp__common(d_expected, '开发次数')
        self._product_devFollowUp__common(d_expected, '提单科室')
        self._product_devFollowUp__common(d_expected, '提单规则')

        # # 过会规则
        # 操作逻辑，先反勾选所有复选框，再勾选预期值
        ele2 = self.Web_PO.getLabelTextUpEle2("span", '过会规则', "../..")
        l_actual = self.Web_PO.eleGetShadowRoots(ele2, ".//textarea", "div")
        l_actual = l_actual[0].split(", ")
        if dict(Counter(l_actual)) != dict(Counter(d_expected['过会规则'])):
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[4]/div/div[2]/div/textarea")
            l_afterMeetingRule = self.Web_PO.getTextsByX("//div[@role='checkbox']/span")
            dd_ = dict(enumerate(l_afterMeetingRule, start=1))
            d_afterMeetingRule = {v: k for k, v in dd_.items()}
            # 先反勾选所有复选框
            ele = self.Web_PO.getDivTextUpEle("选择过会规则")
            self.Web_PO.eleClksByX(ele, ".//div[@class='van-checkbox__icon van-checkbox__icon--round van-checkbox__icon--checked']")
            # 再勾选预期值
            for i in range(len(d_expected["过会规则"])):
                self.Web_PO.eleClkByX(ele, ".//div[2]/div[" + str(d_afterMeetingRule[d_expected["过会规则"][i]]) + "]/div")
            self.Web_PO.eleClkByX(ele, ".//div[3]/button[2]")

        self._product_devFollowUp__common(d_expected, '提单状态')
        self._product_devFollowUp__common(d_expected, '药剂科会前确认信息')
        self._common_date(d_expected, '药事会计划结束日期', " 请选择药事会结束时间 ", ".//div[2]/div/div", ".//div[3]/button[2]")
        self._common_date(d_expected, '药事会计划开始日期', " 请选择药事会开始时间 ", ".//div[2]/div/div", ".//div[3]/button[2]")
        self._common_dateTime(d_expected, '药事会实际召开时间', "药事会实际召开时间选择", ".//div[2]/div[2]", ".//div[2]/div[1]/button[2]")
        self._product_devFollowUp__common(d_expected, '会前评估能否过会')
        self._product_devFollowUp__common(d_expected, '经改进后能否过会')
        if d_expected['会前评估能否过会'] == '是' or d_expected['经改进后能否过会'] == '是':
            self._common_date(d_expected, '过会日期',  "过会时间选择", ".//div[2]/div[2]", ".//div[2]/div[1]/button[2]")

        # 提交
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[4]/button[2]")
        # 拜访人信息录入成功（确定）
        ele4 = self.Web_PO.getLabelTextUpEle2("div", "开发跟进信息录入成功", "../..")
        self.Web_PO.eleClkByX(ele4, ".//div[5]")

    def get_product_devFollowUp(self, d_expected):
        # 开发跟进反馈 - 获取数据

        # 选择标签
        if d_expected['标签'] == '跟进中':
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[1]/span")
        elif d_expected['标签'] == '已结束':
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/span")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div/input", d_expected['搜索'])
        # 点击开发跟进
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[3]/button[2]")

        d_getCurrData = {}

        # 1 获取医院开发信息
        ele = self.Web_PO.getLabelTextUpEle2("span", "医院信息", "../../../..")
        l_shadow = self.Web_PO.eleGetShadowRoots(ele, './/input', 'div:nth-last-of-type(1)')
        l_field = self.Web_PO.eleGetTextsByX(ele, ".//span")
        d_devInfo = dict(zip(l_field, l_shadow))
        d_getCurrData["医院开发信息"] = d_devInfo

        # 2 获取开发跟进信息
        ele = self.Web_PO.getLabelTextUpEle2("span", "开发次数", "../../../..")
        l_shadow = self.Web_PO.eleGetShadowRoots(ele, './/input', 'div:nth-last-of-type(1)')
        l_field = self.Web_PO.eleGetTextsByX(ele, ".//span")
        l_field.remove('过会规则')
        d_getCurrData["开发跟进信息"] = dict(zip(l_field, l_shadow))
        # 追加过会规则
        l_text_shadow = self.Web_PO.getShadowRoots('//textarea', 'div')
        d_getCurrData['开发跟进信息']['过会规则'] = l_text_shadow[0]
        # 追加采购时间和更新时间
        l_text_span = self.Web_PO.getTextsByX("//div[@class='van-col van-col--24']/span")
        d_getCurrData['开发跟进信息']['采购时间'] = l_text_span[0]
        d_getCurrData['开发跟进信息']['更新时间'] = l_text_span[1]

        return d_getCurrData


    def set_product_visitor(self, d_getCurrDate, d_expected):
        # 拜访及态度 - 修改数据
        # 修改逻辑，将 d_getCurrDate 与 d_expected 比对，如不一致则更新。

        # 更新主要成员
        ele = self.Web_PO.getLabelTextUpEle2("th", "主要成员", "../..")
        d_post = {"科室主任": 2, "药剂科主任": 3, "医务处长" : 4, "业务院长": 5, "院长": 6}
        for k, v in d_getCurrDate['拜访及态度']['主要成员'].items():
            if k in d_expected['拜访及态度']['主要成员']:
                if v != d_expected['拜访及态度']['主要成员'][k]:
                    if v[0] != d_expected['拜访及态度']['主要成员'][k][0]:
                        # 主要成员
                        self.Web_PO.eleClkByX(ele, ".//tr[" + str(d_post[k]) + "]/td[1]/div/div/div/input")
                        ele2 = self.Web_PO.getDivTextUpEle(" 主要成员选择 ")
                        self.Web_PO.eleSetTextByX(ele2, ".//div[2]/div/div/div[2]/div/input", d_expected['拜访及态度']['主要成员'][k][0])
                        self.Web_PO.eleClkByX(ele2, ".//div[3]/div/div[2]/button[2]", 2)
                    elif v[1] != d_expected['拜访及态度']['主要成员'][k][1]:
                        # 态度
                        self.Web_PO.eleClkByX(ele, ".//tr[" + str(d_post[k]) + "]/td[3]/div/div/div/input")
                        ele2 = self.Web_PO.getDivTextUpEle(" 态度选择 ")
                        self.Web_PO.eleSetTextByX(ele2, ".//div[2]/div/div/div[2]/div/input", d_expected['拜访及态度']['主要成员'][k][1])
                        self.Web_PO.eleClkByX(ele2, ".//div[3]/div/div[2]/button[2]", 2)

        # 更新其他药事会成员
        # 操作逻辑：删除所有会员后再添加
        # 遍历删除
        ele3 = self.Web_PO.getLabelTextUpEle2("th", "其他药事会成员", "../..")
        qty_row = self.Web_PO.eleGetQtyByX(ele3, ".//div/div[@class='van-swipe-cell']")
        for i in range(qty_row):
            self.Web_PO.scrollLeftRight(ele3, ".//div/div[1]/div", -50)
            self.Web_PO.eleClkByX(ele3, ".//div/div[1]/div/div/div/button")
        # 点击增加一行新记录
        for i in range(len(d_expected['拜访及态度']['其他药事会成员'])):
            self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[3]/table[2]/div/div/button")
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/table[2]/div/div/button")
            # 其他药事会成员
            self.Web_PO.eleClkByX(ele3, ".//div/div[" + str(i+1) + "]/div/tr/td[1]/div/div/div/input")
            ele2 = self.Web_PO.getDivTextUpEle(" 主要成员选择 ")
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/div/div/div[2]/div/input", d_expected['拜访及态度']['其他药事会成员'][i][0])
            self.Web_PO.eleClkByX(ele2, ".//div[3]/div/div[2]/button[2]")
            # 态度
            self.Web_PO.eleClkByX(ele3, ".//div/div[" + str(i+1) + "]/div/tr/td[4]/div/div/div/input")
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/div/div/div[2]/div/input", d_expected['拜访及态度']['其他药事会成员'][i][1])
            self.Web_PO.eleClkByX(ele2, ".//div[3]/div/div[2]/button[2]")

        # # 提交
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[4]/button[2]")
        # # 拜访人信息录入成功（确定），返回产品开发列表页
        ele4 = self.Web_PO.getLabelTextUpEle2("div", "拜访人信息录入成功", "../..")
        self.Web_PO.eleClkByX(ele4, ".//div[5]")

    def get_product_visitor(self, d_expected):
        # 拜访及态度 - 获取数据

        # {'医院开发信息': {'医院信息': 'HCO00000122-崇中心', '产品信息': '氨叶-CP102', '负责人': '薛伟、彭琦'},
        # '拜访及态度': {'主要成员': {'科室主任': ['陈海群', '中立'], '药剂科主任': ['杨忠英', '中立'], '医务处长': ['王久文', '支持'], '业务院长': ['陈健', '中立'], '院长': ['王旭辉', '支持']},
        # '其他药事会成员': [['郭震', '支持'], ['杨忠英', '反对'], ['陈健', '中立'], ['张金春', '支持'], ['石来新', '反对'], ['沈亚雯', '中立']]}}

        # 选择标签
        if d_expected['标签'] == '跟进中':
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[1]/span")
        elif d_expected['标签'] == '已结束':
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/span")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div/input", d_expected['搜索'])
        # 点击拜访人
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[3]/button[1]")

        d_getCurrData = {}

        # 1 获取医院开发信息
        ele = self.Web_PO.getLabelTextUpEle2("span", "医院信息", "../../../..")
        l_shadow = self.Web_PO.eleGetShadowRoots(ele, './/input', 'div:nth-last-of-type(1)')
        l_field = self.Web_PO.eleGetTextsByX(ele, ".//span")
        d_devInfo = dict(zip(l_field, l_shadow))
        d_getCurrData["医院开发信息"] = d_devInfo

        # 2 获取拜访及态度
        d_getCurrData["拜访及态度"] = self.__getVisitor()

        # 关闭，返回产品开发列表页
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[4]/button[1]")
        return d_getCurrData


    def _product_new__common_xpath(self, varDiv):
        # 公共表单（产品开发 - 新增产品开发）
        # 第一层
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[" + str(varDiv) + "]/div[2]/div/input", 2)
    def _product_new__common_xpathDate(self, varDiv):
        # 公共表单（产品开发 - 新增产品开发）
        # 第一层
        return "/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[" + str(varDiv) + "]/div[2]/div/input"
    def _product_new__common(self, varDiv, varValue):
        # 公共表单（产品开发 - 新增产品开发）
        self._product_new__common_xpath(varDiv)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div/input", varValue)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[4]/button[2]")
    def new_product(self, d_new):
        # 新增产品开发

        # 新增（产品开发右上角）
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[3]")

        # 1,开发医院类型
        self._product_new__common_xpath(1)
        ele = self.Web_PO.getDivTextUpEle(" 请选择开发医院类型 ")
        l_hospitalType = (self.Web_PO.eleGetTextsByLabelByX(ele, ".//div[2]/div/div[1]/ul/li", './/div'))
        d_hospitalType = dict(enumerate(l_hospitalType, start=1))
        d_hospitalType = {v: k for k, v in d_hospitalType.items()}
        self.Web_PO.eleClkByX(ele, ".//div[2]/div/div[1]/ul/li[" + str(d_hospitalType[d_new['开发医院类型']]) + "]")
        self.Web_PO.eleClkByX(ele, ".//div[3]/button[2]")

        # 2,开发医院信息
        self._product_new__common_xpath(2)
        # 搜索,单选框
        ele = self.Web_PO.getSpanTextUpEle2("请选择开发医院信息", "../../../..")
        self.Web_PO.eleSetTextClkByX(ele, ".//div[3]/div[1]/div/div/div/div/div[2]/div/input", d_new['开发医院信息'], ".//div[3]/div[3]/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/div")
        self.Web_PO.eleClkByX(ele, ".//div[6]/button[2]")

        if d_new['开发医院类型'] == "医院":
            # 4,开发产品名称
            self._product_new__common(4, d_new['开发产品名称'])
            # 5,开发负责人1
            self._product_new__common(5, d_new['开发负责人1'])
            # 6,开发负责人2
            if d_new['开发负责人2'] != "":
                self._product_new__common(6, d_new['开发负责人2'])
            # 8,药事会计划结束日期
            self._common_date(self._product_new__common_xpathDate(8), " 请选择药事会结束时间 ", ".//div[2]/div/div", d_new['药事会计划结束日期'], ".//div[3]/button[2]")
            # 7,药事会计划开始日期
            self._common_date(self._product_new__common_xpathDate(7), " 请选择药事会开始时间 ", ".//div[2]/div/div", d_new['药事会计划开始日期'], ".//div[3]/button[2]")
            # 9,提单科室
            self._product_new__common(9, d_new['提单科室'])
            # # 提交
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[11]/button[2]")

        else:
            # 站点
            self._product_new__common(5, d_new['开发产品名称'])
            self._product_new__common(6, d_new['开发负责人1'])
            if d_new['开发负责人2'] != "":
                self._product_new__common(7, d_new['开发负责人2'])
            self._common_date(self._product_new__common_xpathDate(9), " 请选择药事会结束时间 ", ".//div[2]/div/div", d_new['药事会计划结束日期'], ".//div[3]/button[2]")
            self._common_date(self._product_new__common_xpathDate(8), " 请选择药事会开始时间 ", ".//div[2]/div/div", d_new['药事会计划开始日期'], ".//div[3]/button[2]")
            self._product_new__common(10, d_new['提单科室'])
            # 提交
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[12]/button[2]")


    def get_product_info(self, d_expected):

        # 产品开发详情

        # 获取产品开发详情
        # 选择标签
        if d_expected['标签'] == '跟进中':
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[1]/span", 2)
        elif d_expected['标签'] == '已结束':
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/span", 2)

        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div/input", d_expected["搜索"])
        sleep(2)
        # 如果开发医院没有结果，则切换标签打开发站点
        l_ = self.Web_PO.getTextsByX("//span")
        if '开发医院（0）' in l_:
            # 开发站点
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[2]/div[1]/div/div", 2)
            # 2 点击标题进入产品开发详情
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]", 2)
        else:
            # 2 点击标题进入产品开发详情
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[1]", 2)

        d_info = {}
        # 开发基础信息
        ele1 = self.Web_PO.getLabelTextUpEle2("div", "开发编码", "../..")
        l_devInfo_field = self.Web_PO.eleGetTextsByX(ele1, ".//div/div")
        l_devInfo_value = self.Web_PO.eleGetTextsByX(ele1, ".//div/span")
        d_devInfo = dict(zip(l_devInfo_field, l_devInfo_value))
        d_info['开发基础信息'] = d_devInfo

        # 开发跟进信息
        ele2 = self.Web_PO.getLabelTextUpEle2("div", "开发次数", "../..")
        l_devFollowUp_field = self.Web_PO.eleGetTextsByX(ele2, ".//div/div")
        l_devFollowUp_value = self.Web_PO.eleGetTextsByX(ele2, ".//div/span")
        d_devFollowUp = dict(zip(l_devFollowUp_field, l_devFollowUp_value))
        d_info['开发跟进信息'] = d_devFollowUp

        d_post = {}
        ele3 = self.Web_PO.getLabelTextUpEle2("th", "主要成员", "../..")
        l_principle_members = self.Web_PO.eleGetTextsByX(ele3, ".//td")
        l_principle_members = self.List_PO.group(l_principle_members, 3)
        # print("l_principle_members =>", l_principle_members)
        d_principle_members = {}
        for i in range(len(l_principle_members)):
            d_principle_members[l_principle_members[i].pop(1)] = l_principle_members[i]
        # print("主要成员 =>", d_principle_members)
        d_post['职务'] = d_principle_members

        d_members = {}
        ele3 = self.Web_PO.getLabelTextUpEle2("th", "其他药事会成员", "../..")
        l_other_members = self.Web_PO.eleGetTextsByX(ele3, ".//td")
        l_other_members = self.List_PO.group(l_other_members, 4)
        # print("l_other_members =>", l_other_members)
        d_other_members = {}
        for i in range(len(l_other_members)):
            d_other_members[l_other_members[i].pop(0)] = l_other_members[i]
        # print("其他药事会成员 =>", d_other_members)
        d_members['其他药事会成员'] = d_other_members

        d_post.update(d_members)
        d_info['拜访及态度'] = d_post

        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")
        return d_info




   # todo 审批中心
    def get_approve_list(self, d_expected):

        # 审批中心
        # 获取审批中心列表数据

        # 选择标签
        if d_expected['标签'] == '未审批':
            varDiv = 3
        elif d_expected['标签'] == '已审批':
            varDiv = 4

        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div[" + str(varDiv-2) + "]", 4)  # 点击标签（未审批或已审批）
        # 获取审批条数
        s_count = self.Web_PO.getTextByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[3]/span[1]")
        self.Web_PO.scrollToEndByKeys("/html/body/div[1]/div/div[1]/div/div[2]/div/div[" + str(varDiv) + "]/div/div/div[1]/div[2]/div[1]", 10, "/html/body/div[1]/div/div[1]/div/div[2]/div/div[" + str(varDiv) + "]/div[1]/div/div[2]", 2)
        l_approved = self.Web_PO.getTextsByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[" + str(varDiv) + "]/div/div/div[1]/div[@class='collapse-list']")
        l_approved = self.List_PO.deduplication(l_approved)
        l_no = ([i.split("\n")[0] for i in l_approved])
        d_no = dict(enumerate(l_no, start=1))
        d_no = {v:k for k,v in d_no.items()}
        print(d_no)  # {'CV340': 1, 'CV338': 2, 'CV334': 3, 'CV337': 4, 'CV336': 5}
        if s_count == len(d_no):
            print("ok, 审批条数一致", d_expected['标签'] + "共", s_count, "条审批")
        else:
            print("errorrrrrrrrrr, 审批条数不一致! ", d_expected['标签'] + "共", s_count, "条审批, 列表统计共", len(d_no), "条")

        d_approved = dict(enumerate(l_approved, start=1))
        return d_approved


        # sys.exit(0)
        #
        # # 筛选审批状态
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/img")
        # # 点击已通过
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/form/div[2]/div[2]/div[1]/div")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/form/div[3]/button[2]")
        #
        # # 选择第2个
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[4]/div/div/div[1]/div[2]")
        # # 获取审批详情
        # ele = self.Web_PO.getLabelTextUpEle2("div", "审批基础信息", "../../..")
        # l_div = self.Web_PO.eleGetTextsByX(ele, ".//div[@class='van-col van-col--24']/div")
        # l_span = self.Web_PO.eleGetTextsByX(ele, ".//div[@class='van-col van-col--24']/span")
        # d_approveList = dict(zip(l_div, l_span))
        # print(d_approveList)
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")  # 返回



    def get_approve_searchInfo(self, d_expected):
        # 审批中心

        # 选择标签
        if d_expected['标签'] == '未审批':
            varDiv = 3
        elif d_expected['标签'] == '已审批':
            varDiv = 4

        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div[" + str(varDiv-2) + "]", 2)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div[2]/div/input", d_expected['搜索'])
        self.Web_PO.scrollToEndByKeys("/html/body/div[1]/div/div[1]/div/div[2]/div/div[" + str(varDiv) + "]/div/div/div[1]/div[2]/div[1]", 8)
        l_approved = self.Web_PO.getTextsByX("//div[@class='collapse-list']")
        l_approved = self.List_PO.deduplication(l_approved)
        l_no = ([i.split("\n")[0] for i in l_approved])
        d_no = dict(enumerate(l_no, start=1))
        d_no = {v:k for k,v in d_no.items()}
        print(d_no)  # {'CV340': 1, 'CV338': 2, 'CV334': 3, 'CV337': 4, 'CV336': 5}
        # d_approved = dict(enumerate(l_approved, start=1))
        # print(d_approved)

        if d_expected['编号'] in d_no.keys():
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[" + str(varDiv) + "]/div/div/div[1]/div[" + str(d_no[d_expected['编号']]) + "]/div[2]")
            # 获取审批详情
            ele = self.Web_PO.getLabelTextUpEle2("div", "审批基础信息", "../../..")
            l_div = self.Web_PO.eleGetTextsByX(ele, ".//div[@class='van-col van-col--24']/div")
            l_span = self.Web_PO.eleGetTextsByX(ele, ".//div[@class='van-col van-col--24']/span")
            d_approve_info = dict(zip(l_div, l_span))
            # print(d_approve_info)
            return d_approve_info


        sys.exit(0)

        # 筛选审批状态
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/img")
        # 点击已通过
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/form/div[2]/div[2]/div[1]/div")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/form/div[3]/button[2]")

        # 选择第2个
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[4]/div/div/div[1]/div[2]")
        # 获取审批详情
        ele = self.Web_PO.getLabelTextUpEle2("div", "审批基础信息", "../../..")
        l_div = self.Web_PO.eleGetTextsByX(ele, ".//div[@class='van-col van-col--24']/div")
        l_span = self.Web_PO.eleGetTextsByX(ele, ".//div[@class='van-col van-col--24']/span")
        d_approveList = dict(zip(l_div, l_span))
        print(d_approveList)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")  # 返回


        # l_ = self.Web_PO.getTextsByX("//div[@class='hospital-ul van-clearfix']")
        # print(l_)


    def approve(self):
        self.Web_PO.clkByX("//a[@href='#/approve']")
        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")


 # todo 工作计划
    def jobPlan(self):
        self.Web_PO.clkByX("//a[@href='#/jobPlan']")
        # 返回
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")


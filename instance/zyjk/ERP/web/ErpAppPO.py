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
    def _common_date(self, varXpathIn, varTitle, varXpathDiv, l_expected, varXpathConfirm):

        # 选择年月日（公共封装）
        # 如：药事会计划开始日期，药事会计划结束日期

        for i in range(len(l_expected)):
            # 获取组件年月日
            ele, l_getModuleDate = self._common_date__get(varXpathIn, varTitle, varXpathDiv, varXpathConfirm)
            # 获取预期值与组件值之步长并校验比对年月日
            self._common_date__verify(ele, varXpathIn, l_expected[i], l_getModuleDate[i], varXpathDiv, i+1, varXpathConfirm)


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
    def _common_dateTime(self, varXpathIn, varTitle, varXpathDiv, l_expected, varXpathConfirm):

        # 选择年月日时分（公共封装）
        # 如：药事会实际召开时间

        for i in range(len(l_expected)):
            # 获取组件年月日
            ele, l_getModuleDate = self._common_dateTime__get(varXpathIn, varTitle, varXpathDiv, varXpathConfirm)
            # 获取预期值与组件值之步长并校验比对年月日
            self._common_dateTime__verify(ele, varXpathIn, l_expected[i], l_getModuleDate[i], varXpathDiv, i + 1, varXpathConfirm)




    def _product_new__list(self):
        # 获取新增产品开发列表页数据

        # 1/3 获取字段列表（不包括所属医院信息）
        # 统计字段数量
        i_fieldCount = self.Web_PO.getQtyByX("//form[@class='van-form']/div")
        l_field = []
        for i in range(i_fieldCount-2):
            s_text = self.Web_PO.getTextByX("//form[@class='van-form']/div[" + str(i+1) + "]/div[1]/div/div/div")
            if s_text != '所属医院信息':
                l_field.append(s_text)
        # print(l_field)  # ['开发医院类型', '开发医院信息', '开发医院级别', '开发产品名称', '开发负责人1', '开发负责人2', '药事会计划开始日期', '药事会计划结束日期', '提单科室']

        # 2/3 获取字段的shadow的的值（不包括所属医院信息的值）
        l_text_shadow = self.Web_PO.getShadowRoots('//input', 'div:nth-of-type(2)')
        # print(l_text_shadow)  # ['站点', '曹路社区永丰村卫生室', '一级医院', '依叶', '薛伟', '陈东升', '2025-10-09', '2025-11-11', '呼吸科', '', '曹路社区']
        l_value = l_text_shadow[:-2]

        # 3/3 合并字典
        d_new = dict(zip(l_field, l_value))
        # 追加'所属医院信息'
        ele_upup = self.Web_PO.getDivTextUpEle2("所属医院信息", "../../../..")
        s_text = self.Web_PO.eleGetTextByX(ele_upup, ".//div[2]/span")
        d_new['所属医院信息'] = s_text
        print(d_new)
        return d_new
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
    def product_new(self, d_new):
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

            # 获取新增产品开发列表页数据
            d_new = self._product_new__list()

            # # 提交
            # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[11]/button[2]")
            # # 取消
            # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[11]/button[1]")

        else:
            # 站点
            self._product_new__common(5, d_new['开发产品名称'])
            self._product_new__common(6, d_new['开发负责人1'])
            if d_new['开发负责人2'] != "":
                self._product_new__common(7, d_new['开发负责人2'])
            self._common_date(self._product_new__common_xpathDate(9), " 请选择药事会结束时间 ", ".//div[2]/div/div", d_new['药事会计划结束日期'], ".//div[3]/button[2]")
            self._common_date(self._product_new__common_xpathDate(8), " 请选择药事会开始时间 ", ".//div[2]/div/div", d_new['药事会计划开始日期'], ".//div[3]/button[2]")
            self._product_new__common(10, d_new['提单科室'])

            # 获取新增产品开发列表页数据
            d_new = self._product_new__list()

            # 提交
            # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[12]/button[2]")
            # 取消
            # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[12]/button[1]")



    def _product_visitor(self, d_expected):

        # 拜访及态度

        # 1 获取医院开发信息，生成字典d_devInfo
        ele = self.Web_PO.getSpanTextUpEle2("医院开发信息", "../..")
        i_fieldCount = self.Web_PO.eleGetQtyByX(ele, ".//div[2]/div[@class='van-col van-col--24']")
        l_field = []
        for i in range(i_fieldCount):
            s_text = self.Web_PO.eleGetTextByX(ele, ".//div[2]/div[" + str(i+1) + "]/div/div[1]/span")
            l_field.append(s_text)
        # print(l_field)  # ['医院信息', '产品信息', '负责人']
        # 获取医院开发信息shadow值
        l_devInfo_shadow = []
        l_shadow = self.Web_PO.getShadowRoots('//input', 'div:nth-last-of-type(1)')
        l_devInfo_shadow.append(l_shadow.pop(0))
        l_devInfo_shadow.append(l_shadow.pop(0))
        l_devInfo_shadow.append(l_shadow.pop(0))
        # print(l_devInfo_shadow)  # ['HCO00000122-崇中心', '氨叶-CP102', '薛伟、彭琦']
        d_devInfo = dict(zip(l_field, l_devInfo_shadow))
        print(d_devInfo)  # {'医院信息': 'HCO00000122-崇中心', '产品信息': '氨叶-CP102', '负责人': '薛伟、彭琦'}

        # 2 获取开发跟进信息，生成字典d_actual
        # 2.1 主要成员及态度
        # print(l_shadow)  # ['韦彩雯', '支持', '杨忠英', '支持', ...
        l_post = ['科室主任', '药剂科主任', '医务处长', '业务院长', '院长']
        d_actual = {}
        for i in range(len(l_post)):
            l_1 = []
            l_1.append(l_shadow.pop(0))
            l_1.append(l_shadow.pop(0))
            d_1 = self.List_PO.pair2dict(l_1)
            d_actual[l_post[i]] = d_1
        # print(d_actual)  # {'科室主任': {'陈健': '支持'}, '药剂科主任': {'杨忠英': '支持'}, '医务处长': {'陈海群': '支持'}, '业务院长': {'陈海群': '支持'}, '院长': {'陈健': '支持'}}

        # 2.2 其他药事会成员及态度
        # print(l_shadow)  # ['韦彩雯', '支持', '杨忠英', '支持', ...
        d_devFollowUp = self.List_PO.pair2dict(l_shadow)
        # print(d_devFollowUp)  # {'韦彩雯': '支持', '杨忠英': '支持', '陈海群': '支持'...
        d_actual['其他药事会成员'] = d_devFollowUp


        # 3 比对预期值与开发跟进信息和其他药事会成员数据，如不一致则进行更新。
        print("d_actual =>", d_actual)
        print("d_expected =>", d_expected)

        # 3.1 修改主要成员
        for index, i in enumerate(l_post, start=2):
            if d_expected[i] != d_actual[i]:
                if list(d_expected[i].keys())[0] != list(d_actual[i].keys())[0]:
                    self.Web_PO.eleClkByX(ele, ".//table[1]/tr[" + str(index) + "]/td[1]/div/div/div/input")
                    ele2 = self.Web_PO.getDivTextUpEle(" 主要成员选择 ")
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/div/div/div[2]/div/input", list(d_expected[i].keys())[0])
                    self.Web_PO.eleClkByX(ele2, ".//div[3]/div/div[2]/button[2]", 2)
                if list(d_expected[i].values())[0] != list(d_actual[i].values())[0]:
                    self.Web_PO.eleClkByX(ele, ".//table[1]/tr[" + str(index) + "]/td[3]/div/div/div/input")
                    ele2 = self.Web_PO.getDivTextUpEle(" 主要成员选择 ")
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/div/div/div[2]/div/input", list(d_expected[i].values())[0])
                    self.Web_PO.eleClkByX(ele2, ".//div[3]/div/div[2]/button[2]", 2)


        # 3.2 修改其他药事会成员
        # 操作逻辑：删除所有记录后再添加
        # 删除第一条
        ele3 = self.Web_PO.getLabelTextUpEle2("th", "其他药事会成员", "../..")
        qty_row = self.Web_PO.eleGetQtyByX(ele3, ".//div/div[@class='van-swipe-cell']")
        # print(qty_row)
        for i in range(qty_row):
            self.Web_PO.scrollLeftRight(ele3, ".//div/div[1]/div", -50)
            self.Web_PO.eleClkByX(ele3, ".//div/div[1]/div/div/div/button")

        # 点击增加一行新记录
        for i in range(len(d_expected['其他药事会成员'])):

            self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[3]/table[2]/div/div/button")
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/table[2]/div/div/button")

            self.Web_PO.eleClkByX(ele, ".//table[2]/div/div[" + str(i+1) + "]/div/tr/td[1]/div/div/div/input")
            ele2 = self.Web_PO.getDivTextUpEle(" 主要成员选择 ")
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/div/div/div[2]/div/input", list(d_expected['其他药事会成员'].keys())[i])
            self.Web_PO.eleClkByX(ele2, ".//div[3]/div/div[2]/button[2]")

            self.Web_PO.eleClkByX(ele, ".//table[2]/div/div[" + str(i+1) + "]/div/tr/td[4]/div/div/div/input")
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/div/div/div[2]/div/input", list(d_expected['其他药事会成员'].values())[i])
            self.Web_PO.eleClkByX(ele2, ".//div[3]/div/div[2]/button[2]")


        # 提交
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[4]/button[2]")
        # 拜访人信息录入成功（确定）
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[5]")

    def _product_devFollowUp__list(self):
        # 获取开发跟进反馈列表页数据
        d_dev = {}

        # 1/3 获取shadow的的值
        l_text_shadow = self.Web_PO.getShadowRoots('//input', 'div')
        # print(l_text_shadow)
        l_value = l_text_shadow[:-1]
        l_field = ['医院信息', '产品信息', '负责人', '开发次数', '提单科室', '提单规则', '提单状态', '药剂科会前确认信息', '药事会计划开始日期', '药事会计划结束日期',
                   '药事会实际召开时间', '会前评估能否过会', '经改进后能否过会', '过会日期']
        d_dev = dict(zip(l_field, l_value))

        # 2/3 过会规则
        l_text_shadow = self.Web_PO.getShadowRoots('//textarea', 'div')
        d_dev['过会规则'] = l_text_shadow

        # 3/3 获取span的值
        l_text_span = self.Web_PO.getTextsByX("//div[@class='van-col van-col--24']/span")
        d_dev['采购时间'] = l_text_span[0]
        d_dev['更新时间'] = l_text_span[1]
        return d_dev
    def _product_devFollowUp__common_xpath(self, varDiv):
        # 公共表单（产品开发 - 开发跟进反馈）
        # 第一层
        return "/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[" + str(varDiv) + "]/div/div[2]/div/input"
    def _product_devFollowUp__common(self, varDiv, varValue):
        # 公共表单（产品开发 - 开发跟进反馈）
        self.Web_PO.clkByX(self._product_devFollowUp__common_xpath(varDiv))
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[2]/div/div/div[2]/div/input", varValue)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/button[2]")  # 确认
    def _product_devFollowUp(self, d_edit):
        # 开发跟进


        # 点击开发跟进（产品开发）
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[3]/button[2]")

        # 开发次数
        self._product_devFollowUp__common(1, d_edit['开发次数'])

        # 提单科室
        self._product_devFollowUp__common(2, d_edit['提单科室'])

        # 提单规则
        self._product_devFollowUp__common(3, d_edit['提单规则'])

        # # 过会规则
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[4]/div/div[2]/div/textarea")
        l_afterMeetingRule = self.Web_PO.getTextsByX("//div[@role='checkbox']/span")
        dd_ = dict(enumerate(l_afterMeetingRule, start=1))
        d_afterMeetingRule = {v: k for k, v in dd_.items()}
        ele = self.Web_PO.getDivTextUpEle("选择过会规则")
        for i in range(len(d_edit["过会规则"])):
            self.Web_PO.eleClkByX(ele, ".//div[2]/div[" + str(d_afterMeetingRule[d_edit["过会规则"][i]]) + "]/div")
        self.Web_PO.eleClkByX(ele, ".//div[3]/button[2]")

        # 提单状态
        self._product_devFollowUp__common(5, d_edit['提单状态'])

        # 药剂科会前确认信息
        self._product_devFollowUp__common(6, d_edit['药剂科会前确认信息'])

        # 药事会计划结束日期
        self._common_date(self._product_devFollowUp__common_xpath(8), " 请选择药事会结束时间 ", ".//div[2]/div/div", d_edit['药事会计划结束日期'], ".//div[3]/button[2]")

        # # 药事会计划开始日期
        self._common_date(self._product_devFollowUp__common_xpath(7), " 请选择药事会开始时间 ", ".//div[2]/div/div", d_edit['药事会计划开始日期'], ".//div[3]/button[2]")

        # # 药事会实际召开时间
        self._common_dateTime(self._product_devFollowUp__common_xpath(9), "药事会实际召开时间选择", ".//div[2]/div[2]", d_edit['药事会实际召开时间'], ".//div[2]/div[1]/button[2]")

        # 会前评估能否过会
        self._product_devFollowUp__common(10, d_edit['会前评估能否过会'])

        # 经改进后能否过会
        self._product_devFollowUp__common(11, d_edit['经改进后能否过会'])

        if d_edit['会前评估能否过会'] == '是' or d_edit['经改进后能否过会'] == '是':
            self._common_date(self._product_devFollowUp__common_xpath(12), "过会时间选择", ".//div[2]/div[2]", d_edit['过会日期'], ".//div[2]/div[1]/button[2]")

        # 获取开发跟进反馈列表页数据
        d_dev = self._product_devFollowUp__list()


        # 提交
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[4]/button[2]")


    def product_dev(self, d_visotor, d_edit):

        # 产品开发

        # 开发医院 - 拜访人
        # 搜索医院、负责人
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div/input", d_visotor['搜索'])
        # 点击拜访人
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[3]/button[1]")
        self._product_visitor(d_visotor)

        # 开发医院 - 开发跟进
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div/input",d_edit['搜索'])
        # 点击开发跟进
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[3]/button[2]")
        # d_dev = self._product_devFollowUp(d_edit)
        # print(d_dev)



    # todo 产品开发
    def product(self, d_new, d_visitor, d_edit):

        # 点击产品开发
        self.Web_PO.clkByX("//a[@href='#/product']")

        # 新增产品开发
        # self.product_new(d_new)

        # # 开发医院（拜访人,开发跟进）
        self.product_dev(d_visitor, d_edit)



        # 返回
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")


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


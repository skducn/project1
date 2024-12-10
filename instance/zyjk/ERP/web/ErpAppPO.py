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

    def _topRank_getStep(self, l_expected, l_actual):
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
            self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
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
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
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
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
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
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
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

    def _topRank_getStep(self, l_expected, l_actual):
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
            self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
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
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
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
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
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
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div/div[" + str(
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
        l_ = self._topRank_getStep(l_expected, l_sysDate)
        # print(l_)  # (40, 220, 100)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span")
        self.Web_PO.scrollDateTime(
            "//div[@class='van-picker van-datetime-picker']/div/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
            l_[0])
        self.Web_PO.scrollDateTime(
            "//div[@class='van-picker van-datetime-picker']/div/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
            l_[1])
        self.Web_PO.scrollDateTime(
            "//div[@class='van-picker van-datetime-picker']/div/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
            l_[2])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[3]/button[2]")

        # 获取修改后的日期
        l_actual_tmp = self._topRank_getDate()
        print("l_actual_tmp =>", l_actual_tmp)  # [2022, 4, 1]

        # 校验日期
        self._topRank_verifyDate(l_expected[0], l_actual_tmp[0], 1)
        self._topRank_verifyDate(l_expected[1], l_actual_tmp[1], 2)
        self._topRank_verifyDate(l_expected[2], l_actual_tmp[2], 3)

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

    def _hospital_getStep(self, l_expected, l_actual):
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


    def __hospital_dataTime(self, varTD, l_dateTime ):
        # __hospital_dataTime(6, d_['药事会实际召开时间'])
        # __hospital_dataTime(9, d_['过会日期'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)

        l_ = self._hospital_getStep(l_dateTime, self._hospital_getDateTime())
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[" + str(varTD) + "]/div[2]/div/input", 2)
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[0])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[1])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[2])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[4]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[3])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[5]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[4])
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
                                 # /html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[2]/div/tr/td[1]/div/div/div/input
        self.Web_PO.scrollToLeft("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div", -50)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div/div/div/button")
                          # /html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[2]/div/div/div/button
        # self.Web_PO.scrollToLeft("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[2]/div[1]/div/tr/td[1]/div/div/div", 444)
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


    def _product_verifyDate_afterMeeting(self, varPathIn, varPathConfirm, varExpected, varActual, varLoc):
        # 校验日期
        sleep(2)
        if varExpected != varActual:
            self.Web_PO.clkByX(varPathIn)
            if varExpected > varActual:
                var_ = (varExpected - varActual) * -20
            else:
                var_ = (varActual - varExpected) * 20
            self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
            sleep(2)
            varActual = self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
            varActual = int(varActual[:-1])
            self.Web_PO.clkByX(varPathConfirm)

            if varExpected != varActual:
                self.Web_PO.clkByX(varPathIn)
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX(varPathConfirm)
            if varExpected != varActual:
                self.Web_PO.clkByX(varPathIn)
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX(varPathConfirm)
            if varExpected != varActual:
                self.Web_PO.clkByX(varPathIn)
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX(varPathConfirm)

    def _product_verifyDate(self, varPathIn, varPathConfirm, varExpected, varActual, varLoc):
        # 校验日期
        sleep(2)
        if varExpected != varActual:
            self.Web_PO.clkByX(varPathIn)
            if varExpected > varActual:
                var_ = (varExpected - varActual) * -20
            else:
                var_ = (varActual - varExpected) * 20
            # self.Web_PO.scrollDateTime("//div[@class='van-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
            self.Web_PO.scrollDateTime("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
            sleep(2)
            # varActual = self.Web_PO.getTextByX("//div[@class='van-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
            varActual = self.Web_PO.getTextByX("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
            varActual = int(varActual[:-1])
            self.Web_PO.clkByX(varPathConfirm)
            if varExpected != varActual:
                self.Web_PO.clkByX(varPathIn)
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                # self.Web_PO.scrollDateTime("//div[@class='van-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                self.Web_PO.scrollDateTime("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                # varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = self.Web_PO.getTextByX("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX(varPathConfirm)

                # self.Web_PO.clkByX("//div[@class='van-popup van-popup--round van-popup--bottom']/div[3]/button[2]")
            if varExpected != varActual:
                self.Web_PO.clkByX(varPathIn)
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                # self.Web_PO.scrollDateTime("//div[@class='van-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                self.Web_PO.scrollDateTime("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                # varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = self.Web_PO.getTextByX("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX(varPathConfirm)

                # self.Web_PO.clkByX("//div[@class='van-popup van-popup--round van-popup--bottom']/div[3]/button[2]")
            if varExpected != varActual:
                self.Web_PO.clkByX(varPathIn)
                if varExpected > varActual:
                    var_ = (varExpected - varActual) * -20
                else:
                    var_ = (varActual - varExpected) * 20
                # self.Web_PO.scrollDateTime("//div[@class='van-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                self.Web_PO.scrollDateTime("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
                sleep(2)
                # varActual = int(self.Web_PO.getTextByX("//div[@class='van-picker']/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
                varActual = self.Web_PO.getTextByX("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
                varActual = int(varActual[:-1])
                self.Web_PO.clkByX(varPathConfirm)

                # self.Web_PO.clkByX("//div[@class='van-popup van-popup--round van-popup--bottom']/div[3]/button[2]")

    def _product_dateModule_afterMeeting(self, varPathIn, varTitle, varPathConfirm):

        # 获取日期
        self.Web_PO.clkByX(varPathIn, 3)
        ele = self.Web_PO.getDivTextUpEle(varTitle, "..")
        year = self.Web_PO.eleGetTextByX(ele, ".//div[2]/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
        month = self.Web_PO.eleGetTextByX(ele, ".//div[2]/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
        day = self.Web_PO.eleGetTextByX(ele, ".//div[2]/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
        l_1 = []
        l_1.append(year)
        l_1.append(month)
        l_1.append(day)
        print("过会日期 => ", l_1)
        l_actual_tmp = []
        for i in l_1:
            i = i.replace("年", "").replace("月", "").replace("日", "")
            l_actual_tmp.append(int(i))

        self.Web_PO.eleClkByX(ele, varPathConfirm)
        # day = self.Web_PO.eleClkByX(ele, ".//div[@class='van-popup van-popup--round van-popup--bottom']/div/div[2]/div[1]/button[2]")

        # self.Web_PO.clkByX(varPathConfirm)
        return l_actual_tmp

    def _product_dateModule(self, varPathIn, varTitle, varPathConfirm):

        # 获取日期
        self.Web_PO.clkByX(varPathIn, 2)
        # ele = self.Web_PO.getDivTextUpEle(" 请选择药事会结束时间 ", "..")
        ele = self.Web_PO.getDivTextUpEle(varTitle, "..")
        # print(self.Web_PO.eleGetAttrByX(ele, "style"))

        # self.Web_PO.eleClkByX(ele, ".//div[3]/button[2]")
        # # print(self.Web_PO.eleGetTextByX(ele, "//div[1]"))
        # print(self.Web_PO.getTextByX("//div[2]/div/div/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        # print(self.Web_PO.getTextByX("//div[2]/div/div/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        # print(self.Web_PO.getTextByX("//div[2]/div/div/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        # sys.exit(0)

        year = self.Web_PO.eleGetTextByX(ele, ".//div[2]/div/div/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
        month = self.Web_PO.eleGetTextByX(ele, ".//div[2]/div/div/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
        day = self.Web_PO.eleGetTextByX(ele, ".//div[2]/div/div/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
        l_1 = []
        l_1.append(year)
        l_1.append(month)
        l_1.append(day)
        # l_1 = self.Web_PO.getTextsByX("//ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div")
        # l_1 = self.List_PO.dels(l_1, "")
        # print("日期 => ", l_1)
        l_actual_tmp = []
        for i in l_1:
            i = i.replace("年", "").replace("月", "").replace("日", "")
            l_actual_tmp.append(int(i))
        # print(varPathConfirm)
        self.Web_PO.eleClkByX(ele, varPathConfirm)
        # self.Web_PO.clkByX(varPathConfirm)
        # self.Web_PO.clkByX("//div[@class='van-popup van-popup--round van-popup--bottom']/div[3]/button[2]")

        return l_actual_tmp

    def _product_date_afterMeeting(self, varPathIn, varTitle, l_expected, varPathConfirm):

        # 过会日期 - 选择年月日

        # 第一次获取日期组件默认年月日
        l_actual_tmp = self._product_dateModule_afterMeeting(varPathIn, varTitle, varPathConfirm)

        # 模拟鼠标上下滚动，修改日期
        l_ = self._topRank_getStep(l_expected, l_actual_tmp)
        self.Web_PO.clkByX(varPathIn)
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[0])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[1])
        self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[2])
        self.Web_PO.clkByX(varPathConfirm)

        # 第二次获取日期组件默认年月日（即修改后的日期）
        l_actual_tmp = self._product_dateModule_afterMeeting(varPathIn, varTitle, varPathConfirm)
        # print("修改日期 =>", l_actual_tmp)  # [2022, 4, 1]

        # 校验日期
        self._product_verifyDate_afterMeeting(varPathIn, varPathConfirm, l_expected[0], l_actual_tmp[0], 1)
        self._product_verifyDate_afterMeeting(varPathIn, varPathConfirm, l_expected[1], l_actual_tmp[1], 2)
        self._product_verifyDate_afterMeeting(varPathIn, varPathConfirm, l_expected[2], l_actual_tmp[2], 3)

        # 第N次获取日期组件默认年月日（即最终修改后的日期）
        l_actual_tmp = self._product_dateModule_afterMeeting(varPathIn, varTitle, varPathConfirm)
        print("过会日期 =>", l_actual_tmp)  # [2022, 1, 1]

        if l_expected == l_actual_tmp:
            print(1)
            return 1
        else:
            print(0)
            return 0

    def _product_date(self, varPathIn, varTitle, l_expected, varPathConfirm):

        # 药事会计划开始日期，药事会计划结束日期 - 选择年月日

        # 第一次获取日期组件默认年月日
        l_actual_tmp = self._product_dateModule(varPathIn, varTitle, varPathConfirm)

        # 模拟鼠标上下滚动，修改日期
        l_ = self._topRank_getStep(l_expected, l_actual_tmp)
        self.Web_PO.clkByX(varPathIn, 2)
        ele = self.Web_PO.getDivTextUpEle(varTitle, "..")
        self.Web_PO.scrollDateTime(ele, ".//div[2]/div/div/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[0])
        self.Web_PO.scrollDateTime(ele, ".//div[2]/div/div/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[1])
        self.Web_PO.scrollDateTime(ele, ".//div[2]/div/div/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[2])
        # self.Web_PO.scrollDateTime("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[0])
        # self.Web_PO.scrollDateTime("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[1])
        # self.Web_PO.scrollDateTime("//div[@class='van-popup van-popup--round van-popup--bottom']/div[2]/div/div/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[2])
        self.Web_PO.eleClkByX(ele, varPathConfirm)
        # self.Web_PO.clkByX(varPathConfirm)
        # self.Web_PO.clkByX("//div[@class='van-popup van-popup--round van-popup--bottom']/div[3]/button[2]")

        # 第二次获取日期组件默认年月日（即修改后的日期）
        l_actual_tmp = self._product_dateModule(varPathIn, varTitle, varPathConfirm)
        # print("修改日期 =>", l_actual_tmp)  # [2022, 4, 1]

        # 校验日期
        self._product_verifyDate(varPathIn, varPathConfirm, l_expected[0], l_actual_tmp[0], 1)
        self._product_verifyDate(varPathIn, varPathConfirm, l_expected[1], l_actual_tmp[1], 2)
        self._product_verifyDate(varPathIn, varPathConfirm, l_expected[2], l_actual_tmp[2], 3)

        # 第N次获取日期组件默认年月日（即最终修改后的日期）
        l_actual_tmp = self._product_dateModule(varPathIn, varTitle, varPathConfirm)
        print(varTitle, " =>", l_actual_tmp)  # [2022, 1, 1]

        if l_expected == l_actual_tmp:
            print(1)
            return 1
        else:
            print(0)
            return 0

    # def _product_date1(self, l_expected, varPath, varXpathButton):
    #
    #     # 药事会计划开始日期，药事会计划结束日期 - 选择年月日
    #
    #     # 第一次获取日期组件默认年月日
    #     l_actual_tmp = self._product_dateModule(varPath, varXpathButton)
    #
    #     # 模拟鼠标上下滚动，修改日期
    #     l_ = self._topRank_getStep(l_expected, l_actual_tmp)
    #     self.Web_PO.clkByX(varPath)
    #     self.Web_PO.scrollDateTime("//div[@class='van-picker']/div/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[0])
    #     self.Web_PO.scrollDateTime("//div[@class='van-picker']/div/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[1])
    #     self.Web_PO.scrollDateTime("//div[@class='van-picker']/div/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[2])
    #     self.Web_PO.clkByX(varXpathButton)
    #
    #
    #     # 第二次获取日期组件默认年月日（即修改后的日期）
    #     l_actual_tmp = self._product_dateModule(varPath, varXpathButton)
    #     print("修改日期 =>", l_actual_tmp)  # [2022, 4, 1]
    #
    #     # 校验日期
    #     self._product_verifyDate(varPath, l_expected[0], l_actual_tmp[0], 1, varXpathButton)
    #     self._product_verifyDate(varPath, l_expected[1], l_actual_tmp[1], 2, varXpathButton)
    #     self._product_verifyDate(varPath, l_expected[2], l_actual_tmp[2], 3, varXpathButton)
    #
    #     # 第N次获取日期组件默认年月日（即最终修改后的日期）
    #     l_actual = self._product_dateModule(varPath, varXpathButton)
    #     print(varTitle, " =>", l_actual)  # [2022, 1, 1]
    #
    #     if l_expected == l_actual:
    #         print(1)
    #         return 1
    #     else:
    #         print(0)
    #         return 0

    def _product_new(self, d_):

        # 新增（产品开发右上角）
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[3]")

        # 1,开发医院类型
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[1]/div[2]/div/input")
        if d_['开发医院类型'] == '医院':
            # 医院
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/ul/li[1]", 2)
        else:
            # 站点
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/ul/li[2]", 2)
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[3]/button[2]")  # 确认
        # 2,开发医院信息
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[2]/div[2]/div/input", 2)
        # 搜索
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div[2]/div/div/div[3]/div[1]/div/div/div/div/div[2]/div/input", d_['开发医院信息'])
        # 单选框
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div[2]/div/div/div[3]/div[3]/div[1]/div/div/div/div[1]/div[1]/div[1]/div")
        # 确定
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div[2]/div/div/div[6]/button[2]")
        # 3,开发产品名称
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[4]/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div/input", d_['开发产品名称'])
        # 确认
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[4]/button[2]")
        # 4.1,开发负责人1
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[5]/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div/input", d_['开发负责人1'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[4]/button[2]")  # 确认
        # 4.2,开发负责人2
        if d_['开发负责人2'] != "":
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[6]/div[2]/div/input")
            self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div/input", d_['开发负责人2'])
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[4]/button[2]")  # 确认

        # # 6,药事会计划结束日期
        self._product_date("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[8]/div[2]/div/input",
                           " 请选择药事会结束时间 ", d_['药事会计划结束日期'], ".//div[3]/button[2]")

        # 5,药事会计划开始日期
        self._product_date("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[7]/div[2]/div/input",
                           " 请选择药事会开始时间 ", d_['药事会计划开始日期'], ".//div[3]/button[2]")

        # 7,提单科室
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[9]/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div/input", d_['提单科室'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[2]/div[4]/button[2]")  # 确认

        # 提交
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/form/div[11]/button[2]")

    def _product_verifyDateTime(self, varXpath, varActual, varExpected, varLoc):
        # verifyDateTime(6, d_['药事会实际召开时间'][2], defaultDay, varDay, 3)
        if varActual != varExpected:
            self.Web_PO.clkByX(varXpath, 2)
            if varActual > varExpected:
                var_ = (varActual - varExpected) * -20
            else:
                var_ = (varExpected - varActual) * 20
            self.Web_PO.scrollDateTime("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", var_)
            sleep(3)
            varExpected = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[" + str(varLoc) + "]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
            self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")
            if varActual != varExpected:
                self.Web_PO.clkByX(varXpath, 2)
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
                self.Web_PO.clkByX(varXpath, 2)
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
                self.Web_PO.clkByX(varXpath, 2)
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

    def __product_dataTime(self, varXpathIn, l_dateTime):
        # __product_dataTime(6, d_['药事会实际召开时间'])
        # __product_dataTime(9, d_['过会日期'])
        self.Web_PO.clkByX(varXpathIn, 2)
        l_ = self._hospital_getStep(l_dateTime, self._hospital_getDateTime())

        self.Web_PO.clkByX(varXpathIn, 2)
        ele = self.Web_PO.getDivTextUpEle("药事会实际召开时间选择","..")
        self.Web_PO.scrollDateTime(ele,".//div[2]/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[0])
        self.Web_PO.scrollDateTime(ele,".//div[2]/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[1])
        self.Web_PO.scrollDateTime(ele,".//div[2]/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[2])
        self.Web_PO.scrollDateTime(ele,".//div[2]/div[2]/div[4]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[3])
        self.Web_PO.scrollDateTime(ele,".//div[2]/div[2]/div[5]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", l_[4])
        # self.Web_PO.scrollDateTime(
        #     "//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
        #     l_[1])
        # self.Web_PO.scrollDateTime(
        #     "//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
        #     l_[2])
        # self.Web_PO.scrollDateTime(
        #     "//div[@class='van-picker van-datetime-picker']/div[2]/div[4]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
        #     l_[3])
        # self.Web_PO.scrollDateTime(
        #     "//div[@class='van-picker van-datetime-picker']/div[2]/div[5]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div",
        #     l_[4])
        l_revise = self._hospital_getDateTime()

        # 校验年月日时分(varTD 对应 div[6])
        self._product_verifyDateTime(varXpathIn, l_dateTime[0], l_revise[0], 1)
        self._product_verifyDateTime(varXpathIn, l_dateTime[1], l_revise[1], 2)
        self._product_verifyDateTime(varXpathIn, l_dateTime[2], l_revise[2], 3)
        self._product_verifyDateTime(varXpathIn, l_dateTime[2], l_revise[2], 3)  # 重复跑
        self._product_verifyDateTime(varXpathIn, l_dateTime[3], l_revise[3], 4)
        self._product_verifyDateTime(varXpathIn, l_dateTime[3], l_revise[3], 4)
        self._product_verifyDateTime(varXpathIn, l_dateTime[4], l_revise[4], 5)
        self._product_verifyDateTime(varXpathIn, l_dateTime[4], l_revise[4], 5)
        self._product_verifyDateTime(varXpathIn, l_dateTime[4], l_revise[4], 5)

        self.Web_PO.clkByX(varXpathIn, 2)
        l_result = self._hospital_getDateTime()
        if l_dateTime == l_result:
            return 1
        else:
            return 0

    def __product_devFollowUp(self, d_edit):


        # 开发跟进
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[3]/button[2]")

        # # # # 开发次数
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[1]/div/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[2]/div/div/div[2]/div/input", d_edit['开发次数'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/button[2]")  # 确认
        # #
        # # # 提单科室
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[2]/div/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[2]/div/div/div[2]/div/input", d_edit['提单科室'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/button[2]")
        # #
        # # # 提单规则
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[3]/div/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[2]/div/div/div[2]/div/input", d_edit['提单规则'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/button[2]")
        # #
        # # # # 过会规则
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[4]/div/div[2]/div/textarea")
        l_afterMeetingRule = self.Web_PO.getTextsByX("//div[@role='checkbox']/span")
        # print("l_afterMeetingRule => ", l_afterMeetingRule)
        dd_ = dict(enumerate(l_afterMeetingRule, start=1))
        d_afterMeetingRule = {v: k for k, v in dd_.items()}
        # print("d_afterMeetingRule => ", d_afterMeetingRule)  # {'药剂科主任确认即可过会': 1, '需投票，过二分之一票数': 2, '需投票，过三分之二票数': 3, '院长确认即可过会': 4, '分院院长确认即可过会': 5, '临床主任确认即可过会': 6}
        for i in range(len(d_edit["过会规则"])):
            self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[7]/div/div[2]/div[" + str(d_afterMeetingRule[d_edit["过会规则"][i]]) + "]/div")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[7]/div/div[3]/button[2]")
        # #
        # # 提单状态
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[5]/div/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[2]/div/div/div[2]/div/input", d_edit['提单状态'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/button[2]")
        #
        # # # 药剂科会前确认信息
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[6]/div/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[2]/div/div/div[2]/div/input", d_edit['药剂科会前确认信息'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/button[2]")
        # # #

        # # 药事会计划结束日期
        self._product_date("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[8]/div/div[2]/div/input",
                           " 请选择药事会结束时间 ", d_edit['药事会计划结束日期'], ".//div[3]/button[2]")

        # 药事会计划开始日期
        self._product_date("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[7]/div/div[2]/div/input",
                           " 请选择药事会开始时间 ", d_edit['药事会计划开始日期'], ".//div[3]/button[2]")

        # # 药事会实际召开时间
        conveningTime = self.__product_dataTime("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[9]/div/div[2]/div/input", d_edit['药事会实际召开时间'])
        # # print(conveningTime) # 1

        # # # 会前评估能否过会
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[10]/div/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[2]/div/div/div[2]/div/input", d_edit['会前评估能否过会'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/button[2]")
        #
        # # 经改进后能否过会
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[11]/div/div[2]/div/input")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[2]/div/div/div[2]/div/input", d_edit['经改进后能否过会'])
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/button[2]")

        if d_edit['会前评估能否过会'] =='是' or d_edit['经改进后能否过会'] =='是':
            # 过会日期(in,title,value,confirm)
            self._product_date_afterMeeting("/html/body/div[1]/div/div[1]/div/div[3]/div[4]/div[12]/div/div[2]/div/input",
                                            "过会时间选择", d_edit['过会日期'], ".//div/div[2]/div[1]/button[2]")



        # 获取列表页所有值
        # 1/2 获取shadow的的值
        l_text_shadow = self.Web_PO.getShadowRoots('//input', 'div')
        print(l_text_shadow)
        l_text_shadow = self.Web_PO.getShadowRoots('//textarea', 'div')
        print("过会规则 =>", l_text_shadow)

        # 2/2获取span的值
        l_text_span = self.Web_PO.getTextsByX("//div[@class='van-col van-col--24']/span")
        print(l_text_span)


        # 提交
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[4]/button[2]")

    def _product_edit(self, d_edit):

        self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div/input", d_edit['搜索'])

        # self.__product_visitor()
        # 拜访人
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[3]/div/div[2]/div[5]/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[3]/button[1]")

        # 开发跟进反馈
        self.__product_devFollowUp(d_edit)



    # todo 产品开发
    def product(self, d_new, d_edit):
        # 产品开发
        self.Web_PO.clkByX("//a[@href='#/product']")

        # 新增产品开发
        # self._product_new(d_new)

        # # 编辑产品开发
        self._product_edit(d_edit)



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


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

    # def scroll_from_element(self, on_element, xoffset, yoffset):
    #     """
    #     从on_element开始触摸和滚动，通过xoffset和yoffset移动。
    #
    #
    #     :Args:
    #      - on_element: The element where scroll starts.
    #      - xoffset: X offset to scroll to.
    #      - yoffset: Y offset to scroll to.
    #     """
    #     self._actions.append(lambda: self._driver.execute(Command.TOUCH_SCROLL, {
    #             'element': on_element.id,
    #             'xoffset': int(xoffset),
    #             'yoffset': int(yoffset)}))
    #     return self

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
        # 产品信息
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/input")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[3]/div/div[2]/div[1]/button[2]", 2)

        # 1 拜访及态度
        # 主要成员
        # 科室主任 - 主要成员
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[2]/td[1]/div/div/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input", d_['科室主任'][0])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[3]/div[1]/button[2]")
        # # 科室主任 - 态度
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[2]/td[3]/div/div/div/input", 2)
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[2]/div[1]/ul/li[" + str(self._attitude(d_['科室主任'][1])) + "]")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[1]/button[2]")
        # # 院长 - 主要成员
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[6]/td[1]/div/div/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input", d_['院长'][0])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[3]/div[1]/button[2]")
        # # 院长 - 态度
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/table[1]/tr[6]/td[3]/div/div/div/input", 2)
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[2]/div[1]/ul/li[" + str(self._attitude(d_['院长'][1])) + "]")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[7]/div/div[2]/div[1]/button[2]")

        # 2 开发跟进反馈
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[1]/div/div[2]", 2)

        # # # 提单科室
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[2]/div/div/div[2]/div/input", d_['提单科室'])
        #                       # /html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[2]/div/div/div[2]/div/input
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[3]/div[1]/button[2]")
        # # 提单规则
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[2]/div[2]/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[2]/div/div/div[2]/div/input", d_['提单规则'])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[3]/div[1]/button[2]")
        # # 提单状态
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[3]/div[2]/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[2]/div/div/div[2]/div/input", d_['提单状态'])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[3]/div[1]/button[2]")
        # # 过会规则
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[4]/div[2]/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[2]/div/div/div[2]/div/input", d_['过会规则'])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[3]/div[1]/button[2]")

        # 定位到底部元素
        self.Web_PO.scrollToView("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[11]", 2)

        # # 药剂科会前确认信息
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[5]/div[2]/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[2]/div/div/div[2]/div/input", d_['药剂科会前确认信息'])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[3]/div[1]/button[2]")

        # # 药事会实际召开时间
        # # d_['药事会实际召开时间'] = [2026, 10, 20, 10, 10, 0]
        # # print(time.strftime("%H:%M:%S"))  # 15:19:28
        # base_year = int(Time_PO.getYear())
        # base_month = int(Time_PO.getMonth())
        # base_day = int(Time_PO.getDay())
        # if d_['药事会实际召开时间'][0] > base_year:
        #     varYear = (d_['药事会实际召开时间'][0] - base_year) * -20  # 鼠标往上滚动，取大值（预期值大于当前值）
        # else:
        #     varYear = (base_year - d_['药事会实际召开时间'][0]) * 20  # 鼠标往下滚动，取小值（预期值小于当前值）
        # print("药事会实际召开时间varYear: " + str(varYear))
        #
        # if d_['药事会实际召开时间'][1] > base_month:
        #     varMonth = (d_['药事会实际召开时间'][1] - base_month) * -20
        # else:
        #     varMonth = (base_month - d_['药事会实际召开时间'][1]) * 20
        # print("药事会实际召开时间varMonth: " + str(varMonth))
        #
        # if d_['药事会实际召开时间'][2] > base_day:
        #     varDay = (d_['药事会实际召开时间'][2] - base_day) * -20
        # else:
        #     varDay = (base_day - d_['药事会实际召开时间'][2]) * 20
        # print("药事会实际召开时间varDay: " + str(varDay))
        #
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/input")
        # self.Web_PO.yearMonthDay("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", varYear)
        # self.Web_PO.yearMonthDay("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", varMonth)
        # self.Web_PO.yearMonthDay("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", varDay)
        # sleep(3)
        # base_year = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        # base_month = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        # base_day = int(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        # # print(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[4]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        # # print(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[5]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        # print(base_year)
        # print(base_month)
        # print(base_day)
        #
        # self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")

        # # 会前评估能否过会
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[7]/div[2]/div/input", 2)

        self.Web_PO.test('会前评估能否过会')

        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[2]/div/div/div[2]/div/input", d_['会前评估能否过会'])
        # /html/body/div[1]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input
        # //*[@id="app"]/div/div[1]/div/div[6]/div/div[5]/div/div[2]/div/div/div[2]/div/input
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[3]/div[1]/button[2]")
        # # 经改进后能否过会
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[8]/div[2]/div/input", 2)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[2]/div/div/div[2]/div/input", d_['经改进后能否过会'])
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[9]/div/div[3]/div[1]/button[2]")
        # # 过会日期
        # d_['过会日期']: [2022, 1, 2, 10, 10, 0]
        print(base_year)  # 2026
        print(base_month)  # 10
        print(base_day)  # 20

        if d_['过会日期'][0] > base_year:
            varYear = (d_['过会日期'][0] - base_year) * -20   # 鼠标往上滚动，取大值（预期值大于当前值）
        else:
            varYear = (base_year - d_['过会日期'][0]) * 20   # 鼠标往下滚动，取小值（预期值小于当前值）
        print("过会日期varYear: " + str(varYear))

        if d_['过会日期'][1] > base_month:
            varMonth = (d_['过会日期'][1] - base_month) * -20
        else:
            varMonth = (base_month - d_['过会日期'][1]) * 20
        print("过会日期varMonth: " + str(varMonth))

        if d_['过会日期'][2] > base_day:
            varDay = (d_['过会日期'][2] - base_day) * -20
        else:
            varDay = (base_day - d_['过会日期'][2]) * 20
        print("过会日期varDay: " + str(varDay))

        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[9]/div[2]/div/input")
        self.Web_PO.yearMonthDay("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", varYear)
        self.Web_PO.yearMonthDay("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", varMonth)
        self.Web_PO.yearMonthDay("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div", varDay)
        sleep(3)
        print(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[1]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        print(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[2]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        print(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[3]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        print(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[4]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        print(self.Web_PO.getTextByX("//div[@class='van-picker van-datetime-picker']/div[2]/div[5]/ul/li[@class='van-picker-column__item van-picker-column__item--selected']/div"))
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[11]/div/div[2]/div[1]/button[2]")
        self.Web_PO.clkByX("//div[@class='van-picker van-datetime-picker']/div[1]/button[2]")

        # # self.Web_PO.clsReadonlyByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[9]/div[2]/div/input")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[9]/div[2]/div/input")
        # self.Web_PO.test("/html/body/div[1]/div/div[1]/div/div[6]/div/div[11]/div/div[2]/div[2]/div[2]/ul/li[9]")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[6]/div/div[11]/div/div[2]/div[1]/button[2]")


        # # 返回
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]")

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


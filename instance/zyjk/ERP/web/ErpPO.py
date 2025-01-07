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


class ErpPO(object):

    def __init__(self):
        self.List_PO = ListPO()
        self.Time_PO = TimePO()
        self.Color_PO = ColorPO()
        self.List_PO = ListPO()
        self.Str_PO = StrPO()
        # self.Dom_PO = DomPO()


    def login(self, varURL, varUser, varPass):
        self.Web_PO = WebPO("chrome")
        # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开
        # self.Web_PO.driver.maximize_window()  # 全屏
        self.Web_PO.openURL(varURL)
        self.Web_PO.setTextByX('/html/body/div/div/form/div[1]/div/div/div/input', varUser)
        self.Web_PO.setTextByX('/html/body/div/div/form/div[2]/div/div/div/input', varPass)
        self.Web_PO.clkByX('//*[@id="app"]/div/form/div[3]/div/button', 2)
        self.Web_PO.clkByX('/html/body/div/div/form/div[2]/div[2]/button[2]', 2)

    def getMenuUrl(self):

        self.Web_PO.clkByXs("//div[@class='el-sub-menu__title']", 1)
        d_menu_url = self.Web_PO.getDictTextAttrValueByXs("//a", "href")
        return (d_menu_url)

    def newLabel(self,varUrl, varNo):
        self.Web_PO.opnLabel(varUrl, 2)
        self.Web_PO.swhLabel(varNo)

    def swhLabel(self, varNo):
        self.Web_PO.swhLabel(varNo)






    # todo 主数据管理 - 1医院管理

    def _dropdownDateByAriaHidden(self, v):
            # 日期区间
            # 如：医院管理最后更新时间

            varPrefix = "//div[@class='el-popper is-pure is-light el-picker__popper' and @aria-hidden='false']"

            # 1 获取日期年和月
            defaultYM = self.Web_PO.getTextByX(varPrefix + "/div/div/div/div[1]/div/div")
            defaultYear = int(defaultYM.split(" 年 ")[0])
            defaultMonth = int(defaultYM.split(" 年 ")[1].split(" 月")[0])
            # print("defaultYear", defaultYear)
            # print("defaultMonth", defaultMonth)

            # 2 切换年
            if v[0] < defaultYear:
                year = defaultYear - v[0]
                for i in range(year):
                    self.Web_PO.clkByX(varPrefix + "/div/div/div/div[1]/div/button[1]")
                    # /html/body/div[2]/div[7]/div/div/div/div[1]/div/button[1]
            else:
                year = v[0] - defaultYear
                for i in range(year):
                    self.Web_PO.clkByX(varPrefix + "/div/div/div/div[2]/div/button[1]")
                    # /html/body/div[2]/div[7]/div/div/div/div[2]/div/button[1]
            # 切换月
            if v[1] < defaultMonth:
                month = defaultMonth - v[1]
                for i in range(month):
                    self.Web_PO.clkByX(varPrefix + "/div/div/div/div[1]/div/button[2]")
                    # /html/body/div[2]/div[7]/div/div/div/div[1]/div/button[2]
            else:
                month = v[1] - defaultMonth
                for i in range(month):
                    self.Web_PO.clkByX(varPrefix + "/div/div/div/div[2]/div/button[2]")


            # 开始日期
            tr2 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[2]")
            tr3 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[3]")
            tr4 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[4]")
            tr5 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[5]")
            tr6 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[6]")
            tr7 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[7]")
            l_1 = []
            l_tr2 = tr2[0].split("\n")
            l_tr2 = [int(i) for i in l_tr2]
            l_tr2 = [0 if i > 10 else i for i in l_tr2]
            l_1.append(l_tr2)
            l_tr3 = tr3[0].split("\n")
            l_tr3 = [int(i) for i in l_tr3]
            l_1.append(l_tr3)
            l_tr4 = tr4[0].split("\n")
            l_tr4 = [int(i) for i in l_tr4]
            l_1.append(l_tr4)
            l_tr5 = tr5[0].split("\n")
            l_tr5 = [int(i) for i in l_tr5]
            l_1.append(l_tr5)
            l_tr6 = tr6[0].split("\n")
            l_tr6 = [int(i) for i in l_tr6]
            l_tr6 = [0 if i < 10 else i for i in l_tr6]
            l_1.append(l_tr6)
            l_tr7 = tr7[0].split("\n")
            l_tr7 = [int(i) for i in l_tr7]
            l_tr7 = [0 if i < 10 else i for i in l_tr7]
            l_1.append(l_tr7)
            # print("开始日期", l_1)  # [[0, 0, 0, 0, 0, 0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26, 27, 28, 29], [30, 31, 0, 0, 0, 0, 0]]
            for i in range(len(l_1)):
                for j in range(len(l_1[i])):
                    if l_1[i][j] == v[2]:
                        self.Web_PO.clkByX(
                            varPrefix + "/div/div/div/div[1]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 2)

            # 结束日期
            if v[1] == v[4]:
                varLoc = 1
            else:
                varLoc = 2
            tr2 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[2]")
            tr3 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[3]")
            tr4 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[4]")
            tr5 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[5]")
            tr6 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[6]")
            tr7 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[7]")
            l_1 = []
            l_tr2 = tr2[0].split("\n")
            l_tr2 = [int(i) for i in l_tr2]
            l_tr2 = [0 if i > 10 else i for i in l_tr2]
            l_1.append(l_tr2)
            l_tr3 = tr3[0].split("\n")
            l_tr3 = [int(i) for i in l_tr3]
            l_1.append(l_tr3)
            l_tr4 = tr4[0].split("\n")
            l_tr4 = [int(i) for i in l_tr4]
            l_1.append(l_tr4)
            l_tr5 = tr5[0].split("\n")
            l_tr5 = [int(i) for i in l_tr5]
            l_1.append(l_tr5)
            l_tr6 = tr6[0].split("\n")
            l_tr6 = [int(i) for i in l_tr6]
            l_tr6 = [0 if i < 10 else i for i in l_tr6]
            l_1.append(l_tr6)
            l_tr7 = tr7[0].split("\n")
            l_tr7 = [int(i) for i in l_tr7]
            l_tr7 = [0 if i < 10 else i for i in l_tr7]
            l_1.append(l_tr7)
            # print("结束日期", l_1)  # [[0, 0, 0, 0, 0, 0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26, 27, 28, 29], [30, 31, 0, 0, 0, 0, 0]]
            for i in range(len(l_1)):
                for j in range(len(l_1[i])):
                    if l_1[i][j] == v[5]:
                        self.Web_PO.clkByX(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[" + str(
                            i + 2) + "]/td[" + str(j + 1) + "]", 1)

    def _dropdown3(self, ele, elePath, v):
        # 公共下拉框3
        # 新增员工 - 主管信息
        self.Web_PO.eleClkByX(ele, elePath, 1)
        l_ = self.Web_PO.getTextByXs("//div[@class='el-popper is-pure is-light el-select__popper styleMyStaffTitle' and @aria-hidden='false']/div/div[2]/div[1]/ul/li/div")
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper styleMyStaffTitle' and @aria-hidden='false']/div/div[2]/div[1]/ul/li[" + str(d_4[v]) + "]", 1)

    def _dropdown4(self, ele, elePath, v):
        # 下拉框多选
        # 非销售岗位关联
        # _dropdown4(ele, "//", '分院')
        self.Web_PO.eleClkByX(ele, elePath, 1)
        l_ = self.Web_PO.getTextByXs("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li")
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}  # {'总院': 1, '分院': 2, '门诊部': 3}
        # print(d_4)
        # 取消当前已勾选的项
        for i in range(len(d_4)):
            varClass = self.Web_PO.getAttrValueByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(i+1) + "]", 'class')
            if varClass == 'el-select-dropdown__item is-selected is-hovering' or varClass == 'el-select-dropdown__item is-selected':
                self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(i+1) + "]", 1)

        # 勾选
        for i in range(len(v)):
            self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(d_4[v[i]]) + "]", 1)

    def _dropdown2(self, ele, elePath, v):
        # 公共下拉框
        # _dropdown2(ele, "//", '分院')
        self.Web_PO.eleClkByX(ele, elePath, 1)
        l_ = self.Web_PO.getTextByXs("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li")
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}  # {'总院': 1, '分院': 2, '门诊部': 3}
        # print(d_4)
        self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(d_4[v]) + "]", 1)

    def _dropdown(self, ele, elePath, l_, v):
        # 公共下拉框
        # _dropdown(ele, "//", ['总院', '分院', '门诊部'], '分院')
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}  # {'总院': 1, '分院': 2, '门诊部': 3}
        self.Web_PO.eleClkByX(ele, elePath, 1)
        self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(d_4[v]) + "]", 1)


    def _hospitalPCC(self, ele, elePath, v):
        # 公共 - 省份城市区县
        self.Web_PO.eleClkByX(ele, elePath, 1)
        l_1 = self.Web_PO.getTextByXs("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul")
        # l_1 = self.Web_PO.getListTextByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul")
        l_2 = l_1[0].split("\n")
        d_3 = dict(enumerate(l_2, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(d_4[v]) + "]", 1)


    def hospital_search(self, d_):
        # 医院管理 - 查询

        # 判断展开还是收起，如果已展开则不操作，否则展开
        ele2 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        s_ = self.Web_PO.eleGetTextByX(ele2, ".//div[2]/button[1]/span")
        if s_ == "展开":
            self.Web_PO.eleClkByX(ele2, ".//div[2]/button[1]", 1)  # 展开

        ele3 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../../..")
        for k, v in d_.items():
            if k == '医院编码':
                self.Web_PO.eleSetTextByX(ele3, ".//form/div/div/div[1]/div/div/div/div/input", v)
            elif k == '医院名称':
                self.Web_PO.eleSetTextByX(ele3, ".//form/div/div/div[2]/div/div/div/div/input", v)
            elif k == '别名':
                self.Web_PO.eleSetTextByX(ele3, ".//form/div/div/div[3]/div/div/div/div/input", v)
            elif k == '医院级别':
                self._dropdown2(ele3, ".//form/div/div/div[4]/div/div/div/div/div[1]/div[2]", v)
            elif k == '省份':
                self._hospitalPCC(ele3, ".//form/div/div/div[5]/div/div/div/div/div[1]/div[2]", v)
            elif k == '城市':
                self._hospitalPCC(ele3, ".//form/div/div/div[6]/div/div/div/div/div[1]/div[2]", v)
            elif k == '区县':
                self._hospitalPCC(ele3, ".//form/div/div/div[7]/div/div/div/div/div[1]/div[2]", v)
            elif k == '启用状态':
                self._dropdown2(ele3, ".//form/div/div/div[8]/div/div/div/div/div[1]/div[2]", v)
            elif k == '最后更新时间':
                self.Web_PO.eleClkByX(ele3, ".//form/div/div/div[9]/div/div[2]/div/input[1]")
                self._dropdownDateByAriaHidden(v)
        # # 点击查询
        self.Web_PO.eleClkByX(ele2, ".//div[2]/button[2]", 1)

        # 返回搜索结果数量
        return self._getId()


    def hospital_reset(self):
        # 医院管理 - 重置

        # 点击重置
        ele = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[3]", 1)

    def hospital_add(self, varQty, d_):
        # 医院管理 - 新增

        if varQty == None:

            # 点击新增
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../..")
            self.Web_PO.eleClkByX(ele, ".//div[2]/button[2]", 1)

            ele2 = self.Web_PO.getSuperEleByX("//span[text()='医院基础信息']", "../..")
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[1]/div[2]/div/div/div/div/input", d_['医院全称'])
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[2]/div[1]/div/div/div/div/input", d_['医院简称'])
            self._dropdown2(ele2, ".//div[2]/form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['医院类型'])
            self._dropdown2(ele2, ".//div[2]/form/div[3]/div[2]/div/div/div/div/div[1]/div[2]", d_['医院级别'])
            self._hospitalPCC(ele2, ".//div[2]/form/div[4]/div[1]/div/div/div/div/div[1]/div[2]", d_['省份'])
            self._dropdown2(ele2, ".//div[2]/form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", d_['启用状态'])
            self._hospitalPCC(ele2, ".//div[2]/form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", d_['城市'])
            self._hospitalPCC(ele2, ".//div[2]/form/div[5]/div[2]/div/div/div/div/div[1]/div[2]", d_['区县'])
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[6]/div[1]/div/div/div/div/input", d_['详细地址'])
            self._dropdown2(ele2, ".//div[2]/form/div[6]/div[2]/div/div/div/div/div[1]/div[2]", d_['获取方式'])
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[8]/div[1]/div/div/div/div/input", d_['邮政编码'])
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[8]/div[2]/div/div/div/div/input", d_['电话'])
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[9]/div[1]/div/div/div/div/input", d_['邮箱'])
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[9]/div[2]/div/div/div/div/input", d_['网址'])
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[10]/div[1]/div/div/div/div/input", d_['床位数'])
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[10]/div[2]/div/div/div/div/input", d_['门诊量'])
            self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[11]/div/div/textarea", d_['备注信息'])
            # 提交 bug改文字为确定
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='医院基础信息']", "../../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 提交



    def _hospital_setup_checkbox(self, ele2, varNum, varField):
        # 列表是否显示，先判断勾选框是否勾选
        # _hospital_setup_checkbox(ele2, 3, v['列表是否显示'])
        s_attr = self.Web_PO.eleGetAttrValueByX(ele2, ".//div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varNum) + "]/div/label", "class")
        if s_attr == 'el-checkbox el-checkbox--default is-checked noLabelCheckBox':
            if varField == '否':
                self.Web_PO.eleClkByX(ele2, ".//div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varNum) + "]/div/label")
        else:
            if varField == '是':
                self.Web_PO.eleClkByX(ele2, ".//div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varNum) + "]/div/label")
    def hospital_setup(self, varButtonLoc, d_):
        # 设置

        # 点击设置
        ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../..")
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[" + str(varButtonLoc) + "]", 1)

        # 列表字段展示，搜索后点击查询
        ele2 = self.Web_PO.getSuperEleByX("//span[text()='列表字段设置']", "../..")
        for k, v in d_.items():
            self.Web_PO.eleSetTextByX(ele2, ".//div/div/div[1]/div/div/input", k)
            self.Web_PO.eleClkByX(ele2, ".//div/div/div[1]/button", 1)  # 点击查询

            # 字段宽度设置
            self.Web_PO.eleSetTextBackspaceEnterByX(ele2, ".//div/div/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div/div/div/div/input", 3, v['字段宽度设置'], 2)

            # 列表是否显示，先判断勾选框是否勾选
            self._hospital_setup_checkbox(ele2, 3, v['列表是否显示'])

            # 详情是否显示，先判断勾选框是否勾选
            self._hospital_setup_checkbox(ele2, 4, v['详情是否显示'])

            # 是否固定，先判断勾选框是否勾选
            self._hospital_setup_checkbox(ele2, 5, v['是否固定'])

        self.Web_PO.eleClkByX(ele2, ".//footer/span/button[2]")  # 提交


    def hospital_edit(self, varQty, d_):
        # 医院管理 - 修改

        if varQty == 1:

            # 1 获取td数量，定位修改按钮(因为td字段可通过配置显示或隐藏),点击修改
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/div/button[1]")

            # 医院基础信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='医院基础信息']", "../..")
            for k, v in d_.items():
                if k == '医院全称':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[1]/div[2]/div/div/div/div/input", d_['医院全称'])
                if k == '医院简称':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[2]/div[1]/div/div/div/div/input", d_['医院简称'])
                if k == '医院级别':
                    self._dropdown2(ele2, ".//div[2]/form/div[3]/div[2]/div/div/div/div/div[1]/div[2]", d_['医院级别'])
                if k == '省份':
                    self._hospitalPCC(ele2, ".//div[2]/form/div[4]/div[1]/div/div/div/div/div[1]/div[2]", d_['省份'])
                if k == '启动状态':
                    self._dropdown2(ele2, ".//div[2]/form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", d_['启用状态'])
                if k == '城市':
                    self._hospitalPCC(ele2, ".//div[2]/form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", d_['城市'])
                if k == '区县':
                    self._hospitalPCC(ele2, ".//div[2]/form/div[5]/div[2]/div/div/div/div/div[1]/div[2]", d_['区县'])
                if k == '详细地址':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[6]/div[1]/div/div/div/div/input", d_['详细地址'])
                if k == '获取方式':
                    self._dropdown2(ele2, ".//div[2]/form/div[6]/div[2]/div/div/div/div/div[1]/div[2]", d_['获取方式'])
                if k == '邮政编码':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[8]/div[1]/div/div/div/div/input", d_['邮政编码'])
                if k == '电话':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[8]/div[2]/div/div/div/div/input", d_['电话'])
                if k == '邮箱':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[9]/div[1]/div/div/div/div/input", d_['邮箱'])
                if k == '网址':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[9]/div[2]/div/div/div/div/input", d_['网址'])
                if k == '床位数':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[10]/div[1]/div/div/div/div/input", d_['床位数'])
                if k == '门诊量':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[10]/div[2]/div/div/div/div/input", d_['门诊量'])
                if k == '备注信息':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[11]/div/div/textarea", d_['备注信息'])

            ele3 = self.Web_PO.getSuperEleByX("//span[text()='医院基础信息']", "../../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 提交


    def hospital_info(self, varQty):
        # 医院管理 - 详情

        if varQty == 1:

            # 1 获取td数量，定位详情按钮(因为td字段可通过配置显示或隐藏)，点击详情
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele3, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele3, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/div/button[2]")

            # 2 获取列表信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='医院基础信息']", "../..")
            l_ = self.Web_PO.eleGetTextByXs(ele2, ".//div[2]/div/table/tr")

            # 3 关闭
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='医院详情']", "../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[1]", 1)

            print(l_)  # ['医院全称\n天津自动化医院1\n医院简称\n天自院1', '医院级别\n二级医院\n医院类型\n分院',...
            return l_



    # todo 主数据管理 - 3经销商管理
    def dealer_search(self, d_):
        # 经销商管理 - 查询

        # 判断展开还是收起，如果已展开则不操作，否则展开
        ele2 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        s_ = self.Web_PO.eleGetTextByX(ele2, ".//div[2]/button[1]/span")
        if s_ == "展开":
            self.Web_PO.eleClkByX(ele2, ".//div[2]/button[1]", 1)  # 展开

        ele3 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../../..")
        for k, v in d_.items():
            if k == '经销商名称':
                self.Web_PO.eleSetTextByX(ele3, ".//form/div/div/div[2]/div/div/div/div/input", v)
            if k == '经销商级别':
                self._dropdown2(ele3, ".//form/div/div/div[4]/div/div/div/div/div[1]/div[2]", v)
            if k == '省份':
                self._hospitalPCC(ele3, ".//form/div/div/div[5]/div/div/div/div/div[1]/div[2]", v)
            if k == '城市':
                self._hospitalPCC(ele3, ".//form/div/div/div[6]/div/div/div/div/div[1]/div[2]", v)
            if k == '区县':
                self._hospitalPCC(ele3, ".//form/div/div/div[7]/div/div/div/div/div[1]/div[2]", v)
            if k == '启用状态':
                self._dropdown2(ele3, ".//form/div/div/div[8]/div/div/div/div/div[1]/div[2]", v)
            if k == '最后更新时间':
                self.Web_PO.eleClkByX(ele3, ".//form/div/div/div[9]/div/div[2]/div/input[1]")
                self._dropdownDateByAriaHidden(v)

        # 点击查询
        self.Web_PO.eleClkByX(ele2, ".//div[2]/button[2]", 1)

        # 返回搜索结果数量
        return self._getId()

    def dealer_add(self, varQty, d_):
        # 经销商管理 - 新增

        if varQty == None:

            # 点击新增
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../..")
            self.Web_PO.eleClkByX(ele, ".//div[2]/button[2]", 1)

            # 医院基础信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='经销商基础信息']", "../..")
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[1]/div[2]/div/div/div/div/input", d_['经销商名称'])
            self._hospitalPCC(ele2, ".//form/div[2]/div[1]/div/div/div/div/div[1]/div[2]", d_['省份'])
            self._hospitalPCC(ele2, ".//form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['城市'])
            self._hospitalPCC(ele2, ".//form/div[3]/div[1]/div/div/div/div/div[1]/div[2]", d_['区县'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div[2]/div/div/div/div/input", d_['详细地址'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[4]/div[1]/div/div/div/div/input", d_['联系电话'])
            self._dropdown2(ele2, ".//form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", d_['启用状态'])
            self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", d_['经销商级别'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[6]/div/div/div/div/textarea", d_['备注信息'])
            # 确定
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='经销商基础信息']", "../../../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 确定


    def dealer_edit(self, varQty, d_):
        # 经销商管理 - 修改

        if varQty == 1:

            # 获取td数量，定位修改按钮(因为td字段可通过配置显示或隐藏)，点击修改
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/button[1]")  # 修改

            # 经销商基础信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='经销商基础信息']", "../..")
            for k, v in d_.items():
                if k == '经销商名称':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[1]/div[2]/div/div/div/div/input", d_['经销商名称'])
                if k == '省份':
                    self._hospitalPCC(ele2, ".//form/div[2]/div[1]/div/div/div/div/div[1]/div[2]", d_['省份'])
                if k == '城市':
                    self._hospitalPCC(ele2, ".//form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['城市'])
                if k == '区县':
                    self._hospitalPCC(ele2, ".//form/div[3]/div[1]/div/div/div/div/div[1]/div[2]", d_['区县'])
                if k == '详细地址':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div[2]/div/div/div/div/input", d_['详细地址'])
                if k == '联系电话':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[4]/div[1]/div/div/div/div/input", d_['联系电话'])
                if k == '启用状态':
                    self._dropdown2(ele2, ".//form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", d_['启用状态'])
                if k == '经销商级别':
                    self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", d_['经销商级别'])
                if k == '备注信息':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[6]/div/div/div/div/textarea", d_['备注信息'])
            # 确定
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='经销商基础信息']", "../../../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 确定


    def dealer_info(self, varQty):
        # 经销商管理 - 详情

        if varQty == 1:

            # 1 获取td数量，定位详情按钮(因为td字段可通过配置显示或隐藏)，点击详情
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele3, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele3, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/button[2]", 1)

            # 2 获取列表信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='经销商基础信息']", "../..")
            l_ = self.Web_PO.eleGetTextByXs(ele2, ".//div[2]/div/table/tr")

            # 3 关闭
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='经销商详情']", "../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[1]", 1)

            print(l_)  # ['经销商编码\nDLR000003\n经销商名称\n百慕大自动优质经销商1', ,...
            return l_


    # todo 主数据管理 - 5商业公司管理

    def business_search(self, d_):
        # 商业公司管理 - 查询

        # 判断展开还是收起，如果已展开则不操作，否则展开
        ele2 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        s_ = self.Web_PO.eleGetTextByX(ele2, ".//div[2]/button[1]/span")
        if s_ == "展开":
            self.Web_PO.eleClkByX(ele2, ".//div[2]/button[1]", 1)  # 展开


        ele3 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../../..")
        for k, v in d_.items():
            if k == '商业公司编码':
                self.Web_PO.eleSetTextByX(ele3, ".//div[2]/form/div[1]/div[1]/div/div/div/div/input", v)
            elif k == '商业公司全称':
                self.Web_PO.eleSetTextByX(ele3, ".//div[2]/form/div[1]/div[2]/div/div/div/div/input", v)
            elif k == '联系人':
                self.Web_PO.eleSetTextByX(ele3, ".//div[2]/form/div[1]/div[3]/div/div/div/div/input", v)
            elif k == '启用状态':
                self._dropdown2(ele3, ".//div[2]/form/div[1]/div[4]/div/div/div/div/div[1]/div[2]", v)
            elif k == '最后更新时间':
                self.Web_PO.eleClkByX(ele3, ".//div[2]/form/div[2]/div/div/div/div[2]/div/input[1]", 1)
                self._dropdownDateByAriaHidden(v)

        self.Web_PO.eleClkByX(ele2, ".//div[2]/button[2]", 3)  # 查询

        # 返回搜索结果数量
        return self._getId()

    def business_add(self, varQty, d_):
        # 商业公司管理 - 新增

        if varQty == None:

            # 点击新增
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../..")
            self.Web_PO.eleClkByX(ele, ".//div[2]/button[2]", 1)

            # 商业公司基础信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='商业公司基础信息']", "../..")
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[1]/div[2]/div/div/div/div/input", d_['商业公司全称'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[2]/div[1]/div/div/div/div/input", d_['商业公司简称'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[2]/div[2]/div/div/div/div/input", d_['商业公司地址'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div[1]/div/div/div/div/input", d_['联系人'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div[2]/div/div/div/div/input", d_['联系人电话'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[4]/div[1]/div/div/div/div/input", d_['合同开始日期'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[4]/div[2]/div/div/div/div/input", d_['合同结束日期'])
            # self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div/div/div/input", d_['合同编号'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[2]/div/div/div/div/input", d_['许可证编号'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[6]/div[1]/div/div/div/div/input", d_['许可证有效期'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[6]/div[2]/div/div/div/div/input", d_['营业执照编号'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[7]/div[1]/div/div/div/div/input", d_['营业执照有效期'])
            self._dropdown2(ele2, ".//form/div[7]/div[2]/div/div/div/div/div[1]/div[2]", d_['企业类别'])
            self._dropdown2(ele2, ".//form/div[8]/div/div/div/div/div/div[1]/div[2]", d_['启用状态'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[9]/div/div/div/div/textarea", d_['生产(经营)范围'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[10]/div/div/div/div/textarea", d_['备注信息'])

            # 确认 bug改文字为确定
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='商业公司基础信息']", "../../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 确认


    def business_edit(self, varQty, d_):
        # 商业公司管理 - 修改

        if varQty == 1:

            # 获取td数量，定位修改按钮(因为td字段可通过配置显示或隐藏),点击修改
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/div/button[1]")

            # 商业公司基础信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='商业公司基础信息']", "../..")
            for k, v in d_.items():
                if k == '商业公司全称':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[1]/div[2]/div/div/div/div/input", d_['商业公司全称'])
                if k == '商业公司简称':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[2]/div[1]/div/div/div/div/input", d_['商业公司简称'])
                if k == '商业公司地址':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[2]/div[2]/div/div/div/div/input", d_['商业公司地址'])
                if k == '联系人':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div[1]/div/div/div/div/input", d_['联系人'])
                if k == '联系人电话':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div[2]/div/div/div/div/input", d_['联系人电话'])
                if k == '合同开始日期':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[4]/div[1]/div/div/div/div/input", d_['合同开始日期'])
                if k == '合同结束日期':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[4]/div[2]/div/div/div/div/input", d_['合同结束日期'])
                if k == '许可证编号':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[2]/div/div/div/div/input", d_['许可证编号'])
                if k == '许可证有效期':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[6]/div[1]/div/div/div/div/input", d_['许可证有效期'])
                if k == '营业执照编号':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[6]/div[2]/div/div/div/div/input", d_['营业执照编号'])
                if k == '营业执照有效期':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[7]/div[1]/div/div/div/div/input", d_['营业执照有效期'])
                if k == '企业类别':
                    self._dropdown2(ele2, ".//form/div[7]/div[2]/div/div/div/div/div[1]/div[2]", d_['企业类别'])
                if k == '启动状态':
                    self._dropdown2(ele2, ".//form/div[8]/div/div/div/div/div/div[1]/div[2]",  d_['启用状态'])
                if k == '生产(经营)范围':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[9]/div/div/div/div/textarea", d_['生产(经营)范围'])
                if k == '备注信息':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[10]/div/div/div/div/textarea", d_['备注信息'])

            ele3 = self.Web_PO.getSuperEleByX("//span[text()='商业公司基础信息']", "../../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 提交


    def business_info(self, varQty):
        # 商业公司管理 - 详情

        if varQty == 1:

            # 1 获取td数量，定位详情按钮(因为td字段可通过配置显示或隐藏)，点击详情
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele3, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele3, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/div/button[2]")

            # 2 获取列表信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='商业公司基础信息']", "../..")
            l_ = self.Web_PO.eleGetTextByXs(ele2, ".//div[2]/table/tr")

            # 3 关闭
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='商业公司详情']", "../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[1]", 1)

            print(l_)  # ['商业公司编码 COM00004 商业公司全称 阿依达商业自动化有限公司3', ...
            return l_



    def _business_setup_checkbox(self, ele2, varField, varValue):
        # 列表是否显示，先判断勾选框是否勾选
        l_ = self.Web_PO.eleGetTextByXs(ele2, ".//div/div/div[2]/div[2]/div/div")
        # print(l_)  # ['', '', '', '', '', '', '', '', '启用状态', '', '', '']
        varLoc = l_.index(varField) + 1
        # print(varLoc)
        s_attr = self.Web_PO.eleGetAttrValueByX(ele2, ".//div/div/div[2]/div[2]/div/div[" + str(varLoc) + "]/div[1]/label", "class")
        if s_attr == 'el-checkbox el-checkbox--default is-checked':
            if varValue == '否':
                self.Web_PO.eleClkByX(ele2, ".//div/div/div[2]/div[2]/div/div[" + str(varLoc) + "]/div[1]/label")
        else:
            if varValue == '是':
                self.Web_PO.eleClkByX(ele2, ".//div/div/div[2]/div[2]/div/div[" + str(varLoc) + "]/div[1]/label")
    def business_setup(self, varButtonLoc, d_):
        # 设置

        # 点击设置
        ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../..")
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[" + str(varButtonLoc) + "]", 1)

        # 列表字段展示，搜索后点击查询
        ele2 = self.Web_PO.getSuperEleByX("//span[text()='列表字段设置']", "../..")
        for k, v in d_.items():
            self.Web_PO.eleSetTextByX(ele2, ".//div/div/div[1]/div/div/input", k)
            self.Web_PO.eleClkByX(ele2, ".//div/div/div[1]/button", 1)  # 点击查询
            # 先判断勾选框是否勾选
            self._business_setup_checkbox(ele2, k, v)
        self.Web_PO.eleClkByX(ele2, ".//footer/span/button[2]")  # 提交




    # todo 组织架构管理 - 3员工管理

    def _dropdownDate(self, v):
        # 公共 - 日期区间
        # 如：最后更新时间，入职日期，离职日期

        varPrefix = "//div[@class='el-picker-panel el-date-range-picker' and @visible='true']"

        # 1 获取日期年和月
        defaultYM = self.Web_PO.getTextByX(varPrefix + "/div/div/div[1]/div/div")
        defaultYear = int(defaultYM.split(" 年 ")[0])
        defaultMonth = int(defaultYM.split(" 年 ")[1].split(" 月")[0])
        # print("defaultYear", defaultYear)
        # print("defaultMonth", defaultMonth)

        # 2 切换年
        if v[0] < defaultYear:
            year = defaultYear - v[0]
            for i in range(year):
                self.Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[1]/button[1]")
                             # /html/body/div[2]/div[7]/div/div/div/div[1]/div/button[1]
        else:
            year = v[0] - defaultYear
            for i in range(year):
                self.Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[4]/button[2]")
                             # /html/body/div[2]/div[7]/div/div/div/div[2]/div/button[1]
        # 切换月
        if v[1] < defaultMonth:
            month = defaultMonth - v[1]
            for i in range(month):
                self.Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[1]/button[2]")
                             # /html/body/div[2]/div[7]/div/div/div/div[1]/div/button[2]
        else:
            month = v[1] - defaultMonth
            for i in range(month):
                self.Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[4]/button[1]")
                             # /html/body/div[2]/div[7]/div/div/div/div[2]/div/button[2]

        # if v[0] < int(defaultYear):
        #     self.Web_PO.clkByX(varPrefix + "/div/div/div[1]/div/button[2]", 1)
        #     defaultYM = self.Web_PO.getTextByX(varPrefix + "/div/div/div[1]/div/div")
        #     defaultMonth = defaultYM.split(" 年 ")[1].split(" 月")[0]
        #     if v[1] < int(defaultMonth):
        #         b = int(defaultMonth) - v[1]
        #         # print(b)
        #         for i in range(b):
        #             self.Web_PO.clkByX("//div[@class='el-picker-panel el-date-range-picker' and @visible='true']/div/div/div[1]/div/button[2]", 1)

        # 开始日期
                     # /html/body/div[2]/div[7]/div/div/div/div[1]/table/tbody/tr[2]
        tr2 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[2]")
        tr3 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[3]")
        tr4 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[4]")
        tr5 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[5]")
        tr6 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[6]")
        tr7 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[7]")
        l_1 = []
        l_tr2 = tr2[0].split("\n")
        l_tr2 = [int(i) for i in l_tr2]
        l_tr2 = [0 if i > 10 else i for i in l_tr2]
        l_1.append(l_tr2)
        l_tr3 = tr3[0].split("\n")
        l_tr3 = [int(i) for i in l_tr3]
        l_1.append(l_tr3)
        l_tr4 = tr4[0].split("\n")
        l_tr4 = [int(i) for i in l_tr4]
        l_1.append(l_tr4)
        l_tr5 = tr5[0].split("\n")
        l_tr5 = [int(i) for i in l_tr5]
        l_1.append(l_tr5)
        l_tr6 = tr6[0].split("\n")
        l_tr6 = [int(i) for i in l_tr6]
        l_tr6 = [0 if i < 10 else i for i in l_tr6]
        l_1.append(l_tr6)
        l_tr7 = tr7[0].split("\n")
        l_tr7 = [int(i) for i in l_tr7]
        l_tr7 = [0 if i < 10 else i for i in l_tr7]
        l_1.append(l_tr7)
        # print("开始日期", l_1)  # [[0, 0, 0, 0, 0, 0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26, 27, 28, 29], [30, 31, 0, 0, 0, 0, 0]]
        for i in range(len(l_1)):
            for j in range(len(l_1[i])):
                if l_1[i][j] == v[2]:
                    self.Web_PO.clkByX(varPrefix + "/div/div/div[1]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 2)

        # 结束日期
        if v[1] == v[4]:
            varLoc = 1
        else:
            varLoc = 2
        tr2 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[2]")
        tr3 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[3]")
        tr4 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[4]")
        tr5 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[5]")
        tr6 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[6]")
        tr7 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[7]")
        l_1 = []
        l_tr2 = tr2[0].split("\n")
        l_tr2 = [int(i) for i in l_tr2]
        l_tr2 = [0 if i > 10 else i for i in l_tr2]
        l_1.append(l_tr2)
        l_tr3 = tr3[0].split("\n")
        l_tr3 = [int(i) for i in l_tr3]
        l_1.append(l_tr3)
        l_tr4 = tr4[0].split("\n")
        l_tr4 = [int(i) for i in l_tr4]
        l_1.append(l_tr4)
        l_tr5 = tr5[0].split("\n")
        l_tr5 = [int(i) for i in l_tr5]
        l_1.append(l_tr5)
        l_tr6 = tr6[0].split("\n")
        l_tr6 = [int(i) for i in l_tr6]
        l_tr6 = [0 if i < 10 else i for i in l_tr6]
        l_1.append(l_tr6)
        l_tr7 = tr7[0].split("\n")
        l_tr7 = [int(i) for i in l_tr7]
        l_tr7 = [0 if i < 10 else i for i in l_tr7]
        l_1.append(l_tr7)
        # print("结束日期", l_1)  # [[0, 0, 0, 0, 0, 0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26, 27, 28, 29], [30, 31, 0, 0, 0, 0, 0]]
        for i in range(len(l_1)):
            for j in range(len(l_1[i])):
                if l_1[i][j] == v[5]:
                    self.Web_PO.clkByX(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 1)

    def _dropdownDateSingle(self, v):
        # 公共 - 单个日期控件
        # 如：入职日期，离职日期

        varPrefix = "//div[@class='el-popper is-pure is-light el-picker__popper' and @aria-hidden='false']"

        # 1 获取当前年和月
        defaultY = self.Web_PO.getTextByX(varPrefix + "/div/div[1]/div/div[2]/span[2]")
        defaultM = self.Web_PO.getTextByX(varPrefix + "/div/div[1]/div/div[2]/span[3]")
        defaultYear = int(defaultY.split(" 年")[0])
        defaultMonth = int(defaultM.split(" 月")[0])
        # print("defaultYear", defaultYear)
        # print("defaultMonth", defaultMonth)

        # 2 切换年
        if v[0] < defaultYear:
            year = defaultYear - v[0]
            for i in range(year):
                self.Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[1]/button[1]")
        else:
            year = v[0] - defaultYear
            for i in range(year):
                self.Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[4]/button[2]")
        # 切换月
        if v[1] < defaultMonth:
            month = defaultMonth - v[1]
            for i in range(month):
                self.Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[1]/button[2]")
        else:
            month = v[1] - defaultMonth
            for i in range(month):
                self.Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[4]/button[1]")

        # 3 遍历日期列表
        tr2 = self.Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[3]/table/tbody/tr[2]")
        tr3 = self.Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[3]/table/tbody/tr[3]")
        tr4 = self.Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[3]/table/tbody/tr[4]")
        tr5 = self.Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[3]/table/tbody/tr[5]")
        tr6 = self.Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[3]/table/tbody/tr[6]")
        tr7 = self.Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[3]/table/tbody/tr[7]")
        l_1 = []
        l_tr2 = tr2[0].split("\n")
        l_tr2 = [int(i) for i in l_tr2]
        l_tr2 = [0 if i > 10 else i for i in l_tr2]
        l_1.append(l_tr2)
        l_tr3 = tr3[0].split("\n")
        l_tr3 = [int(i) for i in l_tr3]
        l_1.append(l_tr3)
        l_tr4 = tr4[0].split("\n")
        l_tr4 = [int(i) for i in l_tr4]
        l_1.append(l_tr4)
        l_tr5 = tr5[0].split("\n")
        l_tr5 = [int(i) for i in l_tr5]
        l_1.append(l_tr5)
        l_tr6 = tr6[0].split("\n")
        l_tr6 = [int(i) for i in l_tr6]
        l_tr6 = [0 if i < 10 else i for i in l_tr6]
        l_1.append(l_tr6)
        l_tr7 = tr7[0].split("\n")
        l_tr7 = [int(i) for i in l_tr7]
        l_tr7 = [0 if i < 10 else i for i in l_tr7]
        l_1.append(l_tr7)
        # print("日期列表", l_1)  # [[0, 0, 0, 0, 0, 0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26, 27, 28, 29], [30, 31, 0, 0, 0, 0, 0]]

        # 选择日期
        for i in range(len(l_1)):
            for j in range(len(l_1[i])):
                if l_1[i][j] == v[2]:
                    self.Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[3]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 2)

    def staff_search(self, d_):
        # 员工管理 - 查询

        # 判断展开还是收起，如果已展开则不操作，否则展开
        ele2 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        s_ = self.Web_PO.eleGetTextByX(ele2, ".//div[2]/button[1]/span")
        if s_ == "展开":
            self.Web_PO.eleClkByX(ele2, ".//div[2]/button[1]", 1)  # 展开

        ele2 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../../..")
        for k, v in d_.items():
            if k == '员工信息':
                self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[1]/div[1]/div/div/div/div/div[1]/div[2]", v)
            if k == '联系方式':
                self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[1]/div[2]/div/div/div/div/input", v)
            if k == '职位':
                self._dropdown2(ele2, ".//div[2]/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]",  v)
            if k == '是否在职':
                self._dropdown2(ele2, ".//div[2]/form/div[1]/div[4]/div/div/div/div/div[1]/div[2]",  v)
            if k == '入职日期':
                self.Web_PO.eleClkByX(ele2, ".//div[2]/form/div[2]/div[1]/div[1]/div/div[2]/div/input[1]", 1)
                self._dropdownDate(v)
            if k == '主管信息':
                self._dropdown3(ele2, ".//div[2]/form/div[2]/div[1]/div[3]/div/div/div/div/div[1]/div[2]", v)
            if k == '启用状态':
                self._dropdown2(ele2, ".//div[2]/form/div[2]/div[1]/div[4]/div/div/div/div/div[1]/div[2]", v)
            if k == '最后更新时间':
                self.Web_PO.eleClkByX(ele2, ".//div[2]/form/div[2]/div[2]/div/div/div[2]/div/input[1]", 1)
                self._dropdownDate(v)
        # 点击查询
        self.Web_PO.eleClkByX(ele2, ".//div[2]/button[2]", 3)

        # 返回搜索结果数量
        return self._getId()

    #
    def _getId(self):
        # 获取xx编码
        # 返回搜索结果数量
        # 如果多余1条或者0条，返回null)
        d_ = {}
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":
            try:
                d_['id'] = self.Web_PO.getTextByX("//tr[@class='el-table__row']/td[1]/div")
                d_['qty'] = 1
            except:
                d_['id'] = self.Web_PO.getTextByX("//tr[@class='el-table__row current-row']/td[1]/div")
                d_['qty'] = 1
            return d_
        else:
            d_['id'] = None
            d_['qty'] = None
        return d_


    def staff_add(self, varQty, d_):
        # 员工管理 - 新增

        if varQty == None:

            # 点击新增
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../..")
            self.Web_PO.eleClkByX(ele, ".//div[2]/button[2]", 1)

            # 员工基本信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='员工基本信息']", "..")
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[1]/div[2]/div/div/div/div/input", d_['员工姓名'])
            self._hospitalPCC(ele2, ".//form/div[2]/div[1]/div/div/div/div/div[1]/div[2]", d_['省份'])
            self._hospitalPCC(ele2, ".//form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['城市'])
            self._dropdown(ele2, ".//form/div[3]/div[1]/div/div/div/div/div[1]/div[2]", ["女", "男", "不详"], d_['性别'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div[2]/div/div/div/div/input", d_['联系方式'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[4]/div[1]/div/div/div/div/input", d_['邮箱'])
            self._dropdown2(ele2, ".//form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", d_['职称'])
            self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", d_['是否在职'])
            self.Web_PO.eleSetTextEnterByX(ele2, ".//form/div[5]/div[2]/div/div/div/div/input", d_['入职日期'])
            self._dropdown3(ele2, ".//form/div[6]/div[2]/div/div/div/div/div[1]/div[2]", d_['主管信息'])
            self._dropdown2(ele2, ".//form/div[7]/div[1]/div/div/div/div/div[1]/div[2]", d_['启用状态'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[8]/div/div/textarea", d_['备注信息'])

            # 提交 bug改文字为确定
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='员工基本信息']", "../../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 提交


    def staff_edit(self, varQty, d_):
        # 员工管理 - 修改

        if varQty == 1:

            # # 获取td数量，定位修改按钮(因为td字段可通过配置显示或隐藏),点击修改
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele3, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele3, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/button[1]")  # 修改

            ele1 = self.Web_PO.getSuperEleByX("//span[text()='员工基本信息']", "..")
            isJob = 0
            for k, v in d_.items():
                if k == '员工姓名':
                    self.Web_PO.eleSetTextByX(ele1, ".//form/div[1]/div[2]/div/div/div/div/input", d_['员工姓名'])
                elif k == '省份':
                    self._hospitalPCC(ele1, ".//form/div[2]/div[1]/div/div/div/div/div[1]/div[2]", d_['省份'])
                elif k == '城市':
                    self._hospitalPCC(ele1, ".//form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['城市'])
                elif k == '性别':
                    self._dropdown2(ele1, ".//form/div[3]/div[1]/div/div/div/div/div[1]/div[2]", d_['性别'])
                elif k == '联系方式':
                    self.Web_PO.eleSetTextByX(ele1, ".//form/div[3]/div[2]/div/div/div/div/input", d_['联系方式'])
                elif k == '邮箱':
                    self.Web_PO.eleSetTextByX(ele1, ".//form/div[4]/div[1]/div/div/div/div/input", d_['邮箱'])
                elif k == '职称':
                    self._dropdown2(ele1, ".//form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", d_['职称'])
                elif k == '是否在职':
                    self._dropdown2(ele1, ".//form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", d_['是否在职'])
                    if d_['是否在职'] == '在职':
                        isJob = 1
                    else:
                        isJob = 2
                elif isJob == 1 and k == '入职日期':
                    self.Web_PO.eleClkByX(ele1, ".//form/div[5]/div[2]/div/div/div/div/input")
                    self._dropdownDateSingle(d_['入职日期'])
                elif isJob == 2 and k == '离职日期':
                    self.Web_PO.eleClkByX(ele1, ".//form/div[6]/div[1]/div/div/div/div/input")
                    self._dropdownDateSingle(d_['离职日期'])
                elif k == '主管信息':
                    self._dropdown2(ele1, ".//form/div[6]/div[2]/div/div/div/div/div[1]/div[2]", d_['主管信息'])
                elif k == '启动状态':
                    self._dropdown2(ele1, ".//form/div[7]/div[1]/div/div/div/div/div[1]/div[2]", d_['启用状态'])
                elif k == '备注信息':
                    self.Web_PO.eleSetTextByX(ele1, ".//form/div[8]/div/div/textarea", d_['备注信息'])

            ele4 = self.Web_PO.getSuperEleByX("//span[text()='员工基本信息']", "../../../..")
            self.Web_PO.eleClkByX(ele4, ".//div[2]/div/button[2]", 1)  # 提交


    def staff_info(self, varQty):
        # 员工管理 - 详情

        if varQty == 1:

            # 1 获取td数量，定位详情按钮(因为td字段可通过配置显示或隐藏)，点击详情
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele3, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele3, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/button[2]")

            # 2 获取列表信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='员工基本信息']", "../..")
            l_ = self.Web_PO.eleGetTextByXs(ele2, ".//div[2]/table/tr")

            # 3 关闭
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='员工详情']", "../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[1]", 1)

            print(l_)  # ['医院全称\n天津自动化医院1\n医院简称\n天自院1', '医院级别\n二级医院\n医院类型\n分院',...
            return l_


    # todo 辖区管理 - 1辖区分配


    def _dropdownByAreaAssign(self):
        # 辖区分配

        varPrefix = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']"
        l_ = self.Web_PO.getTextByXs("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li")
        print(l_)


    def setInfo(self, d_):

        # 点击 所在周期版本
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/form/div/div/div/div[2]/div/div")
        l_ = self.Web_PO.getTextByXs(
            "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li")
        # print(l_)  # ['202501版本', '202412版本', '202411版本'。。。
        d_1 = dict(enumerate(l_, start=1))
        d_1 = {v:k for k, v in d_1.items()}
        # print(d_1)  # {'202501版本': 1, '202412版本': 2, '202411版本': 3,
        self.Web_PO.clkByX(
            "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(
                d_1[d_['周期版本']]) + "]")

        # 辖区信息里搜索辖区名称
        ele3 = self.Web_PO.getSuperEleByX("//span[text()='辖区信息']", "../../..")
        self.Web_PO.eleSetTextEnterByX(ele3, ".//div[3]/div[1]/div[1]/div/div/input", d_['辖区名称'])

        varSign = 0

        # 获取总监数量
        ele2 = self.Web_PO.getSuperEleByX("//span[text()='总部']", "../..")
        varZjQty = self.Web_PO.eleGetQtyByXByXs(ele2, ".//div[2]")
        # print("varZjQty", varZjQty)

        # 点击 代表岗位
        if varSign == 0:
            self.Web_PO.eleClkByX(ele3, ".//div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]", 2)
            # 判断辖区名字是否是代表岗位
            areaName = self.Web_PO.eleGetShadowByXByC(ele3, ".//div[3]/div[2]/div/div/form/div[2]/div/div/div/div/div/input", 'div:nth-last-of-type(1)')
            if areaName == d_['辖区名称']:
                print("代表岗位", areaName)
                varSign = 1
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[2]/div[2]/button[3]")  # 编辑
                self.Web_PO.eleSetTextByX(ele3, ".//div[3]/div[2]/div/div/form/div[2]/div/div/div/div/div/input", d_['编辑']['辖区名称'])
                self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[3]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['辖区级别'])
                self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[4]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['上级辖区'])
                self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[5]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['销售岗位关联'])
                self._dropdown4(ele3, ".//div[3]/div[2]/div/div/form/div[8]/div/div/div/div/div/div[1]", d_['编辑']['非销售岗位关联'])
                self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[9]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['启用状态'])
                self.Web_PO.eleSetTextByX(ele3, ".//div[3]/div[2]/div/div/form/div[10]/div/div/div/div/textarea", d_['编辑']['备注信息'])
                # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[2]/div[2]/button[3]")  # 保存

        # 点击 经理岗位
        if varSign == 0:
            for j in range(varZjQty):
                if varSign == 0:
                    l_jl1 = self.Web_PO.eleGetTextByXsByX(ele3, ".//div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div[" + str(j+1) + "]/div[2]/div", ".//div[1]")
                    # print(11)  # ['浦东/闵行/徐汇\n(\n薛伟)', '奉贤/金山\n(\n陈东升)', ...
                    for i in range(len(l_jl1)):
                        if d_['辖区名称'] in l_jl1[i]:
                            # print("经理岗位", d_['辖区名称'], i+1)
                            self.Web_PO.eleClkByX(ele3, ".//div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div[" + str(j+1) + "]/div[2]/div[" + str(i+1) + "]/div[1]", 2)
                            varSign = 1
                            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[2]/div[2]/button[3]")  # 编辑
                            self.Web_PO.eleSetTextByX(ele3, ".//div[3]/div[2]/div/div/form/div[2]/div/div/div/div/div/input", d_['编辑']['辖区名称'])
                            self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[3]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['辖区级别'])
                            self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[4]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['上级辖区'])
                            self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[5]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['销售岗位关联'])
                            self._dropdown4(ele3, ".//div[3]/div[2]/div/div/form/div[8]/div/div/div/div/div/div[1]", d_['编辑']['非销售岗位关联'])
                            self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[9]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['启用状态'])
                            self.Web_PO.eleSetTextByX(ele3, ".//div[3]/div[2]/div/div/form/div[10]/div/div/div/div/textarea", d_['编辑']['备注信息'])
                            # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[2]/div[2]/button[3]")  # 保存
                            break

        # 点击 总监岗位（耗材部）
        if varSign == 0:
            l_1 = []
            for i in range(varZjQty):
                l_1.append(self.Web_PO.eleGetTextByX(ele3, ".//div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div[" + str(i+1) + "]/div[1]/span[1]"))
            d_1 = dict(enumerate(l_1, start=1))
            d_1 = {v:k for k, v in d_1.items()}
            # print(d_1)
            for k, v in d_1.items():
                if k == d_['辖区名称']:
                    self.Web_PO.eleClkByX(ele3, ".//div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div[" + str(v) + "]/div[1]", 2)
            # 判断辖区名字是否是总监岗位
            areaName = self.Web_PO.eleGetShadowByXByC(ele3, ".//div[3]/div[2]/div/div/form/div[2]/div/div/div/div/div/input", 'div:nth-last-of-type(1)')
            if areaName == d_['辖区名称']:
                # print("总监岗位", areaName)
                varSign = 1
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[2]/div[2]/button[3]")  # 编辑
                self.Web_PO.eleSetTextByX(ele3, ".//div[3]/div[2]/div/div/form/div[2]/div/div/div/div/div/input", d_['编辑']['辖区名称'])
                self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[3]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['辖区级别'])
                self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[4]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['上级辖区'])
                self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[5]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['销售岗位关联'])
                self._dropdown4(ele3, ".//div[3]/div[2]/div/div/form/div[8]/div/div/div/div/div/div[1]", d_['编辑']['非销售岗位关联'])
                self._dropdown2(ele3, ".//div[3]/div[2]/div/div/form/div[9]/div/div/div/div/div/div[1]/div[2]", d_['编辑']['启用状态'])
                self.Web_PO.eleSetTextByX(ele3, ".//div[3]/div[2]/div/div/form/div[10]/div/div/div/div/textarea", d_['编辑']['备注信息'])
                # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[2]/div[2]/button[3]")  # 保存


    # todo 产品管理 - 产品信息管理

    def _dropdownDate_product(self, v):
        # 产品信息管理 - 最后更新时间

        varPrefix = "//div[@class='el-popper is-pure is-light el-picker__popper' and @aria-hidden='false']"

        # 1 获取日期年和月
        defaultYM = self.Web_PO.getTextByX(varPrefix + "/div/div/div/div[1]/div/div")
        defaultYear = int(defaultYM.split(" 年 ")[0])
        defaultMonth = int(defaultYM.split(" 年 ")[1].split(" 月")[0])
        # print("defaultYear", defaultYear)
        # print("defaultMonth", defaultMonth)

        # 2 切换年
        if v[0] < defaultYear:
            year = defaultYear - v[0]
            for i in range(year):
                self.Web_PO.clkByX(varPrefix + "/div/div/div/div[1]/div/button[1]")
        else:
            year = v[0] - defaultYear
            for i in range(year):
                self.Web_PO.clkByX(varPrefix + "/div/div/div/div[3]/div/button[1]")
        # 切换月
        if v[1] < defaultMonth:
            month = defaultMonth - v[1]
            for i in range(month):
                self.Web_PO.clkByX(varPrefix + "/div/div/div/div[1]/div/button[2]")
        else:
            month = v[1] - defaultMonth
            for i in range(month):
                self.Web_PO.clkByX(varPrefix + "/div/div/div/div[2]/div/button[2]")

        # 开始日期
        tr2 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[2]")
        tr3 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[3]")
        tr4 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[4]")
        tr5 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[5]")
        tr6 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[6]")
        tr7 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[7]")
        l_1 = []
        l_tr2 = tr2[0].split("\n")
        l_tr2 = [int(i) for i in l_tr2]
        l_tr2 = [0 if i > 10 else i for i in l_tr2]
        l_1.append(l_tr2)
        l_tr3 = tr3[0].split("\n")
        l_tr3 = [int(i) for i in l_tr3]
        l_1.append(l_tr3)
        l_tr4 = tr4[0].split("\n")
        l_tr4 = [int(i) for i in l_tr4]
        l_1.append(l_tr4)
        l_tr5 = tr5[0].split("\n")
        l_tr5 = [int(i) for i in l_tr5]
        l_1.append(l_tr5)
        l_tr6 = tr6[0].split("\n")
        l_tr6 = [int(i) for i in l_tr6]
        l_tr6 = [0 if i < 10 else i for i in l_tr6]
        l_1.append(l_tr6)
        l_tr7 = tr7[0].split("\n")
        l_tr7 = [int(i) for i in l_tr7]
        l_tr7 = [0 if i < 10 else i for i in l_tr7]
        l_1.append(l_tr7)
        # print("开始日期", l_1)  # [[0, 0, 0, 0, 0, 0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26, 27, 28, 29], [30, 31, 0, 0, 0, 0, 0]]
        for i in range(len(l_1)):
            for j in range(len(l_1[i])):
                if l_1[i][j] == v[2]:
                    self.Web_PO.clkByX(varPrefix + "/div/div/div/div[1]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 2)

        # 结束日期
        if v[1] == v[4]:
            varLoc = 1
        else:
            varLoc = 2
        tr2 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[2]")
        tr3 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[3]")
        tr4 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[4]")
        tr5 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[5]")
        tr6 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[6]")
        tr7 = self.Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[7]")
        l_1 = []
        l_tr2 = tr2[0].split("\n")
        l_tr2 = [int(i) for i in l_tr2]
        l_tr2 = [0 if i > 10 else i for i in l_tr2]
        l_1.append(l_tr2)
        l_tr3 = tr3[0].split("\n")
        l_tr3 = [int(i) for i in l_tr3]
        l_1.append(l_tr3)
        l_tr4 = tr4[0].split("\n")
        l_tr4 = [int(i) for i in l_tr4]
        l_1.append(l_tr4)
        l_tr5 = tr5[0].split("\n")
        l_tr5 = [int(i) for i in l_tr5]
        l_1.append(l_tr5)
        l_tr6 = tr6[0].split("\n")
        l_tr6 = [int(i) for i in l_tr6]
        l_tr6 = [0 if i < 10 else i for i in l_tr6]
        l_1.append(l_tr6)
        l_tr7 = tr7[0].split("\n")
        l_tr7 = [int(i) for i in l_tr7]
        l_tr7 = [0 if i < 10 else i for i in l_tr7]
        l_1.append(l_tr7)
        # print("结束日期", l_1)  # [[0, 0, 0, 0, 0, 0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26, 27, 28, 29], [30, 31, 0, 0, 0, 0, 0]]
        for i in range(len(l_1)):
            for j in range(len(l_1[i])):
                if l_1[i][j] == v[5]:
                    self.Web_PO.clkByX(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 2)

    def product_search(self, d_):
        # 产品信息管理 - 查询

        # 判断展开还是收起，如果已展开则不操作，否则展开
        ele2 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        s_ = self.Web_PO.eleGetTextByX(ele2, ".//div[2]/button[1]/span")
        if s_ == "展开":
            self.Web_PO.eleClkByX(ele2, ".//div[2]/button[1]", 1)  # 展开

        ele3 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../../..")
        for k, v in d_.items():
            if k == '产品编码':
                self.Web_PO.eleSetTextByX(ele3, ".//form/div/div/div[1]/div/div/div/div/input", v)
            elif k == '产品名称':
                self.Web_PO.eleSetTextByX(ele3, ".//form/div/div/div[2]/div/div/div/div/input", v)
            elif k == '品规编码':
                self.Web_PO.eleSetTextByX(ele3, ".//form/div/div/div[3]/div/div/div/div/input", v)
            elif k == '品规':
                self.Web_PO.eleSetTextByX(ele3, ".//form/div/div/div[4]/div/div/div/div/input", v)
            elif k == '剂型类别':
                self._dropdown2(ele3, ".//form/div/div/div[5]/div/div/div/div/div[1]/div[2]",  v)
            elif k == '产品类型':
                self._dropdown2(ele3, ".//form/div/div/div[6]/div/div/div/div/div[1]/div[2]",  v)
            elif k == '启用状态':
                self._dropdown2(ele3, ".//form/div/div/div[7]/div/div/div/div/div[1]/div[2]", v)
            elif k == '最后更新时间':
                self.Web_PO.eleClkByX(ele3, ".//form/div/div/div[8]/div/div[2]/div/input[1]", 1)
                self._dropdownDate_product(v)
        # 点击查询
        self.Web_PO.eleClkByX(ele2, ".//div[2]/button[2]", 3)

        # 返回搜索结果数量
        return self._getId()

    def product_add(self, varQty, d_):
        # 产品信息管理 - 新增

        if varQty == None:

            # 点击新增
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../..")
            self.Web_PO.eleClkByX(ele2, ".//div[2]/button[2]", 1)

            ele2 = self.Web_PO.getSuperEleByX("//span[text()='产品基础信息']", "../..")
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[1]/div[2]/div/div/div/div/input", d_['产品名称'])
            self.Web_PO.eleSetTextByX(ele2, ".//form/div[2]/div[1]/div/div/div/div/input", d_['通用名称'])
            self._dropdown2(ele2, ".//form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['产品类型'])
            if len(d_['产品观念']) == 1:
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div/div/div/div/div[2]/div[1]/div/div/div/input", d_['产品观念'][0])
            else:
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div/div/div/div/div[2]/div[1]/div/div/div/input", d_['产品观念'][0])
                self.Web_PO.eleClkByX(ele2, ".//form/div[3]/div/div/div/div/div[2]/div[2]")
                for i in range(len(d_['产品观念'])-1):
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div/div/div[2]/div/div[2]/div[" + str(i+2) + "]/div/div/div/input", d_['产品观念'][i+1])
                    self.Web_PO.eleClkByX(ele2, ".//form/div[3]/div/div/div[2]/div/div[2]/div[" + str(i+3) + "]")
                self.Web_PO.eleClkByX(ele2, ".//form/div[3]/div/div/div[2]/div/div[2]/div[" + str(i+3) + "]/div/button")

            if len(d_['产品品规信息']) == 1:
                # 品规1
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[1]/div[2]/div/div/div/div/input", d_['产品品规信息'][i]['品规'])
                self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[2]/div[1]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][i]['剂型类别'])
                self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][i]['计量单位'])
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[3]/div[1]/div/div/div/div/input", d_['产品品规信息'][i]['零售价格'])
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[3]/div[2]/div/div/div/div/input", d_['产品品规信息'][i]['成本价格'])
                self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[4]/div[1]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][i]['产品有效期'])
                self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][i]['启用状态'])
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[5]/div/div/div/div/textarea", d_['备注信息'])
            else:
                # 品规1
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[1]/div[2]/div/div/div/div/input", d_['产品品规信息'][0]['品规'])
                self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[2]/div[1]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][0]['剂型类别'])
                self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][0]['计量单位'])
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[3]/div[1]/div/div/div/div/input", d_['产品品规信息'][0]['零售价格'])
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[3]/div[2]/div/div/div/div/input", d_['产品品规信息'][0]['成本价格'])
                self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[4]/div[1]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][0]['产品有效期'])
                self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][0]['启用状态'])
                self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[1]/form/div[5]/div/div/div/div/textarea", d_['产品品规信息'][0]['备注信息'])
                for i in range(1, len(d_['产品品规信息'])):
                    # 点击增加品规
                    self.Web_PO.eleClkByX(ele2, ".//form/div[4]/button", 2)
                    self.Web_PO.eleScrollKeysEndByX(ele2, ".//form/div[5]/div[1]/div")
                    # 品规2-N
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[" + str(i*2+1) + "]/form/div[1]/div[2]/div/div/div/div/input", d_['产品品规信息'][i]['品规'])
                    self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[" + str(i*2+1) + "]/form/div[2]/div[1]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][i]['剂型类别'])
                    self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[" + str(i*2+1) + "]/form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][i]['计量单位'])
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[" + str(i*2+1) + "]/form/div[3]/div[1]/div/div/div/div/input", d_['产品品规信息'][i]['零售价格'])
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[" + str(i*2+1) + "]/form/div[3]/div[2]/div/div/div/div/input", d_['产品品规信息'][i]['成本价格'])
                    self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[" + str(i*2+1) + "]/form/div[4]/div[1]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][i]['产品有效期'])
                    self._dropdown2(ele2, ".//form/div[5]/div[1]/div/div[" + str(i*2+1) + "]/form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", d_['产品品规信息'][i]['启用状态'])
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[5]/div[1]/div/div[" + str(i*2+1) + "]/form/div[5]/div/div/div/div/textarea", d_['产品品规信息'][i]['备注信息'])

            # 确定
            ele5 = self.Web_PO.getSuperEleByX("//span[text()='产品基础信息']", "../../../../..")
            self.Web_PO.eleClkByX(ele5, ".//div[2]/div/button[2]", 1)








    def clickMemuOA(self, varMemuName, varSubName):

        '''左侧菜单选择模块及浮层模块（无标题）'''

        sleep(2)
        x = self.Web_PO.getXpathsText("//div")
        list1 = []
        for i in x:
            if "快捷菜单" in i:
                list1.append(i)
                break
        list2 = []
        for i in range(len(str(list1[0]).split("\n"))):
            if Str_PO.isContainChinese(str(list1[0]).split("\n")[i]) == True:
                list2.append(str(list1[0]).split("\n")[i])
        # print(list2)
        for j in range(len(list2)):
            if list2[j] == varMemuName:
                self.Web_PO.clickXpath("//ul[@id='first_menu']/li[" + str(j + 1) + "]", 2)
                x = self.Web_PO.getXpathsText("//li")
                list3 = []
                list4 = []
                for i in x:
                    if varMemuName in i:
                        list3.append(i)
                        break
                # print(list3)
                for i in range(len(str(list3[0]).split("\n"))):
                    if str(list3[0]).split("\n")[i] != varMemuName and Str_PO.isContainChinese(
                            str(list3[0]).split("\n")[i]) == True:
                        list4.append(str(list3[0]).split("\n")[i])
                for k in range(len(list4)):
                    if list4[k] == varSubName:
                        self.Web_PO.clickXpath(
                            "//ul[@id='first_menu']/li[" + str(j + 1) + "]/div[2]/ul/li[" + str(k + 1) + "]/a", 2)

    def clickMemuERP(self, menu1, menu2):

        # 盛蕴ERP管理平台 之菜单树

        l_menu1 = self.Web_PO.getXpathsText("//li")
        l_menu1_tmp = self.List_PO.delRepeatElem(l_menu1)
        for i in range(len(l_menu1_tmp)):
            if menu1 in l_menu1_tmp[i]:
                self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/div', 2)
                l_menu2_a = self.Web_PO.getXpathsText('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/ul/li/ul/a')
                # print(l_menu2_a)  # ['拜访分析报表', '会议分析表', '投入产出分析表', '协访分析表', '重点客户投入有效性分析', '开发计划总揽']
                for j in range(len(l_menu2_a)):
                    if menu2 == l_menu2_a[j]:
                        self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/ul/li/ul/a[' + str(j + 1) + ']', 2)

        self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/div[2]/div/div[1]/input', "1234测试")

    def maxBrowser(self, varWhichWindows):
        # 对当前browse全屏
        # Oa_Po.maxBrowser(1)
        self.Web_PO.switchLabel(varWhichWindows)
        self.Web_PO.driver.maximize_window()  # 全屏
        sleep(2)

    def zoom(self, percent):

        # 缩放比率

        # js = "document.body.style.zoom='70%'"
        js = "document.body.style.zoom='" + str(percent) + "%'"
        self.Web_PO.driver.execute_script(js)

    def quit(self):
        self.Web_PO.quit()

    def close(self):
        self.Web_PO.close()


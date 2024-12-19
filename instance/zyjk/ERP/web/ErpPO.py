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

        self.Web_PO.clksByX("//div[@class='el-sub-menu__title']", 1)
        d_menu_url = self.Web_PO.getDictTextAttrByAttrByX("//a", "href")
        return (d_menu_url)

    def newLabel(self,varUrl, varNo):
        self.Web_PO.opnLabel(varUrl, 2)
        self.Web_PO.swhLabel(varNo)

    def swhLabel(self, varNo):
        self.Web_PO.swhLabel(varNo)



    # todo 医院管理

    def _hospitalLevel(self, v ):
        # 公共 - 医院级别
        if v == '一级医院':
            self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[1]", 1)
        elif v == '二级医院':
            self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[2]", 1)
        elif v == '三级医院':
            self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[3]", 1)
        elif v == '民营':
            self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[4]", 1)
    def _hospitalPCC(self, v):
        # 公共 - 省份城市区县
        l_1 = self.Web_PO.getListTextByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul")
        l_2 = l_1[0].split("\n")
        d_3 = dict(enumerate(l_2, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(d_4[v]) + "]", 1)
    def _hospitalStatus(self, v):
        # 公共 - 启用状态
        if v == '停用':
            self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[1]")
        else:
            self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[2]")
    def _hospitalGetWay(self, v):
        # 公共 - 获取方式
        if v == '自动获取':
            self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[1]")
        else:
            self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[2]")


    def hospital_search(self, d_):
        # 查询
        # 展开
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/div/div[2]/button[1]", 3)

        for k, v in d_.items():
            if k == '医院编码':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[1]/div/div/div/div/input", v)
            if k == '医院名称':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[2]/div/div/div/div/input", v)
            if k == '医院级别':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[4]/div/div/div/div/div[1]/div[2]", 1)
                self._hospitalLevel(v)
            if k == '省份':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[5]/div/div/div/div/div[1]/div[2]", 2)
                self._hospitalPCC(v)
            if k == '城市':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[6]/div/div/div/div/div[1]/div[2]", 1)
                self._hospitalPCC(v)
            if k == '区县':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[7]/div/div/div/div/div[1]/div[2]", 1)
                self._hospitalPCC(v)
            if k == '启用状态':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[8]/div/div/div/div/div[1]/div[2]", 1)
                self._hospitalStatus(v)
            if k == '最后更新时间':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[9]/div/div[2]/div/input[1]", 1)
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[9]/div/div[2]/div/input[1]", v[0])
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[9]/div/div[2]/div/input[2]", 1)
                self.Web_PO.setTextEnterByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[9]/div/div[2]/div/input[2]", v[1])
            # 查询
            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/div/div[2]/button[2]", 2)

    def hospital_add(self):
        # 新增
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[2]/div[2]/button[2]", 1)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div/div/div/input", '上海医院')

        # 提交
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[2]/div/button[2]", 5)
        # 取消
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[2]/div/button[1]", 1)

    def hospital_edit(self, d_):
        # 修改
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[14]/div/div/button[1]", 2)
        # 医院全称
        for k, v in d_.items():
            if k == '医院全称':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[1]/div[2]/div/div/div/div/input", v)
            if k == '医院简称':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[2]/div[1]/div/div/div/div/input", v)
            if k == '医院级别':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", 2)
                self._hospitalLevel(v)
            if k == '省份':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[3]/div[1]/div/div/div/div/div[1]/div[2]", 1)
                self._hospitalPCC(v)
            if k == '城市':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[4]/div[1]/div/div/div/div/div[1]/div[2]", 1)
                self._hospitalPCC(v)
            if k == '区县':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", 1)
                self._hospitalPCC(v)
            if k == '启动状态':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[3]/div[2]/div/div/div/div/div[1]/div[2]", 1)
                self._hospitalStatus(v)
            if k == '详细地址':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[5]/div[1]/div/div/div/div/input", v)
            if k == '获取方式':
                self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[5]/div[2]/div/div/div/div/div[1]/div[2]", 1)
                self._hospitalGetWay(v)
            if k == '邮政编码':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[7]/div[1]/div/div/div/div/input", v)
            if k == '电话':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[7]/div[2]/div/div/div/div/input", v)
            if k == '邮箱':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[8]/div[1]/div/div/div/div/input", v)
            if k == '网址':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[8]/div[2]/div/div/div/div/input", v)
            if k == '床位数':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[9]/div[1]/div/div/div/div/input", v)
            if k == '门诊量':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[9]/div[2]/div/div/div/div/input", v)
            if k == '备注信息':
                self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[1]/div/div[2]/form/div[10]/div/div/textarea", v)

        # 取消
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[2]/div/button[1]", 1)
        # 提交
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[2]/div/button[2]", 1)

    def hospital_info(self):
        # 详情
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[14]/div/div/button[2]", 2)
        # 关闭
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[4]/div/div/div[2]/div/button", 1)

    def hospital_reset(self):
        # 重置
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div[1]/div/div/div[2]/button[3]", 2)

    # todo 经销商管理
    def dealer_search(self, d_):

        for k,v in d_.items():
            if k == '经销商名称':
                self.Web_PO.setTextByX(
                    "/html/body/div[1]/div/div[2]/section/div/div[1]/div/form/div/div/div[2]/div/div/div/div/input",
                    v)


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


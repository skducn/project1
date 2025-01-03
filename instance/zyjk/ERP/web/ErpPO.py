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



    # todo 医院管理

    def _dropdown(self, ele, elePath, l_, v):
        # 公共下拉框
        # _dropdown(ele, "//", ['总院', '分院', '门诊部'], '分院')
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}  # {'总院': 1, '分院': 2, '门诊部': 3}
        self.Web_PO.eleClkByX(ele, elePath, 1)
        self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(d_4[v]) + "]", 1)

    # def _hospitalType(self, ele, elePath, v):
    #     # 公共 - 医院类型
    #     self.Web_PO.eleClkByX(ele, elePath, 1)
    #     if v == '总院':
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[1]", 1)
    #     elif v == '分院':
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[2]", 1)
    #     elif v == '门诊部':
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[3]", 1)
    # def _hospitalLevel(self, ele, elePath, v):
    #     # 公共 - 医院类型、经销商级别
    #     self.Web_PO.eleClkByX(ele, elePath, 1)
    #     if v == '一级医院' or v == '一级':
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[1]", 1)
    #     elif v == '二级医院' or v == '二级':
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[2]", 1)
    #     elif v == '三级医院' or v == '三级':
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[3]", 1)
    #     elif v == '民营':
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[4]", 1)
    def _hospitalPCC(self, ele, elePath, v):
        # 公共 - 省份城市区县
        self.Web_PO.eleClkByX(ele, elePath, 1)
        l_1 = self.Web_PO.getTextByXs("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul")
        # l_1 = self.Web_PO.getListTextByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul")
        l_2 = l_1[0].split("\n")
        d_3 = dict(enumerate(l_2, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[" + str(d_4[v]) + "]", 1)
    # def _hospitalStatus(self, ele, elePath, v):
    #     # 公共 - 启用状态
    #     self.Web_PO.eleClkByX(ele, elePath, 1)
    #     if v == '停用':
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[1]")
    #     else:
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[2]")
    # def _hospitalGetWay(self, ele, elePath, v):
    #     # 公共 - 获取方式
    #     self.Web_PO.eleClkByX(ele, elePath, 1)
    #     if v == '自动获取':
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[1]")
    #     else:
    #         self.Web_PO.clkByX("//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li[2]")


    def hospital_search(self, d_):
        # 筛选查询

        # 点击展开
        ele = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[1]", 1)

        ele2 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../../..")
        for k, v in d_.items():
            if k == '医院编码':
                self.Web_PO.eleSetTextByX(ele2, ".//form/div/div/div[1]/div/div/div/div/input", v)
            if k == '医院名称':
                self.Web_PO.eleSetTextByX(ele2, ".//form/div/div/div[2]/div/div/div/div/input", v)
            if k == '别名':
                self.Web_PO.eleSetTextByX(ele2, ".//form/div/div/div[3]/div/div/div/div/input", v)
            if k == '医院级别':
                self._dropdown(ele2, ".//form/div/div/div[4]/div/div/div/div/div[1]/div[2]", ["一级医院", "二级医院", "三级医院", "民营"], v)
            if k == '省份':
                self._hospitalPCC(ele2, ".//form/div/div/div[5]/div/div/div/div/div[1]/div[2]", v)
            if k == '城市':
                self._hospitalPCC(ele2, ".//form/div/div/div[6]/div/div/div/div/div[1]/div[2]", v)
            if k == '区县':
                self._hospitalPCC(ele2, ".//form/div/div/div[7]/div/div/div/div/div[1]/div[2]", v)
            if k == '启用状态':
                self._dropdown(ele2, ".//form/div/div/div[8]/div/div/div/div/div[1]/div[2]", ["停用", "启用"], v)
            if k == '最后更新时间':
                self.Web_PO.eleClkByX(ele2, ".//form/div/div/div[9]/div/div[2]/div/input[1]", 1)
                self.Web_PO.eleSetTextByX(ele2, ".//form/div/div/div[9]/div/div[2]/div/input[1]", v[0])
                self.Web_PO.eleClkByX(ele2, ".//form/div/div/div[9]/div/div[2]/div/input[2]", 1)
                self.Web_PO.eleSetTextByX(ele2, ".//form/div/div/div[9]/div/div[2]/div/input[2]", v[1])
        # 点击查询
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[2]", 1)

    def hospital_reset(self):
        # 重置

        # 点击重置
        ele = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[3]", 1)

    def hospital_add(self, d_):
        # 新增，并获取新增后的医院编码

        # 点击新增
        ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../..")
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[2]", 1)

        # 医院基础信息
        ele2 = self.Web_PO.getSuperEleByX("//span[text()='医院基础信息']", "../..")
        self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[1]/div[2]/div/div/div/div/input", d_['医院全称'])
        self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[2]/div[1]/div/div/div/div/input", d_['医院简称'])
        self._dropdown(ele2, ".//div[2]/form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", ['总院', '分院', '门诊部'], d_['医院类型'])
        self._dropdown(ele2, ".//div[2]/form/div[3]/div[2]/div/div/div/div/div[1]/div[2]", ["一级医院", "二级医院", "三级医院", "民营"], d_['医院级别'])
        self._hospitalPCC(ele2, ".//div[2]/form/div[4]/div[1]/div/div/div/div/div[1]/div[2]", d_['省份'])
        self._dropdown(ele2, ".//div[2]/form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", ["停用", "启用"], d_['启用状态'])
        self._hospitalPCC(ele2, ".//div[2]/form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", d_['城市'])
        self._hospitalPCC(ele2, ".//div[2]/form/div[5]/div[2]/div/div/div/div/div[1]/div[2]", d_['区县'])
        # 以下非必填
        self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[6]/div[1]/div/div/div/div/input", d_['详细地址'])
        self._dropdown(ele2, ".//div[2]/form/div[6]/div[2]/div/div/div/div/div[1]/div[2]", ["自动获取", "手动输入"], d_['获取方式'])
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

        # 2.2 新增后获取医院编码
        self.hospital_search({"医院全称": d_['医院全称']})
        # 判断搜索结果数量，如果是1条直接修改，否则提示多条
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":
            d_['医院编码'] = self.Web_PO.getTextByX("//tr[@class='el-table__row']/td[1]/div/span")
            print("医院编码:", d_['医院编码'] )
        else:
            print("warning! 搜索结果有多条或0条！")


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

        # self.Web_PO.eleClkByX(ele2, ".//footer/span/button[2]")  # 提交


    def hospital_edit(self, d_search, d_):
        # 修改

        # 先搜索
        self.hospital_search(d_search)

        # 判断搜索结果数量，如果是1条直接修改，否则提示多条
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":

            # 获取医院编码
            d_['医院编码'] = self.Web_PO.getTextByX("//tr[@class='el-table__row']/td[1]/div/span")
            print("医院编码:", d_['医院编码'] )

            # 获取td数量，定位修改按钮(因为td字段可通过配置显示或隐藏),点击修改
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/div/button[1]")  # 修改

            # 医院基础信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='医院基础信息']", "../..")
            for k, v in d_.items():
                if k == '医院全称':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[1]/div[2]/div/div/div/div/input", d_['医院全称'])
                if k == '医院简称':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[2]/div[1]/div/div/div/div/input", d_['医院简称'])
                if k == '医院级别':
                    self._dropdown(ele2, ".//div[2]/form/div[3]/div[2]/div/div/div/div/div[1]/div[2]",["一级医院", "二级医院", "三级医院", "民营"], d_['医院级别'])
                if k == '省份':
                    self._hospitalPCC(ele2, ".//div[2]/form/div[4]/div[1]/div/div/div/div/div[1]/div[2]", d_['省份'])
                if k == '启动状态':
                    self._dropdown(ele2, ".//div[2]/form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", ["停用", "启用"], d_['启用状态'])
                if k == '城市':
                    self._hospitalPCC(ele2, ".//div[2]/form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", d_['城市'])
                if k == '区县':
                    self._hospitalPCC(ele2, ".//div[2]/form/div[5]/div[2]/div/div/div/div/div[1]/div[2]", d_['区县'])
                if k == '详细地址':
                    self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[6]/div[1]/div/div/div/div/input", d_['详细地址'])
                if k == '获取方式':
                    self._dropdown(ele2, ".//div[2]/form/div[6]/div[2]/div/div/div/div/div[1]/div[2]", ["自动获取", "手动输入"], d_['获取方式'])
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
            # self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[1]", 1) # 取消
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 提交
        else:
            print("warning! 搜索结果有多条或0条！")

    def hospital_info(self, d_search):
        # 详情

        # 先搜索
        self.hospital_search(d_search)

        # 判断搜索结果数量，如果是1条直接修改，否则提示多条
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":

            # 获取td数量，定位修改按钮(因为td字段可通过配置显示或隐藏)，点击详情
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/div/button[2]")  # 详情

            # 医院详情 - 医院基础信息
            ele = self.Web_PO.getSuperEleByX("//span[text()='医院基础信息']", "../..")
            l_ = self.Web_PO.eleGetTextByXs(ele, ".//div[2]/div/table/tr")
            print(l_)  # ['医院全称\n天津自动化医院1\n医院简称\n天自院1', '医院级别\n二级医院\n医院类型\n分院',...

            # 关闭
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='医院详情']", "../../..")
            self.Web_PO.eleClkByX(ele2, ".//div[2]/div/button[1]", 1)  # 关闭
        else:
            print("warning! 搜索结果有多条或0条！")



    # todo 经销商管理
    def dealer_search(self, d_):
        # 筛选查询

        # 点击展开
        ele = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[1]", 1)

        ele2 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../../..")
        for k, v in d_.items():
            if k == '经销商编码':
                self.Web_PO.eleSetTextByX(ele2, ".//form/div/div/div[1]/div/div/div/div/input", v)
            if k == '经销商名称':
                self.Web_PO.eleSetTextByX(ele2, ".//form/div/div/div[2]/div/div/div/div/input", v)
            if k == '经销商级别':
                self._dropdown(ele2, ".//form/div/div/div[4]/div/div/div/div/div[1]/div[2]", ["一级", "二级", "三级"], v)
            if k == '省份':
                self._hospitalPCC(ele2, ".//form/div/div/div[5]/div/div/div/div/div[1]/div[2]", v)
            if k == '城市':
                self._hospitalPCC(ele2, ".//form/div/div/div[6]/div/div/div/div/div[1]/div[2]", v)
            if k == '区县':
                self._hospitalPCC(ele2, ".//form/div/div/div[7]/div/div/div/div/div[1]/div[2]", v)
            if k == '启用状态':
                self._dropdown(ele2, ".//form/div/div/div[8]/div/div/div/div/div[1]/div[2]", ["停用", "启用"], v)
            if k == '最后更新时间':
                self.Web_PO.eleClkByX(ele2, ".//form/div/div/div[9]/div/div[2]/div/input[1]", 1)
                self.Web_PO.eleSetTextByX(ele2, ".//form/div/div/div[9]/div/div[2]/div/input[1]", v[0])
                self.Web_PO.eleClkByX(ele2, ".//form/div/div/div[9]/div/div[2]/div/input[2]", 1)
                self.Web_PO.eleSetTextByX(ele2, ".//form/div/div/div[9]/div/div[2]/div/input[2]", v[1])
        # 点击查询
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[2]", 1)

    def dealer_add(self, d_):
        # 新增，并获取新增后的经销商编码

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
        self._dropdown(ele2, ".//form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", ["停用", "启用"], d_['启用状态'])
        self._dropdown(ele2, ".//form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", ["一级", "二级", "三级"], d_['经销商级别'])
        self.Web_PO.eleSetTextByX(ele2, ".//form/div[6]/div/div/div/div/textarea", d_['备注信息'])
        # 确定
        ele3 = self.Web_PO.getSuperEleByX("//span[text()='经销商基础信息']", "../../../../..")
        self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 确定

        # 2.2 新增后获取经销商编码
        self.dealer_search({"经销商名称": d_['经销商名称']})
        # 判断搜索结果数量，如果是1条直接修改，否则提示多条
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":
            d_['经销商编码'] = self.Web_PO.getTextByX("//tr[@class='el-table__row']/td[1]/div/span")
            print("经销商编码:", d_['经销商编码'] )
        else:
            print("warning! 搜索结果有多条或0条！")

    def dealer_edit(self, d_search, d_):
        # 修改

        # 先搜索
        self.dealer_search(d_search)

        # 判断搜索结果数量，如果是1条直接修改，否则提示多条
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":

            # 获取经销商编码
            d_['经销商编码'] = self.Web_PO.getTextByX("//tr[@class='el-table__row']/td[1]/div/span")
            print("经销商编码:", d_['经销商编码'])

            # 获取td数量，定位修改按钮(因为td字段可通过配置显示或隐藏)，点击修改
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/button[1]")  # 修改

            # 经销商基础信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='经销商基础信息']", "../..")
            for k, v in d_.items():
                # 医院基础信息
                if k == '经销商名称':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[1]/div[2]/div/div/div/div/input", d_['经销商名称'])
                if k == '省份':
                    self._hospitalPCC(ele2, ".//form/div[2]/div[1]/div/div/div/div/div[1]/div[2]", d_['省份'])
                if k == '城市':
                    self._hospitalPCC(ele2, ".//form/div[2]/div[2]/div/div/div/div/div[1]/div[2]", d_['城市'])
                if k == '区县':
                    self._hospitalPCC(ele2, ".//form/div[3]/div[1]/div/div/div/div/div[1]/div[2]", d_['区县'])
                if k == '联系地址':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[3]/div[2]/div/div/div/div/input", d_['详细地址'])
                if k == '联系电话':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[4]/div[1]/div/div/div/div/input", d_['联系电话'])
                if k == '启动状态':
                    self._dropdown(ele2, ".//form/div[4]/div[2]/div/div/div/div/div[1]/div[2]", ["停用", "启用"], d_['启用状态'])
                if k == '经销商级别':
                    self._dropdown(ele2, ".//form/div[5]/div[1]/div/div/div/div/div[1]/div[2]", ["一级", "二级", "三级"], d_['经销商级别'])
                if k == '备注信息':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[6]/div/div/div/div/textarea", d_['备注信息'])
            # 确定
            ele3 = self.Web_PO.getSuperEleByX("//span[text()='经销商基础信息']", "../../../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 确定

        else:
            print("warning! 搜索结果有多条或0条！")

    def dealer_info(self, d_search):
        # 获取记录详情

        # 先搜索
        self.dealer_search(d_search)

        # 判断搜索结果数量，如果是1条直接修改，否则提示多条
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":

            # 获取td数量，定位详情按钮(因为td字段可通过配置显示或隐藏)，点击详情
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele, ".//div[3]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/button[2]", 1)  # 详情

            # 经销商修改 - 经销商基础信息
            ele = self.Web_PO.getSuperEleByX("//span[text()='经销商基础信息']", "../..")
            l_ = self.Web_PO.eleGetTextByXs(ele, ".//div[2]/div/table/tr")
            print(l_)  # ['经销商编码\nDLR000003\n经销商名称\n百慕大自动优质经销商1', ,...

            # 关闭
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='经销商详情']", "../../..")
            self.Web_PO.eleClkByX(ele2, ".//div[2]/div/button[1]", 1)  # 关闭
        else:
            print("warning! 搜索结果有多条或0条！")



    # todo 商业公司管理

    def business_search(self, d_):
        # 筛选查询

        ele = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../..")
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[1]", 1)  # 展开

        ele2 = self.Web_PO.getSuperEleByX("//span[text()='筛选查询']", "../../..")
        for k, v in d_.items():
            if k == '商业公司编码':
                self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[1]/div[1]/div/div/div/div/input", v)
            if k == '商业公司全称':
                self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[1]/div[2]/div/div/div/div/input", v)
            if k == '联系人':
                self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[1]/div[3]/div/div/div/div/input", v)
            if k == '启用状态':
                self._dropdown(ele2, ".//div[2]/form/div[1]/div[4]/div/div/div/div/div[1]/div[2]", ["停用", "启用"], v)
            if k == '最后更新时间':
                self.Web_PO.eleClkByX(ele2, ".//div[2]/form/div[2]/div/div/div/div[2]/div/input[1]", 1)
                self.Web_PO.eleSetTextByX(ele2, ".//div[2]/form/div[2]/div/div/div/div[2]/div/input[1]", v[0])
                self.Web_PO.eleClkByX(ele2, ".//div[2]/form/div[2]/div/div/div/div[2]/div/input[2]", 1)
                self.Web_PO.eleSetTextTabByX(ele2, ".//div[2]/form/div[2]/div/div/div/div[2]/div/input[2]", v[1])
        self.Web_PO.eleClkByX(ele, ".//div[2]/button[2]", 1)  # 查询

    def business_add(self, d_):
        # 新增，并获取新增后的医院编码

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
        self._dropdown(ele2, ".//form/div[7]/div[2]/div/div/div/div/div[1]/div[2]", ["生产", "经营"], d_['企业类别'])
        self._dropdown(ele2, ".//form/div[8]/div/div/div/div/div/div[1]/div[2]", ["停用", "启用"], d_['启用状态'])
        self.Web_PO.eleSetTextByX(ele2, ".//form/div[9]/div/div/div/div/textarea", d_['生产(经营)范围'])
        self.Web_PO.eleSetTextByX(ele2, ".//form/div[10]/div/div/div/div/textarea", d_['备注信息'])

        # 确认 bug改文字为确定
        ele3 = self.Web_PO.getSuperEleByX("//span[text()='商业公司基础信息']", "../../../..")
        self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 确认

        # # 2.2 新增后获取医院编码
        self.business_search({"商业公司全称": d_['商业公司全称']})
        # 判断搜索结果数量，如果是1条直接修改，否则提示多条
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":
            d_['商业公司编码'] = self.Web_PO.getTextByX("//tr[@class='el-table__row']/td[1]/div/span")
            print("商业公司编码:", d_['商业公司编码'])
        else:
            print("warning! 搜索结果有多条或0条！")

    def business_edit(self, d_search, d_):
        # 修改

        # 先搜索
        self.business_search(d_search)

        # 判断搜索结果数量，如果是1条直接修改，否则提示多条
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":

            # 获取商业公司编码
            d_['商业公司编码'] = self.Web_PO.getTextByX("//tr[@class='el-table__row']/td[1]/div/span")
            print("商业公司编码:", d_['商业公司编码'] )

            # 获取td数量，定位修改按钮(因为td字段可通过配置显示或隐藏),点击修改
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/div/button[1]")  # 修改

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
                    self._dropdown(ele2, ".//form/div[7]/div[2]/div/div/div/div/div[1]/div[2]", ["生产", "经营"], d_['企业类别'])
                if k == '启动状态':
                    self._dropdown(ele2, ".//form/div[8]/div/div/div/div/div/div[1]/div[2]", ["停用", "启用"], d_['启用状态'])
                if k == '生产(经营)范围':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[9]/div/div/div/div/textarea", d_['生产(经营)范围'])
                if k == '备注信息':
                    self.Web_PO.eleSetTextByX(ele2, ".//form/div[10]/div/div/div/div/textarea", d_['备注信息'])

            ele3 = self.Web_PO.getSuperEleByX("//span[text()='商业公司基础信息']", "../../../..")
            self.Web_PO.eleClkByX(ele3, ".//div[2]/div/button[2]", 1)  # 提交
        else:
            print("warning! 搜索结果有多条或0条！")

    def business_info(self, d_search):
        # 详情

        # 先搜索
        self.business_search(d_search)

        # 判断搜索结果数量，如果是1条直接修改，否则提示多条
        if self.Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":

            # 获取td数量，定位修改按钮(因为td字段可通过配置显示或隐藏)，点击详情
            ele = self.Web_PO.getSuperEleByX("//span[text()='数据列表']", "../../..")
            varTdLoc = self.Web_PO.eleGetQtyByXs(ele, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td")
            self.Web_PO.eleClkByX(ele, ".//div[4]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[" + str(varTdLoc) + "]/div/div/button[2]")  # 详情

            # 商业公司详情 - 商业公司基础信息
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='商业公司基础信息']", "../..")
            l_ = self.Web_PO.eleGetTextByXs(ele2, ".//div[2]/table/tr")
            print(l_)  # ['商业公司编码 COM00004 商业公司全称 阿依达商业自动化有限公司3', ...

            # 关闭
            ele2 = self.Web_PO.getSuperEleByX("//span[text()='商业公司详情']", "../../..")
            self.Web_PO.eleClkByX(ele2, ".//div[2]/div/button[1]", 1)  # 关闭
        else:
            print("warning! 搜索结果有多条或0条！")











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


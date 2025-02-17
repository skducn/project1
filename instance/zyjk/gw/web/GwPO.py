# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-7-25
# Description:
# https://chromedriver.storage.googleapis.com/index.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import sys
sys.path.append("/Users/linghuchong/Downloads/51/Python/project/")
# sys.path.append('../../..')

from PO.WebPO import *
Web_PO = WebPO("chrome")

from PO.ListPO import *
List_PO = ListPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.SysPO import *
Sys_PO = SysPO()

from PO.Base64PO import *
Base64_PO = Base64PO()

import logging, os, sys
import signal

import ddddocr

class GwPO():

    def __init__(self, varFile):
        # 配置日志
        if os.name == 'nt':
            logging.basicConfig(filename=varFile, level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
        else:
            logging.basicConfig(filename=varFile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        # print(varFile, datetime.datetime.now())


    # 定义信号处理函数
    def handle_signal(self, signum, frame):
        self.logger.info('Received signal: {}'.format(signal.Signals(signum).name))
        self.logger.info('Program is terminating...')
        # 在这里可以添加额外的清理代码或日志记录

    # todo common

    def pagination(self, varGoto):

        d_ = {}
        ele = Web_PO.getSuperEleByX("//div[@class='my-table-pagination']", '.')
        s_totalRecord = Web_PO.eleGetTextByX(ele, './/div/span[1]')
        s_totalRecord = s_totalRecord.split('共 ')[1].split(' 条')[0]
        d_['totalRecord'] = int(s_totalRecord)  # 共 17 条

        s_totalPage = int(d_['totalRecord'] / 10) + 1
        d_['totalPage'] = s_totalPage  # 2   //2页

        # 设置每页显示40条
        # Web_PO.eleClkByX(ele, './/input', 1)
        # Web_PO.clkByX('/html/body/div[2]/div[15]/div/div/div[1]/ul/li[4]')

        # 前往第几页
        Web_PO.eleSetTextBackspaceEnterByX(ele, './/div/span[3]/div/input', 3, varGoto)
        s_gotoPage = Web_PO.eleGetShadowByXByC(ele, './/div/span[3]/div/input', 'div:nth-last-of-type(1)')
        d_['gotoPage'] = int(s_gotoPage)
        return d_  #


    def _clkDropdownNoPath(self, ele, eleXpath, varXpaths, v):

        # 选择下拉框的值
        # self._clkDropdownNoPath(Web_PO.eleGetSuperEleByX(ele, ".//label[text()='" + k + "']", ".."), ".//div[2]/div/div", _liByX1, d_['周期版本'])
        Web_PO.eleClkByX(ele, eleXpath, 1)
        l_ = Web_PO.getTextByXs(varXpaths)
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
        Web_PO.clkByX(varXpaths + "[" + str(d_4[v]) + "]", 1)

    # def _eleClkDropdownSpan(self, k, ele, varXpath, varXpaths, v):
    #     # 选择下拉框的值
    #     # self._eleClkDropdown(k, _dropdownByX, _liByXs, v)
    #     # self._eleClkDropdown(k, ele, ".//div/div/div/div[1]/div[2]", "/html/body/div[2]/div[6]/div/div[2]/div[1]/ul/li", v)
    #     ele2 = Web_PO.eleGetSuperEleByX(ele, ".//span[text()='" + k + "']", "..")
    #     Web_PO.eleClkByX(ele2, varXpath, 1)
    #     l_ = Web_PO.getTextByXs(varXpaths)
    #     d_3 = dict(enumerate(l_, start=1))
    #     d_4 = {v: k for k, v in d_3.items()}
    #     # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
    #     Web_PO.clkByX(varXpaths + "[" + str(d_4[v]) + "]", 1)

    def _eleClkDropdown(self, ele, varXpath, varXpaths, v):
        # 选择下拉框的值
        # self._eleClkDropdown(ele, ".//div/div/div/div[1]/div[2]", "/html/body/div[2]/div[6]/div/div[2]/div[1]/ul/li", v)

        # ele2 = Web_PO.eleGetSuperEleByX(ele, ".//label[text()='" + k + "']", "..")
        Web_PO.eleClkByX(ele, varXpath, 1)
        l_ = Web_PO.getTextByXs(varXpaths)
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
        if isinstance(v, str):
            Web_PO.clkByX(varXpaths + "[" + str(d_4[v]) + "]", 1)
        elif isinstance(v, list):
            for i in range(len(v)):
                Web_PO.clkByX(varXpaths + "[" + str(d_4[v[i]]) + "]", 1)


    # def _eleClkRadio(self, ele, varXpaths, v):
    #     # 选择单选框的值(定位label左[v的对应值])
    #     # Web_PO.eleRadioLeftLabel(self._eleDiv(ele, k), ".//div[2]/div/div/div", v)
    #     l_ = Web_PO.eleGetTextByXs(ele, varXpaths)
    #     # if l_ == ['门诊\n家庭\n电话']:
    #     #     l_ = l_[0].split('\n')
    #     # elif l_ == ['有\n无']:
    #     #     l_ = l_[0].split('\n')
    #     # elif l_ == ['是\n否']:
    #     #     l_ = l_[0].split('\n')
    #     if "\n" in l_[0]:
    #         l_ = l_[0].split('\n')
    #     # print(l_)
    #     d_3 = dict(enumerate(l_, start=1))
    #     d_4 = {v: k for k, v in d_3.items()}
    #     # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
    #
    #     # 获取单选框所有值的状态
    #     l_value = Web_PO.eleGetTextByXs(ele, ".//label/span[2]")
    #     # print(l_value)  # ['是', '否']
    #     l_class = Web_PO.eleGetAttrValueByXs(ele, ".//label", "class")
    #     # print(l_class)  # ['el-radio el-radio--default', 'el-radio is-checked el-radio--default']
    #     l_isChecked = []
    #     for i in range(len(l_class)):
    #         if l_class[i] == 'el-radio is-checked el-radio--default' or l_class[i] == 'el-radio is-disabled is-checked el-radio--default':
    #             l_isChecked.append(1)
    #         else:
    #             l_isChecked.append(0)
    #     d_default = dict(zip(l_value, l_isChecked))
    #     # print(d_default)  # {'是': 0, '否': 1}
    #
    #     # 检查是否已经选中，如果未选择则勾选，否则不操作。
    #     if d_default[v] == 0:
    #         Web_PO.eleClkByX(ele, varXpaths + "[" + str(d_4[v]) + "]/label", 1)
    #         # 如：/html/body/div[1]/div/div[3]/section/div/form/div[2]/div[7]/div[2]/div[2]/div/div/div[2]/label


    # def _eleClkRadioByLabel(self, ele, varXpaths, v):
    #     # 选择单选框的值(定位label右[v的对应值])
    #     # Web_PO.eleRadioLeftLabel(self._eleDiv(ele, k), ".//div[2]/div/div/div/label", v)
    #
    #     l_ = Web_PO.eleGetTextByXs(ele, varXpaths)
    #     if "\n" in l_[0]:
    #         l_ = l_[0].split('\n')
    #     # print(l_)
    #     d_3 = dict(enumerate(l_, start=1))
    #     d_4 = {v: k for k, v in d_3.items()}
    #     # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
    #
    #     # 获取单选框所有值的状态
    #     l_value = Web_PO.eleGetTextByXs(ele, ".//label/span[2]")
    #     # print(l_value)  # ['是', '否']
    #     l_class = Web_PO.eleGetAttrValueByXs(ele, ".//label", "class")
    #     # print(l_class)  # ['el-radio el-radio--default', 'el-radio is-checked el-radio--default']
    #     l_isChecked = []
    #     for i in range(len(l_class)):
    #         if l_class[i] == 'el-radio is-checked el-radio--default' or l_class[i] == 'el-radio is-disabled is-checked el-radio--default':
    #             l_isChecked.append(1)
    #         else:
    #             l_isChecked.append(0)
    #     d_default = dict(zip(l_value, l_isChecked))
    #     # print(d_default)  # {'是': 0, '否': 1}
    #
    #     # 检查是否已经选中，如果未选择则勾选，否则不操作。
    #     if d_default[v] == 0:
    #         Web_PO.eleClkByX(ele, varXpaths + "[" + str(d_4[v]) + "]", 1)
    #         # 如 /html/body/div[1]/div/div[3]/section/div/form/div[2]/div[8]/div[1]/div[2]/div/div/div/label[2]





   
    def _eleCheckboxPay(self, ele, v, default='remain'):
        # 医疗费用支付方式
        # 选择复选框的值

        ele = Web_PO.getSuperEleByX("//div[text()=' 医疗费用支付方式 ']", '..')

        # 1, 全部不勾选
        if default != "remain":
            # 城镇职工基本医疗保险
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div/label", "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div/label", 1)
            # 城镇居民基本医疗保险
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/label", "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/label", 1)
            # 贫困救助
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/label", "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/label", 1)
            # 商业医疗保险
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", 1)
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", 1)
            # 全公费
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[5]/label", "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[5]/label", 1)
            # 全自费
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[6]/label", "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[6]/label", 1)
            # 其他
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[7]/label", "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[7]/label", 1)

        # 更改
        for i in range(len(v)):
            if isinstance(v[i], str):
                if v[i] == '商业医疗保险':
                    varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", "class")
                    if varClass != 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", 1)
                        # Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", 1)
                if v[i] == "全公费":
                    varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[5]/label", "class")
                    if varClass != 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[5]/label", 1)
                if v[i] == "全自费":
                    varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[6]/label", "class")
                    if varClass != 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[6]/label", 1)
            elif isinstance(v[i], list):
                if v[i][0] == '城镇职工基本医疗保险':
                    varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div/label", "class")
                    if varClass != 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div/label", 1)
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/input", v[i][1])
                if v[i][0] == '城镇居民基本医疗保险':
                    varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/label", "class")
                    if varClass != 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/label", 1)
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[1]/div[3]/div/div/div/div/input", v[i][1])
                if v[i][0] == '贫困救助':
                    varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/label", "class")
                    if varClass != 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/label", 1)
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[2]/div/div/div/input", v[i][1])
                if v[i][0] == '其他':
                    varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[7]/label", "class")
                    if varClass != 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[7]/label", 1)
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[2]/div[2]/div/div/div/div/input", v[i][1])


    def _dropdownDate(self, v):
        # 公共 - 日期区间
        # 如：最后更新时间，入职日期，离职日期

        varPrefix = "//div[@class='el-picker-panel el-date-range-picker' and @visible='true']"

        # 1 获取日期年和月
        defaultYM = Web_PO.getTextByX(varPrefix + "/div/div/div[1]/div/div")
        defaultYear = int(defaultYM.split(" 年 ")[0])
        defaultMonth = int(defaultYM.split(" 年 ")[1].split(" 月")[0])
        # print("defaultYear", defaultYear)
        # print("defaultMonth", defaultMonth)

        # 2 切换年
        if v[0] < defaultYear:
            year = defaultYear - v[0]
            for i in range(year):
                Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[1]/button[1]")
                # /html/body/div[2]/div[7]/div/div/div/div[1]/div/button[1]
        else:
            year = v[0] - defaultYear
            for i in range(year):
                Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[4]/button[2]")
                # /html/body/div[2]/div[7]/div/div/div/div[2]/div/button[1]
        # 切换月
        if v[1] < defaultMonth:
            month = defaultMonth - v[1]
            for i in range(month):
                Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[1]/button[2]")
                # /html/body/div[2]/div[7]/div/div/div/div[1]/div/button[2]
        else:
            month = v[1] - defaultMonth
            for i in range(month):
                Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[2]/span[4]/button[1]")
                # /html/body/div[2]/div[7]/div/div/div/div[2]/div/button[2]

        # if v[0] < int(defaultYear):
        #     Web_PO.clkByX(varPrefix + "/div/div/div[1]/div/button[2]", 1)
        #     defaultYM = Web_PO.getTextByX(varPrefix + "/div/div/div[1]/div/div")
        #     defaultMonth = defaultYM.split(" 年 ")[1].split(" 月")[0]
        #     if v[1] < int(defaultMonth):
        #         b = int(defaultMonth) - v[1]
        #         # print(b)
        #         for i in range(b):
        #             Web_PO.clkByX("//div[@class='el-picker-panel el-date-range-picker' and @visible='true']/div/div/div[1]/div/button[2]", 1)

        # 开始日期
        # /html/body/div[2]/div[7]/div/div/div/div[1]/table/tbody/tr[2]
        tr2 = Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[2]")
        tr3 = Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[3]")
        tr4 = Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[4]")
        tr5 = Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[5]")
        tr6 = Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[6]")
        tr7 = Web_PO.getTextByXs(varPrefix + "/div/div/div[1]/table/tbody/tr[7]")
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
                    Web_PO.clkByX(
                        varPrefix + "/div/div/div[1]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 2)

        # 结束日期
        if v[1] == v[4]:
            varLoc = 1
        else:
            varLoc = 2
        tr2 = Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[2]")
        tr3 = Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[3]")
        tr4 = Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[4]")
        tr5 = Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[5]")
        tr6 = Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[6]")
        tr7 = Web_PO.getTextByXs(varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[7]")
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
                    Web_PO.clkByX(
                        varPrefix + "/div/div/div[" + str(varLoc) + "]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(
                            j + 1) + "]", 1)

    def _clkDropdownByDate(self, k, eleXpath, v):
        # 产品信息管理 - 最后更新时间
        # self._clkDropdownByDate(k, ".//div[2]/div/input[1]", v)

        ele = Web_PO.getSuperEleByX("//div[text()='" + k + "']", "..")
        Web_PO.eleClkByX(ele, eleXpath, 1)

        varPrefix = "//div[@class='el-popper is-pure is-light el-picker__popper' and @aria-hidden='false']"

        # 1 获取日期年和月
        defaultYM = Web_PO.getTextByX(varPrefix + "/div/div/div/div[1]/div/div")
        defaultYear = int(defaultYM.split(" 年 ")[0])
        defaultMonth = int(defaultYM.split(" 年 ")[1].split(" 月")[0])
        # print("defaultYear", defaultYear)
        # print("defaultMonth", defaultMonth)

        # 2 切换年
        if v[0] < defaultYear:
            year = defaultYear - v[0]
            for i in range(year):
                Web_PO.clkByX(varPrefix + "/div/div/div/div[1]/div/button[1]")
        else:
            year = v[0] - defaultYear
            for i in range(year):
                Web_PO.clkByX(varPrefix + "/div/div/div/div[3]/div/button[1]")
        # 切换月
        if v[1] < defaultMonth:
            month = defaultMonth - v[1]
            for i in range(month):
                Web_PO.clkByX(varPrefix + "/div/div/div/div[1]/div/button[2]")
        else:
            month = v[1] - defaultMonth
            for i in range(month):
                Web_PO.clkByX(varPrefix + "/div/div/div/div[2]/div/button[2]")

        # 开始日期
        tr2 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[2]")
        tr3 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[3]")
        tr4 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[4]")
        tr5 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[5]")
        tr6 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[6]")
        tr7 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[1]/table/tbody/tr[7]")
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
                    Web_PO.clkByX(
                        varPrefix + "/div/div/div/div[1]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 2)

        # 结束日期
        if v[1] == v[4]:
            varLoc = 1
        else:
            varLoc = 2
        tr2 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[2]")
        tr3 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[3]")
        tr4 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[4]")
        tr5 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[5]")
        tr6 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[6]")
        tr7 = Web_PO.getTextByXs(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[7]")
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
                    Web_PO.clkByX(varPrefix + "/div/div/div/div[" + str(varLoc) + "]/table/tbody/tr[" + str(
                        i + 2) + "]/td[" + str(j + 1) + "]", 2)

    def _dropdownDateSingle(self, ele, elePath, v):
        # 公共 - 单个日期控件
        # 如：入职日期，离职日期

        Web_PO.eleScrollViewByX(ele, elePath, 2)
        Web_PO.eleClkByX(ele, elePath)
        # print(v)

        varPrefix = "//div[@class='el-popper is-pure is-light el-picker__popper' and @aria-hidden='false']"

        # 1 获取当前年和月
        defaultY = Web_PO.getTextByX(varPrefix + "/div/div[1]/div/div[1]/span[1]")
        defaultM = Web_PO.getTextByX(varPrefix + "/div/div[1]/div/div[1]/span[2]")
        defaultYear = int(defaultY.split(" 年")[0])
        defaultMonth = int(defaultM.split(" 月")[0])
        # print("defaultYear", defaultYear)
        # print("defaultMonth", defaultMonth)

        # 2 切换年
        if v[0] < defaultYear:
            year = defaultYear - v[0]
            for i in range(year):
                # 上年
                Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[1]/button[1]")
        elif defaultYear < v[0]:
            year = v[0] - defaultYear
            for i in range(year):
                # 后年
                Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[1]/button[3]")
        # 切换月
        if v[1] < defaultMonth:
            month = defaultMonth - v[1]
            for i in range(month):
                # 上月
                Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[1]/button[2]")
        elif defaultMonth < v[1]:
            month = v[1] - defaultMonth
            for i in range(month):
                # 后月
                Web_PO.clkByX(varPrefix + "/div/div[1]/div/div[1]/button[4]")

        # 3 遍历日期列表
        tr2 = Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[2]/table/tbody/tr[2]")
        tr3 = Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[2]/table/tbody/tr[3]")
        tr4 = Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[2]/table/tbody/tr[4]")
        tr5 = Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[2]/table/tbody/tr[5]")
        tr6 = Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[2]/table/tbody/tr[6]")
        tr7 = Web_PO.getTextByXs(varPrefix + "/div/div[1]/div/div[2]/table/tbody/tr[7]")
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
                    Web_PO.clkByX(
                        varPrefix + "/div/div[1]/div/div[2]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]",
                        2)

    
    def clsApp(self, varApp):

        '''
        关闭应用程序
        :param varApp:
        :return:
         # clsApp("chrome.exe")
        '''

        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()

    def _sm2(self, Web_PO):

        # Web_PO.openURL("https://config.net.cn/tools/sm2.html")
        Web_PO.opnLabel("https://config.net.cn/tools/sm2.html")
        # 私钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[1]",
                          "124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62")
        # 公钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[2]",
                          '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249')

    def encrypt(self, varSource):

        # 在线sm2加密

        # Web_PO = WebPO("noChrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", varSource)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[1]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", "value")
        return r

    def decrypt(self, varEncrypt):

        # 在线sm2解密

        # Web_PO = WebPO("chrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", varEncrypt)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[2]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", "value")
        Web_PO.cls()
        return r


    def login(self, varUrl, varUser, varPass):
        # 登录
        Web_PO.openURL(varUrl)
        Web_PO.driver.maximize_window()  # 全屏
        Web_PO.setTextByX("//input[@placeholder='请输入用户名']", varUser)
        Web_PO.setTextByX("//input[@placeholder='输入密码']", varPass)
        Web_PO.clkByX("//button[@type='button']", 4)

        # 系统接口404
        l_ = Web_PO.getTextByXs("//div")
        if '系统接口404异常' in l_:
            print('系统接口404异常')
            self.logger.error('系统接口404异常')
            Web_PO.cls()
            sys.exit(0)

    def getDecode(self, varKey, varSm2Data):

        # 在线sm2解密数据
        d = {}
        # Web_PO.openURL("https://the-x.cn/zh-cn/cryptography/Sm2.aspx")
        Web_PO.opnLabel("https://the-x.cn/zh-cn/cryptography/Sm2.aspx")
        Web_PO.swhLabel(1)
        # 解密秘钥：124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
        Web_PO.setTextByX("/html/body/div/form/div[1]/div[1]/div[1]/textarea", "124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62")
        Web_PO.setTextByX("/html/body/div/form/div[1]/div[1]/div[2]/textarea", varSm2Data)
        Web_PO.clkByX("/html/body/div/form/div[2]/div[2]/input[2]", 2)
        s_result = Web_PO.getAttrValueByX("/html/body/div/form/div[3]/textarea", "value")
        d_result = eval(s_result)
        d[varKey] = d_result
        Web_PO.cls()
        Web_PO.swhLabel(0)
        return d

    def getMenu2Url(self):

        # 获取菜单连接

        # 统计ur数量
        c = Web_PO.getCount("ul")
        varLabelCount = c-3

        # 获取二级菜单名
        Web_PO.clsDisplayByTagName("ul", varLabelCount)  # 展开所有二级菜单（去掉display：none）
        l_menu2 = Web_PO.getTextByXs("//ul/div/a/li/span[2]")
        # print(l_menu2)  # ['健康档案概况', '个人健康档案', '家庭健康档案', ...

        # 获取二级菜单链接
        l_menu2Url = Web_PO.getAttrValueByXs("//a", "href")
        # print(l_menu2Url) # ['http://192.168.0.203:30080/#/phs/HealthRecord/ehrindex', 'http://192.168.0.203:30080/#/phs/HealthRecord/Personal', ...

        # 生成字典{菜单：URL}
        d_menuUrl = dict(zip(l_menu2, l_menu2Url))
        # print(d_menuUrl)  # {'健康档案概况': 'http://192.168.0.203:30080/#/phs/HealthRecord/ehrindex',...

        return d_menuUrl

    def menu1(self, varMenu1):

        '''格式化一级菜单'''

        l_menu = Web_PO.getTextByXs("//li")
        # 去掉''
        l_menu = [i for i in l_menu if i != '']  # ['首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单']

        # 序列化成字典
        d_menu = (dict(enumerate(l_menu, start=1)))
        # print(d_menu)  # {1: '首页', 2: '基本公卫', 3: '三高共管六病同防', 4: '系统配置', 5: '社区管理', 6: '报表', 7: '更多菜单'}

        # 序列化反转
        d_menu = {v: k for k, v in d_menu.items()}
        print(d_menu)  # {'首页': 1, '基本公卫': 2, '三高共管六病同防': 3, '系统配置': 4, '社区管理': 5, '报表': 6, '更多菜单': 7}

        if varMenu1 == '更多菜单':
            Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li["+ (str(d_menu[varMenu1]))+ "]")
        else:
            Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li["+ (str(d_menu[varMenu1]))+ "]")
                         # /html/body/div[1]/div/div[1]/div[2]/ul/li[2]
                         # /html/body/div[1]/div/div[2]/div[2]/ul/li[3]
                         # /html/body/div[1]/div/div[2]/div[2]/ul/li[4]
            # /html/body/div[1]/div/div[2]/div[2]/ul/li[3]
            # /html/body/div[1]/div/div[1]/div[2]/ul/li[3]
            # /html/body/div[1]/div/div[2]/div[2]/ul/li[1]
        # return d_menu

    def menu2(self, d_menu1, varMenuName):

        '''格式化二级菜单'''
        # ['健康档案管理', '', '', '', '', '', '儿童健康管理', '', '', '', '', '孕产妇管理', '', '', '', '', '老年人健康管理', '', '', '', '', '', '肺结核患者管理', '', '', '', '', '残疾人健康管理', '', '', '', '', '严重精神障碍健康管理', '', '', '', '', '健康教育', '', '高血压管理', '', '', '', '糖尿病管理', '', '', '', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单', '', '', '', '', '', '', '']

        Web_PO.clkByX('//*[@id="topmenu-container"]/li[' + str(d_menu1[varMenuName]) + ']', 2)

        # 获取二级菜单
        l_menu2 = Web_PO.getTextByXs("//li")

        # 去掉''
        l_menu2 = [i for i in l_menu2 if i != '']
        # print(l_menu2)  # ['健康档案管理', '儿童健康管理', '孕产妇管理', '老年人健康管理', '肺结核患者管理', '残疾人健康管理', '严重精神障碍健康管理', '健康教育', '高血压管理', '糖尿病管理', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单']

        # 序列化成字典
        d_menu2 = (dict(enumerate(l_menu2, start=1)))
        # print(d_menu2)  # {1: '健康档案管理', 2: '儿童健康管理', 3: '孕产妇管理', 4: '老年人健康管理', 5: '肺结核患者管理', 6: '残疾人健康管理', 7: '严重精神障碍健康管理', 8: '健康教育', 9: '高血压管理', 10: '糖尿病管理', 11: '首页', 12: '基本公卫', 13: '三高共管六病同防', 14: '系统配置', 15: '社区管理', 16: '报表', 17: '更多菜单'}

        # 序列化反转
        d_menu2 = {v: k for k, v in d_menu2.items()}
        # print(d_menu2)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理': 9, '糖尿病管理': 10, '首页': 11, '基本公卫': 12, '三高共管六病同防': 13, '系统配置': 14, '社区管理': 15, '报表': 16, '更多菜单': 17}

        return d_menu2

        # return d_menu2[varMenuName]

    def menu3(self, d_menu2, varMenu2Name, varMenu3Name):

        '''格式化三级菜单'''
        # ['健康档案管理', '', '', '', '', '', '儿童健康管理', '', '', '', '', '孕产妇管理', '', '', '', '', '老年人健康管理', '', '', '', '', '', '肺结核患者管理', '', '', '', '', '残疾人健康管理', '', '', '', '', '严重精神障碍健康管理', '', '', '', '', '健康教育', '', '高血压管理\n高血压专项\n高血压随访\n高血压报病', '高血压专项', '高血压随访', '高血压报病', '糖尿病管理', '', '', '', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单', '', '', '', '', '', '', '']
        # 定位 '高血压管理\n高血压专项\n高血压随访\n高血压报病'

        Web_PO.clk('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[' + str(d_menu2[varMenu2Name]) + ']/li', 2)

        # 获取三级菜单
        l_menu3 = Web_PO.getTexts("//li")

        # 去掉''
        l_menu3 = [i for i in l_menu3 if i != '']
        # print(l_menu3)  # ['健康档案管理', '儿童健康管理', '孕产妇管理', '老年人健康管理', '肺结核患者管理', '残疾人健康管理', '严重精神障碍健康管理', '健康教育', '高血压管理\n高血压专项\n高血压随访\n高血压报病', '高血压专项', '高血压随访', '高血压报病', '糖尿病管理', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单']

        # 序列化成字典
        d_menu3 = (dict(enumerate(l_menu3, start=1)))
        # print(d_menu3)  # {1: '健康档案管理', 2: '儿童健康管理', 3: '孕产妇管理', 4: '老年人健康管理', 5: '肺结核患者管理', 6: '残疾人健康管理', 7: '严重精神障碍健康管理', 8: '健康教育', 9: '高血压管理\n高血压专项\n高血压随访\n高血压报病', 10: '高血压专项', 11: '高血压随访', 12: '高血压报病', 13: '糖尿病管理', 14: '首页', 15: '基本公卫', 16: '三高共管六病同防', 17: '系统配置', 18: '社区管理', 19: '报表', 20: '更多菜单'}

        # 序列化反转
        d_menu3 = {v: k for k, v in d_menu3.items()}
        # print(d_menu3)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理\n高血压专项\n高血压随访\n高血压报病': 9, '高血压专项': 10, '高血压随访': 11, '高血压报病': 12, '糖尿病管理': 13, '首页': 14, '基本公卫': 15, '三高共管六病同防': 16, '系统配置': 17, '社区管理': 18, '报表': 19, '更多菜单': 20}

        for k, v in d_menu3.items():
            if varMenu2Name + "\n" in k:
                list1 = k.split("\n")  # ['高血压管理', '高血压专项', '高血压随访', '高血压报病']
                for i in range(len(list1)):
                    if list1[i] == varMenu3Name:
                        Web_PO.clk('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[' + str(d_menu2[varMenu2Name]) + ']/li/ul/div[' + str(i) + ']/a', 2)
                        break
                break

    def newMedicalInstitution(self, hospital, hospitalCode, hospitalReg, hospitalLevel, hospitalPerson, hospitalAddress, hospitalPhone, hospitalIntro):

        # 新增医疗机构
        Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/div[1]/button', 1)
        Web_PO.setText("//input[@placeholder='请输入医院名称']", hospital)
        Web_PO.setText("//input[@placeholder='请输入医院代码']", hospitalCode)
        Web_PO.setText("//input[@placeholder='请输入医院登记号']", hospitalReg)
        Web_PO.jsReadonly("//input[@placeholder='请输入级别']")
        Web_PO.setText("//input[@placeholder='请输入级别']", hospitalLevel)
        Web_PO.setText("//input[@placeholder='请输入医院负责人姓名']", hospitalPerson)
        Web_PO.setText("//input[@placeholder='请输入医院详细地址']", hospitalAddress)
        Web_PO.setText("//input[@placeholder='请输入医院联系电话']", hospitalPhone)
        Web_PO.setText("//textarea[@placeholder='请输入医院介绍']", hospitalIntro)
        Web_PO.clk('/html/body/div[4]/div/div/div[3]/div/button[1]', 1)

    def editMedicalInstitution(self, oldHospital, hospital, hospitalCode, hospitalReg, hospitalLevel, hospitalPerson, hospitalAddress, hospitalPhone, hospitalIntro):

        # 编辑医疗机构
        # 获取列表中指定医院所在的行，点击次行的'编辑'
        varTr = self.getHospitalTR(oldHospital)
        if varTr == None:
            print("warning, 未找到医院名称")
            return None
        Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(varTr) + ']/td[8]/div/button[1]', 1)

        Web_PO.setText("//input[@placeholder='请输入医院名称']", hospital)
        Web_PO.setText("//input[@placeholder='请输入医院代码']", hospitalCode)
        Web_PO.setText("//input[@placeholder='请输入医院登记号']", hospitalReg)
        Web_PO.jsReadonly("//input[@placeholder='请输入级别']")
        Web_PO.setText("//input[@placeholder='请输入级别']", hospitalLevel)
        Web_PO.setText("//input[@placeholder='请输入医院负责人姓名']", hospitalPerson)
        Web_PO.setText("//input[@placeholder='请输入医院详细地址']", hospitalAddress)
        Web_PO.setText("//input[@placeholder='请输入医院联系电话']", hospitalPhone)
        Web_PO.setText("//textarea[@placeholder='请输入医院介绍']", hospitalIntro)
        Web_PO.clk('/html/body/div[4]/div/div/div[3]/div/button[1]', 1)

    def getHospitalTR(self, varHospital):

        '''获取行'''

        l_1 = Web_PO.getTexts("//tr")
        # 序列化成字典
        d_1 = (dict(enumerate(l_1, start=0)))
        # 序列化反转
        d_1 = {v: k for k, v in d_1.items()}
        for k, v in d_1.items():
            if varHospital + "\n" in k:
                return v

    def editOffice(self, hospital, d_officeCode):

        # 科室维护
        # 获取列表中指定医院所在的行，点击次行的'科室维护'

        varTr = self.getHospitalTR(hospital)
        if varTr == None:
            print("warning, 未找到医院名称")
            return None
        Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(varTr) + ']/td[8]/div/button[2]', 1)

        # 获取所有科室
        if Web_PO.isElement("//input"):
            l_office_Code = Web_PO.getValuesByAttr("//input", "value")
            # print(l_office_Code)  # ['骨科', '000', '儿科', '9876']
            d_officeCode_old = List_PO.list2dictBySerial(l_office_Code)
            print(d_officeCode_old)  # {'骨科': '000', '儿科': '9876'}

            # 删除所有科室
            for i in range(len(d_officeCode_old)):
                Web_PO.clk('/html/body/div[5]/div/div/div[2]/form/div[' + str(2) + ']/div[3]/i', 1)

        # 新增科室
        for index, (k, v) in enumerate(d_officeCode.items()):
            Web_PO.clk('/html/body/div[5]/div/div/div[2]/form/div[1]/div[2]/i', 1)
            Web_PO.setText("/html/body/div[5]/div/div/div[2]/form/div[" + str(index+2) + "]/div[1]/div/div/div/input", k)
            Web_PO.setText("/html/body/div[5]/div/div/div[2]/form/div[" + str(index+2) + "]/div[2]/div/div/div/input", v)
        # 保存
        Web_PO.clk('/html/body/div[5]/div/div/div[3]/div/button[1]', 1)

    def _getQty(self):
        # 获取查询结果数量

        if Web_PO.isEleExistByX("//div[@class='el-pagination is-background']/span"):
            if Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":
                return 1
            else:
                s_ = Web_PO.getTextByX("//div[@class='el-pagination is-background']/span")
                s_ = s_.split("共 ")[1].split(" 条")[0]
                return s_
        else:
            return 0



    def _getEleByLabelText(self, k):
        return Web_PO.getSuperEleByX("//label[text()='" + k + "']", "..")

    def _eleLabel(self, ele, k, varLoc=".."):
        return Web_PO.eleGetSuperEleByX(ele, ".//label[text()='" + k + "']", varLoc)

    def _eleDiv(self, ele, k, varLoc=".."):
        return Web_PO.eleGetSuperEleByX(ele, ".//div[text()='" + k + "']", varLoc)

    def _eleSpan(self, ele, k, varLoc=".."):
        return Web_PO.eleGetSuperEleByX(ele, ".//span[text()='" + k + "']", varLoc)

    def _eleTd(self, ele, k, varLoc=".."):
        return Web_PO.eleGetSuperEleByX(ele, ".//td[text()='" + k + "']", varLoc)


    def _jws(self, ele, k, k_sub, v1, _dropdownByX, varLoc):

        if isinstance(v1, list):
            Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/div", "无")
            Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/div", "有")
            for i in range(len(v1) - 1):
                # +
                Web_PO.eleClkByX(self._eleDiv(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/i", 2)
            for i in range(len(v1)):
                # 名称
                Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), "./div[2]/div[" + str(varLoc) + "]/div[2]/div[" + str(i + 1) + "]/div[1]/div[2]/div/div/div/input", v1[i][0])
                # 时间
                self._dropdownDateSingle(self._eleDiv(ele, k), "./div[2]/div[" + str(varLoc) + "]/div[2]/div[" + str(i + 1) + "]/div[2]/div[1]/div/div/div/input", v1[i][1])
        else:
            if v1 != "remain":
                Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/div", "无")

    def _getRadio(self, varField):
        d_ = {}
        ele2 = Web_PO.getSuperEleByX("//div[text()='" + varField + "']", "..")
        l_blood_1 = Web_PO.eleGetTextByXs(ele2, ".//label/span[2]")
        # print(l_blood_1)
        l_blood_tmp = Web_PO.eleGetAttrValueByXs(ele2, ".//label", "class")
        # print(l_blood_tmp)
        l_blood_2 = []
        for i in range(len(l_blood_tmp)):
            if l_blood_tmp[i] == 'el-radio is-disabled is-checked el-radio--default':
                l_blood_2.append(1)
            else:
                l_blood_2.append(0)
        d_blood = dict(zip(l_blood_1, l_blood_2))
        varField = varField.strip()
        d_[varField] = d_blood
        # print(d_)
        return d_

    def _getCheckbox(self, varField):
        d_ = {}
        ele2 = Web_PO.getSuperEleByX("//div[text()='" + varField + "']", "..")
        l_blood_1 = Web_PO.eleGetTextByXs(ele2, ".//label/span[2]")
        # print(l_blood_1)
        l_blood_tmp = Web_PO.eleGetAttrValueByXs(ele2, ".//label", "class")
        # print(l_blood_tmp)
        l_blood_2 = []
        for i in range(len(l_blood_tmp)):
            if l_blood_tmp[i] == 'el-checkbox el-checkbox--default is-disabled is-checked':
                l_blood_2.append(1)
            else:
                l_blood_2.append(0)
        d_blood = dict(zip(l_blood_1, l_blood_2))
        varField = varField.strip()
        d_[varField] = d_blood
        # print(d_)
        return d_

    def _getText(self, varField, varLoc=".."):
        d_ = {}
        ele = Web_PO.getSuperEleByX("//div[text()='" + varField + "']", varLoc)
        l_ = Web_PO.eleGetShadowByXsByC(ele, ".//div/div/div/input", 'div:nth-last-of-type(1)')
        varField = varField.strip()
        d_[varField] = l_
        # print(d_)
        return d_

    def _getTextarea(self, varField):
        d_ = {}
        ele = Web_PO.getSuperEleByX("//div[text()='" + varField + "']", "../..")
        l_ = Web_PO.eleGetShadowByXsByC(ele, ".//div/div/div/textarea", 'div:nth-last-of-type(1)')
        varField = varField.strip()
        d_[varField] = l_
        # print(d_)
        return d_

    def _getJWS(self, varField, varQty, l_):
        l_4 = []
        d_2 = {}
        for _ in range(varQty*2):
            l_4.append(l_.pop(0))
        d_2[varField] = l_4
        return d_2


    def __eleRadioLeftLabel(self, ele, varXpaths, v):
        # eleRadioLabels
        # 选择单选框
        # 内部调用，用于随访
        l_ = Web_PO.eleGetTextByXs(ele, varXpaths)
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
        Web_PO.eleClkByX(ele, varXpaths + "[" + str(d_4[v]) + "]/label", 1)
    def __eleRadioRightLabel(self, ele, varXpaths, v):
        # eleRadioLabels
        # 选择单选框
        # 内部调用，用于随访
        l_ = Web_PO.eleGetTextByXs(ele, varXpaths)
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
        Web_PO.eleClkByX(ele, varXpaths + "[" + str(d_4[v]) + "]", 1)


    # todo 2.1.2 基本公卫 - 健康档案管理 - 个人健康档案

    def phs_healthrecord_personal_query(self, d_):

        # 个人健康档案 - 查询

        # 1 查询
        ele = Web_PO.getSuperEleByX("//span[text()='展开']", "../../..")  # form
        Web_PO.eleClkByX(ele, "./div/div", 1)  # 展开
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '建档人', '本人电话']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[1]/div/div/input", v[0])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[2]/div/div/input", v[1])
                elif k in ['性别', '人群分类', '档案是否开放', '档案状态', '血型', '常住类型', '是否签约', '是否残疾', '今年是否体检', '既往史', '今年是否已更新', '医疗费用支付方式', '档案缺失项目']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期范围', '今年体检日期', '今年更新日期', '建档日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX, v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div[1]/div[2]/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div/div/div[2]/div/input", v[2])
                elif k in ['管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k),  ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li["+str(i+1)+"]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i+1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_healthrecord_personal_operation(self, varOperation):

        # 个人健康档案 - 操作

        # 获取查询数量
        s_ = self._getQty()
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        try:
            # 操作
            # 点击姓名等同于更新
            if s_ == 1 and varOperation == '姓名':
                Web_PO.clkByX("//tr[@class='el-table__row']/td[2]/div", 2)
            elif s_ == 1 and varOperation == '查看':
                Web_PO.eleClkByX(ele2, ".//tr/td[16]/div/div[1]", 2)
            elif s_ == 1 and varOperation == '更新':
                Web_PO.eleClkByX(ele2, ".//tr/td[16]/div/div[2]", 2)
            elif s_ == 1 and varOperation[0] == '终结':
                Web_PO.eleClkByX(ele2, ".//tr/td[16]/div/div[3]", 2)  # 更多
                Web_PO.clkByX("//div[@class='el-popper is-light el-popover' and @aria-hidden='false']/div[1]", 2)  # 终结
                ele2 = Web_PO.getSuperEleByX("//span[text()='终结健康档案']", "../..")
                # 判断档案状态
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                for k,v in varOperation[1].items():
                    Web_PO.eleRadioSplitLabels(self._eleLabel(ele2, '档案状态'), "./div/div", k)
                    if k == '暂不管理':
                        self._eleClkDropdown(self._eleLabel(ele2, '暂不管理原因'), ".//div/div/div/div/input", _dropdownByX, v['暂不管理原因'])
                        self._dropdownDateSingle(self._eleLabel(ele2, '暂不管理日期'), "./div/div/input", v['暂不管理日期'])
                    elif k == '已死亡':
                        self._dropdownDateSingle(self._eleLabel(ele2, '档案注销日期'), "./div/div/input", v['档案注销日期'])
                        self._dropdownDateSingle(self._eleLabel(ele2, '死亡日期'), "./div/div/input", v['死亡日期'])
                # Web_PO.eleClkByX(ele2, ".//button[1]")  # 确认
                # Web_PO.eleClkByX(ele2, ".//div[3]/span/button[1]")  # 确认
            elif s_ == 1 and varOperation == '更新历史':
                Web_PO.eleClkByX(ele2, ".//tr/td[16]/div/div[3]", 2)  # 更多
                # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[16]/div/div[3]", 2)  # 更多
                Web_PO.clkByX("//div[@class='el-popper is-light el-popover' and @aria-hidden='false']/div[2]", 2)  # 更新历史
                ele2 = Web_PO.getSuperEleByX("//span[text()='更新历史']", "../..")
                l_ = Web_PO.eleGetTextByXs(ele2, ".//div[2]")
                print(l_[0])
                Web_PO.eleClkByX(ele2, ".//button")  # 关闭
                # Web_PO.eleClkByX(ele2, "./div[3]/span/button")  # 关闭
            else:
                print("查询数量多余1个，无法操作")
            self.logger.info("点击" + varOperation)
        except:
            self.logger.error(varOperation + "失败！")

    def phs_healthrecord_personal_detail(self):

        # 个人健康档案 - 详情

        print("处理中...")
        try:
            d_ = self._getText(' 身份证号码 ')
            d_.update(self._getText(' 档案编号 '))
            d_.update(self._getText(' 姓名 '))
            d_.update(self._getText(' 性别 '))
            d_.update(self._getText(' 出生日期 '))
            d_.update(self._getText(' 民族 '))
            d_.update(self._getText(' 现住址 ', "../.."))
            d_.update(self._getText(' 本人电话 '))
            d_.update(self._getText(' 联系人姓名 '))
            d_.update(self._getText(' 联系人电话 '))
            d_.update(self._getRadio(' 常住类型 '))
            d_.update(self._getText(' 文化程度 '))
            d_.update(self._getText(' 职业 '))
            d_.update(self._getText(' 工作单位 '))
            d_.update(self._getText(' 婚姻状况 '))
            d_.update(self._getRadio(' 血型 '))
            d_.update(self._getRadio(' RH血型 '))

            d_1 = self._getCheckbox(' 医疗费用支付方式 ')
            if d_1['医疗费用支付方式']['城镇职工基本医疗保险'] == 1:
                d_2 = self._getText(' 医疗费用支付方式 ')
                d_1['医疗费用支付方式']['城镇职工基本医疗保险'] = {1: d_2['医疗费用支付方式'][0]}
                d_.update(d_1)
            if d_1['医疗费用支付方式']['城镇居民基本医疗保险'] == 1:
                d_2 = self._getText(' 医疗费用支付方式 ')
                d_1['医疗费用支付方式']['城镇居民基本医疗保险'] = {1: d_2['医疗费用支付方式'][1]}
                d_.update(d_1)
            if d_1['医疗费用支付方式']['贫困救助'] == 1:
                d_2 = self._getText(' 医疗费用支付方式 ')
                d_1['医疗费用支付方式']['贫困救助'] = {1: d_2['医疗费用支付方式'][2]}
                d_.update(d_1)
            elif d_1['医疗费用支付方式']['贫困救助'] == 0:
                d_2 = self._getText(' 医疗费用支付方式 ')
                d_1['医疗费用支付方式']['贫困救助'] = {0: d_2['医疗费用支付方式'][2]}
                d_.update(d_1)
            if d_1['医疗费用支付方式']['其他'] == 1:
                d_2 = self._getText(' 医疗费用支付方式 ')
                d_1['医疗费用支付方式']['input'] = d_2['医疗费用支付方式'][3]
                d_.update(d_1)

            d_1 = self._getCheckbox(' 药物过敏史 ')
            if d_1['药物过敏史']['其他药物过敏源'] == 1:
                d_2 = self._getTextarea(' 药物过敏史 ')
                d_1['药物过敏史']['input'] = d_2['药物过敏史'][0]
            d_.update(d_1)

            d_.update(self._getCheckbox(' 暴露史 '))

            ele = Web_PO.getSuperEleByX("//div[text()=' 既往史 ']", "..")
            l_ = Web_PO.eleGetTextByXs(ele, ".//div")
            a = (l_[1].count("疾病名称"))
            b = (l_[1].count("手术名称"))
            c = (l_[1].count("外伤名称"))
            d = (l_[1].count("输血原因"))
            l_ = Web_PO.eleGetShadowByXsByC(ele, ".//div/div/div/input", 'div:nth-last-of-type(1)')
            d_1 = self._getJWS("疾病", a, l_)
            d_2 = self._getJWS("手术", b, l_)
            d_1.update(d_2)
            d_3 = self._getJWS("外伤", c, l_)
            d_1.update(d_3)
            d_4 = self._getJWS("输血", d, l_)
            d_1.update(d_4)
            d_5 = {}
            varField = ' 既往史 '.strip()
            d_5[varField] = d_1
            d_.update(d_5)

            d_1 = self._getRadio(' 家族史 ')
            # print('家族史', d_1)
            if d_1['家族史'] != {}:
                d_2 = self._getText(' 家族史 ')
                d_1['家族史']['input'] = d_2['家族史']
            else:
                d_1['家族史'] = '无'
            d_.update(d_1)

            d_1 = self._getRadio(' 遗传病史 ')
            # print('遗传病史', d_1)
            if d_1['遗传病史'] != {}:
                d_2 = self._getText(' 遗传病史 ', "../..")
                d_1['遗传病史']['疾病名称'] = d_2['遗传病史'][0]
            else:
                d_1['遗传病史'] = '无'
            d_.update(d_1)

            d_1 = self._getCheckbox(' 残疾情况 ')
            d_2 = self._getText(' 残疾情况 ')
            # print("d_1", d_1)
            # print("d_2", d_2)
            if d_2['残疾情况'] != []:
                d_1['残疾情况']['input'] = d_2['残疾情况'][0]
            d_.update(d_1)

            d_.update(self._getText(' 残疾证号 '))

            d_1 = self._getText(' 与户主关系 ')
            d_1.update(self._getText(' 户主姓名 '))
            d_1.update(self._getText(' 户主身份证号 '))
            d_1.update(self._getText(' 家庭人口数 '))
            d_1.update(self._getText(' 家庭结构 '))
            d_1.update(self._getRadio(' 居住情况 '))
            d_.update({'家庭情况': d_1})

            d_1 = self._getRadio(' 厨房排风设施 ')
            d_1.update(self._getRadio(' 燃料类型 '))
            d_1.update(self._getRadio(' 饮水 '))
            d_1.update(self._getRadio(' 厕所 '))
            d_1.update(self._getRadio(' 禽畜栏 '))
            d_.update({'生活环境': d_1})

            d_.update(self._getText(' 建档单位 '))
            d_.update(self._getText(' 管理机构 '))
            d_.update(self._getText(' 档案是否开放 '))
            d_.update(self._getText(' 建档日期 '))
            d_.update(self._getText(' 建档人 '))

            Web_PO.cls()
            self.logger.info("查看 => " + str(d_))
            return d_
        except:
            self.logger.error("查看失败")

    def phs_healthrecord_personal_modify(self, d_):

        # 个人健康档案 - 更新

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        print("更新中...")

        ele = Web_PO.getSuperEleByX("//div[text()='居民健康档案']", "../../..")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in [' 性别 ', ' 民族 ', ' 文化程度 ', ' 职业 ', ' 婚姻状况 ', ' 与户主关系 ', ' 档案是否开放 ']:
                    self._eleClkDropdown(self._eleDiv(ele, k), ".//div[2]/div/div/div/div/div/input", _dropdownByX, v)

                elif k in [' 现住址 ']:
                    self._eleClkDropdown(self._eleDiv(ele, k, "../.."), ".//div[1]/div[2]/div/div/div/div/div/input", _dropdownByX, v[0])
                    self._eleClkDropdown(self._eleDiv(ele, k, "../.."), ".//div[2]/div[1]/div/div/div/div/div/input", _dropdownByX, v[1])
                    self._eleClkDropdown(self._eleDiv(ele, k, "../.."), ".//div[2]/div[2]/div/div/div/div/div/input", _dropdownByX, v[2])
                    self._eleClkDropdown(self._eleDiv(ele, k, "../.."), ".//div[3]/div[1]/div/div/div/div/div/input", _dropdownByX, v[3])
                    self._eleClkDropdown(self._eleDiv(ele, k, "../.."), ".//div[3]/div[2]/div/div/div/div/div/input", _dropdownByX, v[4])
                    Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k, "../.."), ".//div[4]/div[2]/div/div/div/input", v[5])

                elif k in [' 残疾情况 ']:
                    # 先判断是否勾选了无，如果勾选，则取消，取消后才能输入残疾证号
                    varDiv1class = Web_PO.eleGetAttrValueByX(self._eleDiv(ele, k), ".//div[2]/div/div/div/div/div[1]/label", "class")
                    if varDiv1class == 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(self._eleDiv(ele, k), ".//div[2]/div/div/div/div/div[1]/label/span[1]")
                    Web_PO.eleCheckboxDivs(self._eleDiv(ele, k), ".//div[2]/div/div/div/div[1]/div", v)
                    for i in range(len(v)):
                        if isinstance(v[i], list):
                            # Web_PO.eleScrollViewByX(ele, ".//div[1]/div[2]/div/div/div/div[2]/div/div/input")
                            Web_PO.eleSetTextByX(self._eleDiv(ele, k), ".//div[2]/div/div/div/div[2]/div/div/input", v[i][1])

                elif k in [' 姓名 ', ' 本人电话 ', ' 联系人姓名 ', ' 联系人电话 ', ' 工作单位 ', ' 残疾证号 ', ' 户主姓名 ', ' 户主身份证号 ', ' 家庭人口数 ', ' 家庭结构 ']:
                    Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//div[2]/div/div/div/input", v)

                elif k in [' 出生日期 ', ' 建档日期 ']:
                    self._dropdownDateSingle(self._eleDiv(ele, k), ".//div[2]/div/div/div/input", v)

                elif k in [' 居住情况 ', ' 血型 ', ' 常住类型 ', ' 血型 ', ' RH血型 ', ' 厨房排风设施 ', ' 燃料类型 ', ' 饮水 ', ' 厕所 ', ' 禽畜栏 ', ' 更新方式 ']:
                    Web_PO.eleRadioLeftLabel(self._eleDiv(ele, k), ".//div[2]/div/div/div", v)

                elif k in [' 医疗费用支付方式 ']:
                    self._eleCheckboxPay(self._eleDiv(ele, k), v)

                elif k in [' 药物过敏史 ']:
                    # 先判断是否勾选了无，如果勾选，则取消
                    varDiv1class = Web_PO.eleGetAttrValueByX(self._eleDiv(ele, k), ".//div[2]/div/div/div/div[1]/label", "class")
                    if varDiv1class == 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(self._eleDiv(ele, k), ".//div[2]/div/div/div/div[1]/label/span[1]")
                    Web_PO.eleCheckboxDivs(self._eleDiv(ele, k, "../.."), "./div[1]/div[2]/div/div/div/div", v)
                    for i in range(len(v)):
                        if isinstance(v[i], list):
                            Web_PO.eleSetTextByX(self._eleDiv(ele, k, "../.."), "./div[2]/div/div/div/div/textarea", v[i][1])

                elif k in [' 暴露史 ']:
                    # 先判断是否勾选了无，如果勾选，则取消
                    varDiv1class = Web_PO.eleGetAttrValueByX(self._eleDiv(ele, k), ".//div[2]/div/div/div/div[1]/label", "class")
                    if varDiv1class == 'el-checkbox el-checkbox--default is-checked':
                        Web_PO.eleClkByX(self._eleDiv(ele, k), ".//div[2]/div/div/div/div[1]/label/span[1]")
                    Web_PO.eleCheckboxDivs(self._eleDiv(ele, k), "./div[2]/div/div/div/div", v, default='clear')

                elif k in [' 既往史 ']:
                    for k1, v1 in v.items():
                        if k1 == '疾病':
                            if isinstance(v1, list):
                                Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[1]/div[1]/div[2]/div/div/div", "无")
                                Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[1]/div[1]/div[2]/div/div/div", "有")
                                for i in range(len(v1) - 1):
                                    Web_PO.eleClkByX(self._eleDiv(ele, k), ".//div[2]/div[1]/div[1]/div[2]/div/div/i", 2)  # +
                                for i in range(len(v1)):
                                    # 疾病名称
                                    self._eleClkDropdown(self._eleDiv(ele, k), ".//div[2]/div[1]/div[2]/div[" + str(i+1) + "]/div[1]/div[2]/div/div/div/div/div/input", _dropdownByX, v1[i][0])
                                    # 确诊时间
                                    self._dropdownDateSingle(self._eleDiv(ele, k), ".//div[2]/div[1]/div[2]/div[" + str(i+1) + "]/div[2]/div[1]/div/div/div/input", v1[i][1])
                            else:
                                if v1 != "remain":
                                    Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[1]/div[1]/div[2]/div/div/div", "无")
                        if k1 == '手术':
                            if isinstance(v1, list):
                                # self._jws(ele, k, v1, _dropdownByX, 2)
                                self._jws(ele, k, "手术", v1, _dropdownByX, 2)
                            else:
                                if v1 != "remain":
                                    Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[2]/div[1]/div[2]/div/div/div", "无")
                        if k1 == '外伤':
                            if isinstance(v1, list):
                                # self._jws(ele, k, v1, _dropdownByX, 3)
                                self._jws(ele, k, "外伤", v1, _dropdownByX, 3)
                            else:
                                if v1 != "remain":
                                    # /html/body/div[1]/div/div[3]div[2]/div[12]/div[2]/div[3]/div[1]/div[2]/div/div/div/label[2]
                                    Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[3]/div[1]/div[2]/div/div/div", "无")
                        if k1 == '输血':
                            if isinstance(v1, list):
                                self._jws(ele, k, "输血", v1, _dropdownByX, 4)
                                # self._jws(ele, k, v1, _dropdownByX, 4)
                            else:
                                if v1 != "remain":
                                    # /html/body/div[1]/div/div[3]/section/div/f div[2]/div[4]/div[1]/div[2]/div/div/div/label[2]
                                    Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[4]/div[1]/div[2]/div/div/div", "无")

                elif k in [' 家族史 ']:
                    if v == '无':
                        Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[1]/div/div/div/div", "无")
                    elif isinstance(v, list):
                        Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[1]/div/div/div/div", "有")
                        for i in range(len(v)-1):
                            Web_PO.eleClkByX(self._eleDiv(ele, k), ".//div[2]/div[1]/div/div/div/i", 2)  # +
                        for i in range(len(v)):
                            # 疾病名称
                            self._eleClkDropdown(self._eleDiv(ele, k), ".//div[2]/div[2]/div/div[" + str(i+1) + "]/div[1]/div[2]/div/div/div/div/div/input", _dropdownByX, v[i][0])
                            # 与本人关系
                            self._eleClkDropdown(self._eleDiv(ele, k), ".//div[2]/div[2]/div/div[" + str(i+1) + "]/div[2]/div[2]/div/div/div/div/div/input", _dropdownByX, v[i][1])

                elif k in [' 遗传病史 ']:
                    if v == '无':
                        Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k, "../.."), ".//div[1]/div[2]/div/div", "无")
                    if isinstance(v, list):
                        Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k, "../.."), ".//div[1]/div[2]/div/div", v[0])
                        Web_PO.eleSetTextByX(self._eleDiv(ele, k, "../.."), ".//div[2]/div[2]/div/div/div/input", v[1])

                elif k in [' 管理机构 ']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleDiv(ele, k),  ".//div[2]/div/div/div/div/input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # print(l_1) # ['招远市卫健局', '金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                    # 招远市卫健局
                    if l_1[0] == v[0].strip():
                        Web_PO.clkByX(_dropdownByX2 + "/div/div[1]/div[1]/ul/li/label")
                    elif v[0].strip() in l_1 and len(v) == 1:
                        # 卫生院
                        for i in range(len(l_1)):
                            if v[0].strip() == l_1[i]:
                                Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i) + "]/label")
                    elif v[0].strip() in l_1 and len(v) == 2:
                        # 卫生室,(先点卫生院再点卫生室)
                        for i in range(len(l_1)):
                            if v[0].strip() == l_1[i]:
                                Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i) + "]/label")
                                break
                        # 卫生室
                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                        # print(l_3)  # ['金岭镇原疃村卫生室', '金岭镇黄泥沟村卫生室', '金岭镇原疃郭家村卫生室'
                        if v[1].strip() in l_3:
                            for i in range(len(l_3)):
                                if v[1].strip() == l_3[i]:
                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(i) + "]/label")

                elif k in [' 更新内容 ']:
                    Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k, "../.."), ".//div[2]/div/div/div/input", v)
            except:
                self.logger.error("更新失败 => " + str(k) + ": " + str(v))

        # 2 保存
        # Web_PO.eleClkByX(ele, ".//button[1]", 2)
        self.logger.info("更新 => " + str(d_))

    def phs_healthrecord_personal_info(self):
        # 点击姓名，获取居民健康档案
        # Web_PO.opnLabel(varUrl)
        # Web_PO.swhLabel(2)

        d_ = self._getText(' 身份证号码 ')
        d_.update(self._getText(' 档案编号 '))
        d_.update(self._getText(' 姓名 '))
        d_.update(self._getText(' 性别 '))
        d_.update(self._getText(' 出生日期 '))
        d_.update(self._getText(' 民族 '))
        d_.update(self._getText(' 现住址 ', "../.."))
        d_.update(self._getText(' 本人电话 '))
        d_.update(self._getText(' 联系人姓名 '))
        d_.update(self._getText(' 联系人电话 '))
        d_.update(self._getRadio(' 常住类型 '))
        d_.update(self._getText(' 文化程度 '))
        d_.update(self._getText(' 职业 '))
        d_.update(self._getText(' 工作单位 '))
        d_.update(self._getText(' 婚姻状况 '))
        d_.update(self._getRadio(' 血型 '))
        d_.update(self._getRadio(' RH血型 '))

        d_1 = self._getCheckbox(' 医疗费用支付方式 ')
        if d_1['医疗费用支付方式']['城镇职工基本医疗保险'] == 1:
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['城镇职工基本医疗保险'] = {1: d_2['医疗费用支付方式'][0]}
            d_.update(d_1)
        if d_1['医疗费用支付方式']['城镇居民基本医疗保险'] == 1:
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['城镇居民基本医疗保险'] = {1: d_2['医疗费用支付方式'][1]}
            d_.update(d_1)
        if d_1['医疗费用支付方式']['贫困救助'] == 1:
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['贫困救助'] = {1: d_2['医疗费用支付方式'][2]}
            d_.update(d_1)
        elif d_1['医疗费用支付方式']['贫困救助'] == 0:
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['贫困救助'] = {0: d_2['医疗费用支付方式'][2]}
            d_.update(d_1)
        if d_1['医疗费用支付方式']['其他'] == 1:
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['input'] = d_2['医疗费用支付方式'][3]
            d_.update(d_1)

        d_1 = self._getCheckbox(' 药物过敏史 ')
        if d_1['药物过敏史']['其他药物过敏源'] == 1:
            d_2 = self._getTextarea(' 药物过敏史 ')
            d_1['药物过敏史']['input'] = d_2['药物过敏史'][0]
            d_.update(d_1)

        d_.update(self._getCheckbox(' 暴露史 '))

        ele = Web_PO.getSuperEleByX("//div[text()=' 既往史 ']", "..")
        l_ = Web_PO.eleGetTextByXs(ele, ".//div")
        a = (l_[1].count("疾病名称"))
        b = (l_[1].count("手术名称"))
        c = (l_[1].count("外伤名称"))
        d = (l_[1].count("输血原因"))
        l_ = Web_PO.eleGetShadowByXsByC(ele, ".//div/div/div/input", 'div:nth-last-of-type(1)')
        d_1 = self._getJWS("疾病", a, l_)
        d_2 = self._getJWS("手术", b, l_)
        d_1.update(d_2)
        d_3 = self._getJWS("外伤", c, l_)
        d_1.update(d_3)
        d_4 = self._getJWS("输血", d, l_)
        d_1.update(d_4)
        d_5 = {}
        varField = ' 既往史 '.strip()
        d_5[varField] = d_1
        d_.update(d_5)

        d_1 = self._getRadio(' 家族史 ')
        if d_1['家族史']['有'] == 1:
            d_2 = self._getText(' 家族史 ')
            d_1['家族史']['input'] = d_2['家族史']
        d_.update(d_1)

        d_1 = self._getRadio(' 遗传病史 ')
        d_2 = self._getText(' 遗传病史 ', "../..")
        d_1['遗传病史']['疾病名称'] = d_2['遗传病史'][0]
        d_.update(d_1)

        d_1 = self._getCheckbox(' 残疾情况 ')
        d_2 = self._getText(' 残疾情况 ')
        d_1['残疾情况']['input'] = d_2['残疾情况'][0]
        d_.update(d_1)

        d_.update(self._getText(' 残疾证号 '))

        d_1 = self._getText(' 与户主关系 ')
        d_1.update(self._getText(' 户主姓名 '))
        d_1.update(self._getText(' 户主身份证号 '))
        d_1.update(self._getText(' 家庭人口数 '))
        d_1.update(self._getText(' 家庭结构 '))
        d_1.update(self._getRadio(' 居住情况 '))
        d_.update({'家庭情况': d_1})

        d_1 = self._getRadio(' 厨房排风设施 ')
        d_1.update(self._getRadio(' 燃料类型 '))
        d_1.update(self._getRadio(' 饮水 '))
        d_1.update(self._getRadio(' 厕所 '))
        d_1.update(self._getRadio(' 禽畜栏 '))
        d_.update({'生活环境': d_1})

        d_.update(self._getText(' 建档单位 '))
        d_.update(self._getText(' 管理机构 '))
        d_.update(self._getText(' 档案是否开放 '))
        d_.update(self._getText(' 建档日期 '))
        d_.update(self._getText(' 建档人 '))
        d_.update(self._getText(' 更新日期 '))
        d_.update(self._getRadio(' 更新方式 '))
        d_.update(self._getText(' 更新人 '))
        d_.update(self._getText(' 更新内容 ', "../.."))

        Web_PO.cls()
        # print(d_)
        return d_



    # todo 2.1.3 基本公卫 - 健康档案管理 - 家庭健康档案

    def phs_healthrecord_family_query(self, d_):

        # 家庭健康档案 - 查询

        # 1 查询
        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '现住址']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['家庭住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div/div/div[1]/div/div/div/div/input", _dropdownByX, v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div/div/div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div/div/div[3]/div/div/div/div/input", _dropdownByX, v[2])
                elif k in ['管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k),  ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li["+str(i+1)+"]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i+1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_healthrecord_family_operation(self, varOperation):

        # 家庭健康档案 - 操作

        # 获取查询数量
        s_ = self._getQty()
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        try:
            # 操作
            # 点击姓名等同于更新
            if s_ == 1 and varOperation == '姓名':
                Web_PO.clkByX("//tr[@class='el-table__row']/td[1]/div", 2)
            elif s_ == 1 and varOperation == '查看':
                Web_PO.clkByX("//tr[@class='el-table__row']", 2)
                Web_PO.eleClkByX(ele2, ".//tr/td[16]/div/div[1]", 2)
            elif s_ == 1 and varOperation == '维护家庭成员':
                Web_PO.clkByX("//tr[@class='el-table__row']", 2)
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[2]/div/div/div[2]/div[1]/span[2]/button', 2)  # 点击 +维护家庭成员

            else:
                print("查询数量多余1个，无法操作")
            self.logger.info("点击" + varOperation)
        except:
            self.logger.error(varOperation + "失败！")

    def phs_healthrecord_family_modify(self, l_):

        # 维护家庭成员 - 更新

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele = Web_PO.getSuperEleByX("(//span[text()='维护家庭成员'])[last()]", "../..")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for d_ in l_:
            name = Web_PO.eleGetTextByX(ele, "./div[2]/div/form/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[1]/div")

            if name == d_['姓名']:
                # /html/body/div[1]/div/div[3]/section/div/div/div[2]/div/div/div[2]/div[3]/div/div/div[2]/div/form/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[1]/div
                Web_PO.eleSetTextEnterByX(ele, "./div[2]/div/form/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div/div/input", d_['户主姓名'])
                Web_PO.eleSetTextEnterByX(ele, "./div[2]/div/form/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[3]/div/div/input", d_['户主身份证号'])
                self._eleClkDropdown(ele, "./div[2]/div/form/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[4]/div/div/div/div/div/input", _dropdownByX, d_['与户主关系'])
        # Web_PO.eleClkByX(ele, ".//button[1]", 2) # 保存
        # Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 取消

        self.logger.info("更新 => " + str(l_))

    def phs_healthrecord_family_export(self, varFile):

        # 家庭健康档案 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击导出
        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)




    # todo 2.1.4 基本公卫 - 健康档案管理 - 迁入申请

    def phs_healthrecord_immigration_query(self, d_):

        # 迁入申请 - 查询

        # 1 查询
        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '申请人']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['状态']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['申请日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/div/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[3]/div/input", v[1])
                elif k in ['申请机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k),  ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li["+str(i+1)+"]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i+1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_healthrecord_immigration_operation(self, varOperation):

        # 迁入申请 - 操作

        # 获取查询数量
        s_ = self._getQty()
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        try:
            # 操作
            if s_ == 1 and varOperation == '查看':
                Web_PO.eleClkByX(ele2, ".//button[1]", 2)
            elif s_ == 1 and varOperation == '撤回':
                Web_PO.eleClkByX(ele2, ".//button[2]", 2)
                Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 取消
                # Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 确认
            else:
                print("查询数量多余1个，无法操作")
            self.logger.info("点击" + varOperation)
        except:
            self.logger.error(varOperation + "失败！")

    def phs_healthrecord_immigration_detail(self):

        # 迁入申请 - 查看

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        d_1 = {}
        # 申请信息
        ele = Web_PO.getSuperEleByX("//div[text()='申请信息']", "../..")
        l_1 = Web_PO.eleGetTextByXs(ele, ".//div")
        l_2 = l_1[0].split("\n")
        l_2.pop(0) # 去掉申请信息
        # print(l_2)  # ['姓名', '六四', '性别', '女', '身份证号', '
        l_application = List_PO.pair2dict(l_2)
        # print(l_application)  # {'姓名': '六四', '性别': '女',
        d_1['申请信息'] = l_application

        # 审批信息
        ele2 = Web_PO.getSuperEleByX("//div[text()='审批信息']")
        l_3 = Web_PO.eleGetTextByXs(ele2, ".//span")
        l_4 = l_3.pop(0)
        # print(l_4)
        d_1['审批结果'] = l_4

        l_approval = List_PO.pair2dict(l_3)
        # print(l_approval)  # {'审核日期': '2024-11-29', '审核人': '1'}
        d_1['审批信息'] = l_approval

        # 关闭
        ele3 = Web_PO.getSuperEleByX("//span[text()='档案迁移信息']", "../..")
        Web_PO.eleClkByX(ele3, ".//button")

        return d_1

    def phs_healthrecord_immigration_new(self, d_):

        # 迁入申请 - 新增

        # 1 新增
        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击新增

        ele = Web_PO.getSuperEleByX("//span[text()='新增档案迁入']", "../..")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        varSign = 0
        for k, v in d_.items():
            try:
                if k in ['身份证号']:
                    Web_PO.eleSetTextEnterByX(self._eleSpan(ele, k, "../.."), ".//input", v)
                    Web_PO.eleClkByX(self._eleSpan(ele, k, "../.."), ".//button", 2)
                    varSign = 1
                if k in ['勾选'] and varSign == 1:
                    if isinstance(v, str) and v == '所有人':
                        # 勾选所有人
                        Web_PO.eleClkByX(ele, ".//table/tbody/tr/td[1]/div/label")
                    elif isinstance(v, list):
                        # 勾选人
                        for i in range(len(v)):
                            if Web_PO.eleGetTextByX(ele, ".//table/tbody/tr[" + str(i+1) + "]/td[2]/div") == v[i]:
                                Web_PO.eleClkByX(ele, ".//table/tbody/tr[" + str(i+1) + "]/td[1]/div/label")
                if k in ['申请迁入原因']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['迁入地址']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//div[1]/div[1]/div/div/div/div/input", _dropdownByX, v[0])
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//div[1]/div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//div[1]/div[3]/div/div/div/div/input", _dropdownByX, v[2])
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//div[2]/div[1]/div/div/div/div/input", _dropdownByX, v[3])
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//div[2]/div[2]/div/div/div/div/input", _dropdownByX, v[4])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[2]/div[3]/div/div/input", v[5])
            except:
                self.logger.error("新增失败 => " + str(k) + ": " + str(v))

        # Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 申请键入
        # Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 取消
        self.logger.info("新增 => " + str(d_))



    # todo 2.1.5 基本公卫 - 健康档案管理 - 迁出审核

    def phs_healthrecord_exit_query(self, d_):

        # 迁出审核 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '申请人']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['状态']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['申请日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/div/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[3]/div/input", v[1])
                elif k in ['管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k),  ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li["+str(i+1)+"]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i+1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_healthrecord_exit_operation(self, varOperation):

        # 迁出审核 - 操作

        # 获取查询数量
        s_ = self._getQty()
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        try:
            # 操作
            if s_ == 1 and varOperation == '同意':
                Web_PO.eleClkByX(ele2, ".//button[1]", 2)
                ele3 = Web_PO.getSuperEleByX("//div[text()=' 同意迁出该居民个人健康档案？ ']", "../..")
                # Web_PO.eleClkByX(ele3, ".//button[1]")  # 确认
                Web_PO.eleClkByX(ele3, ".//button[2]")  # 取消
                self.logger.info("点击" + varOperation)
            elif s_ == 1 and varOperation == '拒绝':
                Web_PO.eleClkByX(ele2, ".//button[2]", 2)
                ele3 = Web_PO.getSuperEleByX("//div[text()='拒绝迁出原因']")
                Web_PO.setTextByX(ele3, ".//textarea", "test222")
                ele4 = Web_PO.getSuperEleByX("//span[text()='档案迁移信息']", "../..")
                # Web_PO.eleClkByX(ele4, ".//button[1]") # 确认
                Web_PO.eleClkByX(ele4, ".//button[2]") # 取消
                self.logger.info("点击" + varOperation)
            else:
                print("查询数量不等于1，无法操作")
                self.logger.error("查询数量不等于1，无法操作")
        except:
            self.logger.error(varOperation + "失败！")



    # todo 2.1.7 基本公卫 - 健康档案管理 - 死亡管理

    def phs_healthrecord_deathmanagement_query(self, d_):

        # 死亡管理 - 查询

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['死亡日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div/div/div[3]/div/input", v[1])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div/div/div[1]/div/input", v[0])
                elif k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div/div/div[1]/div[1]/div/div/input", _dropdownByX, v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div/div/div[1]/div[2]/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[2]/div/input", v[2])
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_healthrecord_deathmanagement_export(self, varFile):

        # 死亡管理 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击导出
        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)



    # todo 2.1.8 基本公卫 - 健康档案管理 - 区域档案查询

    def phs_healthrecord_regionalfile_query(self, d_):

        # 死亡管理 - 查询

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['身份证号']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))



    # todo 2.1.9 基本公卫 - 健康档案管理 - 接诊信息查询

    def phs_healthrecord_diagnosis_query(self, d_):

        # 接诊信息查询 - 查询

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['就诊日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div/div/div[3]/div/input", v[1])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div/div/div[1]/div/input", v[0])
                elif k in ['导入状态']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k), ".//div/div/div/input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(
                                            i + 1) + "]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i + 1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(
                                                        i + 1) + "]/label/span[1]/span")

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))



    # todo 2.1.10 基本公卫 - 健康档案管理 - 就诊管理

    def phs_healthrecord_visit_query(self, d_):

        # 就诊管理 - 查询

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['就诊日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div/div/div[3]/div/input", v[1])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div/div/div[1]/div/input", v[0])
                elif k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div/div/div/div/input", _dropdownByX, v[0])
                    # /html/body/div[1]/div/div[3]/section/div/main/div[1]/form/div/div[5]/div[1]/div/div/div/div/input
                    # /html/body/div[1]/div/div[3]/section/div/main/div[1]/form/div/div[5]/div[2]/div/div/div/div/input
                    # /html/body/div[1]/div/div[3]/section/div/main/div[1]/form/div/div[5]/div[3]/div/div/input
                    self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    # /html/body/div[1]/div/div[3]/section/div/main/div[1]/form/div/div[5]/div[2]/div/div/div/div/input
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), ".//div[3]/div/div/input", v[2])
                    # /html/body/div[1]/div/div[3]/section/div/main/div[1]/form/div/div[5]/div[2]/div/div/div/div/input
                elif k in ['管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k), ".//div/div/div/input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(
                                            i + 1) + "]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i + 1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(
                                                        i + 1) + "]/label/span[1]/span")

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_healthrecord_visit_export(self, varFile):

        # 就诊管理 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击导出
        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)



    # todo 2.2.1 基本公卫 - 高血压管理(common)

    def __text_value1(self, ele, d_value, varField, varXpath):
        # self.__text_value1(ele, d_['value'], '随访方式', ".//div[2]/div/div/div")
        if varField in d_value:
            Web_PO.eleScrollViewByX(ele, varXpath, 1)
            Web_PO.eleSetTextByX(ele, varXpath, d_value[varField])

    def __text_value2(self, ele, d_value, varField, varXpath1, varXpath2):
        if varField in d_value:
            Web_PO.eleScrollViewByX(ele, varXpath1, 1)
            Web_PO.eleSetTextByX(ele, varXpath1, d_value[varField][0])
            Web_PO.eleSetTextByX(ele, varXpath2, d_value[varField][1])

    def __radioRight(self, ele, d_value, varField, varXpath):
        if varField in d_value:
            Web_PO.eleRadioRightLabel(ele, varXpath, d_value[varField])

    def __radioLeft(self, ele, d_value, varField, varXpath):
        if varField in d_value:
            Web_PO.eleRadioLeftLabel(ele, varXpath, d_value[varField])

    def __radioRight_self(self, ele, d_value, varField, varXpath):
        if varField in d_value:
            self.__eleRadioRightLabel(ele, varXpath, d_value[varField])

    def __gxy(self, d_, index=1):

        # 高血压随访
        ele = Web_PO.getSuperEleByX("(//form)[position()=" + str(index) + "]", ".")
        # ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        self._dropdownDateSingle(ele, ".//div[1]/input", d_['value']['随访日期'])
        self.__radioLeft(ele, d_['value'], '随访方式', ".//div[2]/div/div/div")
        if '症状' in d_['value']:
            Web_PO.eleScrollViewByX(ele, ".//div[3]/div/div/div[1]/div", 1)
            Web_PO.eleCheckboxLeftLabel(ele, ".//div[3]/div/div/div[1]/div", d_['value']['症状'])
            for i in d_['value']['症状']:
                if isinstance(i, dict):
                    Web_PO.eleSetTextByX(ele, ".//div[3]/div/div/div[2]/input", i['其他'])
        self.__text_value2(ele, d_['value'], '血压', ".//div[4]/div[1]/div/div/input", ".//div[4]/div[2]/div/div/input")
        self.__text_value1(ele, d_['value'], '身高', ".//div[5]/div/div/div/input")
        self.__text_value2(ele, d_['value'], '体重', ".//div[6]/div[1]/div/div/input", ".//div[6]/div[2]/div/div/input")
        self.__text_value1(ele, d_['value'], '心率', ".//div[8]/div/div/div/input")
        self.__text_value1(ele, d_['value'], '其他', ".//div[9]/div/div/div/input")
        self.__text_value2(ele, d_['value'], '日吸烟量', ".//div[10]/div[1]/div/div/input",
                           ".//div[10]/div[2]/div/div/input")
        self.__text_value2(ele, d_['value'], '日饮酒量', ".//div[11]/div[1]/div/div/input",
                           ".//div[11]/div[2]/div/div/input")
        self.__radioRight(ele, d_['value'], '运动频率实际', ".//div[12]/div/div/div[1]/label")
        self.__radioRight(ele, d_['value'], '运动频率目标', ".//div[13]/div/div/div[1]/label")
        self.__text_value2(ele, d_['value'], '运动时长', ".//div[14]/div[1]/div/div/input",
                           ".//div[14]/div[2]/div/div/input")
        self.__radioRight(ele, d_['value'], '摄盐量分级实际', ".//div[15]/div/div/div[1]/label")
        self.__radioRight(ele, d_['value'], '摄盐量分级目标', ".//div[16]/div/div/div[1]/label")
        self.__radioRight(ele, d_['value'], '随访饮食合理性评价', ".//div[17]/div/div/div[1]/label")
        self.__radioRight_self(ele, d_['value'], '心理调整评价结果', ".//div[18]/div/div/div[1]/label")
        self.__radioRight_self(ele, d_['value'], '随访遵医行为', ".//div[19]/div/div/div[1]/label")
        self.__text_value1(ele, d_['value'], '辅助检查', ".//div[20]/div/div/div/input")
        self.__radioRight_self(ele, d_['value'], '服药依从性', ".//div[21]/div/div/div[1]/label")
        if '药物不良反应' in d_['value']:
            Web_PO.eleRadioLeftLabel(ele, ".//div[22]/div[1]/div/div", d_['value']['药物不良反应'][0])
            if d_['value']['药物不良反应'][0] == '有':
                Web_PO.eleSetTextByX(ele, ".//div[22]/div[2]/div/div/input", d_['value']['药物不良反应'][1])
        self.__radioRight_self(ele, d_['value'], '随访评价结果', ".//div[23]/div/div/div[1]/label")
        self.__radioRight_self(ele, d_['value'], '下一步管理措施', ".//div[24]/div/div/div[1]/label")
        if '用药情况药物名称1' in d_['value']:
            Web_PO.eleScrollViewByX(ele, ".//div[25]/div/div/div/div/div/input", 2)
            # Web_PO.eleClsReadonlyByX(ele, ".//div[25]/div/div/div/div/div/input", 2)
            # Web_PO.eleSetTextByX(ele, ".//div[25]/div/div/div/div/div/input", d_['value']['用药情况药物名称1'])
            self._eleClkDropdown(ele, ".//div[25]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药情况药物名称1'])
            self._eleClkDropdown(ele, ".//div[26]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药情况用法用量1每日'])  # 每日
            Web_PO.eleSetTextByX(ele, ".//div[26]/div/div[2]/div/div/input", d_['value']['用药情况用法用量1每次'])  # 每次
        if '用药情况药物名称2' in d_['value']:
            # Web_PO.eleClsReadonlyByX(ele, ".//div[27]/div/div/div/div/div/input", 2)
            # Web_PO.eleSetTextByX(ele, ".//div[27]/div/div/div/div/div/input", d_['value']['用药情况药物名称2'])
            self._eleClkDropdown(ele, ".//div[27]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药情况药物名称2'])
            self._eleClkDropdown(ele, ".//div[28]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药情况用法用量2每日'])
            Web_PO.eleSetTextByX(ele, ".//div[28]/div/div[2]/div/div/input", d_['value']['用药情况用法用量2每次'])
        if '用药情况药物名称3' in d_['value']:
            # Web_PO.eleClsReadonlyByX(ele, ".//div[29]/div/div/div/div/div/input", 2)
            # Web_PO.eleSetTextByX(ele, ".//div[29]/div/div/div/div/div/input", d_['value']['用药情况药物名称3'])
            self._eleClkDropdown(ele, ".//div[29]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药情况药物名称3'])
            self._eleClkDropdown(ele, ".//div[30]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药情况用法用量3每日'])
            Web_PO.eleSetTextByX(ele, ".//div[30]/div/div[2]/div/div/input", d_['value']['用药情况用法用量3每次'])
        if '用药调整意见药物名称1' in d_['value']:
            Web_PO.eleScrollViewByX(ele, ".//div[31]/div/div/div/div/div/input", 2)
            # Web_PO.eleClsReadonlyByX(ele, ".//div[31]/div/div/div/div/div/input", 2)
            # Web_PO.eleSetTextByX(ele, ".//div[31]/div/div/div/div/div/input", d_['value']['用药调整意见药物名称1'])
            self._eleClkDropdown(ele, ".//div[31]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见药物名称1'])
            self._eleClkDropdown(ele, ".//div[32]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见用法用量1每日'])
            Web_PO.eleSetTextByX(ele, ".//div[32]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量1每次'])
        if '用药调整意见药物名称2' in d_['value']:
            # Web_PO.eleClsReadonlyByX(ele, ".//div[33]/div/div/div/div/div/input", 2)
            # Web_PO.eleSetTextByX(ele, ".//div[33]/div/div/div/div/div/input", d_['value']['用药调整意见药物名称2'])
            self._eleClkDropdown(ele, ".//div[33]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见药物名称2'])
            self._eleClkDropdown(ele, ".//div[34]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见用法用量2每日'])
            Web_PO.eleSetTextByX(ele, ".//div[34]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量2每次'])
        if '用药调整意见药物名称3' in d_['value']:
            # Web_PO.eleClsReadonlyByX(ele, ".//div[35]/div/div/div/div/div/input", 2)
            # Web_PO.eleSetTextByX(ele, ".//div[35]/div/div/div/div/div/input", d_['value']['用药调整意见药物名称3'])
            self._eleClkDropdown(ele, ".//div[35]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见药物名称3'])
            self._eleClkDropdown(ele, ".//div[36]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见用法用量3每日'])
            Web_PO.eleSetTextByX(ele, ".//div[36]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量3每次'])
        self.__text_value1(ele, d_['value'], '转诊原因', ".//div[37]/div/div/div/input")
        self.__text_value1(ele, d_['value'], '转入医疗机构及科室', ".//div[38]/div/div/div/input")
        self.__text_value1(ele, d_['value'], '联系人', ".//div[39]/div/div/div/input")
        self.__text_value1(ele, d_['value'], '联系人电话', ".//div[40]/div/div/div/input")
        self.__radioLeft(ele, d_['value'], '结果', ".//div[41]/div/div/div")
        self.__text_value1(ele, d_['value'], '备注', ".//div[42]/div/div/div/input")
        if '下次随访日期' in d_['value']:
            Web_PO.eleScrollViewByX(ele, ".//div[43]/div/div/div/input", 2)
            self._dropdownDateSingle(ele, ".//div[43]/div/div/div/input", d_['value']['下次随访日期'])
        if '随访医生' in d_['value']:
            Web_PO.eleScrollViewByX(ele, "..//div[44]/div/div/div/div/div/input", 2)
            self._eleClkDropdown(ele, ".//div[44]/div/div/div/div/div/input", _dropdownByX, d_['value']['随访医生'])
        self.__text_value1(ele, d_['value'], '居民签字', ".//div[45]/div/div/div/input")

        ele = Web_PO.getSuperEleByX("//span[text()='保存']", ".")
        Web_PO.eleClkByX(ele, ".", 2)




    # todo 2.2.1 基本公卫 - 高血压管理 - 高血压专项


    def phs_hypertension_gxyregister_query(self, d_):

        # 高血压专项 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '建卡医生']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['收缩压范围', '舒张压范围']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div/div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['高血压危险分层', '是否终止管理', '随访提醒分类', '档案状态', '随访评价结果']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['上次随访日期', '下次随访日期', '建卡日期', '建档日期', '出生日期范围']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX, v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), ".//div[3]/div/div/input", v[2])
                elif k in ['档案管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k),  ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li["+str(i+1)+"]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i+1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_hypertension_gxyregister_export(self, varFile):

        # 高血压专项 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击导出

        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)

    def _phs_hypertension_gxyregister_operation_common(self, ele, k, varValue, l_):

        # 获取所有选项，生成映射字典
        l_value = Web_PO.eleGetTextByXs(self._eleDiv(ele, k), './/label/span[2]')
        # print(l_value)
        d_3 = dict(enumerate(l_value, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        # print(d_4)  # {'男性>55 岁或女性>65 岁': 1, '吸烟': 2, '糖耐量受损': 3, '血脂异常TC≥5.7mmol/L（220mg/dL） 或LDL-C>3.6mmol/L （140mg/dL） 或 HDL-C<1.0mmol/L （40mg/dL）': 4, '早 发 心血 管病家族 史 （一级亲属发病年龄男 性小于 55 岁，女性小于 65 岁）': 5, '腹型肥胖': 6, '血同型半胱氨酸升高': 7, '糖尿病伴微白蛋白尿': 8, '以静息为主的生活方式': 9, '血浆纤维蛋白原增高': 10, '高敏C反应蛋白≥3mg/L或C反应蛋白≥10mg/L': 11, '以上都无': 12}

        # 默认已勾选以上都无，先取消勾选
        Web_PO.eleClkByX(self._eleDiv(ele, k),
                         ".//div[2]/div/div/div/div[" + str(d_4[varValue]) + "]/label")  # 不勾选'以上都无'

        # 勾选选项
        for i in range(len(l_)):
            Web_PO.eleClkByX(self._eleDiv(ele, k), './/div[2]/div/div/div[1]/div[' + str(d_4[l_[i]]) + ']/label', 2)
    def _phs_hypertension_gxyregister_operation(self, varOperation, d_option):

        # 遍历高血压专项、高血压随访的列表页
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['个人档案编号', '姓名', '提醒', '身份证号', '年龄', '性别', '电话', '居住地址', '建卡日期', '建卡医生', '上次随访日期', '下次随访日期', '操作']
        Web_PO.zoom(100)

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)
        s_class_warn = Web_PO.eleGetAttrValueByX(ele2, ".//td[3]/div/div/div", "style")
        # print(s_class_warn)  # background: rgb(223, 57, 38); width: 16px; height: 16px;
        s_class_warn = s_class_warn.split("rgb")[1].split(";")[0]
        l_value[2] = s_class_warn
        # print(l_value)

        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
            if "提醒" in l_field:
                for i in l_group:
                    i.pop(3)
                    i.pop(3)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
            if "提醒" in l_field:
                for i in l_group:
                    i.pop(3)
                    i.pop(3)
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_hypertension_gxyregister_operation(self, d_):

        # 高血压专项 - 操作

        try:
            if "index" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(self._phs_hypertension_gxyregister_operation('详情\n评估\n随访', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            if d_['operate'] == '详情' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '编辑':
                    ele2 = Web_PO.getSuperEleByX("//span[text()='编辑']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

                    ele = Web_PO.getSuperEleByX("//div[text()='高血压患者管理卡']", "..")
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                    for k, v in d_['value'].items():
                        if k in [' 居住地址 ']:
                            self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'), ".//div[1]/div[2]/div/div/div/div/div/input", _dropdownByX, v[0])
                            self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'), ".//div[2]/div[1]/div/div/div/div/div/input", _dropdownByX, v[1])
                            self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'), ".//div[2]/div[2]/div/div/div/div/div/input", _dropdownByX, v[2])
                            self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'), ".//div[3]/div[1]/div/div/div/div/div/input", _dropdownByX, v[3])
                            self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'), ".//div[3]/div[2]/div/div/div/div/div/input", _dropdownByX, v[4])
                            Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k, '../..'), ".//div[4]/div[2]/div/div/div/input", v[5])
                        elif k in [' 建卡医疗机构 ']:
                            Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//input", v)
                        elif k in [' 终止管理原因 ']:
                            if d_['value'][' 是否终止管理 '] == "是":
                                Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//input", v)
                        elif k in [' 终止管理日期 ']:
                            if d_['value'][' 是否终止管理 '] == "是":
                                self._dropdownDateSingle(self._eleDiv(ele, k), ".//div[1]/input", v)
                        elif k in [' 管理级别 ']:
                            Web_PO.eleRadioLeftLabel(self._eleDiv(ele, k), ".//div[2]/div/div/div", v)
                        elif k in [' 是否终止管理 ']:
                            Web_PO.eleRadioRightLabel(self._eleDiv(ele, k), ".//div[2]/div/div/div/label", v)
                        elif k in [' 建卡医生 ']:
                            self._eleClkDropdown(self._eleDiv(ele, k), ".//input", _dropdownByX, v)
                        elif k in [' 确诊日期 ', ' 建卡时间 ']:
                            self._dropdownDateSingle(self._eleDiv(ele, k), ".//div[1]/input", v)
                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

            if d_['operate'] == '评估' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '新增':
                    ele2 = Web_PO.getSuperEleByX("//span[text()='新增']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

                    ele = Web_PO.getSuperEleByX("//div[text()='高血压患者评估']", "..")
                    for k, v in d_['value'].items():
                        if k in [' 身高(cm) ', ' 体重(kg) ']:
                            Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//input", v)
                        elif k in [' 血压 ']:
                            Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//div[1]/div/div/input", v[0])
                            Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//div[2]/div/div/input", v[1])
                        elif k in [' 危险因素 ']:
                            if isinstance(v, list):
                                self._phs_hypertension_gxyregister_operation_common(ele, k, '以上都无', v)
                        elif k in [' 靶器官损害 ']:
                            if isinstance(v, list):
                                self._phs_hypertension_gxyregister_operation_common(ele, k, '以上都无', v)
                        elif k in [' 并发症情况 ']:
                            if isinstance(v, list):
                                self._phs_hypertension_gxyregister_operation_common(ele, k, '以上情况均无', v)
                        elif k in [' 高血压分级 ', ' 危险分层 ']:
                            Web_PO.eleRadioLeftLabel(self._eleDiv(ele, k), ".//div[2]/div/div/div", v)
                        elif k in [' 评估日期 ']:
                            self._dropdownDateSingle(self._eleDiv(ele, k), ".//div[1]/input", v)
                    ele3 = Web_PO.getSuperEleByX("//div[text()='高血压患者评估']", "../../..")
                    Web_PO.eleClkByX(ele3, ".//button[1]", 2)  # 保存
                    # Web_PO.eleClkByX(ele3, ".//button[2]", 2)  # 取消
                # elif d_['index']['operate2'] == '新增':

            elif d_['operate'] == '随访' and "operate2" in d_['index']:
                # 三种操作，编辑(第一个)、新增、引入上次新增

                if d_['index']['operate2'] == '新增':
                    # 判断血压是否有值，如果没值，表示一条随访记录都没有，编辑(第一个)
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    s_temp = Web_PO.eleGetShadowByXByC(ele, ".//div[4]/div[1]/div/div[1]/input", "div:nth-last-of-type(1)")
                    if s_temp != '':
                        ele3 = Web_PO.getSuperEleByX("//span[text()='新增']", ".")
                        Web_PO.eleClkByX(ele3, ".", 2)
                if d_['index']['operate2'] == '引入上次新增':
                    ele3 = Web_PO.getSuperEleByX("//span[text()='引入上次新增']", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

                # 新增
                self.__gxy(d_)

            else:
                print("error,无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")



    # todo 2.2.2 基本公卫 - 高血压管理 - 高血压随访

    def phs_hypertension_gxyjob_query(self, d_):

        # 高血压随访 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '随访医生']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['收缩压范围', '舒张压范围']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div/div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访方式', '是否终止管理', '数据源', '随访评价结果']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['随访日期', '出生日期范围']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX, v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k),  ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li["+str(i+1)+"]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i+1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_hypertension_gxyjob_export(self, varFile):

        # 高血压随访 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击导出

        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)

    def _phs_hypertension_gxyjob_operation(self, varOperation, d_option):

        # 遍历高血压专项、高血压随访的列表页
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['个人档案编号', '姓名', '提醒', '身份证号', '年龄', '性别', '电话', '居住地址', '建卡日期', '建卡医生', '上次随访日期', '下次随访日期', '操作']
        Web_PO.zoom(100)

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)  # ['李常', '110101199003075678', '1990-03-07',

        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
        # print(l_group)  # [['李常', '110101199003075678', '1990-03-07', ...

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        if d_1 == {}:
            print("warning, 未匹配记录！")
        else:
            max_key = max(d_1, key=d_1.get)
            print("ok, 匹配到第" + str(max_key) + "条记录。")
        return max_key
    def phs_hypertension_gxyjob_operation(self, d_):

        # 高血压随访 - 操作

        try:
            if "index" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(self._phs_hypertension_gxyjob_operation('详情\n编辑\n删除', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            if d_['operate'] == '详情' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '编辑':
                    ele3 = Web_PO.getSuperEleByX("//span[text()='编辑']", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

                    # 定位第几个随访日期
                    Web_PO.zoom(50)
                    ele = Web_PO.getEleByClassName("formList")
                    # ele = Web_PO.getSuperEleByX("//div[@class='formList']", '.')
                    l_followUp_date = Web_PO.eleGetShadowByXsByC(ele, ".//form/div[1]/div/div/div/input", 'div:nth-last-of-type(1)')
                    # print(l_followUp_date)  # ['2025-02-21', '2025-02-19', '2025-02-14', '2025-02-13']
                    index = 0
                    for i in range(len(l_followUp_date)):
                        if l_followUp_date[i] == d_['index']['随访日期']:
                            index = i + 1
                    Web_PO.zoom(100)
                    if index == 0:
                        print("warning, 未匹配记录, 请检查随访日期为", d_['index']['随访日期'], '的记录是否存在！')
                    else:
                        print("ok, 匹配到第", index, "列随访记录，可编辑。")
                        # 编辑
                        self.__gxy(d_, index)

            elif d_['operate'] == '编辑' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '编辑':
                # if d_['index']['operate2'] == '编辑或新增':
                    ...

                    # # 获取所有随访日期
                    # Web_PO.zoom(50)
                    # ele = Web_PO.getEleByClassName("formList")
                    # # ele = Web_PO.getSuperEleByX("//div[@class='formList']", '.')
                    # l_followUp_date = Web_PO.eleGetShadowByXsByC(ele, ".//form/div[1]/div/div/div/input", 'div:nth-last-of-type(1)')
                    # print(l_followUp_date)  # ['2025-02-21', '2025-02-19', '2025-02-14', '2025-02-13']
                    # index = 0
                    # for i in range(len(l_followUp_date)):
                    #     if l_followUp_date[i] == d_['index']['随访日期']:
                    #         index = i + 1
                    # Web_PO.zoom(100)
                    # if index == 0:
                    #     print("warning, 未匹配记录, 新增随访日期为", d_['index']['随访日期'], '的记录.')
                    #     ele3 = Web_PO.getSuperEleByX("//span[text()='新增']", ".")
                    #     Web_PO.eleClkByX(ele3, ".", 2)
                    # else:
                    #     print("ok, 匹配到第", index, "列随访记录，可编辑。")

                elif d_['index']['operate2'] == '新增':
                    ele3 = Web_PO.getSuperEleByX("//span[text()='新增']", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    index = 1
                elif d_['index']['operate2'] == '引入上次新增':
                    ele3 = Web_PO.getSuperEleByX("//span[text()='引入上次新增']", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    index = 1

                # 新增、编辑、引入上次新增
                self.__gxy(d_, index)

            elif d_['operate'] == '删除':
                ...
                Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 二次确认

            self.logger.info("点击" + str(d_['operate']))
        except:
            self.logger.error(str(d_) + "失败！")



    # todo 2.3 基本公卫 - 糖尿病管理(common)

    def __tnb(self, d_, index=1):

        # 糖尿病随访
        ele = Web_PO.getSuperEleByX("(//form)[position()=" + str(index) + "]", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        self._dropdownDateSingle(ele, ".//div[1]/input", d_['value']['随访日期'])
        self.__radioLeft(ele, d_['value'], '随访方式', ".//div[2]/div/div/div")
        # Web_PO.eleRadioLeftLabel(ele, ".//div[2]/div/div/div", d_['value']['随访方式'])
        if '症状' in d_['value']:
            Web_PO.eleScrollViewByX(ele, ".//div[3]/div/div/div[1]/div", 1)
            Web_PO.eleCheckboxLeftLabel(ele, ".//div[3]/div/div/div[1]/div", d_['value']['症状'])
            for i in d_['value']['症状']:
                if isinstance(i, dict):
                    Web_PO.eleSetTextByX(ele, ".//div[3]/div/div/div[2]/input", i['其他'])
        self.__text_value2(ele, d_['value'], '血压', ".//div[4]/div[1]/div/div/input", ".//div[4]/div[2]/div/div/input")
        # Web_PO.eleSetTextByX(ele, ".//div[4]/div[1]/div/div/input", d_['value']['血压'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[4]/div[2]/div/div/input", d_['value']['血压'][1])
        # Web_PO.eleSetTextByX(ele, ".//div[5]/div/div/div/input", d_['value']['身高'])
        self.__text_value1(ele, d_['value'], '身高', ".//div[5]/div/div/div/input")
        self.__text_value2(ele, d_['value'], '体重', ".//div[6]/div[1]/div/div/input", ".//div[6]/div[2]/div/div/input")
        # Web_PO.eleSetTextByX(ele, ".//div[6]/div[1]/div/div/input", d_['value']['体重'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[6]/div[2]/div/div/input", d_['value']['体重'][1])
        # self.__eleRadioRightLabel(ele, ".//div[8]/div/div/div/label", d_['value']['足背动脉搏动'])
        self.__radioRight(ele, d_['value'], '足背动脉搏动', ".//div[8]/div/div/div/label")

        self.__text_value1(ele, d_['value'], '其他', ".//div[9]/div/div/div/input")
        # Web_PO.eleSetTextByX(ele, ".//div[9]/div/div/div/input", d_['value']['其他'])

        # Web_PO.eleSetTextByX(ele, ".//div[10]/div[1]/div/div/input", d_['value']['日吸烟量'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[10]/div[2]/div/div/input", d_['value']['日吸烟量'][1])
        # Web_PO.eleSetTextByX(ele, ".//div[11]/div[1]/div/div/input", d_['value']['日饮酒量'][0])
        # Web_PO.eleSetTextEnterByX(ele, ".//div[11]/div[2]/div/div/input", d_['value']['日饮酒量'][1])
        # Web_PO.eleRadioRightLabel(ele, ".//div[12]/div/div/div[1]/label", d_['value']['运动频率实际'])
        # Web_PO.eleRadioRightLabel(ele, ".//div[13]/div/div/div[1]/label", d_['value']['运动频率目标'])
        # Web_PO.eleSetTextByX(ele, ".//div[14]/div[1]/div/div/input", d_['value']['运动时长'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[14]/div[2]/div/div/input", d_['value']['运动时长'][1])

        self.__text_value2(ele, d_['value'], '日吸烟量', ".//div[10]/div[1]/div/div/input", ".//div[10]/div[2]/div/div/input")
        self.__text_value2(ele, d_['value'], '日饮酒量', ".//div[11]/div[1]/div/div/input", ".//div[11]/div[2]/div/div/input")
        self.__radioRight(ele, d_['value'], '运动频率实际', ".//div[12]/div/div/div[1]/label")
        self.__radioRight(ele, d_['value'], '运动频率目标', ".//div[13]/div/div/div[1]/label")
        self.__text_value2(ele, d_['value'], '运动时长', ".//div[14]/div[1]/div/div/input", ".//div[14]/div[2]/div/div/input")

        self.__text_value2(ele, d_['value'], '日主食量', ".//div[15]/div[1]/div/div/input", ".//div[15]/div[2]/div/div/input")
        # Web_PO.eleSetTextByX(ele, ".//div[15]/div[1]/div/div/input", d_['value']['日主食量'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[15]/div[2]/div/div/input", d_['value']['日主食量'][1])
        # self.__eleRadioRightLabel(ele, ".//div[16]/div/div/div/label", d_['value']['饮食情况'])
        self.__radioRight(ele, d_['value'], '饮食情况', ".//div[16]/div/div/div/label")

        self.__radioRight_self(ele, d_['value'], '心理调整评价结果', ".//div[17]/div/div/div[1]/label")
        self.__radioRight_self(ele, d_['value'], '随访遵医行为', ".//div[18]/div/div/div[1]/label")
        self.__text_value1(ele, d_['value'], '辅助检查', ".//div[19]/div/div/div/input")
        # self.__eleRadioRightLabel(ele, ".//div[17]/div/div/div[1]/label", d_['value']['心理调整评价结果'])
        # self.__eleRadioRightLabel(ele, ".//div[18]/div/div/div[1]/label", d_['value']['随访遵医行为'])
        # Web_PO.eleSetTextByX(ele, ".//div[19]/div/div/div/input", d_['value']['辅助检查'])

        self.__radioRight_self(ele, d_['value'], '服药情况', ".//div[20]/div/div/div[1]/label")
        # self.__eleRadioRightLabel(ele, ".//div[20]/div/div/div[1]/label", d_['value']['服药情况'])

        # Web_PO.eleRadioLeftLabel(ele, ".//div[21]/div[1]/div/div", d_['value']['药物不良反应'][0])
        # if d_['value']['药物不良反应'][0] == '有':
        #     Web_PO.eleSetTextByX(ele, ".//div[21]/div[2]/div/div/input", d_['value']['药物不良反应'][1])

        if '药物不良反应' in d_['value']:
            Web_PO.eleRadioLeftLabel(ele, ".//div[21]/div[1]/div/div", d_['value']['药物不良反应'][0])
            if d_['value']['药物不良反应'][0] == '有':
                Web_PO.eleSetTextByX(ele, ".//div[21]/div[2]/div/div/input", d_['value']['药物不良反应'][1])

        self.__radioRight_self(ele, d_['value'], '随访评价结果', ".//div[22]/div/div/div[1]/label")
        self.__radioRight_self(ele, d_['value'], '下一步管理措施', ".//div[23]/div/div/div[1]/label")
        # self.__eleRadioRightLabel(ele, ".//div[22]/div/div/div[1]/label", d_['value']['随访评价结果'])
        # self.__eleRadioRightLabel(ele, ".//div[23]/div/div/div[1]/label", d_['value']['下一步管理措施'])

        if '用药情况药物名称1' in d_['value']:
            Web_PO.eleScrollViewByX(ele, ".//div[24]/div/div/div/div/div/input", 2)
            self._eleClkDropdown(ele, ".//div[24]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药情况药物名称1'])
            self._eleClkDropdown(ele, ".//div[25]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药情况用法用量1每日'])  # 每日
            Web_PO.eleSetTextByX(ele, ".//div[25]/div/div[2]/div/div/input", d_['value']['用药情况用法用量1每次'])  # 每次

        # Web_PO.eleClsReadonlyByX(ele, ".//div[24]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[24]/div/div/div/div/div/input", d_['value']['用药情况药物名称1'])
        # self._eleClkDropdown(ele, ".//div[25]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['value']['用药情况用法用量1每日'])

        if '用药情况药物名称2' in d_['value']:
            self._eleClkDropdown(ele, ".//div[26]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药情况药物名称2'])
            self._eleClkDropdown(ele, ".//div[27]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药情况用法用量2每日'])
            Web_PO.eleSetTextByX(ele, ".//div[27]/div/div[2]/div/div/input", d_['value']['用药情况用法用量2每次'])

        # Web_PO.eleClsReadonlyByX(ele, ".//div[26]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[26]/div/div/div/div/div/input", d_['value']['用药情况药物名称2'])
        # self._eleClkDropdown(ele, ".//div[27]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['value']['用药情况用法用量2每日'])
        # Web_PO.eleSetTextByX(ele, ".//div[27]/div/div[2]/div/div/input", d_['value']['用药情况用法用量2每次'])

        if '用药情况药物名称3' in d_['value']:
            self._eleClkDropdown(ele, ".//div[28]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药情况药物名称3'])
            self._eleClkDropdown(ele, ".//div[29]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药情况用法用量3每日'])
            Web_PO.eleSetTextByX(ele, ".//div[29]/div/div[2]/div/div/input", d_['value']['用药情况用法用量3每次'])

        # Web_PO.eleClsReadonlyByX(ele, ".//div[28]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[28]/div/div/div/div/div/input", d_['value']['用药情况药物名称3'])
        # self._eleClkDropdown(ele, ".//div[29]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['value']['用药情况用法用量3每日'])
        # Web_PO.eleSetTextByX(ele, ".//div[29]/div/div[2]/div/div/input", d_['value']['用药情况用法用量3每次'])

        if '用药调整意见药物名称1' in d_['value']:
            Web_PO.eleScrollViewByX(ele, ".//div[30]/div/div/div/div/div/input", 2)
            self._eleClkDropdown(ele, ".//div[30]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见药物名称1'])
            self._eleClkDropdown(ele, ".//div[31]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见用法用量1每日'])
            Web_PO.eleSetTextByX(ele, ".//div[31]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量1每次'])

        # Web_PO.eleScrollViewByX(ele, ".//div[30]/div/div/div/div/div/input", 2)
        # Web_PO.eleClsReadonlyByX(ele, ".//div[30]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[30]/div/div/div/div/div/input", d_['value']['用药调整意见药物名称1'])
        # self._eleClkDropdown(ele, ".//div[31]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['value']['用药调整意见用法用量1每日'])

        if '用药调整意见药物名称2' in d_['value']:
            self._eleClkDropdown(ele, ".//div[32]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见药物名称2'])
            self._eleClkDropdown(ele, ".//div[33]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见用法用量2每日'])
            Web_PO.eleSetTextByX(ele, ".//div[33]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量2每次'])

        # Web_PO.eleSetTextByX(ele, ".//div[31]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量1每次'])
        # Web_PO.eleClsReadonlyByX(ele, ".//div[32]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[32]/div/div/div/div/div/input", d_['value']['用药调整意见药物名称2'])
        # self._eleClkDropdown(ele, ".//div[33]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['value']['用药调整意见用法用量2每日'])

        if '用药调整意见药物名称3' in d_['value']:
            self._eleClkDropdown(ele, ".//div[34]/div/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见药物名称3'])
            self._eleClkDropdown(ele, ".//div[35]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['value']['用药调整意见用法用量3每日'])
            Web_PO.eleSetTextByX(ele, ".//div[35]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量3每次'])

        # Web_PO.eleSetTextByX(ele, ".//div[33]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量2每次'])
        # Web_PO.eleClsReadonlyByX(ele, ".//div[34]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[34]/div/div/div/div/div/input", d_['value']['用药调整意见药物名称3'])
        # self._eleClkDropdown(ele, ".//div[35]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['value']['用药调整意见用法用量3每日'])
        # Web_PO.eleSetTextByX(ele, ".//div[35]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量3每次'])

        self.__text_value1(ele, d_['value'], '转诊原因', ".//div[36]/div/div/div/input")
        self.__text_value1(ele, d_['value'], '转入医疗机构及科室', ".//div[37]/div/div/div/input")
        self.__text_value1(ele, d_['value'], '联系人', ".//div[38]/div/div/div/input")
        self.__text_value1(ele, d_['value'], '联系人电话', ".//div[39]/div/div/div/input")
        self.__radioRight(ele, d_['value'], '结果', ".//div[40]/div/div/div/label")
        self.__text_value1(ele, d_['value'], '备注', ".//div[41]/div/div/div/input")

        # Web_PO.eleSetTextByX(ele, ".//div[36]/div/div/div/input", d_['value']['转诊原因'])
        # Web_PO.eleSetTextByX(ele, ".//div[37]/div/div/div/input", d_['value']['转入医疗机构及科室'])
        # Web_PO.eleSetTextByX(ele, ".//div[38]/div/div/div/input", d_['value']['联系人'])
        # Web_PO.eleSetTextByX(ele, ".//div[39]/div/div/div/input", d_['value']['联系人电话'])
        # self.__eleRadioRightLabel(ele, ".//div[40]/div/div/div/label", d_['value']['结果'])
        # Web_PO.eleSetTextByX(ele, ".//div[41]/div/div/div/input", d_['value']['备注'])

        if '下次随访日期' in d_['value']:
            Web_PO.eleScrollViewByX(ele, ".//div[42]/div/div/div/input", 2)
            self._dropdownDateSingle(ele, ".//div[42]/div/div/div/input", d_['value']['下次随访日期'])
        if '随访医生' in d_['value']:
            Web_PO.eleScrollViewByX(ele, "..//div[43]/div/div/div/div/div/input", 2)
            self._eleClkDropdown(ele, ".//div[43]/div/div/div/div/div/input", _dropdownByX, d_['value']['随访医生'])
        self.__text_value1(ele, d_['value'], '居民签字', ".//div[44]/div/div/div/input")

        # self._dropdownDateSingle(ele, ".//div[42]/div/div/div/input", d_['value']['下次随访日期'])
        # self._eleClkDropdown(ele, ".//div[43]/div/div/div/div/div/input", _dropdownByX, d_['value']['随访医生'])
        # Web_PO.eleSetTextByX(ele, ".//div[44]/div/div/div/input", d_['value']['居民签字'])

        ele = Web_PO.getSuperEleByX("//span[text()='保存']", ".")
        Web_PO.eleClkByX(ele, ".", 2)



    # todo 2.3.1 基本公卫 - 糖尿病管理 - 糖尿病专项

    def phs_diabetes_tnbregister_query(self, d_):

        # 糖尿病专项 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '建卡医生']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['是否终止管理', '随访提醒分类', '档案状态', '随访评价结果']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期范围']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['上次随访日期', '下次随访日期', '建卡日期', '建档日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/div/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX, v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), ".//div[3]/div/div/input", v[2])
                elif k in ['档案管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k),  ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li["+str(i+1)+"]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i+1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_diabetes_tnbregister_export(self, varFile):

        # 糖尿病专项 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击导出

        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)

    def _phs_diabetes_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        # 缩小页面，获取所有的字段
        Web_PO.zoom(50)
        # 获取字段列表
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        print(l_field)  # ['姓名', '身份证号', '出生日期', '电话', '居住地址', '性别', '随访医生', '空腹血糖', '随访方式', '随访日期', '随访评价结果', '下次随访日期', '数据源', '操作']
        Web_PO.zoom(100)

        # 获取值列表
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        print(l_value)
        s_class_warn = Web_PO.eleGetAttrValueByX(ele2, ".//td[3]/div/span", "class")
        # print(s_class_warn) # warn-tag warn-red
        l_value[2] = s_class_warn
        print(l_value)
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
        print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        if d_1 == {}:
            print("warning, 未匹配记录, 请检查字段是否存在！")
        else:
            print("ok, 匹配到", d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_diabetes_tnbregister_operation(self, d_):

        # 糖尿病专项 - 操作

        try:

            if "index" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(self._phs_diabetes_operation('详情\n评估\n随访', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '详情' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '编辑':
                    ele2 = Web_PO.getSuperEleByX("//span[text()='编辑']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

                    ele = Web_PO.getSuperEleByX("//th[text()=' 糖尿病患者管理卡 ']", "../..")
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                    for k, v in d_['value'].items():
                        if k in [' 居住地址 ']:
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[2]/div/div/div/div/div/input", _dropdownByX, v[0])
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[3]/div/div/div/div/div/input", _dropdownByX, v[1])
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v[2])
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[5]/div/div/div/div/div/input", _dropdownByX, v[3])
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[6]/div/div/div/div/div/input", _dropdownByX, v[4])
                            Web_PO.eleSetTextEnterByX(self._eleTd(ele, k), ".//td[7]/div/div/div/input", v[5])
                        elif k in ['终止管理原因']:
                            if d_['value'][' 是否终止管理 '] == "是":
                                Web_PO.eleSetTextEnterByX(self._eleSpan(ele, k, '../..'), ".//td[2]/div/div/div/input", v)
                        elif k in ['终止管理日期']:
                            if d_['value'][' 是否终止管理 '] == "是":
                                self._dropdownDateSingle(self._eleSpan(ele, k, '../..'), ".//td[6]/div/div/div/input", v)
                        elif k in [' 是否终止管理 ']:
                            Web_PO.eleRadioRightLabel(self._eleTd(ele, k), ".//td[4]/div/div/div/label", v)
                        elif k in ['建卡医生']:
                            self._eleClkDropdown(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v)
                        elif k in [' 确诊日期 ']:
                            self._dropdownDateSingle(self._eleTd(ele, k), ".//td[2]/div/div/div/input", v)
                        elif k in ['建卡时间']:
                            self._dropdownDateSingle(self._eleSpan(ele, k, '../..'), ".//td[2]/div/div/div/input", v)
                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['operate'] == '评估' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '新增':
                    ele2 = Web_PO.getSuperEleByX("//span[text()='新增']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)
                    # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[1]/button", 2)  # 新增
                    ele = Web_PO.getSuperEleByX("//th[text()=' 糖尿病患者评估 ']", "../..")
                    for k, v in d_['value'].items():
                        if k in [' 空腹血糖 ', ' 糖化血红蛋白 ', ' BMI评价 ', ' 高密度脂蛋白胆固醇 ', ' 吸烟 ', ' 体育锻炼 ', ' 遵医行为 ', ' 心理状态 ', ' 降糖效果 ']:
                            Web_PO.eleRadioRightLabel(self._eleTd(ele, k), ".//td[2]/div/div/div/label", v)
                        if k in [' 餐后血糖 ', ' 血压评价 ', ' 总胆固醇 ', ' 低密度脂蛋白胆固醇 ', ' 饮酒 ', ' 食盐摄入量 ',' 饮食 ', ' 总体评价 ']:
                            Web_PO.eleRadioRightLabel(self._eleTd(ele, k), ".//td[4]/div/div/div/label", v)
                        if k in ['管理程度']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, '../..'), ".//td[4]/div/div/div/label", v)
                        elif k in ['评估日期']:
                            self._dropdownDateSingle(self._eleSpan(ele, k, '../..'), ".//td[4]/div/div/div/input", v)
                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['operate'] == '随访' and "operate2" in d_['index']:
                # 三种操作，编辑(第一个)、新增、引入上次新增

                if d_['index']['operate2'] == '新增':
                    # 判断血压是否有值，如果没值，表示一条随访记录都没有，编辑(第一个)
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    s_temp = Web_PO.eleGetShadowByXByC(ele, ".//div[4]/div[1]/div/div[1]/input", "div:nth-last-of-type(1)")
                    if s_temp != '':
                        ele3 = Web_PO.getSuperEleByX("//span[text()='新增']", ".")
                        Web_PO.eleClkByX(ele3, ".", 2)
                if d_['index']['operate2'] == '引入上次新增':
                    ele3 = Web_PO.getSuperEleByX("//span[text()='引入上次新增']", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

                # 新增
                self.__tnb(d_)

            else:
                print("error,无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")



    # todo 2.3.2 基本公卫 - 糖尿病管理 - 糖尿病随访

    def phs_diabetes_tnbjob_query(self, d_):

        # 糖尿病随访 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '随访医生']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['空腹血糖']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访方式', '是否终止管理', '数据源', '随访评价结果']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期范围']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/div/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX,
                                            v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), ".//div[2]/div/div/div/div/input",
                                            _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k), ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(
                                            i + 1) + "]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i + 1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(
                                                        i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_diabetes_tnbjob_export(self, varFile):

        # 糖尿病随访 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击导出

        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)

    def _phs_diabetes_tnbjob_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        # 缩小页面，获取所有的字段
        Web_PO.zoom(50)
        # 获取字段列表
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        print(l_field)  # ['姓名', '身份证号', '出生日期', '电话', '居住地址', '性别', '随访医生', '空腹血糖', '随访方式', '随访日期', '随访评价结果', '下次随访日期', '数据源', '操作']
        Web_PO.zoom(100)

        # 获取列表所有制
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        print(l_value)

        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
        print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        if d_1 == {}:
            print("warning, 未匹配记录, 请检查字段是否存在！")
        else:
            print("ok, 匹配到", d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key

    def phs_diabetes_tnbjob_operation(self, d_):

        # 糖尿病随访 - 操作

        try:
            if "index" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(self._phs_diabetes_tnbjob_operation('详情\n编辑\n删除', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            if d_['operate'] == '详情' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '编辑':
                    ele3 = Web_PO.getSuperEleByX("//span[text()='编辑']", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

                    # 定位第几个随访日期
                    Web_PO.zoom(50)
                    ele = Web_PO.getEleByClassName("formList")
                    # ele = Web_PO.getSuperEleByX("//div[@class='formList']", '.')
                    l_followUp_date = Web_PO.eleGetShadowByXsByC(ele, ".//form/div[1]/div/div/div/input", 'div:nth-last-of-type(1)')
                    # print(l_followUp_date)  # ['2025-02-21', '2025-02-19', '2025-02-14', '2025-02-13']
                    index = 0
                    for i in range(len(l_followUp_date)):
                        if l_followUp_date[i] == d_['index']['随访日期']:
                            index = i + 1
                    Web_PO.zoom(100)
                    if index == 0:
                        print("warning, 未匹配记录, 请检查随访日期为", d_['index']['随访日期'], '的记录是否存在！')
                    else:
                        print("ok, 匹配到第", index, "列随访记录，可编辑。")
                        # 编辑
                        self.__tnb(d_, index)

            elif d_['operate'] == '编辑' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '编辑或新增':
                    # 获取所有随访日期
                    Web_PO.zoom(50)
                    ele = Web_PO.getEleByClassName("formList")
                    # ele = Web_PO.getSuperEleByX("//div[@class='formList']", '.')
                    l_followUp_date = Web_PO.eleGetShadowByXsByC(ele, ".//form/div[1]/div/div/div/input", 'div:nth-last-of-type(1)')
                    print(l_followUp_date)  # ['2025-02-21', '2025-02-19', '2025-02-14', '2025-02-13']
                    index = 0
                    for i in range(len(l_followUp_date)):
                        if l_followUp_date[i] == d_['index']['随访日期']:
                            index = i + 1
                    Web_PO.zoom(100)
                    if index == 0:
                        print("warning, 未匹配记录, 新增随访日期为", d_['index']['随访日期'], '的记录.')
                        ele3 = Web_PO.getSuperEleByX("//span[text()='新增']", ".")
                        Web_PO.eleClkByX(ele3, ".", 2)
                    else:
                        print("ok, 匹配到第", index, "列随访记录，可编辑。")
                elif d_['index']['operate2'] == '引入上次新增':
                    ele3 = Web_PO.getSuperEleByX("//span[text()='引入上次新增']", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    index = 1

                # 新增、编辑、引入上次新增
                self.__tnb(d_, index)

            elif d_['operate'] == '删除':
                ...
                # Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 二次确认

            self.logger.info("点击" + str(d_['operate']))
        except:
            self.logger.error(str(d_) + "失败！")




    # todo 2.4 基本公卫 - 慢性阻塞性肺病管理(common)

    def __phs(self, d_, index=1):

        # 慢性阻塞性肺病管理随访
        # ele = Web_PO.getSuperEleByX("//form", ".")
        ele = Web_PO.getSuperEleByX("(//form)[position()=" + str(index) + "]", ".")

        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        self._dropdownDateSingle(ele, ".//div[1]/input", d_['value']['随访日期'])
        Web_PO.eleRadioLeftLabel(ele, ".//div[2]/div/div/div", d_['value']['随访方式'])
        Web_PO.eleCheckboxLeftLabel(ele, ".//div[3]/div/div/div[1]/div", d_['value']['症状'])
        for i in d_['value']['症状']:
            if isinstance(i, dict):
                Web_PO.eleSetTextByX(ele, ".//div[3]/div/div/div[2]/input", i['其他'])
        Web_PO.eleSetTextByX(ele, ".//div[4]/div/div/div/input", d_['value']['口唇紫绀'][0])
        Web_PO.eleSetTextByX(ele, ".//div[5]/div/div/div/input", d_['value']['外周水肿'][1])
        Web_PO.eleSetTextByX(ele, ".//div[6]/div/div/div/input", d_['value']['呼吸频率'])
        Web_PO.eleSetTextByX(ele, ".//div[7]/div/div/div/input", d_['value']['心率'])
        Web_PO.eleSetTextByX(ele, ".//div[8]/div/div/div/input", d_['value']['体质指数'])
        Web_PO.eleSetTextByX(ele, ".//div[9]/div/div/div/input", d_['value']['其他'])
        Web_PO.eleCheckboxLeftLabel(ele, ".//div[10]/div/div/div[1]/div[1]/label", d_['value']['症状'])
        for i in d_['value']['合并症']:
            if isinstance(i, dict):
                Web_PO.eleSetTextByX(ele, ".//div[3]/div/div/div[2]/input", i['其他'])

        Web_PO.eleSetTextByX(ele, ".//div[10]/div[1]/div/div/input", d_['value']['日吸烟量'][0])
        Web_PO.eleSetTextByX(ele, ".//div[10]/div[2]/div/div/input", d_['value']['日吸烟量'][1])
        Web_PO.eleSetTextByX(ele, ".//div[11]/div[1]/div/div/input", d_['value']['日饮酒量'][0])
        Web_PO.eleSetTextEnterByX(ele, ".//div[11]/div[2]/div/div/input", d_['value']['日饮酒量'][1])

        Web_PO.eleScrollViewByX(ele, ".//div[12]/div/div/div[1]/label", 2)
        Web_PO.eleRadioRightLabel(ele, ".//div[12]/div/div/div[1]/label", d_['value']['运动频率实际'])
        Web_PO.eleRadioRightLabel(ele, ".//div[13]/div/div/div[1]/label", d_['value']['运动频率目标'])
        Web_PO.eleSetTextByX(ele, ".//div[14]/div[1]/div/div/input", d_['value']['运动时长'][0])
        Web_PO.eleSetTextByX(ele, ".//div[14]/div[2]/div/div/input", d_['value']['运动时长'][1])

        Web_PO.eleScrollViewByX(ele, ".//div[15]/div/div/div[1]/label", 2)
        Web_PO.eleRadioRightLabel(ele, ".//div[15]/div/div/div[1]/label", d_['value']['摄盐量分级实际'])
        Web_PO.eleRadioRightLabel(ele, ".//div[16]/div/div/div[1]/label", d_['value']['摄盐量分级目标'])
        Web_PO.eleRadioRightLabel(ele, ".//div[17]/div/div/div[1]/label", d_['value']['随访饮食合理性评价'])

        Web_PO.eleScrollViewByX(ele, ".//div[18]/div/div/div[1]/label", 2)
        self.__eleRadioRightLabel(ele, ".//div[18]/div/div/div[1]/label", d_['value']['心理调整评价结果'])
        self.__eleRadioRightLabel(ele, ".//div[19]/div/div/div[1]/label", d_['value']['随访遵医行为'])
        Web_PO.eleSetTextByX(ele, ".//div[20]/div/div/div/input", d_['value']['辅助检查'])
        self.__eleRadioRightLabel(ele, ".//div[21]/div/div/div[1]/label", d_['value']['服药依从性'])
        Web_PO.eleRadioLeftLabel(ele, ".//div[22]/div[1]/div/div", d_['value']['药物不良反应'][0])
        if d_['value']['药物不良反应'][0] == '有':
            Web_PO.eleSetTextByX(ele, ".//div[22]/div[2]/div/div/input", d_['value']['药物不良反应'][1])
        self.__eleRadioRightLabel(ele, ".//div[23]/div/div/div[1]/label", d_['value']['随访评价结果'])
        self.__eleRadioRightLabel(ele, ".//div[24]/div/div/div[1]/label", d_['value']['下一步管理措施'])

        Web_PO.eleScrollViewByX(ele, ".//div[25]/div/div/div/div/div/input", 2)
        Web_PO.eleClsReadonlyByX(ele, ".//div[25]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[25]/div/div/div/div/div/input", d_['value']['用药情况药物名称1'])
        self._eleClkDropdown(ele, ".//div[26]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['value']['用药情况用法用量1每日'])
        Web_PO.eleSetTextByX(ele, ".//div[26]/div/div[2]/div/div/input", d_['value']['用药情况用法用量1每次'])

        Web_PO.eleClsReadonlyByX(ele, ".//div[27]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[27]/div/div/div/div/div/input", d_['value']['用药情况药物名称2'])
        self._eleClkDropdown(ele, ".//div[28]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['value']['用药情况用法用量2每日'])
        Web_PO.eleSetTextByX(ele, ".//div[28]/div/div[2]/div/div/input", d_['value']['用药情况用法用量2每次'])

        Web_PO.eleClsReadonlyByX(ele, ".//div[29]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[29]/div/div/div/div/div/input", d_['value']['用药情况药物名称3'])
        self._eleClkDropdown(ele, ".//div[30]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['value']['用药情况用法用量3每日'])
        Web_PO.eleSetTextByX(ele, ".//div[30]/div/div[2]/div/div/input", d_['value']['用药情况用法用量3每次'])

        Web_PO.eleScrollViewByX(ele, ".//div[31]/div/div/div/div/div/input", 2)
        Web_PO.eleClsReadonlyByX(ele, ".//div[31]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[31]/div/div/div/div/div/input", d_['value']['用药调整意见药物名称1'])
        self._eleClkDropdown(ele, ".//div[32]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['value']['用药调整意见用法用量1每日'])
        Web_PO.eleSetTextByX(ele, ".//div[32]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量1每次'])

        Web_PO.eleClsReadonlyByX(ele, ".//div[33]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[33]/div/div/div/div/div/input", d_['value']['用药调整意见药物名称2'])
        self._eleClkDropdown(ele, ".//div[34]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['value']['用药调整意见用法用量2每日'])
        Web_PO.eleSetTextByX(ele, ".//div[34]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量2每次'])

        Web_PO.eleClsReadonlyByX(ele, ".//div[35]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[35]/div/div/div/div/div/input", d_['value']['用药调整意见药物名称3'])
        self._eleClkDropdown(ele, ".//div[36]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['value']['用药调整意见用法用量3每日'])
        Web_PO.eleSetTextByX(ele, ".//div[36]/div/div[2]/div/div/input", d_['value']['用药调整意见用法用量3每次'])

        Web_PO.eleScrollViewByX(ele, ".//div[37]/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[37]/div/div/div/input", d_['value']['转诊原因'])
        Web_PO.eleSetTextByX(ele, ".//div[38]/div/div/div/input", d_['value']['转入医疗机构及科室'])
        Web_PO.eleSetTextByX(ele, ".//div[39]/div/div/div/input", d_['value']['联系人'])
        Web_PO.eleSetTextByX(ele, ".//div[40]/div/div/div/input", d_['value']['联系人电话'])

        Web_PO.eleScrollViewByX(ele, ".//div[41]/div/div/div", 2)
        self.__eleRadioLeftLabel(ele, ".//div[41]/div/div/div", d_['value']['结果'])
        Web_PO.eleSetTextByX(ele, ".//div[42]/div/div/div/input", d_['value']['备注'])
        self._dropdownDateSingle(ele, ".//div[43]/div/div/div/input", d_['value']['下次随访日期'])
        self._eleClkDropdown(ele, ".//div[44]/div/div/div/div/div/input", _dropdownByX, d_['value']['随访医生'])
        Web_PO.eleSetTextByX(ele, ".//div[45]/div/div/div/input", d_['value']['居民签字'])

        ele = Web_PO.getSuperEleByX("//span[text()='保存']", ".")
        Web_PO.eleClkByX(ele, ".", 2)


    # todo 2.4.1  基本公卫 - 慢性阻塞性肺病管理 - 慢阻肺病登记

    def __phs_copd_operation(self, varOperation, l_):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        # 缩小页面，获取所有的字段
        Web_PO.zoom(50)
        # 获取字段列表
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        print(l_field)  # ['姓名', '年龄', '性别', '身份证号', '家庭住址', '联系电话', '操作']
        Web_PO.zoom(100)

        # 获取值列表
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        print(l_value)  # ['szz', '7', '男', '341226199708114773', '关田镇关田村委会22', '13512345678', '专项登记']
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        print(l_group)  # [['szz', '7', '男', '341226199708114773', '关田镇关田村委会22', '13512345678']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in l_[0].items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key

    def phs_copd_register_query(self, d_):

        # 慢阻肺病登记 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '联系电话']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['档案状态', '既往疾病史']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                if k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX, v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k), ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(
                                            i + 1) + "]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(
                                            _dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i + 1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(
                                                        i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_copd_register_operation(self, l_):

        # 慢阻肺病登记 - 操作

        try:
            # 操作
            if l_[1] == '专项登记':
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + l_[1] + "'])[position()=" + str(self.__phs_copd_operation(l_[1], l_)) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)
            elif l_[1] == '编辑':
                ele = Web_PO.getSuperEleByX("//th[text()=' 慢性阻塞性肺患者管理卡 ']", "../..")
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                for k, v in l_[0].items():
                    if k in [' 居住地址 ']:
                        self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[2]/div/div/div/div/div/input", _dropdownByX, v[0])
                        self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[3]/div/div/div/div/div/input", _dropdownByX, v[1])
                        self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v[2])
                        self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[5]/div/div/div/div/div/input", _dropdownByX, v[3])
                        self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[6]/div/div/div/div/div/input", _dropdownByX, v[4])
                        Web_PO.eleSetTextEnterByX(self._eleTd(ele, k), ".//td[7]/div/div/div/input", v[5])
                    elif k in ['终止管理原因']:
                        if l_[0][' 是否终止管理 '] == "是":
                            Web_PO.eleSetTextEnterByX(self._eleSpan(ele, k, '../..'), ".//td[2]/div/div/div/input", v)
                    elif k in ['终止管理日期']:
                        if l_[0][' 是否终止管理 '] == "是":
                            self._dropdownDateSingle(self._eleSpan(ele, k, '../..'), ".//td[6]/div/div/div/input", v)
                    elif k in [' 是否终止管理 ']:
                        Web_PO.eleRadioRightLabel(self._eleTd(ele, k), ".//td[4]/div/div/div/label", v)
                    elif k in ['建卡医生']:
                        self._eleClkDropdown(self._eleSpan(ele, k, '../..'), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v)
                    elif k in [' 确诊日期 ']:
                        self._dropdownDateSingle(self._eleTd(ele, k), ".//div[1]/input", v)
                    elif k in ['建卡时间']:
                        self._dropdownDateSingle(self._eleSpan(ele, k, '../..'), ".//td[2]/div/div/div/input", v)
                ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)
            elif l_[1] == '删除':
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + l_[1] + "'])[position()=" + str(self.__phs_diabetes_operation('详情\n编辑\n删除', l_)) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)
                Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 二次确认
            else:
                print("error, 无法操作!")
            self.logger.info("点击" + str(l_))
        except:
            self.logger.error(str(l_) + "失败！")




    # todo 2.4.2  基本公卫 - 慢性阻塞性肺病管理 - 慢阻肺病专项

    def phs_copd_project_query(self, d_):

        # 慢阻肺病专项 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '建卡医生']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['是否终止管理', '随访提醒分类', '档案状态', '随访评价结果']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期范围']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['上次随访日期', '下次随访日期', '建卡日期', '建档日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/div/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX, v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), ".//div[3]/div/div/input", v[2])
                elif k in ['档案管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k),  ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li["+str(i+1)+"]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i+1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_copd_project_export(self, varFile):

        # 慢阻肺病专项 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击导出

        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)

    def phs_copd_project_operation(self, d_):

        # 慢阻肺病专项 - 操作

        try:
            if "index" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(self._phs_diabetes_operation('详情\n随访', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '详情' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '编辑':
                    ele2 = Web_PO.getSuperEleByX("//span[text()='编辑']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

                    ele = Web_PO.getSuperEleByX("//th[text()=' 慢性阻塞性肺患者管理卡 ']", "../..")
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                    for k, v in d_['value'].items():
                        if k in [' 居住地址 ']:
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[2]/div/div/div/div/div/input", _dropdownByX, v[0])
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[3]/div/div/div/div/div/input", _dropdownByX, v[1])
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v[2])
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[5]/div/div/div/div/div/input", _dropdownByX, v[3])
                            self._clkDropdownNoPath(self._eleTd(ele, k), ".//td[6]/div/div/div/div/div/input", _dropdownByX, v[4])
                            Web_PO.eleSetTextEnterByX(self._eleTd(ele, k), ".//td[7]/div/div/div/input", v[5])
                        elif k in ['终止管理原因']:
                            if d_['value'][' 是否终止管理 '] == "是":
                                Web_PO.eleSetTextEnterByX(self._eleSpan(ele, k, '../..'), ".//td[2]/div/div/div/input", v)
                        elif k in ['终止管理日期']:
                            if d_['value'][' 是否终止管理 '] == "是":
                                self._dropdownDateSingle(self._eleSpan(ele, k, '../..'), ".//td[6]/div/div/div/input", v)
                        elif k in [' 是否终止管理 ']:
                            Web_PO.eleRadioRightLabel(self._eleTd(ele, k), ".//td[4]/div/div/div/label", v)
                        elif k in ['建卡医生']:
                            self._eleClkDropdown(self._eleSpan(ele, k, '../..'), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v)
                        elif k in [' 确诊日期 ']:
                            self._dropdownDateSingle(self._eleTd(ele, k), ".//div[1]/input", v)
                        elif k in ['建卡时间']:
                            self._dropdownDateSingle(self._eleSpan(ele, k, '../..'), ".//td[2]/div/div/div/input", v)
                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['operate'] == '随访' and "operate2" in d_['index']:
                # 三种操作，编辑(第一个)、新增、引入上次新增

                if d_['index']['operate2'] == '新增':
                    # 判断血压是否有值，如果没值，表示一条随访记录都没有，编辑(第一个)
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    s_temp = Web_PO.eleGetShadowByXByC(ele, ".//div[4]/div[1]/div/div[1]/input", "div:nth-last-of-type(1)")
                    if s_temp != '':
                        ele3 = Web_PO.getSuperEleByX("//span[text()='新增']", ".")
                        Web_PO.eleClkByX(ele3, ".", 2)
                if d_['index']['operate2'] == '引入上次新增':
                    ele3 = Web_PO.getSuperEleByX("//span[text()='引入上次新增']", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

                # 新增
                self.__tnb(d_)

            else:
                print("error, 无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")



    # todo 2.4.3 基本公卫 - 慢性阻塞性肺病管理 - 慢阻肺病随访

    def phs_copd_visit_query(self, d_):

        # 慢阻肺病随访 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '随访医生']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
                elif k in ['血氧饱和度']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['空腹血糖']:
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访方式', '是否终止管理', '数据源', '随访评价结果']:
                    self._eleClkDropdown(self._eleLabel(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期范围']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访日期']:
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/div/input", v[0])
                    self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    self._clkDropdownNoPath(self._eleLabel(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX,
                                            v[0])
                    self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), ".//div[2]/div/div/div/div/input",
                                            _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                    Web_PO.eleClkByX(self._eleLabel(ele, k), ".//input")
                    l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    # 卫健局
                    if v == l_1:
                        # print(l_1)  # ['招远市卫健局']
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                    else:
                        Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                        l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                        # 卫生院
                        if len(v) == 1:
                            # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(
                                            i + 1) + "]/label/span[1]/span")
                        else:
                            # 卫生室
                            if v[0] in l_2:
                                for i in range(len(l_2)):
                                    if l_2[i] == v[0]:
                                        Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i + 1) + "]")
                                        l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                        if v[1] in l_3:
                                            # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                            for i in range(len(l_3)):
                                                if l_3[i] == v[1]:
                                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(
                                                        i + 1) + "]/label/span[1]/span")
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_copd_visit_export(self, varFile):

        # 慢阻肺病随访 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击导出

        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)

    def phs_copd_visit_operation(self, l_):

        # 糖尿病随访 - 操作

        try:
            # 操作
            if l_[1] == '详情':
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + l_[1] + "'])[position()=" + str(self.__phs_diabetes_operation('详情\n编辑\n删除', l_)) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)
            elif l_[1] == '详情编辑':
                ele = Web_PO.getSuperEleByX("//div[text()='高血压患者管理卡']", "..")
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                ele2 = Web_PO.getSuperEleByX("//span[text()='编辑']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)
                for k, v in l_[0].items():
                    if k in [' 居住地址 ']:
                        self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'),
                                                ".//div[1]/div[2]/div/div/div/div/div/input", _dropdownByX, v[0])
                        self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'),
                                                ".//div[2]/div[1]/div/div/div/div/div/input", _dropdownByX, v[1])
                        self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'),
                                                ".//div[2]/div[2]/div/div/div/div/div/input", _dropdownByX, v[2])
                        self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'),
                                                ".//div[3]/div[1]/div/div/div/div/div/input", _dropdownByX, v[3])
                        self._clkDropdownNoPath(self._eleDiv(ele, k, '../..'),
                                                ".//div[3]/div[2]/div/div/div/div/div/input", _dropdownByX, v[4])
                        Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k, '../..'), ".//div[4]/div[2]/div/div/div/input",
                                                  v[5])
                    elif k in [' 建卡医疗机构 ']:
                        Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//input", v)
                    elif k in [' 终止管理原因 ']:
                        if l_[0][' 是否终止管理 '] == "是":
                            Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//input", v)
                    elif k in [' 终止管理日期 ']:
                        if l_[0][' 是否终止管理 '] == "是":
                            self._dropdownDateSingle(self._eleDiv(ele, k), ".//div[1]/input", v)
                    elif k in [' 管理级别 ']:
                        Web_PO.eleRadioLeftLabel(self._eleDiv(ele, k), ".//div[2]/div/div/div", v)
                    elif k in [' 是否终止管理 ']:
                        Web_PO.eleRadioRightLabel(self._eleDiv(ele, k), ".//div[2]/div/div/div/label", v)
                    elif k in [' 建卡医生 ']:
                        self._eleClkDropdown(self._eleDiv(ele, k), ".//input", _dropdownByX, v)
                    elif k in [' 确诊日期 ', ' 建卡时间 ']:
                        self._dropdownDateSingle(self._eleDiv(ele, k), ".//div[1]/input", v)
                ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)
            elif l_[1] == '删除':
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + l_[1] + "'])[position()=" + str(self.__phs_diabetes_operation('详情\n编辑\n删除', l_)) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)
                Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 二次确认
            else:
                print("error, 无法操作!")
            self.logger.info("点击" + str(l_))
        except:
            self.logger.error(str(l_) + "失败！")








    # todo 2.12.1 基本公卫 - 健康教育 - 健康教育活动

    def phs_healtheducation_healthactivity_query(self, d_):

        # 健康教育活动 - 查询

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele = Web_PO.getSuperEleByX("//label[text()='活动日期']", "../../../..")  # form

        for k, v in d_.items():
            if k in ['活动地点', '活动形式', '活动主题', '主讲人']:
                Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//input", v)
            elif k in ['活动日期']:
                 self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[1]/div/input", v[0])
                 self._dropdownDateSingle(self._eleLabel(ele, k), ".//div[3]/div/input", v[1])

        Web_PO.eleClkByX(ele, ".//button[1]")  # 查询

    def phs_healtheducation_healthactivity_new(self, d_):

        # 健康教育活动 - 新增

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele2 = Web_PO.getSuperEleByX("//label[text()='活动日期']", "../../../../..")
        Web_PO.eleClkByX(ele2, ".//button[2]")  # 新增
        ele = Web_PO.getSuperEleByX("//div[text()='活动时间']", "../..")  # form
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            if k in ['主讲人', '活动内容', '活动总结评价', '填表人']:
                Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//input", v)
            if k in ['活动地点', '活动人数', '主讲人单位', '负责人', '健康教育资源发放数量']:
                Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//div[4]/div/div/div/input", v)
            if k in ['组织者', '职称']:
                Web_PO.eleSetTextEnterByX(self._eleDiv(ele, k), ".//div[6]/div/div/div/input", v)
            elif k in ['活动时间']:
                self._dropdownDateSingle(self._eleDiv(ele, k), ".//input", v)
            elif k in ['填表时间']:
                self._dropdownDateSingle(self._eleDiv(ele, k), ".//div[6]/div/div/div/input", v)
            elif k in ['活动形式', '活动主题', '接受健康教育人员类别']:
                self._eleClkDropdown(self._eleDiv(ele, k), ".//input", _dropdownByX, v)
            elif k in ['健康教育资源发放种类']:
                Web_PO.eleRadioSplitLabels(self._eleDiv(ele, k), ".//div[2]/div/div/div", v)
            elif k in ['存档资料类型']:
                if v[0] != []:
                    Web_PO.eleCheckboxSplitLabels(self._eleDiv(ele, k), ".//div[2]/div[1]/div/div/div/div", v[0])
                if v[1] != []:
                    Web_PO.upFile("/html/body/div[1]/div/div[3]/section/div/form/div[10]/div[2]/div[2]/div/div/div/ul/div",
                                  v[1])



    # todo 2.13.1 基本公卫 - 健康行为积分 - 本年度未评

    def phs_hbp_noassessdata_query(self, d_):

        # 本年度未评 - 查询

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele = Web_PO.getSuperEleByX("//label[text()='管理机构']", "../../../..")  # form
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            if k in ['姓名', '身份证号']:
                Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div/div/input", v)
            elif k in ['人群分类']:
                Web_PO.eleCheckboxLabels(self._eleLabel(ele, k), ".//span[2]", v)
            elif k in ['档案状态']:
                self._eleClkDropdown(self._eleLabel(ele, k), ".//div/div/div/div/input", _dropdownByX, v)
            elif k in ['现住址']:
                self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), "./div[1]/div/div/div/div/input", _dropdownByX, v[0])
                self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), "./div[2]/div/div/div/div/input", _dropdownByX, v[1])
                Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), "./div[3]/div/div/input", v[2])
            elif k in ['管理机构']:
                _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                Web_PO.eleClkByX(self._eleLabel(ele, k), ".//div/div/div/input")
                l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                # 卫健局
                if v == l_1:
                    # print(l_1)  # ['招远市卫健局']
                    Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                else:
                    Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                    # 卫生院
                    if len(v) == 1:
                        # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                        if v[0] in l_2:
                            for i in range(len(l_2)):
                                if l_2[i] == v[0]:
                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(
                                        i + 1) + "]/label/span[1]/span")
                    else:
                        # 卫生室
                        if v[0] in l_2:
                            for i in range(len(l_2)):
                                if l_2[i] == v[0]:
                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i + 1) + "]")
                                    l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                    if v[1] in l_3:
                                        # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                        for i in range(len(l_3)):
                                            if l_3[i] == v[1]:
                                                Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(
                                                    i + 1) + "]/label/span[1]/span")

        Web_PO.eleClkByX(ele, "./div[2]/div[2]/div/button[1]", 2)  # 点击查询

        # 2 获取查询数量
        s_ = self._getQty()
        return s_

    def phs_hbp_noassessdata_new(self, d_):

        # 本年度未评 - 2025年居民健康行为积分卡

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        # ele = Web_PO.getSuperEleByX("//div[text()='2025年居民健康行为积分卡']", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        varTrQty = Web_PO.eleGetQtyByXs(ele2, ".//tr")

        for k, v in d_.items():
            if k in ['积分']:
                l_ = []
                l_all = []
                for i in range(varTrQty-1):
                    varTdQty = Web_PO.eleGetQtyByXByXs(ele2, "./tr[" + str(i+1) + "]", "./td")
                    # print(varTdQty)
                    if varTdQty == 10:
                        varCrowd = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]")
                        varSeriea = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[2]")
                        varActionName = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[3]")
                    else:
                        varSeriea = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]")
                        varActionName = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[2]")
                    l_.append(varCrowd)
                    l_.append(varSeriea)
                    l_.append(varActionName)
                    l_all.append(l_)
                    l_ = []
                # print(l_all)  # [['所有人', '1', '健康素养'], ['所有人', '2', '健康教育'],...
                d_1 = dict(enumerate(l_all, start=1))
                # print(d_1)  # {1: ['所有人', '1', '健康素养'], 2: ['所有人', '2', '健康教育'],...
                for i in range(len(v)):
                    for k1, v1 in d_1.items():
                        if v1 == v[i][0]:
                            varTdQty = Web_PO.eleGetQtyByXByXs(ele2, "./tr[" + str(k1) + "]", "./td")
                            Web_PO.eleScrollViewByX(ele2, "./tr[" + str(k1) + "]/td["+ str(varTdQty-2) + "]/div/div/div/div/input")
                            self._dropdownDateSingle(ele2, ".//tr[" + str(k1) + "]/td["+ str(varTdQty-2) + "]/div/div/div/div/input", v[i][1])
                            Web_PO.eleSetTextByX(ele2, ".//tr[" + str(k1) + "]/td["+ str(varTdQty-1) + "]/div/div/div/div/input", v[i][2])

            elif k in ['评分日期']:
                self._dropdownDateSingle(ele2, ".//tr[" + str(varTrQty) + "]/td[2]/div/div/div/div/input", v)

            elif k in ['是否兑换']:
                self._eleClkDropdown(ele2, ".//tr[" + str(varTrQty) + "]/td[3]/div/div/div[1]/div/div/div/div/div/input", _dropdownByX, v)

        Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/button[2]")  # 取消
        # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/button[1]")  # 保存

    def phs_hbp_noassessdata_batch(self, d_):
        # Gw_PO.noScored_batch({'身份证号': ['110101194301191302', '340203202407018290']})

        # 本年度未评 - 批量评分
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        varTrQty = Web_PO.eleGetQtyByXs(ele2, ".//tr")
        l_ = []
        for k, v in d_.items():
            if k in ['身份证号']:
                # 1 勾选
                if isinstance(v, str):
                    # 全勾选
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/main/div[2]/div/div[1]/div[2]/table/thead/tr/th[1]/div/label")
                else:
                    # 按照身份证勾选
                    for i in range(varTrQty):
                        varIdcard = Web_PO.eleGetTextByX(ele2, "./tr[" + str(i+1) + "]/td[5]/div")
                        l_.append(varIdcard)
                    d_1 = dict(enumerate(l_, start=1))
                    # print(d_1)  # {1: '341226199708114773', 2: '110101194301191302',
                    for k1, v1 in d_1.items():
                        if v1 in v:
                            Web_PO.eleClkByX(ele2, "./tr[" + str(k1) + "]/td[1]/div/label")
                # 2 点击批量评分
                ele = Web_PO.getSuperEleByX("//label[text()='管理机构']", "../../../..")  # form
                Web_PO.eleClkByX(ele, "./div[2]/div[2]/div/button[2]", 2)  # 点击批量评分
                varText = Web_PO.getTextByX("/html/body/div[1]/div/div[3]/section/div/div/div/div/div[2]/div")
                print(varText) # 批量执行完成，成功1条数据，失败0条数据
                varNum1 = Web_PO.getTextByX("/html/body/div[1]/div/div[3]/section/div/div/div/div/div[2]/div/span[1]")
                print(varNum1) # 1
                varNum2 = Web_PO.getTextByX("/html/body/div[1]/div/div[3]/section/div/div/div/div/div[2]/div/span[2]")
                print(varNum2) # 0
                Web_PO.eleClkByX("/html/body/div[1]/div/div[3]/section/div/div/div/div/div[3]/div/button") # 关闭



    # todo 2.13.2 基本公卫 - 健康行为积分 - 评分信息查询

    def phs_hbp_assessdata_query(self, d_):

        # 评分信息查询 - 查询

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele = Web_PO.getSuperEleByX("//label[text()='管理机构']", "../../../..")  # form
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            if k in ['姓名', '身份证号']:
                Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div/div/input", v)
            elif k in ['得分范围']:
                Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div/div/div[1]/div/input", v[0])
                Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k), ".//div/div/div[3]/div/input", v[1])
            elif k in ['评分日期']:
                self._dropdownDateSingle(self._eleLabel(ele, k), "./div/div/div[1]/div/input", v[0])
                self._dropdownDateSingle(self._eleLabel(ele, k), "./div/div/div[3]/div/input", v[1])
            elif k in ['人群分类']:
                Web_PO.eleCheckboxLabels(self._eleLabel(ele, k), ".//span[2]", v)
            elif k in ['档案状态', '是否兑换']:
                self._eleClkDropdown(self._eleLabel(ele, k), ".//div/div/div/div/input", _dropdownByX, v)
            elif k in ['现住址']:
                self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), "./div[1]/div/div/div/div/input", _dropdownByX, v[0])
                self._clkDropdownNoPath(self._eleLabel(ele, k, "../.."), "./div[2]/div/div/div/div/input", _dropdownByX, v[1])
                Web_PO.eleSetTextEnterByX(self._eleLabel(ele, k, "../.."), "./div[3]/div/div/input", v[2])
            elif k in ['管理机构']:
                _dropdownByX2 = "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']"
                Web_PO.eleClkByX(self._eleLabel(ele, k), ".//div/div/div/input")
                l_1 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div/div[1]/ul/li")
                # 卫健局
                if v == l_1:
                    # print(l_1)  # ['招远市卫健局']
                    Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li/label/span[1]/span")
                else:
                    Web_PO.clkByX(_dropdownByX2 + "/div/div/div[1]/ul/li")
                    l_2 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[2]/div[1]/ul/li")
                    # 卫生院
                    if len(v) == 1:
                        # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                        if v[0] in l_2:
                            for i in range(len(l_2)):
                                if l_2[i] == v[0]:
                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(
                                        i + 1) + "]/label/span[1]/span")
                    else:
                        # 卫生室
                        if v[0] in l_2:
                            for i in range(len(l_2)):
                                if l_2[i] == v[0]:
                                    Web_PO.clkByX(_dropdownByX2 + "/div/div[2]/div[1]/ul/li[" + str(i + 1) + "]")
                                    l_3 = Web_PO.getTextByXs(_dropdownByX2 + "/div/div[3]/div[1]/ul/li")
                                    if v[1] in l_3:
                                        # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                                        for i in range(len(l_3)):
                                            if l_3[i] == v[1]:
                                                Web_PO.clkByX(_dropdownByX2 + "/div/div[3]/div[1]/ul/li[" + str(
                                                    i + 1) + "]/label/span[1]/span")

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询

        # 2 获取查询数量
        s_ = self._getQty()
        return s_

    def phs_hbp_assessdata_modify(self, d_):

        # 评分信息查询 - 修改

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        varTrQty = Web_PO.eleGetQtyByXs(ele2, ".//tr")

        for k, v in d_.items():
            if k in ['积分']:
                l_ = []
                l_all = []
                for i in range(varTrQty-1):
                    varTdQty = Web_PO.eleGetQtyByXByXs(ele2, "./tr[" + str(i+1) + "]", "./td")
                    # print(varTdQty)
                    if varTdQty == 10:
                        varCrowd = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]")
                        varSeriea = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[2]")
                        varActionName = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[3]")
                    else:
                        varSeriea = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]")
                        varActionName = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[2]")
                    l_.append(varCrowd)
                    l_.append(varSeriea)
                    l_.append(varActionName)
                    l_all.append(l_)
                    l_ = []
                # print(l_all)  # [['所有人', '1', '健康素养'], ['所有人', '2', '健康教育'],...
                d_1 = dict(enumerate(l_all, start=1))
                # print(d_1)  # {1: ['所有人', '1', '健康素养'], 2: ['所有人', '2', '健康教育'],...
                for i in range(len(v)):
                    for k1, v1 in d_1.items():
                        if v1 == v[i][0]:
                            varTdQty = Web_PO.eleGetQtyByXByXs(ele2, "./tr[" + str(k1) + "]", "./td")
                            Web_PO.eleScrollViewByX(ele2, "./tr[" + str(k1) + "]/td["+ str(varTdQty-2) + "]/div/div/div/div/input")
                            self._dropdownDateSingle(ele2, ".//tr[" + str(k1) + "]/td["+ str(varTdQty-2) + "]/div/div/div/div/input", v[i][1])
                            Web_PO.eleSetTextByX(ele2, ".//tr[" + str(k1) + "]/td["+ str(varTdQty-1) + "]/div/div/div/div/input", v[i][2])

            elif k in ['评分日期']:
                self._dropdownDateSingle(ele2, ".//tr[" + str(varTrQty) + "]/td[2]/div/div/div/div/input", v)

            elif k in ['是否兑换']:
                self._eleClkDropdown(ele2, ".//tr[" + str(varTrQty) + "]/td[3]/div/div/div[1]/div/div/div/div/div/input", _dropdownByX, v)

        Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/button[2]")  # 取消
        # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/button[1]")  # 保存

    def phs_hbp_assessdata_detail(self):

        # 评分信息查询 - 详情

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        a = Web_PO.eleGetTextByXs(ele, ".//div")
        b = Web_PO.eleGetTextByXs(ele, ".//span")
        print("a", a)
        print("b", b)









    def yjzx(self, varDisease, varProject):

        # 已建专项

        l_disease = Web_PO.getTextByXs("//button/span")
        # print(l_disease)
        for i in range(len(l_disease)):
            if l_disease[i] == varDisease:
                Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/button[" + str(i+1) + "]", 2)
                if varDisease == '高血压专项':
                    if varProject == '专项登记':
                        Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]", 2)
                        # 高血压患者管理卡
                        print(self.hypertensionPatientCard())
                if varDisease == '糖尿病专项':
                    if varProject == '专项登记':
                        Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]", 2)
                        # 高血压患者管理卡
                        print(self.diabetesPatientCard())
                if varDisease == '高血脂专项':
                    if varProject == '专项登记':
                        Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]", 2)
                        # 高血脂患者管理卡
                        print(self.hyperlipidemiaPatientCard())
                break

    def hypertensionPatientCard(self):

        # 高血压患者管理卡

        # 获取字段名
        l_div = Web_PO.getTextByXs("//div[@class='table_line']/div")
        # print(l_div)  # ['管理卡号', '信息来源\n健康档案\n首诊测压\n普查\n门诊就诊\n其他', '', '档案编号'...
        l_div.remove('吸烟情况\n吸烟状况\n戒烟开始日期\n开始吸烟年龄\n岁')
        l_div.remove("未服药血压\nmmHg\nmmHg")
        # print(l_div)  # ['管理卡号', '信息来源\n健康档案\n首诊测压\n普查\n门诊就诊\n其他', '', '档案编号'...

        # 获取radio或checkbox状态
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"

        d_radio = {}
        d_radio1 = {}
        l_2 = []
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_div[i] = l_div[i].replace('饮酒情况\n饮酒频率\n从不\n偶尔\n经常\n每天\n开始饮酒年龄\n岁\n是否饮酒过量\n是\n否','饮酒频率\n从不\n偶尔\n经常\n每天\n是\n否')
                l_div[i] = l_div[i].replace('体育锻炼\n锻炼频率\n每天\n每周一次以上\n偶尔\n不运动','锻炼频率\n每天\n每周一次以上\n偶尔\n不运动')
                l_div[i] = l_div[i].replace('有\n无\n职业暴露危险因素','职业病危害因素接触史\n有\n无')
                l_div[i] = l_div[i].replace('有危害因素的具体职业\n从事职业时长\n年\n防护措施\n无\n有','防护措施\n无\n有')
                l_1 = l_div[i].split("\n")
                l_2.append(l_1.pop(0))
                # print(l_1)  # ['健康档案', '首诊测压', '普查', '门诊就诊', '其他']

                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                    # l_2.append(l_1[i].split("\n")[0])
                # print(l_2)
                d_box = dict(zip(l_1, l_bool))
                d_radio[l_div[ele_n]] = d_box

        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_radio1 = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print(d_radio1)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        l_field = ['管理卡号','其他情况说明','档案编号', '姓名', '性别', '出生日期', '联系电话',
                    '身份证号码', '居住地址', '身高(cm)', '体重(kg)', '吸烟状况', '戒烟开始日期', '开始吸烟年龄',
                    '开始饮酒年龄', '职业暴露危险因素', '有危害因素的具体职业', '从事职业时长',
                    '毫米汞柱起','毫米汞柱始','确诊日期', '终止管理日期', '终止管理原因', '建卡时间', '建卡医生', '建卡医疗机构']
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        # print(l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(8))
        l_input.insert(8, ll)

        d_other = dict(zip(l_field, l_input))
        # print(d_other)  # {'管理卡号': '135', '其他情况说明': '', ...

        d_other.update(d_radio1)
        return d_other

    def diabetesPatientCard(self):

        # 糖尿病患者管理卡

        # 1，获取所有字段名和checkbox值
        l_trtd = Web_PO.getTextByXs("//tr/td")
        l_trtd = [i for i in l_trtd if i != '']
        # print(l_trtd)

        # 2.1，获取非checkbox字段
        ll = []
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                ll.append(l_trtd[ele_before_n])
        l_normalfield = [i for i in l_trtd if "\n" not in i]
        for i in range(len(ll)):
            l_normalfield.remove(ll[i])
        # print(l_normalfield)  # ['档案编号', '姓名', '性别', '出生日期', '身份证号', '职业', '居住地址', '身高(cm)', '体重(kg)', '确诊日期', '终止管理日期', '终止管理原因', '建卡时间', '建卡医生', '建卡医疗机构']
        # 2.2，获取非checkbox值
        l_normalValue = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        # print(l_normalValue)  # ['37068500200200014', '6月26日测试', '女', '1960-01-19'
        # 将居住地址6个值（索引5）组成列表
        l_tmp = []
        for i in range(6):
            l_tmp.append(l_normalValue.pop(5))
        l_normalValue.insert(5, l_tmp)
        # 2.3，合成非checkbox字典
        d_normal = dict(zip(l_normalfield, l_normalValue))
        # print(d_normal)  # {'档案编号': '543912fd978b4634bae81a7b556b95cb', '姓名': '6月26日测试', '性别': '女', '出生日期': '1960-01-19', '身份证号': '110101196001193209', '居住地址': ['山东省', '烟台市', '招远市', '泉山街道', '魁星东社区居民委员会', '1'], '身高(cm)': '145', '体重(kg)': '67', '其他特殊类型糖尿病说明': '', '确诊日期': '2024-06-13', '终止管理日期': '1900-01-01', '终止管理原因': '', '建卡时间': '2024-06-28', '建卡医生': '卫健委', '建卡医疗机构': '招远市卫健局'}

        # 3.1，获取checkbox值(# el-radio__input is-checked)
        l_checkbox = Web_PO.isBooleanAttrValueListByX("//div/label/span[1]", 'class',
                                                      'el-radio__input is-disabled is-checked')
        # print(l_checkbox)  # ['False', 'True', 'False', 'False', ...
        # 3.2，合成checkbox字典
        d_checkbox = {}
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                l_1 = l_trtd[i].split("\n")
                # print(l_1)  # ['健康档案', '社区门诊', '流行病学调查', '其他']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_checkbox.pop(0))
                l_all = dict(zip(l_1, l_bool))
                d_checkbox[l_trtd[ele_before_n]] = l_all
        # print(d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 4，按页面字段名顺序输出
        d_result = {}
        l_trtd1 = [i for i in l_trtd if "\n" not in i and i != '']
        for i in range(len(l_trtd1)):
            for k, v in d_normal.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
        return d_result

    def hyperlipidemiaPatientCard(self):

        # 高血脂患者管理卡

        # 1，获取所有字段名和checkbox值
        l_trtd = Web_PO.getTextByXs("//tr/td")
        l_trtd = [i for i in l_trtd if i != '']
        # print(l_trtd)

        # 2.1，获取非checkbox字段
        ll = []
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                ll.append(l_trtd[ele_before_n])
        l_normalfield = [i for i in l_trtd if "\n" not in i]
        for i in range(len(ll)):
            l_normalfield.remove(ll[i])
        # print(l_normalfield)  # ['档案编号', '姓名', '性别', '出生日期', '身份证号', '职业', '居住地址', '身高(cm)', '体重(kg)', '确诊日期', '终止管理日期', '终止管理原因', '建卡时间', '建卡医生', '建卡医疗机构']
        # 2.2，获取非checkbox值
        l_normalValue = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        # print(l_normalValue)  # ['37068500200200014', '6月26日测试', '女', '1960-01-19'
        # 将居住地址6个值（索引5）组成列表
        l_tmp = []
        for i in range(6):
            l_tmp.append(l_normalValue.pop(6))
        l_normalValue.insert(6, l_tmp)
        # 2.3，合成非checkbox字典
        d_normal = dict(zip(l_normalfield, l_normalValue))
        # print(d_normal)  # {'档案编号': '543912fd978b4634bae81a7b556b95cb', '姓名': '6月26日测试', '性别': '女', '出生日期': '1960-01-19', '身份证号': '110101196001193209', '居住地址': ['山东省', '烟台市', '招远市', '泉山街道', '魁星东社区居民委员会', '1'], '身高(cm)': '145', '体重(kg)': '67', '其他特殊类型糖尿病说明': '', '确诊日期': '2024-06-13', '终止管理日期': '1900-01-01', '终止管理原因': '', '建卡时间': '2024-06-28', '建卡医生': '卫健委', '建卡医疗机构': '招远市卫健局'}

        # 3.1，获取checkbox值(# el-radio__input is-checked)
        l_checkbox = Web_PO.isBooleanAttrValueListByX("//div/label/span[1]", 'class', 'el-radio__input is-checked')
        # print(l_checkbox)  # ['False', 'True', 'False', 'False', ...
        # 3.2，合成checkbox字典
        d_checkbox = {}
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                l_1 = l_trtd[i].split("\n")
                # print(l_1)  # ['健康档案', '社区门诊', '流行病学调查', '其他']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_checkbox.pop(0))
                l_all = dict(zip(l_1, l_bool))
                d_checkbox[l_trtd[ele_before_n]] = l_all
        # print(d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 4，按页面字段名顺序输出
        d_result = {}
        l_trtd1 = [i for i in l_trtd if "\n" not in i and i != '']
        for i in range(len(l_trtd1)):
            for k,v in d_normal.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
        return d_result

    def runUser(self, *varUsername):

        l_username = Web_PO.getTextByXs("//tr/td[1]/div")
        # print(l_username) # ['零跑', '测试', '黎明', '李永波', '胡军', '张建民', '舒雅有', '赵爽', '陈平安']

        if len(varUsername) == 1 and varUsername[0] != 'all':
            for i in range(len(l_username)):
                if l_username[i] == varUsername[0]:
                    # print(l_username[i])
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[1]/div', 2)
                    self.residentHealthRecord(l_username[i])
        elif len(varUsername) > 1:
            print(varUsername)
            for i in range(len(l_username)):
                for j in range(len(varUsername)):
                    if l_username[i] == varUsername[j]:
                        # print(l_username[i])
                        Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[1]/div', 2)
                        self.residentHealthRecord(l_username[i])
                        # 关闭当前标签
                        l_a = Web_PO.getAttrValueByXs("//a",'href')
                        # print(l_a)
                        for i in range(len(l_a)):
                            if "http://192.168.0.203:30080/#/phs/personalAddOrUpdate/addOrUpdate" in l_a[i]:
                                Web_PO.clkByX('/html/body/div[1]/div/div[3]/div[1]/div/div/div[1]/div/a[' + str(i + 1) + ']/span', 2)
        elif len(varUsername) == 1 and varUsername[0] == 'all':
            print(l_username)
            for i in range(len(l_username)):
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[1]/div', 2)
                self.residentHealthRecord(l_username[i])
                # 关闭当前标签
                l_a = Web_PO.getAttrValueByXs("//a", 'href')
                for i in range(len(l_a)):
                    if "http://192.168.0.203:30080/#/phs/personalAddOrUpdate/addOrUpdate" in l_a[i]:
                        Web_PO.clkByX(
                            '/html/body/div[1]/div/div[3]/div[1]/div/div/div[1]/div/a[' + str(i + 1) + ']/span', 2)

    def _residentHealthRecord(self, l_div, i, varDisease, varDiseaseName, varDiseaseTime):

        #  _residentHealthRecord(self, l_div, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
        if l_div[i] == varDisease:
            ele_n = l_div.index(l_div[i])
            ele_after_n = ele_n + 1
            a = len(l_div[ele_after_n].split("\n"))
            # print(a)
            if a == 1:
                l_div[ele_after_n] = varDiseaseName
                ele_n = l_div.index(l_div[ele_after_n])
                ele_after_n = ele_n + 1
                l_div.insert(ele_after_n, varDiseaseTime)
            else:
                l_ = l_div[ele_after_n].split("\n")
                # print(l_)  # ['手术名称', '手术名称', '手术名称']
                if len(l_) > 1:
                    l_div[ele_after_n] = varDiseaseName + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, varDiseaseTime + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(len(l_) - 1):
                        l_div.insert(ele_after_n + j, varDiseaseName + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, varDiseaseTime + str(j + 2))

    def residentHealthRecord(self, varUsername):

        # 居民健康档案

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//div[@class='table_line']/div")
        print("1.1 原始l_div => ", l_div)

        # 1.2 清洗字段
        # 删除
        l_div = [i for i in l_div if i != '']
        for i in range(len(l_div)):
            if l_div[i] == '现住址必填':
                l_div.remove('现住址必填')
            if l_div[i] == '关联户主':
                l_div.remove('关联户主')
        l_div.remove('城镇职工基本医疗保险')
        l_div.remove('城镇居民基本医疗保险')
        l_div.remove('贫困救助')

        # 修改
        for i in range(len(l_div)):
            if l_div[i] == '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾\n残疾情况必填':
                l_div[i] = '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾'
            if l_div[i] == '商业医疗保险\n全公费\n全自费\n其他':
                l_div[i] = '医疗费用支付方式\n城镇职工基本医疗保险'

        # 插入
        l_div[l_div.index('遗传病史\n有\n无') + 1] = '遗传病史疾病名称'
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 1, '职工医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 2, '医疗费用支付方式2\n城镇居民基本医疗保险')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 3, '居民医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 4, '医疗费用支付方式3\n贫困救助')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 5, '贫困救助卡号')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 6, '医疗费用支付方式4\n商业医疗保险\n全公费\n全自费\n其他')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 7, '医疗费用支付方式备注')

        # 动态自增字段 （33是随意值，确保遍历不中断）
        for i in range(len(l_div) + 33):
            if l_div[i] == '更新内容':
                break

            # 既往史，动态自增字段（选择恶性肿瘤时，显示输入框）
            self._residentHealthRecord(l_div, i, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
            self._residentHealthRecord(l_div, i, '手术\n有\n无', '手术名称', '手术时间')
            self._residentHealthRecord(l_div, i, '外伤\n有\n无', '外伤名称', '外伤时间')
            self._residentHealthRecord(l_div, i, '输血\n有\n无', '输血原因', '输血时间')

            # 家族史，动态自增字段（选择恶性肿瘤时，显示输入框）
            if l_div[i] == '有\n无':
                l_div[i] = '家族史\n有\n无'
                ele_n = l_div.index(l_div[i])
                ele_after_n = ele_n + 1
                if l_div[ele_after_n] == '疾病名称\n与本人关系':
                    l_div[ele_after_n] = '家族史疾病名称'
                    l_div.insert(ele_after_n + 1, "与本人关系")
                else:
                    n = int(len(l_div[ele_after_n].split("\n")) / 2)
                    l_div[ele_after_n] = '家族史疾病名称' + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, "与本人关系" + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(n - 1):
                        l_div.insert(ele_after_n + j, '家族史疾病名称' + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, "与本人关系" + str(j + 2))

        # print('1.2 清洗l_div => ', l_div)


        # 2 生成checkbox字典
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"
        # el-radio__input is-disabled is-checked
        d_radio = {}
        d_checkbox = {}
        l_2 = []
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4,d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 生成d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}


        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')

        # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
        if d_checkbox['药物过敏史']['其他药物过敏源'] == 'True':
            l_field.insert(l_field.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')
            # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
            l_textarea = Web_PO.getAttrValueByXs("//div/div/div/textarea", 'value')
            # 在input中23位置插入textarea值
            l_input.insert(23, l_textarea[0])
            print('3.3 l_textarea => ', l_textarea)
            # 更新div
            l_div.insert(l_div.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')

        # 当残疾情况中选择其他残疾时，显示输入框（其他残疾备注）
        if d_checkbox['残疾情况']['其他残疾'] == 'True':
            l_field.insert(l_field.index('残疾证号'), '其他残疾备注')
            # 更新div
            l_div.insert(l_div.index('残疾证号'), '其他残疾备注')

        # 如果既往史或家族史中疾病名称选择了恶性肿瘤，显示输入框（恶性肿瘤备注），插入XXX恶性肿瘤备注字段
        for i in range(len(l_input)):
            if l_input[i] == '恶性肿瘤':
                p = l_field[i - 5] + '恶性肿瘤备注'
                l_field.insert(i - 4, p)
                # 更新div
                for j in range(len(l_div)):
                    ele_n = l_div.index(l_field[i - 5])
                    l_div.insert(ele_n + 1, l_field[i - 5] + '恶性肿瘤备注')

        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(6))
        l_input.insert(6, ll)
        d_normal = dict(zip(l_field, l_input))
        # print(100, d_normal)  # {'管理卡号': '135', '其他情况说明': '', ...
        d_normal.update(d_checkbox)
        # print('混合结果 =>', d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ',  d_result)
        # return d_result

    def residentHealthRecord_update(self, varUsername, varTestUrl):

        # 居民健康档案(更新健康档案)

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//div[@class='table_line']/div")
        # print("1.1 原始l_div => ", l_div)

        # 1.2 清洗字段
        # 删除
        l_div = [i for i in l_div if i != '']
        for i in range(len(l_div)):
            if l_div[i] == '现住址必填':
                l_div.remove('现住址必填')
            if l_div[i] == '关联户主':
                l_div.remove('关联户主')
        l_div.remove('城镇职工基本医疗保险')
        l_div.remove('城镇居民基本医疗保险')
        l_div.remove('贫困救助')

        # 修改
        for i in range(len(l_div)):
            if l_div[i] == '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾\n残疾情况必填':
                l_div[i] = '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾'
            if l_div[i] == '商业医疗保险\n全公费\n全自费\n其他':
                l_div[i] = '医疗费用支付方式1\n城镇职工基本医疗保险'

        # 插入
        l_div[l_div.index('遗传病史\n有\n无') + 1] = '遗传病史疾病名称'
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 1, '职工医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 2, '医疗费用支付方式2\n城镇居民基本医疗保险')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 3, '居民医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 4, '医疗费用支付方式3\n贫困救助')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 5, '贫困救助卡号')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 6, '医疗费用支付方式4\n商业医疗保险\n全公费\n全自费\n其他')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 7, '医疗费用支付方式备注')

        # 动态自增字段 （33是随意值，确保遍历不中断）
        for i in range(len(l_div) + 33):
            if l_div[i] == '建档人':
                break

            # 既往史，动态自增字段（选择恶性肿瘤时，显示输入框）
            self._residentHealthRecord(l_div, i, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
            self._residentHealthRecord(l_div, i, '手术\n有\n无', '手术名称', '手术时间')
            self._residentHealthRecord(l_div, i, '外伤\n有\n无', '外伤名称', '外伤时间')
            self._residentHealthRecord(l_div, i, '输血\n有\n无', '输血原因', '输血时间')

            # 家族史，动态自增字段（选择恶性肿瘤时，显示输入框）
            if l_div[i] == '有\n无':
                l_div[i] = '家族史\n有\n无'
                ele_n = l_div.index(l_div[i])
                ele_after_n = ele_n + 1
                if l_div[ele_after_n] == '疾病名称\n与本人关系':
                    l_div[ele_after_n] = '家族史疾病名称'
                    l_div.insert(ele_after_n + 1, "与本人关系")
                else:
                    n = int(len(l_div[ele_after_n].split("\n")) / 2)
                    l_div[ele_after_n] = '家族史疾病名称' + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, "与本人关系" + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(n - 1):
                        l_div.insert(ele_after_n + j, '家族史疾病名称' + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, "与本人关系" + str(j + 2))
        # print('1.2 清洗l_div => ', l_div)

        # 2 生成checkbox字典
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(len(l_isRadioStatus), l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"
        # el-radio__input is-disabled is-checked
        d_radio = {}
        d_checkbox = {}
        l_2 = []
        ee = 0
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(len(l_1), l_1)  # ['户籍', '非户籍']
                # ee = ee + len(l_1)
                # print(ee)
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4,d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')

        # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
        if d_checkbox['药物过敏史']['其他药物过敏源'] == 'True':
            l_field.insert(l_field.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')
            # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
            l_textarea = Web_PO.getAttrValueByXs("//div/div/div/textarea", 'value')
            # 在input中23位置插入textarea值
            l_input.insert(23, l_textarea[0])
            print('3.3 l_textarea => ', l_textarea)
            # 更新div
            l_div.insert(l_div.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')

        # 当残疾情况中选择其他残疾时，显示输入框（其他残疾备注）
        if d_checkbox['残疾情况']['其他残疾'] == 'True':
            l_field.insert(l_field.index('残疾证号'), '其他残疾备注')
            # 更新div
            l_div.insert(l_div.index('残疾证号'), '其他残疾备注')

        # 如果既往史或家族史中疾病名称选择了恶性肿瘤，显示输入框（恶性肿瘤备注），插入XXX恶性肿瘤备注字段
        for i in range(len(l_input)):
            if l_input[i] == '恶性肿瘤':
                p = l_field[i - 5] + '恶性肿瘤备注'
                l_field.insert(i - 4, p)
                # 更新div
                for j in range(len(l_div)):
                    ele_n = l_div.index(l_field[i - 5])
                    l_div.insert(ele_n + 1, l_field[i - 5] + '恶性肿瘤备注')

        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(6))
        l_input.insert(6, ll)
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        # print('d_normal =>', d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ',  d_result)
        # return d_result


    def physicalExamination(self, varUsername, varTestUrl):

        # 健康体检

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//div[@class='table_line']/div")
        print("1.1 原始l_div => ", l_div)

        # 1.2 清洗字段
        # 删除
        l_div = [i for i in l_div if i != '']
        # for i in range(len(l_div)):
        #     if l_div[i] == '现住址必填':
        #         l_div.remove('现住址必填')
        #     if l_div[i] == '关联户主':
        #         l_div.remove('关联户主')
        # l_div.remove('城镇职工基本医疗保险')
        # l_div.remove('城镇居民基本医疗保险')
        # l_div.remove('贫困救助')

        # 修改
        # for i in range(len(l_div)):
        #     if l_div[i] == '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾\n残疾情况必填':
        #         l_div[i] = '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾'
        #     if l_div[i] == '商业医疗保险\n全公费\n全自费\n其他':
        #         l_div[i] = '医疗费用支付方式1\n城镇职工基本医疗保险'

        # 插入
        # l_div[l_div.index('遗传病史\n有\n无') + 1] = '遗传病史疾病名称'
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 1, '职工医保卡号')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 2, '医疗费用支付方式2\n城镇居民基本医疗保险')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 3, '居民医保卡号')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 4, '医疗费用支付方式3\n贫困救助')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 5, '贫困救助卡号')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 6, '医疗费用支付方式4\n商业医疗保险\n全公费\n全自费\n其他')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 7, '医疗费用支付方式备注')

        # 动态自增字段 （33是随意值，确保遍历不中断）
        for i in range(len(l_div) + 33):
            if l_div[i] == '建档人':
                break

            # 既往史，动态自增字段（选择恶性肿瘤时，显示输入框）
            self._residentHealthRecord(l_div, i, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
            self._residentHealthRecord(l_div, i, '手术\n有\n无', '手术名称', '手术时间')
            self._residentHealthRecord(l_div, i, '外伤\n有\n无', '外伤名称', '外伤时间')
            self._residentHealthRecord(l_div, i, '输血\n有\n无', '输血原因', '输血时间')

            # 家族史，动态自增字段（选择恶性肿瘤时，显示输入框）
            if l_div[i] == '有\n无':
                l_div[i] = '家族史\n有\n无'
                ele_n = l_div.index(l_div[i])
                ele_after_n = ele_n + 1
                if l_div[ele_after_n] == '疾病名称\n与本人关系':
                    l_div[ele_after_n] = '家族史疾病名称'
                    l_div.insert(ele_after_n + 1, "与本人关系")
                else:
                    n = int(len(l_div[ele_after_n].split("\n")) / 2)
                    l_div[ele_after_n] = '家族史疾病名称' + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, "与本人关系" + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(n - 1):
                        l_div.insert(ele_after_n + j, '家族史疾病名称' + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, "与本人关系" + str(j + 2))
        print('1.2 清洗l_div => ', l_div)

        # 2 生成checkbox字典
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(len(l_isRadioStatus), l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"
        # el-radio__input is-disabled is-checked
        d_radio = {}
        d_checkbox = {}
        l_2 = []
        ee = 0
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(len(l_1), l_1)  # ['户籍', '非户籍']
                # ee = ee + len(l_1)
                # print(ee)
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4,d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')

        # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
        if d_checkbox['药物过敏史']['其他药物过敏源'] == 'True':
            l_field.insert(l_field.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')
            # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
            l_textarea = Web_PO.getAttrValueByXs("//div/div/div/textarea", 'value')
            # 在input中23位置插入textarea值
            l_input.insert(23, l_textarea[0])
            print('3.3 l_textarea => ', l_textarea)
            # 更新div
            l_div.insert(l_div.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')

        # 当残疾情况中选择其他残疾时，显示输入框（其他残疾备注）
        if d_checkbox['残疾情况']['其他残疾'] == 'True':
            l_field.insert(l_field.index('残疾证号'), '其他残疾备注')
            # 更新div
            l_div.insert(l_div.index('残疾证号'), '其他残疾备注')

        # 如果既往史或家族史中疾病名称选择了恶性肿瘤，显示输入框（恶性肿瘤备注），插入XXX恶性肿瘤备注字段
        for i in range(len(l_input)):
            if l_input[i] == '恶性肿瘤':
                p = l_field[i - 5] + '恶性肿瘤备注'
                l_field.insert(i - 4, p)
                # 更新div
                for j in range(len(l_div)):
                    ele_n = l_div.index(l_field[i - 5])
                    l_div.insert(ele_n + 1, l_field[i - 5] + '恶性肿瘤备注')

        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(6))
        l_input.insert(6, ll)
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        # print('d_normal =>', d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ',  d_result)
        # return d_result

    def phthisisVisit(self, varUsername, varTestUrl):

        # 肺结核患者第一次入户随访记录表

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//form/div")
        # print("1.1 原始l_div => ", l_div)

        # # 1.2 清洗字段
        # # 删除
        l_div.remove("肺结核患者第一次入户随访记录表")
        # # 插入
        l_div.insert(l_div.index('随访日期\n随访方式\n门诊\n家庭\n电话'), '随访日期')
        # 用药
        l_div.insert(l_div.index('用药\n化疗方案\n用法\n每日\n间歇\n药品剂型\n固定剂量复合制剂\n散装药\n板式组合药\n注射剂'), '化疗方案')
        l_div.insert(l_div.index('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天'), '吸烟1')
        l_div.insert(l_div.index('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天') + 1, '吸烟2')
        l_div.insert(l_div.index('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天') + 2, '饮酒1')
        l_div.insert(l_div.index('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天') + 3, '饮酒2')
        l_div.remove('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天')
        l_div.insert(l_div.index('化疗方案'), '症状及体征其他')
        # 健康教育及培训
        l_div.insert(l_div.index('健康教育及培训\n取药地点、时间\n服药记录卡的填写\n掌握\n未掌握\n服药方法及药品存放\n掌握\n未掌握\n肺结核治疗疗程\n掌握\n未掌握\n不规律服药危害\n掌握\n未掌握\n服药后不良反应及处理\n掌握\n未掌握\n治疗期间复诊查痰\n掌握\n未掌握\n外出期间如何坚持服药\n掌握\n未掌握\n生活习惯及注意事项\n掌握\n未掌握\n密切接触者检查\n掌握\n未掌握'),  '取药地点')
        l_div.insert(l_div.index('健康教育及培训\n取药地点、时间\n服药记录卡的填写\n掌握\n未掌握\n服药方法及药品存放\n掌握\n未掌握\n肺结核治疗疗程\n掌握\n未掌握\n不规律服药危害\n掌握\n未掌握\n服药后不良反应及处理\n掌握\n未掌握\n治疗期间复诊查痰\n掌握\n未掌握\n外出期间如何坚持服药\n掌握\n未掌握\n生活习惯及注意事项\n掌握\n未掌握\n密切接触者检查\n掌握\n未掌握') + 1,  '取药时间')
        l_div.remove('健康教育及培训\n取药地点、时间\n服药记录卡的填写\n掌握\n未掌握\n服药方法及药品存放\n掌握\n未掌握\n肺结核治疗疗程\n掌握\n未掌握\n不规律服药危害\n掌握\n未掌握\n服药后不良反应及处理\n掌握\n未掌握\n治疗期间复诊查痰\n掌握\n未掌握\n外出期间如何坚持服药\n掌握\n未掌握\n生活习惯及注意事项\n掌握\n未掌握\n密切接触者检查\n掌握\n未掌握')
        # # 修改
        for i in range(len(l_div) + 33):
            # 随访方式
            if l_div[i] == '随访日期\n随访方式\n门诊\n家庭\n电话':
                l_div[i] = '随访方式\n门诊\n家庭\n电话'
            # 患者类型\痰菌情况
            if l_div[i] == '患者类型\n初治\n复治\n痰菌情况\n阳性\n阴性\n未查痰':
                l_div[i] = '患者类型\n初治\n复治'
                l_div.insert(l_div.index(l_div[i]) + 1, '痰菌情况\n阳性\n阴性\n未查痰')
            # # 症状及体征
            if l_div[i] == '症状及体征\n没有症状\n咳嗽咳痰\n低热盗汗\n咯血或血痰\n胸痛消瘦\n恶心纳差\n头痛失眠\n视物模糊\n皮肤瘙痒皮疹\n耳鸣听力下降\n其他\n其他':
                l_div[i] = '症状及体征\n没有症状\n咳嗽咳痰\n低热盗汗\n咯血或血痰\n胸痛消瘦\n恶心纳差\n头痛失眠\n视物模糊\n皮肤瘙痒皮疹\n耳鸣听力下降\n其他'
            # 用药
            if l_div[i] == '用药\n化疗方案\n用法\n每日\n间歇\n药品剂型\n固定剂量复合制剂\n散装药\n板式组合药\n注射剂':
                l_div[i] = '用法\n每日\n间歇'
                l_div.insert(l_div.index(l_div[i]) + 1, '药品剂型\n固定剂量复合制剂\n散装药\n板式组合药\n注射剂')
            # 家庭居住环境
            if l_div[i] == '家庭居住环境\n单独的居室\n无\n有\n通风情况\n良好\n一般\n差':
                l_div[i] = '单独的居室\n无\n有'
                l_div.insert(l_div.index(l_div[i]) + 1, '通风情况\n良好\n一般\n差')
            if l_div[i] == '取药时间':
                l_div.insert(l_div.index(l_div[i]) + 1, '服药记录卡的填写\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 2, '服药方法及药品存放\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 3, '肺结核治疗疗程\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 4, '不规律服药危害\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 5, '服药后不良反应及处理\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 6, '治疗期间复诊查痰\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 7, '外出期间如何坚持服药\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 8, '生活习惯及注意事项\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 9, '密切接触者检查\n掌握\n未掌握')
            if l_div[i] == '下次随访日期\n随访医生\n患者（家属）签字':
                l_div.insert(l_div.index(l_div[i]), '下次随访日期')
                l_div.insert(l_div.index(l_div[i])+1, '随访医生')
                l_div.insert(l_div.index(l_div[i])+2, '患者（家属）签字')
                l_div.remove('下次随访日期\n随访医生\n患者（家属）签字')
                break
        # print('1.2 清洗l_div => ', l_div)

        # 2 生成checkbox字典
        # l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', 'is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        d_radio = {}
        d_checkbox = {}
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4, d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        # 选择其他，显示输入框
        if d_checkbox['督导人员选择']['其他'] == 'True':
            l_field.insert(l_field.index('吸烟1'), '督导人员选择其他备注')
            l_div.insert(l_div.index('吸烟1'), '督导人员选择其他备注')  # 更新div
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)
        # print('3.3 d_normal => ', , d_normal)  # {'管理卡号': '135', '其他情况说明': '', ...

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ',  d_result)
        # return d_result


    def _checkbox(self, var_l_div, varContainClassValue):

        # _checkbox(l_div, 'el-radio__input is-disabled is-checked')
        l_tmp = []
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', varContainClassValue)
        l_tmp = l_isRadioStatus[-2:]
        print(l_tmp)  # ['False', 'True', 'False', 'False', ...
        d_radio = {}
        d_checkbox = {}
        for i in range(len(var_l_div)):
            if "\n" in var_l_div[i]:
                ele_n = var_l_div.index(var_l_div[i])
                l_1 = var_l_div[i].split("\n")
                l_1.pop(0)
                print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_tmp.pop(0))

                d_box = dict(zip(l_1, l_bool))
                print(4, d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[var_l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k, v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        print('d_checkbox2 => ', d_checkbox)

        return d_checkbox

    def pregnantWoman(self, varUsername, varTestUrl):

        # 孕产妇

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        # l_div = Web_PO.getTextByXs("//form/div")
        # print("1.1 原始l_div => ", l_div)

        l_div = ['填表日期','是否高危产妇\n是\n否', '丈夫姓名', '丈夫年龄', '丈夫电话', '孕次', '阴1道分娩', '剖宫产', '末次月经\n不详', '周', '天','预产期',
                 '既往史\n无\n心脏病\n肾脏疾病\n肝脏疾病\n高血压\n贫血\n糖尿病\n其他',
                 '家族史\n无\n遗传性疾病史\n精神病史\n其他', '妇科手术史\n有\n无',
                 '个人史\n无特殊\n吸烟\n饮酒\n服用药物\n接触有毒害物质\n接触放射线\n其他',
                 '自然流产', '人工流产','死胎', '死产', '新生儿死亡', '出生缺陷儿',
                 '身高(cm)', '体重(kg)', '体质指数(kg/m²)', '血压收缩压','血压舒张压',
                 '听诊心脏\n未见异常\n异常','听诊肺部\n未见异常\n异常',
                 '外阴\n未见异常\n异常', '阴道\n未见异常\n异常', '宫颈\n未见异常\n异常', '子宫\n未见异常\n异常', '附件\n未见异常\n异常',
                 '血红蛋白值','白细胞计数值','血小板计数值','血常规其他' ,
                 '尿蛋白','尿糖','尿酮体','尿潜血','尿常规其他',
                 '血型\nA型\nB型\nO型\nAB型\n不详','RH血型\nRh阴性\nRh阳性\n不详','血糖',
                 '血清谷丙转氨酶','血清谷草转氨酶','白蛋白','总胆红素','结合胆红素',
                 '血清肌酐','血尿素',
                 '阴道分泌物\n未见异常\n滴虫\n假丝酵母菌\n其他', '阴道清洁度\nI度\nII度\nIII度\nIV度',
                 '乙型肝炎表面抗原','乙型肝炎表面抗体','乙型肝炎e抗原','乙型肝炎e抗体','乙型肝炎核心抗体',
                 '梅毒血清学试验\n阴性\n阳性','HIV抗体检测\n阴性\n阳性',
                 'B超','辅助检查其他',
                 '总体评估\n未见异常\n异常',
                 '保健指导\n生活方式\n心理\n营养\n避免致畸因素和疾病对胚胎的不良影响\n产前筛选宣传告知\n其他',
                 '建册情况\n本次随访同时建册\n已在其他机构建册','建册日期','建册单位',
                 '转诊\n有\n无',
                 '下次访视时间','随访医生签名','居民签名']
        # l_field.insert(l_field.index('末次月经\n不详'), '末次月经日期')

        # 2 生成checkbox字典
        # l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', 'is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        d_radio = {}
        d_checkbox = {}
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4, d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        # print(l_field)
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        if d_checkbox['末次月经']['不详'] == 'False':
            l_field.insert(l_field.index('周'), '末次月经日期')
            l_div.insert(l_div.index('周'), '末次月经日期')  # 更新div
        if d_checkbox['既往史']['其他'] == 'True':
            # l_field.insert(l_field.index('自然流产'), '既往史其他备注')
            l_div.insert(l_div.index('既往史\n无\n心脏病\n肾脏疾病\n肝脏疾病\n高血压\n贫血\n糖尿病\n其他')+1 , '既往史其他备注')  # 更新div
        if d_checkbox['家族史']['其他'] == 'True':
            # l_field.insert(l_field.index('自然流产'), '家族史其他备注')
            l_div.insert(l_div.index('家族史\n无\n遗传性疾病史\n精神病史\n其他')+1, '家族史其他备注')  # 更新div
        if d_checkbox['妇科手术史']['有'] == 'True':
            # l_field.insert(l_field.index('自然流产'), '妇科手术史有备注')
            l_div.insert(l_div.index('妇科手术史\n有\n无')+1, '妇科手术史有备注')  # 更新div
        if d_checkbox['个人史']['其他'] == 'True':
            # l_field.insert(l_field.index('自然流产'), '个人史其他备注')
            l_div.insert(l_div.index('个人史\n无特殊\n吸烟\n饮酒\n服用药物\n接触有毒害物质\n接触放射线\n其他')+1, '个人史其他备注')  # 更新div
        if d_checkbox['听诊心脏']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '心脏异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '心脏异常备注')  # 更新div
        if d_checkbox['听诊肺部']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '肺部异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '肺部异常备注')  # 更新div
        if d_checkbox['外阴']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '外阴异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '外阴异常备注')  # 更新div
        if d_checkbox['阴道']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '阴道异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '阴道异常备注')  # 更新div
        if d_checkbox['宫颈']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '宫颈异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '宫颈异常备注')  # 更新div
        if d_checkbox['子宫']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '子宫异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '子宫异常备注')  # 更新div
        if d_checkbox['附件']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '附件异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '附件异常备注')  # 更新div
        if d_checkbox['阴道分泌物']['其他'] == 'True':
            # l_field.insert(l_field.index('乙型肝炎表面抗原'), '阴道分泌物其他备注')
            l_div.insert(l_div.index('阴道分泌物\n未见异常\n滴虫\n假丝酵母菌\n其他')+1, '阴道分泌物其他备注')  # 更新div
        if d_checkbox['总体评估']['异常'] == 'True':
            # l_field.insert(l_field.index('总体评估\n未见异常\n异常'), '总体评估异常备注')
            l_div.insert(l_div.index('总体评估\n未见异常\n异常')+1, '总体评估异常备注')  # 更新div
        if d_checkbox['保健指导']['其他'] == 'True':
            # l_field.insert(l_field.index('建册日期'), '保健指导其他备注')
            l_div.insert(l_div.index('保健指导\n生活方式\n心理\n营养\n避免致畸因素和疾病对胚胎的不良影响\n产前筛选宣传告知\n其他')+1, '保健指导其他备注')  # 更新div
        if d_checkbox['转诊']['有'] == 'True':
            # l_field.insert(l_field.index('下次访视时间'), '转诊原因')
            l_div.insert(l_div.index('下次访视时间'), '转诊原因')  # 更新div
            # l_field.insert(l_field.index('下次访视时间'), '转诊机构及科室')
            l_div.insert(l_div.index('下次访视时间'), '转诊机构及科室')  # 更新div
            # l_field.insert(l_field.index('下次访视时间'), '转诊联系人')
            l_div.insert(l_div.index('下次访视时间'), '转诊联系人')  # 更新div
            # l_field.insert(l_field.index('下次访视时间'), '转诊方式')
            l_div.insert(l_div.index('下次访视时间'), '转诊方式')  # 更新div
            # l_field.insert(l_field.index('下次访视时间'), '结果\n到位\n未到位')
            l_div.insert(l_div.index('下次访视时间'), '结果\n到位\n未到位')  # 更新div
            d_checkbox2 = self._checkbox(['结果\n到位\n未到位'], 'is-disabled is-checked')

        if d_checkbox['建册情况']['已在其他机构建册'] == 'True':
            # l_field.insert(l_field.index('建册日期'), '已在其他机构建册备注')
            l_div.insert(l_div.index('建册情况\n本次随访同时建册\n已在其他机构建册'), '已在其他机构建册备注')  # 更新div
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        d_normal.update(d_checkbox2)
        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)
        print('3.3 d_normal_checkbox => ', d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
            # for k, v in d_checkbox2.items():
            #     if k in l_div[i]:
            #         d_result[k] = v
        print(varUsername + ' => ', d_result)
        # return d_result


    def hypophrenia(self, varUsername, varTestUrl):

        # 严重精神障碍患者

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//form/div")
        # print("1.1 原始l_div => ", l_div)

        # # 1.2 清洗字段
        # # 删除
        l_div = [i for i in l_div if i != '']
        l_div.remove("严重精神障碍患者个人信息补充表")
        # # 插入
        l_div.insert(l_div.index('档案编号\n监护人姓名\n与患者关系'), '档案编号')
        l_div.insert(l_div.index('档案编号\n监护人姓名\n与患者关系'), '监护人姓名')
        l_div.insert(l_div.index('档案编号\n监护人姓名\n与患者关系'), '与患者关系')
        l_div.remove('档案编号\n监护人姓名\n与患者关系')
        l_div.insert(l_div.index('监护人地址\n监护人电话'), '监护人地址')
        l_div.insert(l_div.index('监护人地址\n监护人电话'), '监护人电话')
        l_div.remove('监护人地址\n监护人电话')
        l_div.insert(l_div.index('辖区村(居)委联系人\n联系人电话'), '辖区村(居)委联系人')
        l_div.insert(l_div.index('辖区村(居)委联系人\n联系人电话'), '联系人电话')
        l_div.remove('辖区村(居)委联系人\n联系人电话')
        l_div.insert(l_div.index('知情同意\n不同意参加管理\n同意参加管理\n签字\n签字日期') + 1, '签字日期')
        l_div.insert(l_div.index('知情同意\n不同意参加管理\n同意参加管理\n签字\n签字日期') + 1, '签字')
        l_div.insert(l_div.index('重性精神疾病分类\n精神分裂症\n双向障碍\n偏执性精神病\n分裂情感障碍\n癫痫所致精神障碍\n精神发育迟滞伴发精神障碍\n其他\n初次发病时间') + 1, '初次发病时间')
        l_div.insert(l_div.index('既往治疗情况\n门诊\n未治\n间断门诊治疗\n连续门诊治疗\n住院\n曾住精神病专科医院/综合医院精神专科\n次') + 1, '住院')
        l_div.insert(l_div.index('目前诊断情况\n诊断\n确诊医院\n确诊日期'), '诊断')
        l_div.insert(l_div.index('目前诊断情况\n诊断\n确诊医院\n确诊日期'), '确诊医院')
        l_div.insert(l_div.index('目前诊断情况\n诊断\n确诊医院\n确诊日期'), '确诊日期')
        l_div.remove('目前诊断情况\n诊断\n确诊医院\n确诊日期')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '自杀未遂')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '自伤')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '其他危害行为')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '肇祸')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '肇事')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '轻度滋事')
        l_div.insert(l_div.index('建卡日期\n登记人\n建卡医疗机构') , '建卡日期')
        l_div.insert(l_div.index('建卡日期\n登记人\n建卡医疗机构') , '登记人')
        l_div.insert(l_div.index('建卡日期\n登记人\n建卡医疗机构') , '建卡医疗机构')
        l_div.remove('建卡日期\n登记人\n建卡医疗机构')
        # # 修改
        for i in range(len(l_div) + 33):
            if l_div[i] == '知情同意\n不同意参加管理\n同意参加管理\n签字\n签字日期':
                l_div[i] = '知情同意\n不同意参加管理\n同意参加管理'
            if l_div[i] == '重性精神疾病分类\n精神分裂症\n双向障碍\n偏执性精神病\n分裂情感障碍\n癫痫所致精神障碍\n精神发育迟滞伴发精神障碍\n其他\n初次发病时间':
                l_div[i] = '重性精神疾病分类\n精神分裂症\n双向障碍\n偏执性精神病\n分裂情感障碍\n癫痫所致精神障碍\n精神发育迟滞伴发精神障碍\n其他'
            if l_div[i] == '既往治疗情况\n门诊\n未治\n间断门诊治疗\n连续门诊治疗\n住院\n曾住精神病专科医院/综合医院精神专科\n次':
                l_div[i] = '既往治疗情况门诊\n未治\n间断门诊治疗\n连续门诊治疗'
            if l_div[i] == '危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次':
                l_div[i] = '危险行为\n无\n有'
            if l_div[i] == '建卡医疗机构':
                break
        # print('1.2 清洗l_div => ', l_div)

        # 2 生成checkbox字典
        # l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', 'is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        d_radio = {}
        d_checkbox = {}
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4, d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        if d_checkbox['既往主要症状']['其他'] == 'True':
            l_field.insert(l_field.index('住院'), '既往主要症状其他备注')
            l_div.insert(l_div.index('住院'), '既往主要症状其他备注')  # 更新div
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)
        # print('3.3 d_normal_checkbox => ', , d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ', d_result)
        # return d_result



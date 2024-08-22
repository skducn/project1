# coding: utf-8
# ***************************************************************
# Author     : John
# Created on : 2020-3-20
# Description: 基类封装(通用)
# # 重新定义 find_element, find_elements, send_keys, input，click，get，print，checkbox，select，iframe，js，exist,alert
# color
# ***************************************************************

import sys, os, platform, psutil
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.abstract_event_listener import *
from selenium.webdriver.support.event_firing_webdriver import *
from selenium.webdriver.support.expected_conditions import *
from PO.ColorPO import *

Color_PO = ColorPO()


class BasePO(object):
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *loc):
        """重写元素定位"""
        try:
            # 注意：入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            # WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            # print u"%s 页面中未能找到元素 %s "%(self, loc)
            print("未找到元素 %s " % (loc))

    def find_elements(self, *loc):
        """重写元素集定位"""
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_elements(*loc)
        except:
            print("未找到元素集 %s " % (loc))

    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        """重写键盘方法"""
        try:
            loc = getattr(self, "_%s" % loc)  # getattr相当于实现self.loc
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            # print u"%s 页面中未能找到 %s 元素"%(self, loc)
            print("未找到元素 %s " % (loc))

    def sendKeysId(self, varId, dimValue):
        # 上传文件
        # Oa_PO.Web_PO.sendKeysId("impload", os.getcwd() + "\\drugTemplet.xls")  # 导入文件
        self.driver.find_element_by_id(varId).send_keys(dimValue)

    def sendKeysName(self, varName, dimValue):
        self.driver.find_element_by_name(varName).send_keys(dimValue)

    def sendKeysXpath(self, dimXpath, dimValue):
        # 上传文件
        # Oa_PO.Web_PO.sendKeysXpath("//input[@id='impload'", os.getcwd() + "\\drugTemplet.xls")  # 导入文件
        self.driver.find_element_by_xpath(dimXpath).send_keys(dimValue)

    """[ASSERT]"""

    def assertTrue(self, testValue, errMsg):
        try:
            if testValue == True:
                return True
            else:
                print(errMsg)
                return False
        except:
            return None

    def assertEqualTrue(self, expected, actual):
        try:
            if expected == actual:
                return True
            else:
                return False
        except:
            return None

    def assertEqual(self, expected, actual, okMsg, errMsg):
        try:
            if expected == actual:
                # print(okMsg)
                Color_PO.consoleColor("31", "36", "[OK]", str(okMsg))
                return True
            else:
                # print(errMsg)
                Color_PO.consoleColor("31", "38", "[ERROR]", str(errMsg))
                return False
        except:
            return None

    def assertEqualValue(self, expected, actual, okMsg, errMsg):
        try:
            if expected == actual:
                Color_PO.consoleColor(
                    "31", "36", "[OK]", str(okMsg) + ", " + str(expected)
                )
                return True
            else:
                Color_PO.consoleColor(
                    "31",
                    "38",
                    "[ERROR]",
                    str(errMsg) + ", 预期值：" + str(expected) + ", 实测值：" + str(actual),
                )
                return False
        except:
            Color_PO.consoleColor(
                "31",
                "33",
                "[ERROR] call "
                + sys._getframe(1).f_code.co_name
                + " (line "
                + str(sys._getframe(1).f_lineno)
                + ", call "
                + sys._getframe(0).f_code.co_name
                + " from '"
                + sys._getframe().f_code.co_filename
                + "')",
                "",
            )

    def assertContain(self, one, all, okMsg, errMsg):
        try:
            if one in all:
                print(okMsg)
                return True
            else:
                print(errMsg)
                return False
        except:
            return None

    def assertEqualNotNone(self, expected, actual):
        try:
            if (expected and actual) and (expected != None and actual != None):
                return 1, expected
            else:
                return 0, 0
        except:
            return None

    """[ERROR TIPS]"""

    def getError(self, varStatus, varErrorInfo, varErrorRow):
        # 当函数返回error时，获取当前语句行号及错误提示。
        # 因此函数必须要有返回值
        # Level_PO.getError(Level_PO.inputId(u"officebundle_tmoffice_officeName", u"自动化科室123"), u"输入框定位错误！",sys._getframe().f_lineno)
        # errorrrrrrrrrrr, 101行, '获取科室文本与对应值的字典'。
        if varStatus == "error":
            print("errorrrrrrrrrrr,", varErrorRow, "行,", varErrorInfo)
            os._exit(0)

    def check_contain_chinese(self, check_str):
        # 判断字符串中是否包含中文符合
        for ch in check_str.decode("utf-8"):
            if "\u4e00" <= ch <= "\u9fff":
                return True
        return False

    """[ INPUT ]"""

    def inputId(self, varId, vatContent):
        try:
            self.find_element(*(By.ID, varId)).send_keys(vatContent)
        except:
            return None

    def inputIdClear(self, varId, varContent):
        try:
            self.find_element(*(By.ID, varId)).clear()
            self.find_element(*(By.ID, varId)).send_keys(varContent)
        except:
            return None

    def inputName(self, varName, varContent):
        try:
            self.find_element(*(By.NAME, varName)).send_keys(varContent)
        except:
            return None

    def inputNameClear(self, varName, varContent):
        try:
            self.find_element(*(By.NAME, varName)).clear()
            self.find_element(*(By.NAME, varName)).send_keys(varContent)
        except:
            return None

    def inputXpath(self, varPath, varContent):
        try:
            self.find_element(*(By.XPATH, varPath)).send_keys(varContent)
        except:
            return None

    def inputXpathClear(self, varPath, varContent):
        try:
            self.find_element(*(By.XPATH, varPath)).clear()
            self.find_element(*(By.XPATH, varPath)).send_keys(varContent)
        except:
            return None

    def inputXpathEnter(self, varPath, varContent):
        try:
            self.find_element(*(By.XPATH, varPath)).send_keys(varContent)
            self.find_element(*(By.XPATH, varPath)).send_keys(Keys.ENTER)
        except:
            return None

    def inputXpathClearEnter(self, varPath, varContent):
        try:
            self.find_element(*(By.XPATH, varPath)).clear()
            self.find_element(*(By.XPATH, varPath)).send_keys(varContent)
            self.find_element(*(By.XPATH, varPath)).send_keys(Keys.ENTER)

        except:
            return None

    """[ 2click ]"""

    def clickId(self, varId, t=0):
        try:
            self.find_element(*(By.ID, varId)).click()
            sleep(t)
        except:
            return None

    def clickLinktext(self, varContent, t=0):
        try:
            self.find_element(*(By.LINK_TEXT, varContent)).click()
            sleep(t)
        except:
            return None

    def clickLinkstext(self, varContent, t=0):
        try:
            for a in self.find_elements(*(By.LINK_TEXT, varContent)):
                a.click()
            sleep(t)
        except:
            return None

    def clickTagname(self, varContent, t=0):
        # clickTagname(u"test", 2)
        try:
            self.find_element(*(By.TAG_NAME, varContent)).click()
            sleep(t)
        except:
            return None

    def clickXpath(self, varPath, t=0):
        # clickXpath(u"//button[@ng-click='action.callback()']", 2)
        try:
            self.find_element(*(By.XPATH, varPath)).click()
            sleep(t)
        except:
            return None

    def clickXpathEnter(self, varPath, t=0):
        try:
            self.find_element(*(By.XPATH, varPath)).send_keys(Keys.ENTER)
            sleep(t)
        except:
            return None

    def clickXpaths(self, varPaths, t=0):
        # 遍历路径
        # self.Level_PO.clickXpaths("//a[contains(@href,'1194')]", 2)  , 表示遍历所有a 中href属性内容包含1194字符串的连接。
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                a.click()
                sleep(t)
        except:
            return None

    def clickXpathsNum(self, varPaths, varNum, t=0):
        # 遍历同一属性的多个click，点击第N个。
        # Level_PO.clickXpathsNum(u"//button[@ng-click='action.callback()']", 5, 2)  ，表示遍历后点击第五个连接。
        try:
            c = 0
            for a in self.find_elements(*(By.XPATH, varPaths)):
                c = c + 1
                if c == varNum:
                    a.click()
                    break
            sleep(t)
        except:
            return None

    def clickXpathsTextContain(self, varPaths, varContain, t=0):
        # 遍历路径，点击text中包含某内容的连接。
        # self.Level_PO.clickXpathsTextContain("//td[@aria-describedby='gridTable_run_name']/a", '20190506059', 2)
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                if varContain in a.text:
                    a.click()
                    break
            sleep(t)
        except:
            return None

    def clickXpathsContain(self, varPaths, varAttr, varContain, t=0):
        # 遍历路径，点击属性varAttr中包含某内容的连接。
        # self.Level_PO.clickXpathsContain("//a", "href", '1194', 2)
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                # print(a.get_attribute(varAttr))
                if varContain in a.get_attribute(varAttr):
                    a.click()
                    break
            sleep(t)
        except:
            return None

    def clickXpathsXpath(self, varPaths, varPaths2, t=0):
        # 遍历路径之路径
        # 一般用于，click后二次确认
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                a.click()
                sleep(t)
                self.find_element(*(By.XPATH, varPaths2)).click()
                sleep(t)
        except:
            return None

    def clickXpathXpath(self, varPath, varPath2, t=0):
        # ? 未侧式
        try:
            elements = self.find_element(*(By.XPATH, varPath))
            actions = ActionChains(self.driver)
            actions.move_to_element(elements).perform()
            yy = self.find_element(*(By.XPATH, varPath2))
            yy.click()
            sleep(t)
        except:
            return None

    def clickXpathRight(self, varPath, varId):
        # ?
        try:
            xx = self.find_element(*(By.XPATH, varPath))
            yy = self.find_element(*(By.ID, varId))
            ActionChains(self.driver).drag_and_drop(xx, yy).perform()
            # ActionChains(self.driver).dra
            # print "end"
            ActionChains(self.driver).click_and_hold(xx).perform()
            # perform()
            # ActionChains(self.driver).click
            ActionChains(self.driver).move_to_element(
                self.find_element(*(By.ID, varId))
            )
        except:
            return None

    """[ 3get ]"""

    def getXpathText(self, varPath):
        # 获取路径的文本
        # Level_PO.getXpathText(u"//input[@类与实例='123']")
        try:

            return self.find_element(*(By.XPATH, varPath)).text
        except:
            return None

    def getXpathsText(self, varPaths):
        # 获取文本列表
        # getXpathsText("//tr")
        try:
            list1 = []
            for a in self.find_elements(*(By.XPATH, varPaths)):
                list1.append(a.text)
            return list1
        except:
            return None

    def getXpathsTextPart(self, varPaths, varText):
        # 获取部分文本列表（从头开始获取直到遇到varText为止）
        # getXpathsText("//div","Copyright © 2019上海智赢健康科技有限公司出品")
        try:
            list1 = []
            for a in self.find_elements(*(By.XPATH, varPaths)):
                if varText in a.text:
                    list1.append(a.text)
                    break
                else:
                    list1.append(a.text)
            return list1
        except:
            return None

    def getXpathsTextPlace(self, varPaths, varContent):
        # 获取文本所在的位置
        # getXpathsTextPlace("//tr", "test")   //3 表示test在第3个tr里，未找到返回None
        r = 0
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                r = r + 1
                if a.text == varContent:
                    return r
            return None
        except:
            return None

    def getXpathsPartTextPlace(self, varPaths, dimPartContent):
        # 获取模糊文本所在的位置
        # getXpathsPartTextPlace("//tr", "test")
        # 如：遍历//table[@id='gridTable']/tbody/tr/td[9]/a"，其中 tr是多行，其中第9个单元格下a标签的文本，得到是在第几个tr中。
        # getXpathsPartTextPlace("//table[@id='gridTable']/tbody/tr/td[9]/a", "2020060422", 2))
        r = 0
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                r = r + 1
                if dimPartContent in a.text:
                    return r
        except:
            return None

    def getXpathsAttrPlace(self, varPaths, varAttr, varValue):
        # 获取某属性值所在的位置
        # varNoRow = self.Web_PO.getXpathsAttrPlace("//td[9]/a", "href", "1122")

        r = 0
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                r = r + 1
                if varValue in a.get_attribute(varAttr):
                    return r
        except:
            return None

    def getXpathAttr(self, varPath, varAttr):
        # 获取属性的值
        # Level_PO.getXpathAttr(u"//input[@类与实例='123']",u"value")
        try:
            return self.find_element(*(By.XPATH, varPath)).get_attribute(varAttr)
        except:
            return None

    def getXpathsQty(self, varPaths):
        # 遍历路径数量
        # 如：获取tr下有多少个div标签， Web_PO.getXpathsQty('//*[@id="app"]/tr/div')
        s = 0
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                s = s + 1
            return s
        except:
            return None

    def getXpathsAttr(self, varPaths, varAttr):
        # 获取属性列表
        # Level_PO.getXpathsAttr(u"//tr", u"id")  获取表格里数据数量。
        l = []
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                l.append(a.get_attribute(varAttr))
            return l
        except:
            return None

    def getXpathsDictTextAttr(self, varPaths, varAttr):
        # 获取遍历路径字典{文本：属性值}
        # Level_PO.getXpathsTextAttr(u"//input[@name='office_id']",u"value")
        dict1 = {}
        list1 = []
        list2 = []
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                list1.append(a.text)
                list2.append(a.get_attribute(varAttr))
            dict1 = dict(zip(list1, list2))
            return dict1
        except:
            return None

    def getLinktextAttr(self, varContent, varAttr):
        # 获取连接文本的属性
        # Level_PO.getLinktextAttr(u"超链接",u"href")
        try:
            return self.find_element(*(By.LINK_TEXT, varContent)).get_attribute(varAttr)
        except:
            return None

    """[ 4print ]"""

    def printLinktextAttr(self, varContent, varAttr):
        # Level_PO.printLinktextAttr(u"测试",u"href")
        try:
            return self.find_element(*(By.LINK_TEXT, varContent)).get_attribute(varAttr)
        except:
            return None

    def printIdTagnameText(self, varId, dimTagname):
        # Level_PO.printIdTagnameText('navbar', "button")
        try:
            print(
                self.find_element(*(By.ID, varId))
                .a.find_element_by_tag_name(dimTagname)
                .text
            )
        except:
            return None

    def printIdTagnamesText(self, varId, dimTagname):
        # Level_PO.printIdTagnamesText('navbar', "dl")
        try:
            a = self.find_element(*(By.ID, varId))
            varContents = a.find_elements_by_tag_name(dimTagname)
            for i in varContents:
                print(i.text)
        except:
            return None

    def printXpathText(self, varPath):
        # Level_PO.printXpathText("//h5")
        try:
            print(self.find_element(*(By.XPATH, varPath)).text)
        except:
            return None

    def printXpathsText(self, varPaths):
        # Level_PO.printXpathsText("//tr")
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                print(a.text)
        except:
            return None

    def printXpathAttr(self, varPath, varAttr):
        # Level_PO.printXpathAttr(u"//input[@类与实例="123"]",u"value")
        try:
            print(self.find_element(*(By.XPATH, varPath)).get_attribute(varAttr))
        except:
            return None

    def printXpathsAttr(self, varPaths, varAttr):
        # Level_PO.printXpathsAttr(u"//tr",u"value")
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                print(a.get_attribute(varAttr))
        except:
            return None

    """[ 5checkbox ]"""

    def isCheckbox(self, varPath):
        # ? 判断是否选中复选框 ，返回 True 或 False
        # Level_PO.isCheckbox(u"//input[@类与实例='123']")
        try:
            return self.find_element(*(By.XPATH, varPath)).is_selected()
        except:
            return False

    def checkboxXpathsClear(self, varPaths):
        # 遍历路径反勾选复选框 （不勾选）
        # Level_PO.checkboxXpathsClear(u"//input[@type='checkbox']")
        try:
            for a in self.find_elements(*(By.XPATH, varPaths)):
                if a.is_selected() == True:
                    a.click()
        except:
            return False

    """[ 6select ]"""

    def selectIdValue(self, varId, dimValue):
        # 通过Id属性选择值
        # self.selectIdValue(u"id", u'10')  ，（一般情况 value=10 , Text=启用）
        try:
            Select(self.driver.find_element_by_id(varId)).select_by_value(dimValue)
        except:
            return None

    def selectIdText(self, varId, varText):
        # 通过Id属性选择文本
        # self.selectIdText(u"id", u'启用')  ，（一般情况 value=1 , Text=启用）
        try:
            Select(self.driver.find_element_by_id(varId)).select_by_visible_text(
                varText
            )
        except:
            return None

    def selectNameText(self, varName, varText):
        # 通过Name属性选择文本
        # 如：Level_PO.selectNameText(u"isAvilable", u"10")
        try:
            Select(self.driver.find_element_by_name(varName)).select_by_visible_text(
                varText
            )
        except:
            return None

    def selectNameValue(self, varName, dimValue):
        # 通过Name属性选择值
        # 如：Level_PO.selectNameValue(u"isAvilable", u"启动")
        try:
            Select(self.driver.find_element_by_name(varName)).select_by_value(dimValue)
        except:
            return None

    def selectXpathText(self, varPath, varText):
        # 遍历Xpath下的Option,
        # self.selectXpathText(u"//select[@regionlevel='1']", u'启用'), （一般情况 value=1 , Text=启用）
        s1 = self.driver.find_element_by_xpath(varPath)
        l_content1 = []
        l_value1 = []
        # varContents = self.driver.find_elements_by_xpath(varByXpath + "/option")
        varContents = self.driver.find_elements_by_xpath(varPath + "/option")
        for a in varContents:
            l_content1.append(a.text)
            l_value1.append(a.get_attribute("value"))
        d_total1 = dict(zip(l_content1, l_value1))
        for i in range(len(d_total1)):
            if sorted(d_total1.items())[i][0] == varText:
                Select(s1).select_by_value(sorted(d_total1.items())[i][1])
                break

    def selectIdStyle(self, varByID, varText):
        # ？ 遍历某ID的下的option (不包含 隐藏的属性，如style=display:none），获取varText对应的值
        # self.selectIdStyle(u"id", u'启用')  # （一般情况 value=1 , Text=启用）
        l_content1 = []
        l_value1 = []
        varCount = 0
        s1 = self.driver.find_element_by_id(varByID)
        varContents = s1.find_elements_by_tag_name("option")
        for a in varContents:
            if a.get_attribute("style") == "" and a.text == varText:
                l_content1.append(a.text)
                l_value1.append(a.get_attribute("value"))
                varCount = 1
        if varCount == 1:
            d_total1 = dict(zip(l_content1, l_value1))
            for i in range(len(d_total1)):
                if sorted(d_total1.items())[i][0] == varText:
                    Select(s1).select_by_value(sorted(d_total1.items())[i][1])
                    break
        else:
            return None

    def selectXpathsMenu1Menu2(self, varPaths1, varMenu, varPaths2, varMenu2, t):
        # 遍历级联菜单（选择一级菜单后再选择二级菜单）
        # Level_PO.selectMenu("//a[@类与实例='dropdown-toggle']", u"作业管理", "//a[@href='#']", u"作业框架管理", 3)
        try:
            for a in self.driver.find_elements_by_xpath(varPaths1):
                if varMenu == a.text:
                    a.click()
                    sleep(t)
                    for a2 in self.driver.find_elements_by_xpath(varPaths2):
                        if varMenu2 == a2.text:
                            a2.click()
                            sleep(t)
                            break
                    break
        except:
            return None

    def get_selectNAMEvalue(self, varByname, varContent):
        # 获取某select下text的value值。（下拉框，定位ByName，选择内容，text != value ）
        s1 = self.driver.find_element_by_name(varByname)
        l_content1 = []
        l_value1 = []
        varContents = self.driver.find_elements_by_xpath(
            "//select[@name='" + varByname + "']/option"
        )
        for a in varContents:
            l_content1.append(a.text)
            l_value1.append(a.get_attribute("value"))
        d_total1 = dict(zip(l_content1, l_value1))
        for i in range(len(d_total1)):
            if sorted(d_total1.items())[i][0] == varContent:
                value = sorted(d_total1.items())[i][1]
                return value

    def get_selectOptionValue(self, varByname, varNum):
        # 获取某个select中text的value值。
        varValue = self.driver.find_element_by_xpath(
            "//select[@name='" + varByname + "']/option[" + varNum + "]"
        ).get_attribute("value")
        return varValue

    """[ 7iframe ]"""

    def iframeId(self, varId, t=0):
        # 定位iframe的id
        # self.Level_PO.iframeId("layui-layer-iframe1", 1)
        self.driver.switch_to_frame(self.driver.find_element_by_id(varId))
        sleep(t)

    def iframeXpath(self, dimXpath, t=0):
        # 定位iframe的Xpath
        # self.Level_PO.iframeXpath("//body[@类与实例='gray-bg top-navigation']/div[4]/iframe", 1)
        self.driver.switch_to_frame(self.driver.find_element_by_xpath(dimXpath))
        sleep(t)

    def iframeXpathAttr(self, dimXpath, varAttr, varContain, t=0):
        # self.Level_PO.iframeXpathAttr("//iframe", "src", "/general/workflow/new/", 2)
        try:
            for a in self.find_elements(*(By.XPATH, dimXpath)):
                if varContain in a.get_attribute(varAttr):
                    self.driver.switch_to_frame(
                        self.driver.find_element_by_xpath(dimXpath)
                    )
                    break
            sleep(t)
        except:
            return None

    def inIframeTopDiv(self, varPath, t=0):
        # 定位iframe的div路径
        # evel_PO.inIframeDiv("[@id='showRealtime']", 2)
        # Home_PO.inIframeDiv("[@类与实例='cetc-popup-content']/div", 2)
        iframe = self.driver.find_element_by_xpath("//div" + varPath + "/iframe")
        # print iframe.get_attribute("src")
        self.driver.switch_to_frame(iframe)
        sleep(t)

    def iframeSwitch(self, t=0):
        # 多个iframe之间切换
        # 如第一层iframe1，第二层iframe2，两者之间切换
        self.driver.switch_to.parent_frame()
        sleep(t)

    def iframeQuit(self, t=0):
        # 退出 iframe
        # self.Level_PO.outIframe(1)
        self.driver.switch_to_default_content()
        sleep(t)

    """[ 8js ]"""

    def jsExecute(self, varJs, t=0):
        # 执行js
        varJs = (
            'document.querySelector("input[type=number]").value=""'  # 清除input输入框内哦那个
        )
        self.driver.execute_script(varJs)
        sleep(t)

    def jsXpathReadonly(self, varXpath, t=0):
        d = self.driver.find_element_by_xpath(varXpath)
        self.driver.execute_script('arguments[0].removeAttribute("readonly")', d)
        sleep(t)

    def jsIdReadonly(self, varId, t=0):
        # 通过id去掉控件只读属性，一般用于第三方日期控件
        self.jsExecute(
            'document.getElementById("' + varId + '").removeAttribute("readonly")', t
        )

    def jsNameReadonly(self, varName, t=0):
        # 通过Name去掉控件只读属性，一般用于第三方日期控件
        # 注意：document不支持getElementByName方法，只有getElementsByName方法获取标签数组，可通过数组第一个元素获取，如 array[0]
        self.jsExecute(
            'document.getElementsByName("'
            + varName
            + '")[0].removeAttribute("readonly")',
            t,
        )

    def jsNameDisplay(self, varName, t=0):
        # 通过name去掉隐藏属性，显示UI
        self.jsExecute(
            'document.getElementsByName("' + varName + '")[0].style.display=""', t
        )

    def displayBlockID(self, varID):
        # 未验证？
        # varJs = 'document.getElementById("filePath").style.display="block"'
        return self.driver.find_element_by_id(varID).style.display

    """[ 9color ]"""

    def printColor(self, macColor, winColor, varContent):
        if platform.system() == "Darwin":
            print(macColor) + varContent + "\033[0m"
        if platform.system() == "Windows":
            (eval(winColor))(varContent.encode("gb2312") + "\n")

    """[ 10exist ]"""

    def isElementId(self, varId):
        # 通过Id方式检查元素是否存在
        flag = False
        try:
            self.driver.find_element_by_id(varId)
            flag = True
        except:
            flag = False
        return flag

    def isElementName(self, varName):
        # 通过Name方式检查元素是否存在
        flag = False
        try:
            self.driver.find_element_by_name(varName)
            flag = True
        except:
            flag = False
        return flag

    def isElementPartialText(self, varPartText):
        # 通过超链接方式检查文本是否包含varText
        flag = False
        try:
            self.driver.find_element_by_partial_link_text(varPartText)
            flag = True
        except:
            flag = False
        return flag

    def isElementLinkText(self, varText):
        # 通过超链接方式检查文本是否存在
        flag = False
        try:
            self.driver.find_element_by_link_text(varText)
            flag = True
        except:
            flag = False
        return flag

    def isElementText(self, varPath, varText):
        # 通过文本比对检查文本是否存在
        flag = False
        try:
            if self.driver.find_element_by_xpath(varPath).text == varText:
                flag = True
        except:
            flag = False
        return flag

    def isElementXpath(self, varPath):
        # 通过Xpath方式检查元素是否存在
        # print(Oa_PO.Web_PO.isElementXpath("//input[@name='DATA_11' and @value='同意' and @checked]")) ，如判断单选框哪个被选中，如检查checked是否存在作为依据。
        flag = False
        try:
            self.driver.find_element_by_xpath(varPath)
            flag = True
        except:
            flag = False
        return flag

    def isElementXpathByAttr(self, varPath, varAttr, varContain):
        # 通过Xpath方式检查特定属性的元素是否存在
        flag = False
        try:
            for a in self.find_elements(*(By.XPATH, varPath)):
                if varContain == a.get_attribute(varAttr):
                    flag = True
                    break
        except:
            flag = False
        return flag

    def isElementVisibleXpath(self, element):
        # 未验证？？？
        driver = self.driver
        try:
            the_element = EC.visibility_of_element_located(
                driver.find_element_by_partial_link_text(element)
            )
            assert the_element(driver)
            flag = True
        except:
            flag = False
        return flag

    def locElement(self, varPath, t=0):
        # 定位到某元素
        try:
            elements = self.find_element(*(By.XPATH, varPath))
            actions = ActionChains(self.driver)
            actions.move_to_element(elements).perform()
            sleep(t)
        except:
            return None

    """ [11 alert] """

    def alertAccept(self):
        # 点击弹框中的确认
        alert = self.driver.switch_to.alert
        alert.accept()

    def alertDismiss(self):
        # 点击弹框中的取消
        alert = self.driver.switch_to.alert
        alert.dismiss()

    def alertText(self):
        # 获取弹框中的文案
        alert = self.driver.switch_to.alert
        return alert.text

    # 关闭进程
    def closePid(self, varApplication):

        """关闭进程
        os.system 输出如果出现乱码，需将 File->Settings->Editor->File Encodings 中 Global Encoding 设置成 GBK"""
        pids = psutil.pids()
        for pid in pids:
            try:
                p = psutil.Process(pid)
                # print('pid=%s,pname=%s' % (pid, p.name()))
                # 关闭excel进程
                if p.name() == varApplication:
                    cmd = "taskkill /F /IM " + varApplication
                    os.system(cmd)
                    sleep(2)
            except Exception as e:
                pass


class alert_is_present(object):
    """判断是否有alert弹窗"""

    def __init__(self, driver):
        self.driver = driver

    def __call__(self):
        try:
            alert = self.driver.switch_to.alert
            alert.text
            return True
        except NoAlertPresentException:
            return False


if __name__ == "__main__":

    Base_PO = BasePO()
    Base_PO.assertEqual(1, 1, "555", "7777")
    # Base_PO.closePid("chrome.exe")

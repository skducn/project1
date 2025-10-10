# coding: utf-8
# ***************************************************************
# Author     : John
# Created on : 2020-3-20
# Description: 通过DOM来操作页面中各种元素，例如添加、删除及替换元素等
# 重新定义： find_element, find_elements, send_keys, sendKeysByX，sendKeysById，sendKeysByname
# clk, get, set, checkbox, select, iframe, js, boolean
# pip install selenium-wire

# selenium 定位方式3-css_selector： https://blog.csdn.net/m0_57162664/article/details/134266949
# 父元素的第几个某类型的子节点 nth-of-type(n) 如：
# span:nth-of-type(2) 定位父元素第二个span类型子节点
# div:nth-last-of-type(2)，定位父元素倒数第二个div类型子节点。
# ***************************************************************

"""

todo clk菜单
单点击 clkByX()
多点击 clkByXs()
单点击某个索引号 clkIndexByXs(varXpaths, varIndex)
单点击超链接文本（文本中包含部分内容）clkTextByTpcByXs(varXpaths, varTpc, t=1):
单点击超链接文本 clkTextByXs(varXpaths, varText)
单点击超链接文本（属性中包含部分内容）clkTextByApcByXs(varXpaths, varAttr, varApc)
单点击超链接文本（属性中对应的值）clkTextByAcByXs(varXpaths, varAttr, varValue)
二次确认 clkByXsByX（varXpaths, varXpath）
clkById
clkByName
clkByTagname
clkByLinktext(varText)
clkByLinkstext(varText)

todo get菜单
获取标签数量 getCountByXs(varXpaths)
获取文本 getTextByX(varXpath)
获取文本列表 getListTextByX(varXpaths)
获取文本的索引号 getIndexByXs(varXpaths, varText)
获取文本包含部分内容(TPC)的索引号 getIndexByTpcByXs(varXpaths, varText)
获取指定文本之前的文本列表 getBeforeTextByXs(varXpaths, varText)
获取属性值 getAttrValueByX(varXpath, varAttr)
获取所有相同属性值的列表 getAttrValueByXs(varXpaths, varAttr)
获取超链接文本的属性值 getAttrValueByLt(varText, varAttr)
获取属性值的索引号 getIndexByAttrByXs(varXpaths, varAttr, varValue)
获取部分包含属性值所在的位置 getIndexByApcByXs(varXpaths, varAttr, varValue)
获取超链接文本及href getDictTextAttrValueByXs(varXpaths, varAttr)

通过标签下文本获取上一层元素 getUpEleByX(varLabel, varText)
通过标签下文本获取上层或上上层元素 getSuperEleByX(varLabel, varText, varXpath)

todo set菜单
通过id设置文本 setTextById()
通过id追加文本 appendTextById()
通过name设置文本 setTextByName()
通过name追加文本 appendTextByName()
通过xpath设置文本 setTextByX()
通过xpath追加文本 appendTextByX()
通过xpath键盘设置文本 setTextEnterByX()
通过xpath键盘追加文本  appendTextEnterByX()

todo checkbox菜单
是否选中复选框 isSelectedByX(varXpath)
取消所有已勾选的复选框clsSelected(varXpaths)

todo select菜单
通过id选择文本 sltTextById(varId, varText)
通过id选择值 sltValueById(varId, varValue)
通过name选择文本 sltTextByName(varName, varText)
通过name选择值 sltValueByName(varName, varValue)

todo iframe菜单
通过Xpath切换到iframe swhIframeByX(varXpath)
通过id切换到iframe   swhIframeById(varId)
通过xpaths遍历遍历属性中包含指定值切换iframe  swhIframeFromApcByXs(varXpaths,varAttr,varValue,2)
多个iframe之间切换  swhIframe(0)
退出iframe  quitIframe(0)

todo js菜单
清除input输入框内容 clsText()
清除readonly属性，是元素可见  clsReadonlyByX(varXpath)
通过id去掉控件只读属性 clsReadonlyById(varId)
通过name去掉只读属性 clsReadonlyByName(varName)
通过name去掉隐藏属性 clsDisplayByName(varName)
通过tagname去掉隐藏属性 clsDisplayByTagName(varLabel, varLen)

todo boolean菜单
通过xpath判断ture或false isEleExistByX(varXpath)
通过xpath判断属性是否存在 isBooleanAttr(varXpath, varAttr)
通过xpath判断属性值是否存在 isBooleanAttrValue(varXpath, varAttr, varValue)
通过Id判断ture或false isEleExistById(varId)
通过name判断ture或false isEleExistByName(varName)
通过超链接判断是否包含varText  isElePartExistByP(varPartText)
通过超链接判断是否存在varText isEleExistByL(varText)
通过xpath判断varText是否存在  isEleTextExistByX(varXpath, varText)

todo alert(system)菜单
点击弹框中的确认 alertAccept()
点击弹框中的取消 alertDismiss()
获取弹框中的文案 alertText()
"""

import requests
# import pyautogui
# print(pyautogui.position())
# import psutil,pyscreeze
import sys, os, platform, subprocess
# import cv2
# import pyautogui
from lxml import etree
from pytesseract import *

from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.event_firing_webdriver import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.abstract_event_listener import *
from selenium.webdriver.support.expected_conditions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageDraw, ImageGrab
# from seleniumwire import webdriver
# from lxml import etree
# import lxml.html
# from lxml.html.clean import Cleaner
# from lxml_html_clean import clean_html
# pip3 install lxml_html_clean

from PO.ListPO import *
List_PO = ListPO()

class DomPO(object):

    def __init__(self, driver):

        self.driver = driver

        # print(type(self.driver))

        self.selectors = {
            'dropdown_popper': "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']",
            'dropdown_dropdown': "//div[@class='el-popper is-pure is-light el-select__dropdown' and @aria-hidden='false']",
            'dropdown_dropdown_1': "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']/div/div/div[1]/ul/li",
            'dropdown_dropdown_2': "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']/div/div[2]/div[1]/ul/li",
            'dropdown_dropdown_3': "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']/div/div[3]/div[1]/ul/li",
            'dropdown_popper_1': "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li",
            'associate_family_confirm': ".//div[3]/div/button[1]",
            'associate_family_cancel': ".//div[3]/div/button[2]"
        }


    def gettest(self, varUrl):

        # cleaned_html = clean_html(raw_html)
        # cleaner = Cleaner()
        # cleaner.javascript = True
        # cleaner.page_structure = False
        # cleaner.style = True

        # base_url = 'http://xxxxxxxxxx'
        # 需要提前下载一个网页，并保存为本地文件test.html

        print(varUrl)

        # with open('/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/ERP/web/test.html', 'r', encoding='utf-8') as f:
        #     html_str = f.read()

# /html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[2]/div/div/div[1]/ul/li[11]/div
#         self.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span/span[1]")

        # /html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[3]/div[2]/div[2]/div[1]

        r = requests.get(varUrl)
        text = r.content.decode('utf8')
        # tree = lxml.html.fromstring(text)
        print(text)
        sleep(6)
        tree = etree.HTML(text)
        sleep(6)
        print(tree)

        # etree_root = clean_html(tree)
        # dom_tree = etree.ElementTree(etree_root)
        # dom_tree = etree.ElementTree(tree)
        # for e in dom_tree.iter():
        #     xpath = dom_tree.getpath(e)
        #     print(xpath)

        # # 解析HTML
        # # tree = etree.HTML(html_content)
        #
        # # 定位元素
        element = tree.xpath('//div[@class="top-main-list"]')[0]
        #
        # # 获取元素的XPath
        xpath = element.getroottree().getpath(element)
        print(xpath)  # 输出: /html/body/div/ul/li[1]

    def getAllWindowHandle(self):

        # 获取所有窗口句柄
        self.all_window_handles = self.driver.window_handles


    def swhWindowIndex(self, varIndex):

        # 切换窗口句柄index
        new_window_handle = self.driver.window_handles[varIndex]
        self.driver.switch_to.window(new_window_handle)


    def getUrlByClk(self):

        # 通过点击链接，获取url

        # 打开url，等待新窗口出现
        #
        # 新窗口总数增加 1
        try:
            WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(len(self.all_window_handles) + 1))
        except Exception as e:
            print(f"等待新窗口超时: {e}")
            self.driver.quit()
            exit()

        # 第二次获取所有窗口句柄
        self.all_window_handles2 = self.driver.window_handles

        # 找出新窗口的句柄
        new_window_handle = [handle for handle in self.all_window_handles2 if handle not in self.all_window_handles][0]

        # 切换到新窗口
        self.driver.switch_to.window(new_window_handle)

        return (self.driver.current_url)



    def find_elementNoWait(self, *loc):
        # 重写元素定位(无需等待)
        try:
            # Python特性，将入参放在元组里，入参loc，加*，变成元组。
            # WebDriverWait(self.driver,5).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下loc入参本身就是元组，所以不需要再加*
            # WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            print("未找到元素 %s " % (loc))

    def find_element(self, *loc):
        """重写元素定位"""
        try:
            # Python特性，将入参放在元组里，入参loc，加*，变成元组。
            # WebDriverWait(self.driver,5).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下loc入参本身就是元组，所以不需要再加*
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            print("未找到元素 %s " % (loc))

    def waitLoading(self, varXpath):
        # 创建WebDriverWait对象
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, varXpath)))

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
            print("未找到元素 %s " % (loc))



   # todo assert


    def assertTrue(self, testValue, errMsg):
        # ???
        try:
            if testValue == True:
                return True
            else:
                print(errMsg)
                return False
        except:
            return None

    def assertEqualTrue(self, varExpected, varActual):
        try:
            if varExpected == varActual:
                return True
            else:
                return False
        except:
            return None

    def assertEqual(self, varExpected, varActual, okMsg, errMsg):
        try:
            if varExpected == varActual:
                print(okMsg)
                return True
            else:
                print(errMsg)
                return False
        except:
            return None


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

    # def getError(self, varStatus, varErrorInfo, varErrorRow):
    #     # 当函数返回error时，获取当前语句行号及错误提示。
    #     # 因此函数必须要有返回值
    #     # Level_PO.getError(Level_PO.inputId(u"officebundle_tmoffice_officeName", u"自动化科室123"), u"输入框定位错误！",sys._getframe().f_lineno)
    #     # errorrrrrrrrrrr, 101行, '获取科室文本与对应值的字典'。
    #     if varStatus == "error":
    #         print("errorrrrrrrrrrr,", varErrorRow, "行,", varErrorInfo)
    #         sys.exit(0)



    # todo clk


    def getUrlByclkByX(self, varXpath, t=1):
        # 单点击，并返回url
        self.find_element(*(By.XPATH, varXpath)).click()
        sleep(7)
        return (self.driver.current_url)

    def clkByX(self, varXpath, t=1):
        # 单点击
        self.find_element(*(By.XPATH, varXpath)).click()
        sleep(t)


    def clkByXs(self, varXpaths, t=1):
        # 多点击
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            a.click()
            sleep(t)

    def clkIndexByXs(self, varXpaths, varIndex, t=1):
        # 单点击某个索引号
        # 如：遍历按钮点击第5个。clkIndexByXs(u"//button[@ng-click='action.callback()']",5)
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if index == varIndex:
                a.click()
                break
        sleep(t)

    def clkTextByTpcByXs(self, varXpaths, varTpc, t=1):
        # 单点击超链接文本（文本中包含部分内容））（varTPC = TextPartialContent)
        # 如：遍历按钮点击所有文本中包含20190506059的内容。clkTextByTpcByXs(u"//td[@aria-describedby='gridTable_run_name']/a",u"20190506059")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varTpc in a.text:
                a.click()
                break
        sleep(t)

    def clkTextByXs(self, varXpaths, varText, t=1):
        # 单点击超链接文本
        # 如：遍历按钮点击所有文本中包含20190506059的内容。clkTextsContain(u"//td[@aria-describedby='gridTable_run_name']/a",u"20190506059")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varText == a.text:
                a.click()
                break
        sleep(t)

    def clkTextByApcByXs(self, varXpaths, varAttr, varApc, t=1):
        # 单点击超链接文本（属性中包含部分内容）varAPC = (AttrPartialContent)
        # 如：遍历点击a链接属性href中包含www内容， clkTextByApcByXs("//a","href","www")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varApc in a.get_attribute(varAttr):
                a.click()
                break
        sleep(t)

    def clkTextByAcByXs(self, varXpaths, varAttr, varValue, t=1):
        # 单点击超链接文本（属性中对应的值）
        # 如：遍历点击a链接属性href = www.baidu.com， clkTextByAcByXs("//a","href","www.baidu.com")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varValue == a.get_attribute(varAttr):
                a.click()
                break
        sleep(t)

    def clkByXsByX(self, varXpaths, varXpath, t=1):
        # 二次确认
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            a.click()
            sleep(t)
            self.find_element(*(By.XPATH, varXpath)).click()
        sleep(t)

    def clkById(self, varId, t=1):
        self.find_element(*(By.ID, varId)).click()
        sleep(t)

    def clkByName(self, varName, t=1):
        self.find_element(*(By.NAME, varName)).click()
        sleep(t)

    def clkByTagname(self, varText, t=1):
        self.find_element(*(By.TAG_NAME, varText)).click()
        sleep(t)

    def clkByLinktext(self, varText, t=1):
        self.find_element(*(By.LINK_TEXT, varText)).click()
        sleep(t)

    def clkByLinkstext(self, varText, t=1):
        """通过linkstext点击"""
        for a in self.find_elements(*(By.LINK_TEXT, varText)):
            a.click()
        sleep(t)



    # todo get

    def getCountByTag(self, varLabel):
        # tag方式获取所有标签的数量
        c = self.find_elements(*(By.TAG_NAME, varLabel))
        return len(c)

    def eleGetCountByTag(self, ele, varLabel):
        # tag方式获取ele标签的数量
        # 获取tbody标签下所有的tr变迁数量
        # ele2 = self.getSuperEleByX("//tbody", ".")
        # self.eleGetCountByLabel(ele2, "tr")
        c = ele.find_elements(*(By.TAG_NAME, varLabel))
        return len(c)



    def getCountByXByXs(self, varXpath, varXpaths="./*"):
        # 获取xpath下标签的数量
        # 获取'.//tr/input'下所有div标签的数量 getCountByXByXs(ele, './/tr/input', "./div")
        # 获取'.//tr/input'下所有标签的数量 getCountByXByXs(ele, './/tr/input', "./*")
        parent_element = self.find_element(*(By.XPATH, varXpath))
        return len(parent_element.find_elements(*(By.XPATH, varXpaths)))

    def eleGetCountByXByXs(self, ele, varXpath, varXpaths="./*"):
        # 获取ele当前层下标签的数量
        # 获取'.//tr/input'下所有div标签的数量 eleGetCountByXByXs(ele, './/tr/input', "./div")
        # 获取'.//tr/input'下所有标签的数量 eleGetCountByXByXs(ele, './/tr/input', "./*")
        parent_element = ele.find_element(*(By.XPATH, varXpath))
        return len(parent_element.find_elements(*(By.XPATH, varXpaths)))

    def getCountByXs(self, varXpaths):
        # 获取标签数量
        # 获取tr下有多少个div标签 getCountByXs('//*[@id="app"]/tr/div')
        c = self.find_elements(*(By.XPATH, varXpaths))
        return len(c)

    def eleGetCountByXs(self, ele, varXpaths):
        # xpath方式获取ele标签数量
        # 获取'.//tr/div'下所有标签数量 eleGetCountByXs(ele, './/tr/div')
        return len(ele.find_elements(*(By.XPATH, varXpaths)))





    # def getTextByXnoWait(self, varXpath):
    #     # 获取文本
    #     # 如：getTextByX(u"//input[@class='123']")
    #     return self.find_elementNoWait(*(By.XPATH, varXpath)).text

    def getTextById(self, id):
        # 获取文本
        # 如：getTextByX(u"//input[@class='123']")
            return self.find_element(*(By.ID, id)).text


    def getTextByX(self, varXpath, wait='no'):
        # 获取文本
        # 如：getTextByX(u"//input[@class='123']")
        if wait == 'no':
            return self.find_elementNoWait(*(By.XPATH, varXpath)).text
        else:
            return self.find_element(*(By.XPATH, varXpath)).text


    def getTextByXs(self, varXpaths):
        # 获取文本列表
        # 如：getTextByXs(u"//input[@class='123']")
        l_ = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_.append(a.text)
        return l_


    def getIndexByXs(self, varXpaths, varText):
        # 获取文本的索引号
        # 获取test文本在tr里的位置，返回3，表示在第三个tr里，未找到返回none， 如：getIndexByXs("//tr",'test')
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if a.text == varText:
                return index
        return None

    def getIndexByTpcByXs(self, varXpaths, varTPC):
        # 获取文本包含部分内容(TPC)的索引号
        # 如：getIndexByTpcByXs("//tr","test")
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if varTPC in a.text:
                return index

    def getBeforeTextByXs(self, varXpaths, varText):
        # 获取指定文本之前的文本列表
        # 如文本集 a,b,c,d, getBeforeTextByXs("//tr",'c'), 返回列表【a,b】
        l_beforeText = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varText == a.text:
                break
            else:
                l_beforeText.append(a.text)
        return l_beforeText

    def getAttrValueByX(self, varXpath, varAttr, wait='no'):
        # 获取属性值
        # 如：getAttrValueByX(u"//input[@class='123']","href")
        if wait == 'no':
            return self.find_elementNoWait(*(By.XPATH, varXpath)).get_attribute(varAttr)
        else:
            return self.find_element(*(By.XPATH, varXpath)).get_attribute(varAttr)



    def getAttrValueByXs(self, varXpaths, varAttr):
        # 获取所有相同属性值的列表
        # 如：获取所有tr标签中 href的值 getAttrValueByXs("//tr", "href")
        l_attrValue = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_attrValue.append(a.get_attribute(varAttr))
        return l_attrValue

    def getAttrValueByLt(self, varText, varAttr):
        # 获取超链接文本的属性值
        # 如：getAttrValueByLt("超链接文本", "href")
        return self.find_element(*(By.LINK_TEXT, varText)).get_attribute(varAttr)

    def getIndexByAttrByXs(self, varXpaths, varAttr, varValue):
        # 获取属性值的索引号
        # 如：getIndexByAttrByXs("//a","href","http://www.baidu.com")
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if varValue == a.get_attribute(varAttr):
                return index

    def getIndexByApcByXs(self, varXpaths, varAttr, varValue):
        # 获取部分包含属性值的索引号 APC = attribute part content
        # 如：getIndexByApcByXs("//td[9]/a","href","http://")
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if varValue in a.get_attribute(varAttr):
                return index

    def getDictTextAttrValueByXs(self, varXpaths, varAttr):
        # 获取超链接文本及href，并组合成字典{文本：属性值}
        # 如获取所有a标签下的文本，getDictTextAttrValueByXs("//a","href")
        # {'首页': 'http://192.168.0.202:28098/index', '医院管理': 'http://192.168.0.202:28098/mainData/mainData/hospital'}
        l_text = []
        l_attrValue = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_text.append(a.text)
            l_attrValue.append(a.get_attribute(varAttr))
        return dict(zip(l_text, l_attrValue))

    def getUpEleByX(self, varXpath):
        # 通过标签下文本获取上一层元素
        # getUpEleByX("//div[@class='van-col']")  # 获取div下文本上一层的元素
        # getUpEleByX("//div[text()='文本']")  # 获取div下文本上一层的元素
        # getUpEleByX("//span[text()='文本']")  # 获取span下文本上一层的元素
        ele = self.find_element(*(By.XPATH, varXpath))
        return self.driver.execute_script("return arguments[0].parentNode;", ele)


    def getSuperEleByX(self, varXpath, varXpath2=".."):
        # 通过标签下文本获取上层或上上层元素
        # ele = self.getSuperEleByX("(//span[text()='详情'])[position()=3]", ".")  # 通过位置定位， 定位到第三个元素
        # 如：ele = self.getSuperEleByX("(//span[text()='过会'])[last()]", '../..') # 通过文本定位， 获取span标签下文本上上层的元素,如果有多个值，匹配最后一个。
        # 如：ele = self.getSuperEleByX("//span[text()='过会']", '../..') # 通过文本定位， 获取span标签下文本上上层的元素
        # ele = self.getSuperEleByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[2]/div[1]/div/div','.')  # 通过决绝路径定位， 获取当前路径
        # ele = self.getSuperEleByX("//div[@class='formList']", '.')  # 通过相对路径定位
        ele = self.find_element(*(By.XPATH, varXpath))
        return ele.find_element(*(By.XPATH, varXpath2))

        # # 计算匹配元素的数量，然后定位最后一个
        # index = len(driver.find_elements_by_xpath("//div[text()='特定文本']")) - 1
        # last_element = driver.find_elements_by_xpath("//div[text()='特定文本']")[index]
        # print(last_element.text)

    def getEleByClassName(self, className):
        ele = self.find_element(*(By.CLASS_NAME, className))
        return ele

    def getEleById(self, varId):
        ele = self.find_element(*(By.ID, varId))
        return ele


    # todo set

    def sendKeysByX(self, varXpath, varKeys, t=1):
        # 操作键盘
        # sendKeysByX(Keys.DELETE)
        self.find_element(*(By.XPATH, varXpath)).send_keys(varKeys)
        sleep(t)

    def eleSendKeysByX(self, ele, varXpath, varKeys, t=1):
        # ele操作键盘
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varKeys)
        sleep(t)

    def setTextById(self, varId, varText):
        """通过id设置文本"""
        self.find_element(*(By.ID, varId)).clear()
        self.find_element(*(By.ID, varId)).send_keys(varText)

    def appendTextById(self, varId, varText):
        """通过id追加文本"""
        self.find_element(*(By.ID, varId)).send_keys(varText)

    def setTextByName(self, varName, varText):
        """通过name设置文本"""
        self.find_element(*(By.ID, varName)).clear()
        self.find_element(*(By.NAME, varName)).send_keys(varText)

    def appendTextByName(self, varName, varText):
        """通过name追加文本"""
        self.find_element(*(By.NAME, varName)).send_keys(varText)


    def clkTabByX(self, varXpath, t=1):
        # 按tab
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.TAB)
        sleep(t)

    def setClearByX(self, varXpath, t=1):
        # 输入框清空
        self.find_element(*(By.XPATH, varXpath)).clear()
        sleep(t)

    def setTextByX(self, varXpath, varText, t=1):
        # 输入框清空后输入文本
        self.find_element(*(By.XPATH, varXpath)).clear()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        sleep(t)

    def setTextEnterByX(self, varXpath, varText, t=1):
        # 输入框清空后输入文本，按回车
        self.find_element(*(By.XPATH, varXpath)).clear()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)

    def setTextTabByX(self, varXpath, varText, t=1):
        # 输入框双击后输入文本，按Tab
        ele = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.double_click(ele).perform()
        sleep(t)
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.TAB)
        sleep(t)

    def setTextTabByX2(self, varXpath, varText, t=1):
        # 输入框双击后输入文本，按Tab
        ele = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        actions.double_click(ele).perform()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.TAB)
        sleep(t)

    def appentTextByX(self, varXpath, varText, t=1):
        # 输入框追加文本
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        sleep(t)

    def appendTextEnterByX(self, varXpath, varText, t=1):
        # 输入框追加文本，按回车
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)




    # todo shadow-root元素

    def getShadowByXByC(self, varXpath, varCss, t=1):
        # 获取shadow-root元素， shadow-root元素通过CSS_SELECTOR方法获得，不支持Xpath
        # 如：获取指定input下shadow-root元素div的文本 getShadowByXByC("//input", "div")
        ele = self.find_element(*(By.XPATH, varXpath))
        shadow_root = ele.shadow_root
        ele2 = shadow_root.find_element(By.CSS_SELECTOR, varCss)
        sleep(t)
        return (ele2.text)

    def getShadowByXsByC(self, varXpaths, varCss, t=1):
        # 获取shadow-root元素， shadow-root元素通过CSS_SELECTOR方法获得，不支持Xpath
        # 如：获取所有input下shadow-root元素div的文本 getShadowByXsByC("//input", "div")
        eles = self.find_elements(*(By.XPATH, varXpaths))
        l_shadow = []
        for i in eles:
            shadow_root = i.shadow_root
            ele2 = shadow_root.find_element(By.CSS_SELECTOR, varCss)
            l_shadow.append(ele2.text)
        sleep(t)
        return l_shadow



    # todo ele元素再定位

    def eleGetSuperEleByX(self, ele, varXpath, varXpath2=".."):
        # 通过标签下文本获取上层或上上层元素
        # 如：ele = self.eleGetSuperEleByX(ele, ".//span[text()='过会']", '../..') # 获取span标签下文本上上层的元素
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        return ele2.find_element(*(By.XPATH, varXpath2))

    def eleClearByX(self, ele, varXpath, t=1):
        # 定位元素之
        # e = ele.find_element(*(By.XPATH, varXpath))
        # e.clear()
        ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)

        # self.find_element(*(By.XPATH, varXpath)).clear()
        # sleep(t)
        sleep(t)

    def eleClkByX(self, ele, varXpath, t=2):
        # 定位元素之点击
        e = ele.find_element(*(By.XPATH, varXpath))
        e.click()
        sleep(t)

    def eleClkByXs(self, ele, varXpaths, t=1):
        # 定位元素之遍历点击
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            a.click()
            sleep(t)
        
    def eleGetShadowByXByC(self, ele, varXpath, varCss, t=1):
        # 定位元素之遍历shadow-root获取文本
        # shadow-root元素通过CSS_SELECTOR方法获得，不支持Xpath
        # 如： 获取input下所有shadow-root元素div的文本 eleGetShadowByXByC(ele, ".//table[1]/input", 'div:nth-last-of-type(1)')
        # 'div:nth-last-of-type(1)' 表示多个div时，获取最后一个div的text
        ele = ele.find_element(*(By.XPATH, varXpath))
        shadow_root = ele.shadow_root
        ele2 = shadow_root.find_element(By.CSS_SELECTOR, varCss)
        sleep(t)
        return ele2.text

    def eleGetShadowByXsByC(self, ele, varXpaths, varCss, t=1):
        # 定位元素之遍历shadow-root获取文本
        # shadow-root元素通过CSS_SELECTOR方法获得，不支持Xpath
        # 如： 获取input下所有shadow-root元素div的文本 eleGetShadowByXsByC(ele, ".//table[1]/input", "div")
        eles = ele.find_elements(*(By.XPATH, varXpaths))
        l_shadow = []
        for i in eles:
            shadow_root = i.shadow_root
            ele2 = shadow_root.find_element(By.CSS_SELECTOR, varCss)
            # ele2 = shadow_root.find_element(By.TAG_NAME, varCss)
            l_shadow.append(ele2.text)
        sleep(t)
        return l_shadow

    def eleGetValueByAttr(self, ele, varAttr):
        # 定位元素之获取属性
        return ele.get_attribute(varAttr)

    def eleGetAttrValueByX(self, ele, varXpath, varAttr):
        # 获取属性值
        # 如：eleGetAttrValueByX(ele, u"//input[@class='123']","href")
        return ele.find_element(*(By.XPATH, varXpath)).get_attribute(varAttr)

    def eleGetAttrValueByXs(sself, ele, varXpaths, varAttr):
        # 遍历获取属性值
        # 如：eleGetAttrValueByXs(ele, u"//input[@class='123']", "href")
        l_ = []
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            l_.append(a.get_attribute(varAttr))
        return l_




   

    def eleGetTextByX(self, ele, varXpath):
        # 定位元素之获取文本
        return ele.find_element(*(By.XPATH, varXpath)).text

    def eleGetTextByXs(self, ele, varXpaths):
        # 定位元素之遍历获取文本
        l_ = []
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            l_.append(a.text)
        return l_

    def eleGetTextByXsByX(self, ele, varXpaths, varXpath):
        # 定位元素之遍历获取div文本
        # eleGetTextByXsByX(ele, ".//div[3]/div", ".//div")  # div下的text
        l_ = []
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            l_.append(a.find_element(*(By.XPATH, varXpath)).text)
        return l_

    def eleSetTextByX(self, ele, varXpath, varValue):
        # 定位元素之输入
        ele.find_element(*(By.XPATH, varXpath)).clear()
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varValue)

    def eleSetTextByX2(self, ele, varXpath, varValue):
        # 定位元素之输入
        # ele.find_element(*(By.XPATH, varXpath)).clear()
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varValue)

    def eleSetTextEnterByX(self, ele, varXpath, varValue, t=1):
        # 定位元素之输入并回车
        ele.find_element(*(By.XPATH, varXpath)).clear()
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varValue)
        ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)

    def eleTabByX(self, ele, varXpath, t=1):
        # 定位元素之输入并回车
        ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.TAB)
        sleep(t)

    def eleSetTextTabByX(self, ele, varXpath, varText, t=1):
        # 输入框双击后输入文本，按Tab
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.double_click(ele2).perform()
        sleep(t)
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.TAB)
        sleep(t)

    def setTextBackspaceEnterByX(self, varXpath, varValue, varN=3):
        # 定位元素之3次点击删除并输入和回车
        # 如：输入框中按键盘删除键3次后再输入和回车 setTextBackspaceEnterByX(varXpath, varValue)
        for i in range(varN):
            self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        # self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.CONTROL, 'a')
        # self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.CONTROL, 'x')
        self.find_element(*(By.XPATH, varXpath)).send_keys(varValue)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(2)

    def eleSetTextBackspaceEnterByX(self, ele, varXpath, varN, varValue, t=3):
        # 定位元素之N次点击删除并输入和回车
        # 如：输入框中按键盘删除键3次后再输入和回车 eleSetTextBackspaceEnterByX(ele, varXpath, 3, varValue)
        for i in range(varN):
            ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        # ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.CONTROL, 'a')
        # ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.CONTROL, 'x')
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varValue)
        ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)

    def setTextClkByXByX(self, varXpath, varValue, varXpath2, t=1):
        # 定位元素之输入与二次确认
        self.find_element(*(By.XPATH, varXpath)).clear()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varValue)
        sleep(t)
        self.find_element(*(By.XPATH, varXpath2)).click()

    def eleSetTextClkByXByX(self, ele, varXpath, varValue, varXpath2, t=1):
        # 定位元素之输入与二次确认
        ele.find_element(*(By.XPATH, varXpath)).clear()
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varValue)
        sleep(t)
        ele.find_element(*(By.XPATH, varXpath2)).click()

    def doubleClkByX(self, varXpath, t=2):
        # 定位元素之双击
        ele2 = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.double_click(ele2).perform()
        sleep(t)

    def eleDoubleClkByX(self, ele, varXpath, t=2):
        # 定位元素之双击
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.double_click(ele2).perform()
        sleep(t)

    def ctrlAByX(self, varXpath, t=2):
        # 定位元素之全选
        ele2 = self.find_element(*(By.XPATH, varXpath))
        ele2.click()
        actions = ActionChains(self.driver)
        actions.key_down(ele2, "Control").send_keys('a').key_up('Control').perform()
        sleep(t)

    def eleCtrlAByX(self, ele, varXpath, t=2):
        # 定位元素之全选
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        ele2.click()
        actions = ActionChains(self.driver)
        actions.key_down(ele2, "Control").send_keys('a').key_up('Control').perform()
        sleep(t)

    def eleScrollUpDownByX(self, ele, varXpath, varStep, t=2):
        # 定位元素之上下滚动（用于app上时间日期控件）
        # step 负数向上滚动，正数向下滚动
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(ele2)
        actions.click_and_hold()
        # actions.move_by_offset(0, varStep)
        if varStep != 0:
            if varStep >= 150:
                actions.move_by_offset(0, 150)
            elif varStep <= -500:
                actions.move_by_offset(0, -500)
            else:
                actions.move_by_offset(0, varStep)
        actions.release()
        actions.perform()
        sleep(t)

    def eleScrollLeftRightByX(self, ele, varXpath, varStep, t=2):
        # 定位元素之左右滚动
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(ele2)
        actions.click_and_hold()
        actions.move_by_offset(varStep, 0)
        actions.release()
        actions.perform()
        sleep(t)

    def eleScrollViewByX(self, ele, varXpath, t=1):
        # 定位元素之元素滚动到可见区域
        # ele = self.find_element(*(By.XPATH, "//a[@href='#/meeting']"))  Xpath方式定位
        # eleScrollViewByX(ele, "//a[last()]")  # 拖动到最后一个a标签
        element = ele.find_element(*(By.XPATH, varXpath))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)  # 将元素滚动到可见区域
        sleep(t)

    def eleScrollBottomByXN(self, ele, varXpath, varCount, t=2):
        # 定位元素之键盘keys.End滚动到底部
        # 逻辑：滚动N次 keys.end 到 varPath元素
        # 用法：先获取整个页面高度，滚动的大框 ，如下实例
        # # 定位大框
        # ele = self.Web_PO.getSuperEleByX('/html/body/div[1]/div/div[3]/section')
        # # 滚动3次到元素
        # self.Web_PO.eleScrollBottomByXN(ele, '/html/body/div[1]/div/div[3]/section/div/div/div[2]/div[2]/div/span[1]', 3, 0)
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        for i in range(varCount):
            ActionChains(self.driver).send_keys_to_element(ele2, Keys.END).perform()
            sleep(1)
        sleep(t)

    def eleScrollBottomByXNX(self, ele, varXpath, varCount, varXpath2, t=2):
        # 定位元素之键盘keys.End滚动到底部
        # 逻辑：定位varPath元素，遍历keys.end N次, 如遇到varPath2元素则停止滚动
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        for i in range(varCount):
            ActionChains(self.driver).send_keys_to_element(ele2, Keys.END).perform()
            sleep(1)
            if self.isEleExistByX(varXpath2):
                break
        sleep(t)

    def eleScrollBottomByX(self, ele, varXpath, t=2):
        # 定位元素之键盘keysEnd滚动到底部(用于移动端)
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        ActionChains(self.driver).send_keys_to_element(ele2, Keys.END).perform()
        sleep(t)




    # todo radio

    def eleRadioLeftLabelByN(self, ele, varXpaths, v):
        # eleRadioSplitDivs
        # 选择单选框
        # 不独立值（有\n拼接）,遍历div
        # self.eleRadioSplitDivs(ele, "/html/body/div[2]/div[6]/div/div[2]/div[1]/ul/li", v)
        l_ = self.eleGetTextByXs(ele, varXpaths)
        l_ = [i for i in l_ if i]  # 过滤掉空的元素
        l_ = l_[0].split('\n')
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}

        # 获取单选框所有值的状态
        l_value = self.eleGetTextByXs(ele, ".//label/span[2]")
        # print(l_value)  # ['是', '否']
        # 获取单选框所有值的状态
        l_class = self.eleGetAttrValueByXs(ele, ".//label", "class")
        # print(l_class)  # ['el-radio el-radio--default', 'el-radio is-checked el-radio--default']
        l_isChecked = []
        for i in range(len(l_class)):
            if l_class[i] == 'el-radio is-checked el-radio--default' or l_class[i] == 'el-radio is-disabled is-checked el-radio--default':
                l_isChecked.append(1)
            else:
                l_isChecked.append(0)
        d_default = dict(zip(l_value, l_isChecked))
        # print(d_default)  # {'是': 0, '否': 1}
        # 检查是否已经选中，如果未选择则勾选，否则不操作。
        if d_default[v] == 0:
            self.eleClkByX(ele, varXpaths + "[" + str(d_4[v]) + "]/label", 1)
    def eleRadioRightLabelByN(self, ele, varXpaths, v):
        # eleRadioSplitLabels
        # 选择单选框
        # 不独立值（有\n拼接），遍历label
        l_ = self.eleGetTextByXs(ele, varXpaths)
        l_ = [i for i in l_ if i]  # 过滤掉空的元素
        l_ = l_[0].split('\n')
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}

        # 获取单选框所有值的状态
        l_value = self.eleGetTextByXs(ele, ".//label/span[2]")
        # print(l_value)  # ['是', '否']
        # 获取单选框所有值的状态
        l_class = self.eleGetAttrValueByXs(ele, ".//label", "class")
        # print(l_class)  # ['el-radio el-radio--default', 'el-radio is-checked el-radio--default']
        l_isChecked = []
        for i in range(len(l_class)):
            if l_class[i] == 'el-radio is-checked el-radio--default' or l_class[
                i] == 'el-radio is-disabled is-checked el-radio--default':
                l_isChecked.append(1)
            else:
                l_isChecked.append(0)
        d_default = dict(zip(l_value, l_isChecked))
        # print(d_default)  # {'是': 0, '否': 1}
        # 检查是否已经选中，如果未选择则勾选，否则不操作。
        if d_default[v] == 0:
            self.eleClkByX(ele, varXpaths + "/label[" + str(d_4[v]) + "]", 1)

    def eleRadioLeftLabel(self, ele, varTextByXs, v):
        # 单选框LL
        d_4 = {v: k for k, v in dict(enumerate(self.eleGetTextByXs(ele, varTextByXs), start=1)).items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
        self.eleClkByX(ele, varTextByXs + "[" + str(d_4[v]) + "]/label", 1)

    def eleRadioLeftLabelByCheck(self, ele, varXpaths, v):
        # 单选框LL + 判断是否选中 ????
        l_ = self.eleGetTextByXs(ele, ".//div")
        print(l_)
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}

        # 获取所有选择值的状态
        l_value = self.eleGetTextByXs(ele, ".//label/span[2]")
        # print(l_value)  # ['是', '否']
        # l_class = self.eleGetAttrValueByXs(ele, ".//label", "class")
        l_class = self.eleGetAttrValueByXs(ele, ".//label[@aria-disabled='false']", "class")
        # print(l_class)  # ['el-radio el-radio--default', 'el-radio is-checked el-radio--default']
        l_isChecked = []
        for i in range(len(l_class)):
            if l_class[i] == 'el-radio is-checked el-radio--default' or l_class[
                i] == 'el-radio is-disabled is-checked el-radio--default':
                l_isChecked.append(1)
            else:
                l_isChecked.append(0)
        d_default = dict(zip(l_value, l_isChecked))
        print('是否选中 =>', d_default)  # {'是': 0, '否': 1}

        # 判断是否选中，如果未选择则勾选，否则不操作。
        if d_default[v] == 0:
            self.eleClkByX(ele, varXpaths + "[" + str(d_4[v]) + "]", 1)
            return 0
        else:
            return 1


    def eleRadioRightLabel(self, ele, varTextByXs, v):
        # 单选框RL
        d_4 = {v: k for k, v in dict(enumerate(self.eleGetTextByXs(ele, varTextByXs), start=1)).items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
        self.eleClkByX(ele, varTextByXs + "[" + str(d_4[v]) + "]", 1)

    def eleRadioRightLabelAndText(self, ele, varRadioRightLableByX, v, varTextByX):
        # 单选框 + 判断是否选中 + 文本输入框
        # 适配：{'有':'123'}
        # self.eleRadioRightLabelAndText(self.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/label", v, ".//div[2]/div[2]/div/div/div/input")
        # self.eleRadioRightLabel(ele, varRadioRightLableByX, list(v.keys())[0])
        isRadio = self.eleRadioRightLabelByCheck(ele, varRadioRightLableByX, list(v.keys())[0])
        # self.eleSetTextByX(ele, varTextByX, v[list(v.keys())[0]][list(v[list(v.keys())[0]].keys())[0]])
        if isRadio == 0:
            self.eleSetTextByX(ele, varTextByX, v[list(v.keys())[0]])

    def eleRadioRightLabelByCheck(self, ele, varXpaths, v):
        # 单选框 + 判断是否选中
        l_ = self.eleGetTextByXs(ele, varXpaths)
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}

        # 获取所有选择值的状态
        l_value = self.eleGetTextByXs(ele, ".//label/span[2]")
        # print(l_value)  # ['是', '否']
        # l_class = self.eleGetAttrValueByXs(ele, ".//label", "class")
        l_class = self.eleGetAttrValueByXs(ele, ".//label[@aria-disabled='false']", "class")
        # print(l_class)  # ['el-radio el-radio--default', 'el-radio is-checked el-radio--default']
        l_isChecked = []
        for i in range(len(l_class)):
            if l_class[i] == 'el-radio is-checked el-radio--default' or l_class[
                i] == 'el-radio is-disabled is-checked el-radio--default':
                l_isChecked.append(1)
            else:
                l_isChecked.append(0)
        d_default = dict(zip(l_value, l_isChecked))
        print('是否选中 =>', d_default)  # {'是': 0, '否': 1}

        # 判断是否选中，如果未选择则勾选，否则不操作。
        if d_default[v] == 0:
            self.eleClkByX(ele, varXpaths + "[" + str(d_4[v]) + "]", 1)
            return 0
        else:
            return 1



    # todo checkbox

    def eleCheckboxLeftLabelByN(self, ele, textByX, v, default="remain"):
        # eleCheckboxSplitDivs
        # 勾选复选框
        # 不独立值（有\n拼接值），divs
        # self._eleClkCheckbox(self._eleDiv(ele, k, "../.."), "./div[1]/div[2]/div/div/div/div", v)

        # 获取所有的选项
        l_ = self.eleGetTextByXs(ele, textByX)
        print(l_)
        l_ = [i for i in l_ if i]  # 过滤掉空的元素
        print(l_)
        l_ = l_[0].split('\n')
        print(l_)  # ['无', '青霉素类抗生素', '磺胺类抗生素', '头孢类抗生素', '含碘药品', '酒精', '镇静麻醉剂', '其他药物过敏源']
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        print(d_4)  # {'无': 1, '青霉素类抗生素': 2, '磺胺类抗生素': 3, '头孢类抗生素': 4, '含碘药品': 5, '酒精': 6, '镇静麻醉剂': 7, '其他药物过敏源': 8}

        # 全部取消勾选项
        if default != 'remain':
            l_2 = []
            for i in range(len(l_)):
                l_2.append(self.eleGetAttrValueByX(ele, textByX + "[" + str(i + 1) + "]/label", "class"))
            d_3 = dict(enumerate(l_2, start=1))
            # print(d_3)  # {1: 'el-checkbox el-checkbox--default is-disabled', 2: 'el-checkbox el-checkbox--default is-checked',
            for k2, v2 in d_3.items():
                if v2 == 'el-checkbox el-checkbox--default is-checked':
                    self.eleClkByX(ele, textByX + "[" + str(k2) + "]/label", 1)

        # 勾选选项(如果已勾选则不操作)
        for i in range(len(v)):
            for k3, v3 in d_4.items():
                if isinstance(v[i], str):
                    if v[i] == k3:
                        varClass = self.eleGetAttrValueByX(ele, textByX + "[" + str(v3) + "]/label", "class")
                        if varClass != 'el-checkbox el-checkbox--default is-checked':
                            self.eleClkByX(ele, textByX + "[" + str(v3) + "]/label", 1)
                elif isinstance(v[i], list):
                    if v[i][0] == k3:
                        varClass = self.eleGetAttrValueByX(ele, textByX + "[" + str(v3) + "]/label", "class")
                        if varClass != 'el-checkbox el-checkbox--default is-checked':
                            self.eleClkByX(ele, textByX + "[" + str(v3) + "]/label", 1)
                if isinstance(v[i], dict):
                    if list(v[i].keys())[0] == k3:
                        varClass = self.eleGetAttrValueByX(ele, textByX + "[" + str(v3) + "]/label", "class")
                        if varClass != 'el-checkbox el-checkbox--default is-checked':
                            self.eleClkByX(ele, textByX + "[" + str(v3) + "]/label", 1)
    def eleCheckboxLeftLabelAndTextByN(self, ele, textByX, v, text2ByX):
        # LLN复选框（全部取消 + 文本输入）
        # self.eleCheckboxLeftLabelAndTextByN(self.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div[1]/div", v, ".//div[2]/div/div/div/div/textarea")
        self.eleCheckboxLeftLabelByN(ele, textByX, v)
        for i in v:
            if isinstance(i, dict):
                self.eleSetTextByX(ele, text2ByX, i[list(i.keys())[0]])

    def eleCheckboxLeftLabel(self, ele, textByX, v, default="remain"):
        # LL复选框(全部取消)
        # self.eleClkCheckbox(self._eleDiv(ele, k, "../.."), "./div[1]/div[2]/div/div/div/div", v)

        # 获取所有的选项
        l_ = self.eleGetTextByXs(ele, textByX)
        # l_= List_PO.dels(l_, "")
        # print(l_)  # ['无', '青霉素类抗生素', '磺胺类抗生素', '头孢类抗生素', '含碘药品', '酒精', '镇静麻醉剂', '其他药物过敏源']
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        # print("d_4: ", d_4)  # {'无': 1, '青霉素类抗生素': 2, '磺胺类抗生素': 3, '头孢类抗生素': 4, '含碘药品': 5, '酒精': 6, '镇静麻醉剂': 7, '其他药物过敏源': 8}

        # 全部取消勾选项
        # if default != 'remain':
        l_2 = []
        for i in range(len(l_)):
            if self.eleIsEleExistByX(ele, textByX + "[" + str(i + 1) + "]/label"):
                l_2.append(self.eleGetAttrValueByX(ele, textByX + "[" + str(i + 1) + "]/label", "class"))
        d_3 = dict(enumerate(l_2, start=1))
        # print(d_3)  # {1: 'el-checkbox el-checkbox--default is-disabled', 2: 'el-checkbox el-checkbox--default is-checked',
        for k2, v2 in d_3.items():
            if v2 == 'el-checkbox el-checkbox--default is-checked':
                self.eleClkByX(ele, textByX + "[" + str(k2) + "]/label", 1)

        # 勾选选项
        for i in range(len(v)):
            for k3, v3 in d_4.items():
                if isinstance(v[i], str):
                    if v[i] == k3:
                        varClass = self.eleGetAttrValueByX(ele, textByX + "[" + str(v3) + "]/label", "class")
                        if varClass != 'el-checkbox el-checkbox--default is-checked':
                            self.eleClkByX(ele, textByX + "[" + str(v3) + "]/label", 1)
                if isinstance(v[i], list):
                    if v[i][0] == k3:
                        varClass = self.eleGetAttrValueByX(ele, textByX + "[" + str(v3) + "]/label", "class")
                        if varClass != 'el-checkbox el-checkbox--default is-checked':
                            self.eleClkByX(ele, textByX + "[" + str(v3) + "]/label", 1)
                if isinstance(v[i], dict):
                    if list(v[i].keys())[0] == k3:
                        varClass = self.eleGetAttrValueByX(ele, textByX + "[" + str(v3) + "]/label", "class")
                        if varClass != 'el-checkbox el-checkbox--default is-checked':
                            self.eleClkByX(ele, textByX + "[" + str(v3) + "]/label", 1)
    def eleCheckboxLeftLabelAndText(self, ele, textByX, v, text2ByX):
        # LL复选框（全部取消 + 文本输入）
        # self.eleCheckboxLeftLabelAndText(self.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div[1]/div", v, ".//div[2]/div/div/div/div/textarea")
        self.eleCheckboxLeftLabel(ele, textByX, v)
        for i in v:
            if isinstance(i, dict):
                self.eleSetTextByX(ele, text2ByX, i[list(i.keys())[0]])

    def eleCheckboxLeftLabel2(self, ele, textByX, v):
        # LL复选框 (全部取消 + 包括字典key)
        # self.eleCheckboxLeftLabel2(self._eleDiv(ele, k, "../.."), "./div[1]/div[2]/div/div/div/div", v)

        # 获取所有的选项
        l_ = self.eleGetTextByXs(ele, textByX)
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        # print(d_4)  # {'无': 1, '青霉素类抗生素': 2, '磺胺类抗生素': 3, '头孢类抗生素': 4, '含碘药品': 5, '酒精': 6, '镇静麻醉剂': 7, '其他药物过敏源': 8}

        # 取消全部勾选项
        for i in range(len(l_)):
            varDiv1class = self.eleGetAttrValueByX(ele, textByX + "[" + str(i + 1) + "]/label", "class")
            if varDiv1class == 'el-checkbox el-checkbox--default is-checked':
                self.eleClkByX(ele, textByX + "[" + str(i + 1) + "]")

        # 遍历勾选选项
        for i in range(len(v)):
            for k3, v3 in d_4.items():
                if isinstance(v[i], str):
                    if v[i] == k3:
                        # varClass = self.eleGetAttrValueByX(ele, _checkboxByX + "[" + str(v3) + "]/label", "class")
                        # if varClass != 'el-checkbox el-checkbox--default is-checked':
                        self.eleClkByX(ele, textByX + "[" + str(v3) + "]/label", 1)
                # elif isinstance(v[i], list):
                #     if v[i][0] == k3:
                #         varClass = self.eleGetAttrValueByX(ele, textByX + "[" + str(v3) + "]/label", "class")
                #         if varClass != 'el-checkbox el-checkbox--default is-checked':
                #             self.eleClkByX(ele, textByX + "[" + str(v3) + "]/label", 1)
                if isinstance(v[i], dict):
                    if list(v[i].keys())[0] == k3:
                        # varClass = self.eleGetAttrValueByX(ele, textByX + "[" + str(v3) + "]/label", "class")
                        # if varClass != 'el-checkbox el-checkbox--default is-checked':
                        self.eleClkByX(ele, textByX + "[" + str(v3) + "]/label", 1)



    def eleCheckboxRightLabel(self, ele, textByX, v):
        # 勾选复选框

        # 获取所有的选项
        l_ = self.eleGetTextByXs(ele, textByX)
        # print(l_)  # ['无', '青霉素类抗生素', '磺胺类抗生素', '头孢类抗生素', '含碘药品', '酒精', '镇静麻醉剂', '其他药物过敏源']
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        # print(d_4)  # {'无': 1, '青霉素类抗生素': 2, '磺胺类抗生素': 3, '头孢类抗生素': 4, '含碘药品': 5, '酒精': 6, '镇静麻醉剂': 7, '其他药物过敏源': 8}

        # 取消全部已勾选项
        self.eleClrSelectedByXs(ele, ".//td[4]/div/div/div/label[1]")
        # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/form/table/tbody/tr[5]/td[4]/div/div/div/label[1]/span[1]/input

        # 勾选选项(如果已勾选则不操作)
        for i in range(len(v)):
            for k3, v3 in d_4.items():
                if isinstance(v[i], str):
                    if v[i] == k3:
                        varClass = self.eleGetAttrValueByX(ele, ".//div/div/label[" + str(v3) + "]", "class")
                        if varClass != 'el-checkbox el-checkbox--default is-checked':
                            self.eleClkByX(ele, ".//div/div/label[" + str(v3) + "]", 1)

    def eleCheckboxRightLabel2(self, ele, textByX, v, varClass='el-checkbox el-checkbox--default is-checked'):
        # 勾选复选框（包括字典key）
        # 步骤：先取消全部勾选项，再勾选指定复选框值
        # 实例：eleCheckboxRightLabel2(ele, ".//td[4]/div/div/div/label", ['糖尿病', {'其他': '123'}]) ， 只勾选 糖尿病和其他，但不处理123

        # 获取所有选项
        l_ = self.eleGetTextByXs(ele, textByX)  # ".//td[4]/div/div/div/label"
        # print(l_)  # ['无', '青霉素类抗生素', '磺胺类抗生素', '头孢类抗生素', '含碘药品', '酒精', '镇静麻醉剂', '其他']
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        print(d_4)  # {'无': 1, '青霉素类抗生素': 2, '磺胺类抗生素': 3, '头孢类抗生素': 4, '含碘药品': 5, '酒精': 6, '镇静麻醉剂': 7, '其他': 8}

        # 取消全部勾选项
        for i in range(len(l_)):
            varDiv1class = self.eleGetAttrValueByX(ele, textByX + "[" + str(i+1) + "]", "class")
            # if varDiv1class == 'el-checkbox el-checkbox--default is-checked':
            # if varDiv1class == 'el-checkbox el-checkbox--large is-checked':
            if varDiv1class == varClass:
                self.eleClkByX(ele, textByX + "[" + str(i+1) + "]")


        # 遍历勾选选项
        for i in range(len(v)):
            for k3, v3 in d_4.items():
                if isinstance(v[i], str):
                    if v[i] == k3:
                        self.eleClkByX(ele, textByX + "[" + str(v3) + "]", 1)
                if isinstance(v[i], dict):
                    if list(v[i].keys())[0] == k3:
                        self.eleClkByX(ele, textByX + "[" + str(v3) + "]", 1)

    def eleCheckbox(self, ele, textByX, v):
        # 勾选复选框（包括字典key）,1个
        # 步骤：先取消全部勾选项，再勾选指定复选框值
        # 实例：eleCheckboxRightLabel2(ele, ".//td[4]/div/div/div/label", ['糖尿病', {'其他': '123'}]) ， 只勾选 糖尿病和其他，但不处理123

        # 获取所有选项
        l_ = self.eleGetTextByXs(ele, textByX)  # ".//td[4]/div/div/div/label"
        # print(l_)  # ['无', '青霉素类抗生素', '磺胺类抗生素', '头孢类抗生素', '含碘药品', '酒精', '镇静麻醉剂', '其他']
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        print(d_4)  # {'无': 1, '青霉素类抗生素': 2, '磺胺类抗生素': 3, '头孢类抗生素': 4, '含碘药品': 5, '酒精': 6, '镇静麻醉剂': 7, '其他': 8}

        # 取消全部勾选项
        for i in range(len(l_)):
            varDiv1class = self.eleGetAttrValueByX(ele, textByX + "[" + str(i+1) + "]", "class")
            if varDiv1class == 'el-checkbox el-checkbox--default is-checked':
                self.eleClkByX(ele, textByX + "[" + str(i+1) + "]")

        # 遍历勾选选项
        for k3, v3 in d_4.items():
            self.eleClkByX(ele,  ".//div[2]/div[" + str(v3+1) + "]/div[1]/div/label", 1)

    def eleCheckboxRightLabelByN(self, ele, textByX, v):
        # eleCheckboxSplitLabels
        # 勾选复选框
        # 不独立值（有\n拼接值），遍历label
        # 获取所有的选项
        l_ = self.eleGetTextByXs(ele, textByX)
        print(l_)
        # l_ = [i for i in l_ if i]  # 过滤掉空的元素
        l_ = l_[0].split('\n')
        print(l_)  # ['无', '青霉素类抗生素', '磺胺类抗生素', '头孢类抗生素', '含碘药品', '酒精', '镇静麻醉剂', '其他药物过敏源']
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        print(d_4)  # {'无': 1, '青霉素类抗生素': 2, '磺胺类抗生素': 3, '头孢类抗生素': 4, '含碘药品': 5, '酒精': 6, '镇静麻醉剂': 7, '其他药物过敏源': 8}

        # 取消全部勾选项
        for i in range(len(l_)):
            varDiv1class = self.eleGetAttrValueByX(ele, textByX + "[" + str(i + 1) + "]", "class")
            if varDiv1class == 'el-checkbox el-checkbox--default is-checked':
                self.eleClkByX(ele, textByX + "[" + str(i + 1) + "]")

        # # 遍历勾选选项
        for i in range(len(v)):
            for k3, v3 in d_4.items():
                if isinstance(v[i], str):
                    if v[i] == k3:
                        self.eleClkByX(ele, textByX + "[" + str(v3) + "]", 1)
                if isinstance(v[i], dict):
                    if list(v[i].keys())[0] == k3:
                        self.eleClkByX(ele, textByX + "[" + str(v3) + "]", 1)

        # # 勾选选项(如果已勾选则不操作)
        # for i in range(len(v)):
        #     for k3, v3 in d_4.items():
        #         if isinstance(v[i], str):
        #             if v[i] == k3:
        #                 varClass = self.eleGetAttrValueByX(ele, ".//div/div/label[" + str(v3) + "]", "class")
        #                 if varClass != 'el-checkbox el-checkbox--default is-checked':
        #                     self.eleClkByX(ele, ".//div/div/label[" + str(v3) + "]", 1)

    def eleCheckboxRightLabel3(self, ele, _textByX, _inputByX, v):
        # 复选框，取消全部勾选，再勾选复选框，输入次数
        # Web_PO.eleCheckboxRightLabel3(Web_PO.eleP(ele, k, "../.."), './/div[2]/div/div[1]/div/div/label', './/div[2]/div/div[1]/div/div/div/input', v)
        # 实例：__eleCheckboxRightLabel3(ele, ".//td[4]/div/div/div/label", {'无':"",'肺炎': '12', '外伤': '44', '其他': "3333"})

        l_v2 = list(v.keys())  # 将字典的键转换为列表

        # 获取所有选项
        l_ = self.eleGetTextByXs(ele, _textByX)  # ".//td[4]/div/div/div/label"
        l_ = [item.strip() for item in l_]
        # print(l_)  # ['无', '青霉素类抗生素', '磺胺类抗生素', '头孢类抗生素', '含碘药品', '酒精', '镇静麻醉剂', '其他药物过敏源']
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        # print(d_4)  # {'无': 1, '青霉素类抗生素': 2, '磺胺类抗生素': 3, '头孢类抗生素': 4, '含碘药品': 5, '酒精': 6, '镇静麻醉剂': 7, '其他药物过敏源': 8}

        # 取消全部勾选项
        for i in range(len(l_)):
            varDiv1class = self.eleGetAttrValueByX(ele, _textByX + "[" + str(i+1) + "]", "class")
            if varDiv1class == 'el-checkbox el-checkbox--default is-checked':
                self.eleClkByX(ele, _textByX + "[" + str(i+1) + "]")

        # 勾选选项, 遇到字典的话，勾选key
        for i in range(len(l_v2)):
            for k3, v3 in d_4.items():
                if l_v2[i] == k3 and k3 != "无":
                    self.eleClkByX(ele, _textByX + "[" + str(v3) + "]", 1)
                    self.eleSetTextByX(ele, _inputByX + "[" + str(v3-1) + "]/input", v[k3])

    def eleCheckboxRightLabelAndText(self, ele, varCheckboxRightLableByX, v, varTextByX):
        # 复选框，rightlabel + 全部取消 + 文本输入框
        # Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleP(ele, k, "../.."), './/div[2]/div/div[1]/div/div/label', v, './/div[2]/div/div[1]/div/div/div/input')
        self.eleCheckboxRightLabel2(ele, varCheckboxRightLableByX, v)
        for i in v:
            if isinstance(i, dict):
                self.eleSetTextByX(ele, varTextByX, i[list(i.keys())[0]])


    def isSelectedByX(self, varXpath):
        # 是否勾选
        # 返回 True 或 False
        # isSelectedByX(u"//input[@class='123']")
        return self.find_element(*(By.XPATH, varXpath)).is_selected()

    def eleIsSelectedByX(self, ele, varXpath):
        # ele是否勾选
        # 返回 True 或 False
        # eleIsSelectedByX(ele, u"//input[@class='123']")
        return ele.find_element(*(By.XPATH, varXpath)).is_selected()

    def clrSelectedByXs(self, varXpaths):
        # 取消所有已勾选的复选框
        # clrSelectedByXs(u"//input[@type='checkbox']")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if a.is_selected() == True:
                a.click()

    def eleClrSelectedByXs(self, ele, varXpaths):
        # ele取消所有已勾选的复选框
        # eleClrSelectedByXs(ele, u"//input[@type='checkbox']")
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            if a.is_selected() == True:
                a.click()


    # todo location

    def button1(self, varButton="保存"):
        # 页面button适配，只限单个按钮
        try:
            self.eleClkByX(self.getSuperEleByX("(//span[text()='" + str(varButton) + "'])[last()]", ".."), ".", 2)
        except:
            try:
                self.eleClkByX(self.getSuperEleByX("(//span[text()=' " + str(varButton) + " '])[last()]", ".."), ".", 2)
            except:
                try:
                    self.eleClkByX(self.getSuperEleByX("(//span[text()='" + str(varButton) + " '])[last()]", ".."), ".", 2)
                except:
                    try:
                        self.eleClkByX(self.getSuperEleByX("(//span[text()=' " + str(varButton) + "'])[last()]", ".."),".", 2)
                    except:
                        try:
                            self.eleClkByX(self.getSuperEleByX("(//div[text()='" + str(varButton) + "'])[last()]", ".."), ".", 2)
                        except:
                            try:
                                self.eleClkByX(self.getSuperEleByX("(//div[text()=' " + str(varButton) + " '])[last()]", ".."), ".", 2)
                            except:
                                try:
                                    self.eleClkByX(self.getSuperEleByX("(//div[text()='" + str(varButton) + " '])[last()]", ".."),".", 2)
                                except:
                                    self.eleClkByX(self.getSuperEleByX("(//div[text()=' " + str(varButton) + "'])[last()]", ".."),".", 2)

    def eleCommon(self, ele, k, varLoc=".."):
        try:
            return self.eleSpan(ele, k)
            # return self.eleGetSuperEleByX(ele, ".//span[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleDiv(ele, k)
                # return self.eleGetSuperEleByX(ele, ".//div[text()='" + k + "']", varLoc)
            except:
                try:
                    return self.eleLabel(ele, k)
                    # return self.eleGetSuperEleByX(ele, ".//label[text()='" + k + "']", varLoc)
                except:
                    try:
                        return self.eleTd(ele, k)
                        # return self.eleGetSuperEleByX(ele, ".//td[text()='" + k + "']", varLoc)
                    except:
                        return self.eleP(ele, k)
                        # return self.eleGetSuperEleByX(ele, ".//p[text()='" + k + "']", varLoc)
    def eleCommon2(self, ele, k, varLoc="../.."):
        try:
            return self.eleSpan2(ele, k)
            # return self.eleGetSuperEleByX(ele, ".//span[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleDiv2(ele, k)
                # return self.eleGetSuperEleByX(ele, ".//div[text()='" + k + "']", varLoc)
            except:
                try:
                    return self.eleLabel2(ele, k)
                    # return self.eleGetSuperEleByX(ele, ".//label[text()='" + k + "']", varLoc)
                except:
                    try:
                        return self.eleTd2(ele, k)
                        # return self.eleGetSuperEleByX(ele, ".//td[text()='" + k + "']", varLoc)
                    except:
                        return self.eleP2(ele, k)
                        # return self.eleGetSuperEleByX(ele, ".//p[text()='" + k + "']", varLoc)

    def eleSpan(self, ele, k, varLoc=".."):
        try:
            return self.eleGetSuperEleByX(ele, ".//span[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//span[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//span[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//span[text()=' " + k + "']", varLoc)
    def eleSpan2(self, ele, k, varLoc="../.."):
        try:
            return self.eleGetSuperEleByX(ele, ".//span[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//span[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//span[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//span[text()=' " + k + "']", varLoc)

    def eleDiv(self, ele, k, varLoc=".."):
        try:
            return self.eleGetSuperEleByX(ele, ".//div[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//div[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//div[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//div[text()=' " + k + "']", varLoc)
    def eleDiv2(self, ele, k, varLoc="../.."):
        try:
            return self.eleGetSuperEleByX(ele, ".//div[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//div[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//div[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//div[text()=' " + k + "']", varLoc)

    def eleLabel(self, ele, k, varLoc=".."):
        try:
            return self.eleGetSuperEleByX(ele, ".//label[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//label[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//label[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//label[text()=' " + k + "']", varLoc)
    def eleLabel2(self, ele, k, varLoc="../.."):
        try:
            return self.eleGetSuperEleByX(ele, ".//label[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//label[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//label[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//label[text()=' " + k + "']", varLoc)

    def eleTd(self, ele, k, varLoc=".."):
        try:
            return self.eleGetSuperEleByX(ele, ".//td[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//td[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//td[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//td[text()=' " + k + "']", varLoc)
    def eleTd2(self, ele, k, varLoc="../.."):
        try:
            return self.eleGetSuperEleByX(ele, ".//td[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//td[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//td[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//td[text()=' " + k + "']", varLoc)

    def eleP(self, ele, k, varLoc=".."):
        try:
            return self.eleGetSuperEleByX(ele, ".//p[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//p[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//p[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//p[text()=' " + k + "']", varLoc)
    def eleP2(self, ele, k, varLoc="../.."):
        try:
            return self.eleGetSuperEleByX(ele, ".//p[text()='" + k + "']", varLoc)
        except:
            try:
                return self.eleGetSuperEleByX(ele, ".//p[text()=' " + k + " ']", varLoc)
            except:
                try:
                    return self.eleGetSuperEleByX(ele, ".//p[text()='" + k + " ']", varLoc)
                except:
                    return self.eleGetSuperEleByX(ele, ".//p[text()=' " + k + "']", varLoc)




    # todo dropdown

    def _dropdown(self, varSelectors, v):
        l_ = self.getTextByXs(varSelectors)
        # print(l_)
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v: k for k, v in d_3.items()}
        # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
        if isinstance(v, str):
            # 单选
            self.clkByX(varSelectors + "[" + str(d_4[v]) + "]", 1)
        elif isinstance(v, list):
            # 多选
            for i in range(len(v)):
                self.clkByX(varSelectors + "[" + str(d_4[v[i]]) + "]", 1)
    def dropdown(self, varXpath, v, varSelectors="//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"):
        # 点击下拉框，遍历文本，选择值
        self.clkByX(varXpath, 1)
        self._dropdown(varSelectors, v)
       
    def eleDropdown(self, ele, varXpath, v, varSelectors="//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"):
        # ele点击下拉框，遍历文本，选择值
        # self.eleDropdown(self.eleCommon(ele, k), ".//div[2]/div/div/div/div/div/input", self.selectors['dropdown_popper'], v)
        self.eleClkByX(ele, varXpath, 1)
        self._dropdown(varSelectors, v)
        

    def dropdownDate1(self, varXpath, v, varSelectors="//div[@class='el-popper is-pure is-light el-picker__popper' and @aria-hidden='false']"):
        # 点击单个日期控件下拉框，选择日期
        # self.dropdownDate1(".//input", v)

        self.clkByX(varXpath)
        # varPrefix = "//div[@class='el-popper is-pure is-light el-picker__popper' and @aria-hidden='false']"

        # 1 获取当前年和月
        defaultY = self.getTextByX(varSelectors + "/div/div[1]/div/div[1]/span[1]")
        defaultM = self.getTextByX(varSelectors + "/div/div[1]/div/div[1]/span[2]")
        defaultYear = int(defaultY.split(" 年")[0])
        defaultMonth = int(defaultM.split(" 月")[0])
        # print("defaultYear", defaultYear)
        # print("defaultMonth", defaultMonth)

        # 2 切换年
        if v[0] < defaultYear:
            year = defaultYear - v[0]
            for i in range(year):
                # 上年
                self.clkByX(varSelectors + "/div/div[1]/div/div[1]/button[1]")
        elif defaultYear < v[0]:
            year = v[0] - defaultYear
            for i in range(year):
                # 后年
                self.clkByX(varSelectors + "/div/div[1]/div/div[1]/button[3]")
        # 切换月
        if v[1] < defaultMonth:
            month = defaultMonth - v[1]
            for i in range(month):
                # 上月
                self.clkByX(varSelectors + "/div/div[1]/div/div[1]/button[2]")
        elif defaultMonth < v[1]:
            month = v[1] - defaultMonth
            for i in range(month):
                # 后月
                self.clkByX(varSelectors + "/div/div[1]/div/div[1]/button[4]")

        # 3 遍历日期列表
        tr2 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[2]")
        tr3 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[3]")
        tr4 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[4]")
        tr5 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[5]")
        tr6 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[6]")
        tr7 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[7]")
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
                    self.clkByX(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 2)

    def eleDropdownDate1(self, ele, varXpath, v, varSelectors="//div[@class='el-popper is-pure is-light el-picker__popper' and @aria-hidden='false']"):
        # ele点击单个日期控件下拉框，选择日期
        # self.eleDropdownDate1(self.eleCommon(ele, k), ".//input", v)

        self.eleScrollViewByX(ele, varXpath, 2)
        self.eleClkByX(ele, varXpath)
        # varPrefix = "//div[@class='el-popper is-pure is-light el-picker__popper' and @aria-hidden='false']"

        # 1 获取当前年和月
        defaultY = self.getTextByX(varSelectors + "/div/div[1]/div/div[1]/span[1]")
        defaultM = self.getTextByX(varSelectors + "/div/div[1]/div/div[1]/span[2]")
        defaultYear = int(defaultY.split(" 年")[0])
        defaultMonth = int(defaultM.split(" 月")[0])
        # print("defaultYear", defaultYear)
        # print("defaultMonth", defaultMonth)

        # 2 切换年
        if v[0] < defaultYear:
            year = defaultYear - v[0]
            for i in range(year):
                # 上年
                self.clkByX(varSelectors + "/div/div[1]/div/div[1]/button[1]")
        elif defaultYear < v[0]:
            year = v[0] - defaultYear
            for i in range(year):
                # 后年
                self.clkByX(varSelectors + "/div/div[1]/div/div[1]/button[3]")
        # 切换月
        if v[1] < defaultMonth:
            month = defaultMonth - v[1]
            for i in range(month):
                # 上月
                self.clkByX(varSelectors + "/div/div[1]/div/div[1]/button[2]")
        elif defaultMonth < v[1]:
            month = v[1] - defaultMonth
            for i in range(month):
                # 后月
                self.clkByX(varSelectors + "/div/div[1]/div/div[1]/button[4]")

        # 3 遍历日期列表
        tr2 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[2]")
        tr3 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[3]")
        tr4 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[4]")
        tr5 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[5]")
        tr6 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[6]")
        tr7 = self.getTextByXs(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[7]")
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
                    self.clkByX(varSelectors + "/div/div[1]/div/div[2]/table/tbody/tr[" + str(i + 2) + "]/td[" + str(j + 1) + "]", 2)



    # todo select

    def sltTextById(self, varId, varText):
        # Select 类（标准 HTML <select> 标签）
        # 通过id选择文本"""
        # 如：value=1 , Text=启用 ，sltTextById("id", u'启用')
        slt = Select(self.find_element(*(By.ID, varId)))
        slt.select_by_visible_text(varText)
        return slt
        # 可通过 assert slt.first_selected_option.text == '健康干预_已患疾病组合'，判断是否选择成功

    def sltValueById(self, varId, varValue):
        # Select 类（标准 HTML <select> 标签）
        # 通过id选择value值
        # 如：value=10 , Text=启用 ，sltTextById("id", '10')
        slt = Select(self.find_element(*(By.ID, varId)))
        slt.select_by_value(varValue)
        return slt
        # 可通过 assert slt.first_selected_option.text == '健康干预_已患疾病组合'，判断是否选择成功

    def sltTextByName(self, varName, varText):
        # Select 类（标准 HTML <select> 标签）
        # 通过name选择文本
        # 如：value=10 , Text=启用 ，sltTextByName("isAvilable", '启动')
        slt = Select(self.find_element(*(By.NAME, varName)))
        slt.select_by_visible_text(varText)
        return slt
        # 可通过 assert slt.first_selected_option.text == '健康干预_已患疾病组合'，判断是否选择成功

    def sltValueByName(self, varName, varValue):
        # Select 类（标准 HTML <select> 标签）
        # 通过name选择value值
        # 如：value=10 , Text=启用 ，sltValueByName("isAvilable", '10')
        slt = Select(self.find_element(*(By.NAME, varName)))
        slt.select_by_value(varValue)
        return slt
        # 可通过 assert slt.first_selected_option.text == '健康干预_已患疾病组合'，判断是否选择成功

    def sltTextByX(self, varXpath, varText):
        # Select 类（标准 HTML <select> 标签）
        # 通过xpath选择文本
        # 如：sltTextByX("//select", '文本')
        slt = Select(self.find_element(*(By.XPATH, varXpath)))
        slt.select_by_visible_text(varText)
        return slt
        # 可通过 assert slt.first_selected_option.text == '健康干预_已患疾病组合'，判断是否选择成功

    def sltTextByX2(self, varXpath1, varXpath2):
        # 自定义下拉框操作（非 <select> 元素）
        # 通过xpath选择文本值
        # 如：sltTextByX2("//div[@class='dropdown']", "//li[text()='Option Text']")
        from selenium.webdriver.common.action_chains import ActionChains
        # 点击下拉框以显示选项
        slt = Select(self.find_element(*(By.XPATH, varXpath1)))
        ActionChains(self.driver).click(slt).perform()
        # 选择指定选项
        option = Select(self.find_element(*(By.XPATH, varXpath2)))
        ActionChains(self.driver).click(option).perform()

    def sltTextsByX2(self, varXpath1, varXpath2, l_options):
        # 自定义下拉框操作（非 <select> 元素）
        # 通过xpath选择多个文本值
        # 如：sltTextsByX2("//div[@class='dropdown']", "//ul[@class='multi-select']/li", ["文本1","文本2"])
        from selenium.webdriver.common.action_chains import ActionChains
        # 点击下拉框以显示选项
        slt = self.find_element(*(By.XPATH, varXpath1))
        ActionChains(self.driver).click(slt).perform()
        # 选择指定选项
        options = self.find_element(*(By.XPATH, varXpath2))
        for option in options:
            if option.text in l_options:
                ActionChains(self.driver).click(option).perform()

    def sltTextsByX3(self, varXpath1, l_varText):
        # 自定义下拉框操作（非 <select> 元素）
        # 通过xpath选择多个文本值
        # 如：sltTextsByX3("//div[@class='dropdown']", ['文本1', '文本2'])
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys
        # 点击下拉框以显示选项
        slt = self.find_element(*(By.XPATH, varXpath1))
        ActionChains(self.driver).click(slt).perform()
        # 选择指定选项
        for varText in l_varText:
            option = self.find_element(*(By.XPATH, "//li[text()='" + str(varText) + "']"))
            ActionChains(self.driver).key_down(Keys.CONTROL).click(option)
        # # 使用 Ctrl 键选择多个选项
        ActionChains(self.driver).key_up(Keys.CONTROL).perform()


    def sltValueByX(self, varXpath, varValue):
        # Select 类（标准 HTML <select> 标签）
        # 通过xpath选择value值
        # 如 <option value="2" ...
        # 如：sltValueByX("//select", '2')
        slt = Select(self.find_element(*(By.XPATH, varXpath)))
        slt.select_by_value(varValue)
        return slt
        # 可通过 assert slt.first_selected_option.text == '健康干预_已患疾病组合'，判断是否选择成功

    def sltIndexByX(self, varXpath, varIndex):
        # Select 类（标准 HTML <select> 标签）
        # 通过xpath定位index，选择值
        # 如：sltIndexByX("//select", 3)
        slt = Select(self.find_element(*(By.XPATH, varXpath)))
        slt.select_by_index(varIndex)
        return slt
        # 可通过 assert slt.first_selected_option.text == '健康干预_已患疾病组合'，判断是否选择成功

    def sltTextsByX(self, varXpath, varText1, varText2):
        # 标准多选框（带 <select multiple> 标签）
        # 通过xpath选择多个文本
        # 如：sltTextByX("//select", '文本1', '文本2')
        m_slt = Select(self.find_element(*(By.XPATH, varXpath)))
        m_slt.select_by_visible_text(varText1)
        m_slt.select_by_visible_text(varText2)
        selected_options = [option.text for option in m_slt.all_selected_options]
        return selected_options
        # 可通过 assert "'文本1" in selected_options and "'文本2" in selected_options ，判断是否选择成功

    def sltValuesByX(self, varXpath, varValue1, varValue2):
        # 标准多选框（带 <select multiple> 标签）
        # 通过xpath选择多个value
        # 如：sltTextByX("//select", '2', '3')
        m_slt = Select(self.find_element(*(By.XPATH, varXpath)))
        m_slt.select_by_value(varValue1)
        m_slt.select_by_value(varValue2)

    def sltIndexsByX(self, varXpath, varIndex1, varIndex2):
        # 标准多选框（带 <select multiple> 标签）
        # 通过xpath选择多个index
        # 如：sltTextByX("//select", 0, 3)
        m_slt = Select(self.find_element(*(By.XPATH, varXpath)))
        m_slt.select_by_index(varIndex1)
        m_slt.select_by_index(varIndex2)

    def deSltAllByX(self, varXpath):
        # 标准多选框（带 <select multiple> 标签）
        # 通过xpath取消所有选项
        # 如：deSltAllByX("//select")
        m_slt = Select(self.find_element(*(By.XPATH, varXpath)))
        m_slt.deselect_all()

    def deSltTextByX(self, varXpath, varText):
        # 标准多选框（带 <select multiple> 标签）
        # 通过xpath取消单个文本选项
        # 如：desltByX("//select", '文本')
        m_slt = Select(self.find_element(*(By.XPATH, varXpath)))
        m_slt.deselect_by_visible_text(varText)

    def deSltValueByX(self, varXpath, varValue):
        # 标准多选框（带 <select multiple> 标签）
        # 通过xpath取消单个value选项
        # 如：desltByX("//select", "2")
        m_slt = Select(self.find_element(*(By.XPATH, varXpath)))
        m_slt.deselect_by_value(varValue)

    def deSltIndexByX(self, varXpath, varIndex):
        # 标准多选框（带 <select multiple> 标签）
        # 通过xpath取消单个index选项
        # 如：desltByX("//select", 0)
        m_slt = Select(self.find_element(*(By.XPATH, varXpath)))
        m_slt.deselect_by_index(varIndex)




    def selectXpathText(self, varXpath, varText):
        # 遍历Xpath下的Option,(待确认)
        # self.selectXpathText(u"//select[@regionlevel='1']", u'启用'), （一般情况 value=1 , Text=启用）
        s1 = self.driver.find_element_by_xpath(varXpath)
        l_content1 = []
        l_value1 = []
        # varContents = self.driver.find_elements_by_xpath(varByXpath + "/option")
        varContents = self.driver.find_elements_by_xpath(varXpath + "/option")
        for a in varContents:
            l_content1.append(a.text)
            l_value1.append(a.get_attribute("value"))
        d_total1 = dict(zip(l_content1, l_value1))
        for i in range(len(d_total1)):
            if sorted(d_total1.items())[i][0] == varText:
                Select(s1).select_by_value(sorted(d_total1.items())[i][1])
                break
    def selectIdStyle(self, varByID, varText):
        # ？ 遍历某ID的下的option (不包含 隐藏的属性，如style=display:none），获取varText对应的值(待确认)
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
    def selectXpathsMenu1Menu2(self, varXpaths1, varMenu, varXpaths2, varMenu2, t):
        # 遍历级联菜单（选择一级菜单后再选择二级菜单）(待确认)
        # Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"作业管理", "//a[@href='#']", u"作业框架管理", 3)
        try:
            for a in self.driver.find_elements_by_xpath(varXpaths1):
                if varMenu == a.text:
                    a.click()
                    sleep(t)
                    for a2 in self.driver.find_elements_by_xpath(varXpaths2):
                        if varMenu2 == a2.text:
                            a2.click()
                            sleep(t)
                            break
                    break
        except:
            return None
    def get_selectOptionValue(self, varByname, varNum):
        # 获取某个select中text的value值。(待确认)
        varValue = self.driver.find_element_by_xpath(
            "//select[@name='" + varByname + "']/option[" + varNum + "]"
        ).get_attribute("value")
        return varValue



    # todo iframe

    def swhIframeByX(self, varXpath, t=1):
        """通过Xpath切换到iframe"""
        # 如：swhIframeByX("//body[@class='gray-bg top-navigation']/div[4]/iframe")
        self.driver.switch_to.frame(self.find_element(*(By.XPATH, varXpath)))
        sleep(t)

    def swhIframeById(self, varId, t=1):
        """通过id切换到iframe"""
        #如：swhIframeById（"layui-layer-iframe1"）
        self.driver.switch_to.frame(self.find_element(*(By.ID, varId)))
        sleep(t)

    def swhIframeFromApcByXs(self, varXpaths, varAttr, varValue, t=1):
        """通过xpaths遍历遍历属性中包含指定值切换iframe"""
        # 如：swhIframeFromApcByXs（"//iframe", "src", "/general/workflow/new/"）
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varValue in a.get_attribute(varAttr):
                self.driver.switch_to.frame(self.find_element(*(By.XPATH, varXpaths)))
                # self.driver.switch_to.frame(self.driver.find_element_by_xpath(varXpaths))
                break
        sleep(t)

    def swhIframe(self, t=1):
        """多个iframe之间切换"""
        # 如：如第一层iframe1，第二层iframe2，两者之间切换
        self.driver.switch_to.parent_frame()
        sleep(t)

    def quitIframe(self, t=1):
        """退出iframe"""
        self.driver.switch_to_default_content()
        sleep(t)

    def inIframeTopDiv(self, varXpath, t=1):
        # 定位iframe的div路径?(未确认)
        # evel_PO.inIframeDiv("[@id='showRealtime']", 2)
        # Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
        iframe = self.driver.find_element_by_xpath("//div" + varXpath + "/iframe")
        # print iframe.get_attribute("src")
        self.driver.switch_to.frame(iframe)
        sleep(t)


    # todo ActionChains
    # https://fishpi.cn/article/1713864467902

    def toEnd(self):
        # 模拟按 End 键
        sleep(4)
        ActionChains(self.driver).send_keys(Keys.END).perform()



    def scrollKeysEndByXs2(self, varValue, varXpaths, varXpath2):
        # 每滚动一次（到底部）返回字典的值
        # self.self.scrollKeysEndByXs2("45%", "//div[@class='van-picker-column']/ul/li", "//div[@class='van-picker-column']")
        l_2 = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_ = self.getTextByXs(varXpath2)
            ActionChains(self.driver).send_keys_to_element(a, Keys.END).perform()
            # print(l_)
            l_1 = l_[0].split("\n")
            for i in l_1:
                l_2.append(i)
            # print(l_2)
            # 去重
            l_3 = sorted(set(l_2), key=l_2.index)
            # print(l_3)
            # 成字典
            d_ = {v: k for k, v in dict(enumerate(l_3, start=1)).items()}
            print(d_)
            if varValue in l_[0]:
                return d_[varValue]


    def scrollKeysEndByXs(self, varXpaths, t=2):
        # 遍历滚动到底部
        # self.self.scrollKeysEndByXs("//div[@class='van-picker-column']/ul/li")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            ActionChains(self.driver).send_keys_to_element(a, Keys.END).perform()
        sleep(t)

    def scrollKeysEndByX(self, varXpath, t=2):
        # 一次性滚动到底部
        # 逻辑：定位varPath元素，遍历keys.end N次, 判断varPath2元素退出
        ele = self.find_element(*(By.XPATH, varXpath))
        ActionChains(self.driver).send_keys_to_element(ele, Keys.END).perform()
        sleep(t)

    def scrollKeysEndByXByX(self, varXpath, varCount, varXpath2, t=2):
        # 键盘keys.End滚动到底部
        # 逻辑：定位varPath元素，遍历keys.end N次, 判断varPath2元素退出
        ele = self.find_element(*(By.XPATH, varXpath))
        for i in range(varCount):
            ActionChains(self.driver).send_keys_to_element(ele, Keys.END).perform()
            sleep(1)
            if self.isEleExistByX(varXpath2):
                break
        sleep(t)
        # ActionChains(self.driver).send_keys_to_element(ele, Keys.PAGE_DOWN).perform()
        # ActionChains(self.driver).send_keys_to_element(ele, Keys.ARROW_DOWN).perform()



    def scrollUpDownByX(self, varXpath, varStep, t=2):
        # 上下滚动（移动，按住不放上下滚动）
        # step 负数向上滚动，正数向下滚动
        # ActionChains(self.driver).move_to_element(elements).click_and_hold().move_by_offset(0, varStep).release().perform()
        sleep(t)
        ele = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(ele)
        actions.click_and_hold()
        if varStep != 0:
            if varStep >= 150:
                actions.move_by_offset(0, 150)
            elif varStep <= -500:
                actions.move_by_offset(0, -500)
            else:
                actions.move_by_offset(0, varStep)
        actions.release()
        actions.perform()
        sleep(t)

    def scrollLeftRightByX(self, varXpath, varStep, t=2):
        # 左右滚动（移动，按住不放左右滚动）
        sleep(t)
        ele = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(ele)
        actions.click_and_hold()
        actions.move_by_offset(varStep, 0)
        actions.release()
        actions.perform()
        sleep(t)

    def scrollLeftRightByXByWeb(self, varXpath, varStep, t=2):
        # 左右滚动（移动，按住不放左右滚动）
        sleep(t)
        ele = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(ele)
        actions.click_and_hold()
        actions.move_by_offset(varStep, 0)
        actions.release()
        actions.perform()
        sleep(t)


    # todo js
    
    
    def scrollBy(self, varStep, t=2):
        # 按步长滚动，模拟用户拖动滚动条的行为。
        # step 负数向上滚动，正数向下滚动
        # scrollByStep(-500)
        # self.driver.execute_script("window.scrollBy(0, -500);")
        self.driver.execute_script('window.scrollBy(0, ' + str(varStep) + ');')
        sleep(t)

    def scrollToLocation(self, varLoc):
        # 滚动到指定位置。
        self.driver.execute_script('window.scrollTo(0, %s)' % varLoc)

    def scrollByStep(self, varStep, t=1):
        # 按步长逐步向下滚动直到页面底部
        # scrollByAuto(50)
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(0, new_height, varStep):
            sleep(t)
            self.driver.execute_script('window.scrollTo(0, %s)' % i)

    def scrollBottom(self, t=1):
        # 直接滚动到页面底部
        # self.driver.execute_script('window.scrollTo(0, 1000)')  # 滚动到页面底部
        # self.driver.execute_script("document.documentElement.scrollTop=1000")  # 滚动到页面底部
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(t)

    def scrollViewByX(self, varXpath, t=1):
        # 将元素滚动到可见区域。
        # 先定位元素，然后使用JavaScript脚本将元素滚动到可见区域。
        # element = self.driver.find_element_by_id(varId)  id方式定位
        # element = self.find_element(*(By.XPATH, "//a[@href='#/meeting']"))  Xpath方式定位
        # ErpApp_PO.self.scrollViewByX("//a[last()]")  # 拖动到最后一个a标签
        ele = self.find_element(*(By.XPATH, varXpath))
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)  # 将元素滚动到可见区域
        sleep(t)



    def clsText(self, t=1):
        # 清除input输入框内容
        self.driver.execute_script('document.querySelector("input[type=number]").value=""')
        sleep(t)

    def clsReadonlyByX(self, varXpath, t=1):
        # 去掉只读属性
        ele = self.find_element(*(By.XPATH, varXpath))
        self.driver.execute_script('arguments[0].removeAttribute("readonly")', ele)
        sleep(t)

    def eleClsReadonlyByX(self, ele, varXpath, t=1):
        # 去掉只读属性
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        self.driver.execute_script('arguments[0].removeAttribute("readonly")', ele2)
        sleep(t)

    def clsReadonlyById(self, varId, t=1):
        # 通过id去掉只读属性, 一般用于第三方日期控件
        self.driver.execute_script('document.getElementById("' + varId + '").removeAttribute("readonly")')
        sleep(t)

    def clsReadonlyByName(self, varName, t=1):
        # 通过name去掉只读属性
        # 注意：document只支持getElementsByName方法获取标签数组，如 array[0]
        self.driver.execute_script('document.getElementsByName("' + varName + '")[0].removeAttribute("readonly")')
        sleep(t)

    def clsDisplayByName(self, varName, t=1):
        # 通过name去掉隐藏属性
        self.driver.execute_script('document.getElementsByName("' + varName + '")[0].style.display=""')
        sleep(t)

    def clsDisplayByTagName(self, varLabel, varLen, t=1):
        # 通过tagname去掉隐藏属性
        # 如：clsDisplayByTagName("ul"，30)
        # 表示清除30个ul标签的display，可以通过Web_PO.getCountByTag("ul")方式获取ul数量。
        for i in range(varLen):
            self.driver.execute_script('document.getElementsByTagName("' + varLabel + '")[' + str(i) + '].style.display=""')
        sleep(t)

    def displayBlockID(self, varID):
        # 未验证？(未确认)
        varJs = 'document.getElementById("filePath").style.display="block"'
        # document.getElementByPath
        return self.driver.find_element_by_id(varID).style.display



    # todo True or False



    def eleIsEleExistByX(self, ele, varXpath):
        # 判断元素是否存在
        flag = False
        try:
            ele.find_element(*(By.XPATH, varXpath))
            flag = True
        except:
            flag = False
        return flag


    def isEleExistByX(self, varXpath):
        # 判断元素是否存在
        flag = False
        try:
            self.find_element(*(By.XPATH, varXpath))
            flag = True
        except:
            flag = False
        return flag

    def isEleExistByXForWait(self, varXpath, varCycle):
        # 循环等待时间，判断元素是否存在，存在则退出

        for i in range(varCycle):
            if self.isEleExistByX(varXpath):
                break
            else:
                sleep(1)







    def isEleAttrExistByX(self, varXpath, varAttr):
        # 判断元素属性是否存在
        flag = False
        try:
            ele = self.find_element(*(By.XPATH, varXpath))
            if ele.get_attribute(varAttr):
                flag = True
        except:
            flag = False
        return flag

    def eleIsEleAttrExistByX(self, ele, varXpath, varAttr):
        # 判断元素属性是否存在
        flag = False
        try:
            ele = ele.find_element(*(By.XPATH, varXpath))
            if ele.get_attribute(varAttr):
                flag = True
        except:
            flag = False
        return flag

    def isEleAttrValueExistByX(self, varXpath, varAttr, varValue):
        # 判断元素属性的值是否存在
        # 如：isEleAttrValueExistByX("//tr","href","www.badu.com")
        flag = False
        try:
            for ele in self.find_elements(*(By.XPATH, varXpath)):
                if varValue == ele.get_attribute(varAttr):
                    flag = True
                    break
        except:
            flag = False
        return flag

    def isEleExistById(self, varId):
        # 通过Id判断ture或false
        flag = False
        try:
            self.find_element(*(By.ID, varId))
            flag = True
        except:
            flag = False
        return flag

    def isEleExistByName(self, varName):
        # 通过name判断ture或false
        flag = False
        try:
            self.find_element(*(By.NAME, varName))
            flag = True
        except:
            flag = False
        return flag

    def isElePartExistByP(self, varPartText):
        # 通过超链接判断是否包含varText
        flag = False
        try:
            self.driver.find_element_by_partial_link_text(varPartText)
            flag = True
        except:
            flag = False
        return flag

    def isEleExistByL(self, varText):
        # 通过超链接判断是否存在varText
        flag = False
        try:
            self.driver.find_element_by_link_text(varText)
            flag = True
        except:
            flag = False
        return flag

    def isEleTextExistByX(self, varXpath, varText):
        # 通过xpath判断文本是否存在
        flag = False
        try:
            if self.find_element(*(By.XPATH, varXpath)).text == varText:
                flag = True
        except:
            flag = False
        return flag

    def isEleTextExistByXForWait(self, varXpath, varText, varCycle):
        # 循环等待时间，通过xpath判断文本是否存在，存在则退出
        for i in range(varCycle):
            if self.isEleTextExistByX(self, varXpath, varText):
                break
            else:
                sleep(1)

    def isBooleanAttrValueListByX(self, varXpath, varAttr, varValue):
        """通过xpath判断属性等于值"""
        # 如：isBooleanAttrValueListByX("//tr","href","www.badu.com")
        # .isBooleanAttrValueListByX("//div/label/span[1]", 'class', 'el-radio__input is-disabled is-checked')
        # 判断单选框是否被选中。

        l1 = []
        for a in self.find_elements(*(By.XPATH, varXpath)):
            if varValue == a.get_attribute(varAttr):
                l1.append("True")
            else:
                l1.append("False")
        return l1

    def isBooleanAttrContainValueListByX(self, varXpath, varAttr, varValue):

        """通过xpath判断属性包含值"""
        # .isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', 'el-radio__input is-disabled is-checked')
        # 判断单选框是否被选中。

        l1 = []
        for a in self.find_elements(*(By.XPATH, varXpath)):
            if varValue in a.get_attribute(varAttr):
                l1.append("True")
            else:
                l1.append("False")
        return l1


    def isElementVisibleXpath(self, element):
        # 未验证？？？（未确认）
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
    def locElement(self, varXpath, t=1):
        # 定位到某元素???（未确认）
        try:
            elements = self.find_element(*(By.XPATH, varXpath))
            actions = ActionChains(self.driver)
            actions.move_to_element(elements).perform()
            sleep(t)
        except:
            return None



    # todo alert(system)

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






    

    def zoom(self, percent):
        # 缩放页面
        # js = "document.body.style.zoom='70%'"
        js = "document.body.style.zoom='" + str(percent) + "%'"
        self.driver.execute_script(js)



    def canvas2base64(self, varXpath):
        # canvas元素转base64图片
        canvas = self.find_element(*(By.XPATH, varXpath))
        data_url = self.driver.execute_script("return arguments[0].toDataURL('image/png');", canvas)
        return data_url


    def upFile(self, ele, varXpath, l_varFile):

        # 上传文件(for mac)

        for i in l_varFile:

            # # 点击 +
            self.eleClkByX(ele, varXpath)

            # 选中文件
            pyautogui.write(i, interval=0.2)
            sleep(2)
            pyautogui.press('enter', 1)
            sleep(2)
            pyautogui.press('enter', 1)

            # 模拟点击“打开”按钮
            # pyautogui.moveTo(1250, 820, duration=1)
            # pyautogui.click()

            # 定位“打开”按钮的坐标，这个坐标需要根据你的Finder窗口实际情况进行调整
            x , y = pyautogui.size()
            open_button_x = x - 170
            # print(open_button_x)
            open_button_y = y - 80
            # print(open_button_y)
            pyautogui.moveTo(x=open_button_x, y=open_button_y, duration=1)
            pyautogui.click()


        # upload_btn = self.find_element(*(By.XPATH, varXpath))
        # self.driver.execute_script("arguments[0].style.visibility='visible'", upload_btn)


        # file_path = os.path.abspath(varFile)
        # self.find_element(*(By.XPATH, "//input[@type='file']")).send_keys(varFile)

        # upload_btn.send_keys(varFile)

        # ActionChains.(self.driver).click(upload_btn).perform()

        # # 将文件路径设为不可见输入框的值
        # self.driver.execute_script("arguments[0].value = arguments[1]", upload_btn, "varFile")
        #
        # # 点击实际的上传按钮
        # self.driver.execute_script("arguments[0].click()", upload_btn)

    def exportExistFile(self, varFile):

        # 导出文件(覆盖)

        # 选中文件
        pyautogui.write(varFile, interval=0.2)
        sleep(2)
        pyautogui.press('enter', 1)
        sleep(2)
        pyautogui.press('enter', 1)
        sleep(2)
        pyautogui.press('tab', 1)
        sleep(2)
        pyautogui.press('space', 1)

    def exportFile(self, varFile):

        # 导出文件（文件不存在，生成）

        # 选中文件
        pyautogui.write(varFile, interval=0.2)
        sleep(2)
        pyautogui.press('enter', 1)
        sleep(2)
        pyautogui.press('enter', 1)
        sleep(2)




    def getXpathByLabel(self, varLabel):
        # 获取所有标签的XPath路径
        # 如 getXpathByLabel('button')
        l_ = []
        varLabel = self.find_elements(*(By.TAG_NAME, varLabel))
        # varLabel = self.driver.find_elements(By.TAG_NAME, varLabel)
        for i, button in enumerate(varLabel):
            xpath = self.driver.execute_script("""
                  function getElementXPath(element) {
                      if (element.id !== '') {
                          return 'id("' + element.id + '")';
                      }
                      if (element === document.body) {
                          return element.tagName;
                      }

                      var ix = 0;
                      var siblings = element.parentNode.childNodes;
                      for (var i = 0; i < siblings.length; i++) {
                          var sibling = siblings[i];
                          if (sibling === element) {
                              return getElementXPath(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                          }
                          if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                              ix++;
                          }
                      }
                  }
                  return getElementXPath(arguments[0]);
                  """, button)
            # print(f'Button {i + 1}: XPath = {xpath}')
            l_.append(xpath)
        return l_

    def eleGetXpathByLabel(self, ele, varLabel):
        # 获取所有标签的XPath路径
        # 如 getXpathByLabel('button')
        l_ = []
        varLabel = ele.find_elements(*(By.TAG_NAME, varLabel))
        # varLabel = ele.find_elements(By.TAG_NAME, varLabel)
        for i, button in enumerate(varLabel):
            xpath = self.driver.execute_script("""
                  function getElementXPath(element) {
                      if (element.id !== '') {
                          return 'id("' + element.id + '")';
                      }
                      if (element === document.body) {
                          return element.tagName;
                      }

                      var ix = 0;
                      var siblings = element.parentNode.childNodes;
                      for (var i = 0; i < siblings.length; i++) {
                          var sibling = siblings[i];
                          if (sibling === element) {
                              return getElementXPath(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                          }
                          if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                              ix++;
                          }
                      }
                  }
                  return getElementXPath(arguments[0]);
                  """, button)
            # print(f'Button {i + 1}: XPath = {xpath}')
            l_.append(xpath)
        return l_

    def getTextXpathByLabel(self, varLabel, varLabel2):
        # 获取路径及标签
        # 如 获取button和下级文本，getTextXpathByLabel("button", "/span")
        # {'登录': 'id("app")/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[4]/BUTTON[1]'}
        d_ = {}
        l_ = self.getXpathByLabel(varLabel)
        try:
            for i, xpath in enumerate(l_):
                # print(xpath, self.getTextByX(xpath + varLabel2))
                # d_[xpath] = self.getTextByX(xpath + varLabel2)
                d_[self.getTextByX(xpath + varLabel2, wait='no')] = xpath
        except:
            ...
        finally:
            return d_

    def getValueXpathByLabel(self, varLabel, attr):
        # 获取路径及标签的属性值
        # 如 获取input的placehoder值，getValueXpathByLabel("input", "placeholder")
        # {'请输入用户名': 'id("app")/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[1]/DIV[1]/DIV[1]/INPUT[1]', '输入密码': 'id("app")/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[2]/DIV[1]/DIV[1]/INPUT[1]'}

        d_ = {}
        l_ = self.getXpathByLabel(varLabel)
        try:
            for i, xpath in enumerate(l_):
                d_[self.getAttrValueByX(xpath, attr, wait='no')] = xpath
        except:
            ...
        finally:
            return d_

    def getTextByLabel(self, varLabel):
        # 获取指定标签的所有文本
        # 如 getTextByLabel('button')
        l_1 = []
        l_ = self.getXpathByLabel(varLabel)
        for i, xpath in enumerate(l_):
            l_1.append(self.getTextByX(xpath))
        return l_1

    def eleGetTextByLabel(self, ele, varLabel):
        # 获取ele指定标签的所有文本
        l_1 = []
        l_ = self.eleGetXpathByLabel(ele, varLabel)
        for i, xpath in enumerate(l_):
            l_1.append(self.getTextByX(xpath))
            # print(self.getTextByX(xpath))
        return l_1



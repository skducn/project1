# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2025
# Description:
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from config.ConfigparserPO import *
# Configparser_PO = ConfigparserPO('config/config.ini')
Configparser_PO = ConfigparserPO('/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/config/config.ini')
varUrl = Configparser_PO.HTTP("url")

import sys
import os

# 获取项目根目录并添加到 sys.path
# project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("/Users/linghuchong/Downloads/51/Python/project")
# print(project_root)

from PO.WebPO import *

from PO.LogPO2 import *
# Log_PO2 = LogPO2("./LogPO3.log")

from PO.CaptchaPO import *
Captcha_PO = CaptchaPO()

from PO.Base64PO import *
Base64_PO = Base64PO()

from PO.FilePO import *
File_PO = FilePO()

import logging
import signal, inspect
import sys

from time import sleep
import datetime
import psutil


class CdrdPO():


    def __init__(self, varFile):

        # 配置日志
        if os.name == 'nt':
            logging.basicConfig(filename=varFile, level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
        else:
            logging.basicConfig(filename=varFile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        print(varFile, datetime.datetime.now())

        # 创建URL与句柄的字典
        self.d_url_handle = {}
        self.d_all = {}


    def handle_signal(self, signum, frame):
        # 信号处理函数
        # 他有2个参数 signum, frame
        # frame对象是signal模块的内部实现细节，通常情况下，我们不需要直接操作或访问frame对象。
        # 如果你需要获取当前调用栈或者进行调试，可以考虑使用其他工具和方法，例如sys模块的exc_info()函数或者内置的pdb调试器。
        self.logger.info('Received signal: {}'.format(signal.Signals(signum).name))
        self.logger.info('Program is terminating...')
        # self.logger.info(inspect.getframeinfo(frame))
        # print(inspect.getframeinfo(frame)) # 函数用于获取关于frame的信息，包括文件名、行号以及函数名等。

        # 在这里可以添加额外的清理代码或日志记录
        sys.exit(0)
        # logger.info("Get TERM signal {0}".format(signal_num))
        # self.terminated_flag = True
        # self._kill_sleep_gevent()  # 轮询结束休眠的协程

    # 注册信号处理函数
    # 当用户按下Ctrl+C时，会触发SIGINT信号，然后调用handle_signal函数，打印出提示信息后退出程序。
    # signal.signal(signal.SIGINT, handle_signal)
    # signal.signal(signal.SIGTERM, handle_signal)


    def count_chrome_tabs(self):
        tab_count = 0
        # 遍历所有进程
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                # 检查是否是Chrome进程
                if proc.info['name'] in ['chrome.exe', 'google-chrome', 'chrome']:
                    cmdline = proc.info['cmdline']
                    # 标签页进程通常包含--type=renderer参数
                    if cmdline and '--type=renderer' in cmdline:
                        tab_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return tab_count

    def login(self):

        # # # 当用户按下Ctrl+C时，会触发SIGINT信号，然后调用handle_signal函数，打印出提示信息后退出程序。
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        # 1，登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(Configparser_PO.HTTP("url"))
        self.Web_PO.setTextByX('/html/body/div/div/div/form/div[3]/div/div/div/input', Configparser_PO.USER("user"))
        self.Web_PO.setTextByX('/html/body/div/div/div/form/div[4]/div/div/div/input', Configparser_PO.USER("password"))
        # # # 验证码
        # # 获取base64
        # base64 = self.Web_PO.getAttrValueByX('/html/body/div/div/div/form/div[5]/div/div/div/span[2]/span/div/img', 'src')
        # # dataURI = '''data:image/gif;base64,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'''
        # Base64_PO.base64ToImg(base64, "cpatcha")
        # # self.Web_PO.setTextByX("/html/body/div/div/div/form/div[5]/div/div/div/input", "1")
        # self.Web_PO.clkByX("/html/body/div/div/div/form/div[6]/div/button", 2)

        self.Web_PO.clkByX("/html/body/div/div/div/form/div[5]/div/button", 2)

        self.logger.info("已登录")
    def logout(self):

        # # # # 当用户按下Ctrl+C时，会触发SIGINT信号，然后调用handle_signal函数，打印出提示信息后退出程序。
        # signal.signal(signal.SIGINT, self.handle_signal)
        # signal.signal(signal.SIGTERM, self.handle_signal)

        # 已登出
        self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div", 1)
        self.Web_PO.clkByX("/html/body/div[2]/div[1]/div/div[1]/div/ul/li[2]", 1)
        self.Web_PO.clkByX("/html/body/div[3]/div/div/div[3]/button[2]", 1)

        self.logger.info("已登出")

    def opnMenu(self, varMenu):
        # 打开菜单, 获取菜单的链接和句柄字典
        d_menu = self.getMenu2Url()
        d_url_handle = self.Web_PO.opnLabel(d_menu[varMenu], 1)
        self.d_url_handle = self.d_url_handle | d_url_handle
        self.Web_PO.swhLabelByHandle(self.d_url_handle[d_menu[varMenu]])

    def swhMenu(self, varMenu):
        # 通过句柄切换菜单
        # self.d_url_handle = {'http://192.168.0.243:8083/system/role': '395985EFE9DBEC2A5A7AA3FC0DA9CF47'}
        # d_menu[varMenu] = 'http://192.168.0.243:8083/system/role'
        d_menu = self.getMenu2Url()
        self.Web_PO.swhLabelByHandle(self.d_url_handle[d_menu[varMenu]])

    def getMenu2Url(self):

        # 获取菜单连接

        # 统计ur数量
        c = self.Web_PO.getCountByTag("ul")
        varLabelCount = c - 3

        # 获取二级菜单名
        self.Web_PO.clsDisplayByTagName("ul", varLabelCount)  # 展开所有二级菜单（去掉display：none）
        l_menu2 = self.Web_PO.getTextByXs("//a/li/span")
        # print(l_menu2)  # ['我的代办', '患者列表', ...

        # 获取二级菜单链接
        l_menu2Url = self.Web_PO.getAttrValueByXs("//a", "href")
        # print(l_menu2Url) # ['http://192.168.0.243:8083/index', 'http://192.168.0.243:8083/patient/list', ...

        # 生成字典{菜单：URL}
        d_menuUrl = dict(zip(l_menu2, l_menu2Url))
        # print(d_menuUrl)  # {'我的代办': 'http://192.168.0.243:8083/index', '患者列表': 'http://192.168.0.243:8083/patient/list', '用户管理': 'http://192.168.0.243:8083/system/user', '角色管理': 'http://192.168.0.243:8083/system/role', '菜单管理': 'http://192.168.0.243:8083/system/menu', '医院管理': 'http://192.168.0.243:8083/system/dept', '科室管理': 'http://192.168.0.243:8083/system/post', '字典管理': 'http://192.168.0.243:8083/system/dict', '参数设置': 'http://192.168.0.243:8083/system/config', '操作日志': 'http://192.168.0.243:8083/log/operlog', '登录日志': 'http://192.168.0.243:8083/log/logininfor'}

        return d_menuUrl


    def run(self, varUser, varPass, d_2):

        # 1，登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrl + "/login")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", varUser)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", varPass)
        # 验证码
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", "1")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)
        for i in range(10):
            dataURI = self.Web_PO.getAttrValueByX(u"//img[@class='login-code-img']", "src")
            imgFile = Base64_PO.base64ToImg(dataURI)
            captcha = Captcha_PO.getCaptchaByDdddOcr(imgFile)
            File_PO.removeFile('', imgFile)
            # print(captcha)
            self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", captcha)
            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)
            if self.Web_PO.isEleExistByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button") == False:
                break

        # 2，遍历身份id
        for k1, v1 in d_2.items():
            for k, v in v1.items():
                l_1 = []
                for i in v:
                    s = varUrl + "#/SignManage/signAssess/component/basicReport?idCard=" + str(i)
                    # s = "http://10.207.237.160:8088/login#/SignManage/signAssess/component/basicReport?idCard=" + str(i)
                    l_1.append(s)
                print(l_1)

                for i in range(len(l_1)):
                    self.Web_PO.opnLabel(l_1[i])
                    self.Web_PO.swhLabel(i + 1)
                    sleep(2)
                    self.Web_PO.isEleExistByXForWait("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]", 30)
                    s_text = self.Web_PO.getTextByX("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]")
                    if s_text == "上传报告":
                        self.Web_PO.scrollViewByX(
                            "/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]")
                        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]", 1)
                        if self.Web_PO.isEleExistByX("/html/body/div[5]/div/div/div[3]/button[2]"):
                            self.Web_PO.clkByX("/html/body/div[5]/div/div/div[3]/button[2]", 1)
                        elif self.Web_PO.isEleExistByX("/html/body/div[3]/div/div/div[3]/button[2]"):
                            self.Web_PO.clkByX("/html/body/div[3]/div/div/div[3]/button[2]", 1)

                    # sleep(2)
                    # l_ = self.Web_PO.getTextByXs("//span")
                    # sleep(1)
                    # for j in l_:
                    #     if j == "上传报告":
                    #         self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]")
                    #         self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]", 1)
                    #         if self.Web_PO.isEleExistByX("/html/body/div[5]/div/div/div[3]/button[2]"):
                    #             self.Web_PO.clkByX("/html/body/div[5]/div/div/div[3]/button[2]", 1)
                    #         elif self.Web_PO.isEleExistByX("/html/body/div[3]/div/div/div[3]/button[2]"):
                    #             self.Web_PO.clkByX("/html/body/div[3]/div/div/div[3]/button[2]", 1)
                sleep(8)
                self.Web_PO.isEleTextExistByXForWait("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]", '待上传市级平台', 30)
                print("已完成", k1, "第", k, "页")

                for i in range(10):
                    self.Web_PO.swhLabel(1)
                    self.Web_PO.cls()
                self.Web_PO.swhLabel(0)



    def getIdcardTest(self, varDoc):
        # 获取每个医生所管理的身份证列表

        # # 注册信号处理函数
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        # 登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrlTest)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", Configparser_PO.USER("user"))
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", Configparser_PO.USER("password"))
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", "1")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)

        # 居民健康服务 - 健康评估及干预
        self.Web_PO.opnLabel(varUrlTest + "/#/SignManage/signAssess", 1)
        self.Web_PO.swhLabel(1)

        # # 人群分类
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[3]/div/div/div/div/div/input", 2)
        # # 老年人
        # self.Web_PO.clkByX("/html/body/div[2]/div[2]/div/div/div[1]/ul/li[4]", 2)
        #
        # # 家庭医生
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input",2)
        li_qty = self.Web_PO.getQtyByXs("/html/body/div[2]/div[3]/div/div/div[1]/ul/li")
        for i in range(int(li_qty)):
            varDocName = self.Web_PO.getTextByX("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[" + str(i+1) + "]/span")
            if varDocName == varDoc:
                self.Web_PO.clkByX("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[" + str(i+1) + "]")  # 修改l[2]
                break
        #
        # # 本年度上传情况
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input", 2)
        self.Web_PO.clkByX("/html/body/div[2]/div[12]/div/div/div[1]/ul/li[1]", 2)
        #
        # 已点击上传
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[2]/div/div/div/div/div/input", 2)
        self.Web_PO.clkByX("/html/body/div[2]/div[13]/div/div/div[1]/ul/li[1]", 2)
        #
        # # 查询
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[3]/div/button")

        # 定位到底部
        self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input")
        # 获取 共 ？条
        isQty = self.Web_PO.getTextByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[1]")
        # print(isQty)  # 共 12 条
        if isQty != "共 0 条":
            # qty  获取总页数

            li_qty = self.Web_PO.getQtyByXs("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/ul/li")
            # print(li_qty)

            if int(li_qty) < 7:
                qty = int(li_qty)
            else:
                qty = 111111

            d_1 = {}
            d_2 = {}
            for k in range(qty):
                # 前往第几页
                self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input")
                self.Web_PO.setTextByDelDouble("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input", k+1, 2)
                ele = self.Web_PO.getSuperEleByX("//div[text()='姓名']", "../../../../../..")
                tr_qty = self.Web_PO.eleGetQtyByX(ele, ".//div[3]/div/div[1]/div/table/tbody/tr")
                # print(tr_qty)
                l_ = []
                for i in range(int(tr_qty)):
                    idcard = self.Web_PO.eleGetTextByX(ele, ".//div[3]/div/div[1]/div/table/tbody/tr["+ str(i+1)+ "]/td[9]/div")
                    l_.append(idcard)
                pp = (str(varDoc) + str(k+1) + str(l_))
                print(varDoc, k+1, l_)
                self.logger.info(pp)
                d_1[k+1] = l_
            d_2[varDoc] = d_1
            # print(d_2)
            # self.logger.info(str(varDoc) + ".json" + str(d_2))
            File_PO.dict2jsonfile(varDoc + ".json", d_2)
            # dd_ = File_PO.jsonfile2dict(varDoc + ".json")
            # print(dd_)
            return d_2

    def getIdcard(self, varUser, varPass, varDoc):
        # 获取每个医生所管理的身份证列表
        # 登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrlTest)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", varUser)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", varPass)
        for i in range(10):
            dataURI = self.Web_PO.getAttrValueByX(u"//img[@class='login-code-img']", "src")
            imgFile = Base64_PO.base64ToImg(dataURI)
            captcha = Captcha_PO.getCaptchaByDdddOcr(imgFile)
            File_PO.removeFile('', imgFile)
            self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", captcha)
            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)
            if self.Web_PO.isEleExistByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button") == False:
                break

        # 居民健康服务 - 健康评估及干预
        self.Web_PO.opnLabel(varUrlTest + "/#/SignManage/signAssess", 1)
        self.Web_PO.swhLabel(1)

        # # 人群分类
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[3]/div/div/div/div/div/input", 2)
        # # 老年人
        self.Web_PO.clkByX("/html/body/div[2]/div[2]/div/div/div[1]/ul/li[4]", 2)
        #
        # # 家庭医生
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input",2)
        li_qty = self.Web_PO.getQtyByXs("/html/body/div[2]/div[3]/div/div/div[1]/ul/li")
        # print(li_qty)
        for i in range(int(li_qty)):
            varDocName = self.Web_PO.getTextByX("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[" + str(i+1) + "]/span")
            if varDocName == varDoc:
                self.Web_PO.clkByX("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[" + str(i+1) + "]")  # 修改l[2]
                break
        #
        # # 本年度上传情况
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input", 2)
        self.Web_PO.clkByX("/html/body/div[2]/div[12]/div/div/div[1]/ul/li[1]", 2)
        #
        # 已点击上传
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[2]/div/div/div/div/div/input", 2)
        self.Web_PO.clkByX("/html/body/div[2]/div[13]/div/div/div[1]/ul/li[1]", 2)
        #
        # # 查询
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[3]/div/button")

        # 定位到底部
        self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input")
        # 获取 共 ？条
        isQty = self.Web_PO.getTextByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[1]")
        print(isQty)  # 共 12 条
        if isQty != "共 0 条":
            # qty  获取总页数

            li_qty = self.Web_PO.getQtyByXs("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/ul/li")
            print(li_qty)

            if int(li_qty) < 7:
                qty = int(li_qty)
            else:
                qty = 111111

            d_1 = {}
            for k in range(qty):
                # 前往第几页
                self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input")
                self.Web_PO.setTextByDelDouble("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input", k+1, 2)
                ele = self.Web_PO.getSuperEleByX("//div[text()='姓名']", "../../../../../..")
                tr_qty = self.Web_PO.eleGetQtyByX(ele, ".//div[3]/div/div[1]/div/table/tbody/tr")
                # print(tr_qty)
                l_ = []
                for i in range(int(tr_qty)):
                    idcard = self.Web_PO.eleGetTextByX(ele, ".//div[3]/div/div[1]/div/table/tbody/tr["+ str(i+1)+ "]/td[9]/div")
                    l_.append(idcard)
                print(k+1, l_)
                d_1[k+1] = l_
            return d_1



    def getDocTest(self, varUser, varPass):
        # 获取家庭医生列表顺序名单(测试环境)
        # 登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrlTest)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", varUser)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", varPass)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", "1")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)

        # 居民健康服务 - 健康评估及干预
        self.Web_PO.opnLabel(varUrlTest + "/#/SignManage/signAssess", 1)
        self.Web_PO.swhLabel(1)

        # # 家庭医生
        self.Web_PO.clkByX(
            "/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input")
        l_doc = self.Web_PO.getTextByXs("/html/body/div[2]/div[3]/div/div/div[1]/ul/li")
        d_doc = dict(enumerate(l_doc, start=1))
        d_doc = {v: k for k, v in d_doc.items()}
        return d_doc

    def getDoc(self, varUser, varPass):
        # 获取家庭医生列表顺序名单
        # 登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrl + "/login")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", varUser)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", varPass)
        for i in range(10):
            dataURI = self.Web_PO.getAttrValueByX(u"//img[@class='login-code-img']", "src")  # getValueByAttr
            imgFile = Base64_PO.base64ToImg(dataURI)
            captcha = Captcha_PO.getCaptchaByDdddOcr(imgFile)
            File_PO.removeFile('', imgFile)
            # print(captcha)
            self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", captcha)
            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)
            if self.Web_PO.isEleExistByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button") == False:
                break

            # 居民健康服务 - 健康评估及干预
            self.Web_PO.opnLabel(varUrl + "/#/SignManage/signAssess", 1)
            self.Web_PO.swhLabel(1)

            # # 家庭医生
            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input")
            l_doc = self.Web_PO.getTextByXs("/html/body/div[2]/div[3]/div/div/div[1]/ul/li")
            d_doc = dict(enumerate(l_doc, start=1))
            d_doc = {v: k for k, v in d_doc.items()}
            return d_doc


    def getPatientCount(self):

        # 获取页面患者总数量

        # 定位大框
        ele = self.Web_PO.getSuperEleByX('/html/body/div[1]/div/div[3]/section')

        # 滚动4次到元素
        self.Web_PO.eleScrollBottomByXN(ele, '/html/body/div[1]/div/div[3]/section/div/div/div[2]/div[2]/div/span[1]', 3, 0)

        # 获取"共 6723 项数据
        # a = self.Web_PO.eleGetTextByX(ele, '/html/body/div[1]/div/div[3]/section/div/div/div[2]/div[2]/div/span[1]')
        s_total = self.Web_PO.eleGetTextByX(ele, "//span[@class='el-pagination__total is-first']")
        s_total = s_total.replace("共 ", "").replace(" 项数据", "")
        print(s_total)

    def getUrlByPatient(self, varPage=1):

        # 获取患者详情页url

        # 点击按钮前, 获取当前所有窗口的句柄
        self.Web_PO.getAllWindowHandle()

        d_ = {}

        for i in range(10):
            # 点击 患者详情
            self.Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i+1) + ']/td[9]/div/button')
                              # /html/body/div[1]/div/div[3]/section/div/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[2]/td[9]/div/button

            # 患者姓名
            s_patient = self.Web_PO.getTextByX('/html/body/div[1]/div/div[3]/section/div/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i+1) + ']/td[1]/div')
            # print(s_patient)  # 李芳兴

            # 患者详情url
            s_patient_url = self.Web_PO.getUrlByClk()
            # print(s_patient_url)  # http://192.168.0.243:8083/patient/patientDetail?patientId=401
            s_patient_url_id = s_patient_url.split("patientId=")[1]
            d_[s_patient_url_id]= s_patient

            # 关闭url
            self.Web_PO.cls()
            # 关闭新窗口后，浏览器焦点不会自动切换回来，需要手动切换
            # self.driver.switch_to.window(self.all_window_handles)

            # 切换窗口（上一个句柄是1）
            self.Web_PO.swhWindowIndex(1)

        # print(d_)  # {'401': '李芳兴', '3647': '朱一栋', '10093': '郑明荣', '15125': '朱龙兴', '27172': '郑世伟', '27480': '何明', '24401': '赵军', '19877': '张玲柏', '2387': '吴一桦', '2440': '韩佳柏'}

        self.d_all[varPage] = d_
        # print(self.d_all)

        return self.d_all



    def setPage(self, varPage):

        # 获取页面患者总数量

        # 定位大框
        ele = self.Web_PO.getSuperEleByX('/html/body/div[1]/div/div[3]/section')

        # 滚动4次到元素
        self.Web_PO.eleScrollBottomByXN(ele, '/html/body/div[1]/div/div[3]/section/div/div/div[2]/div[2]/div/span[1]', 4, 0)

        # 前往N页
        self.Web_PO.setTextByDelDouble('/html/body/div[1]/div/div[3]/section/div/div/div[2]/div[2]/div/span[3]/div/div/input', varPage)







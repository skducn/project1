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

from collections import ChainMap

# d_g_type_func = {}

# exec("""for i in range(2):
#     self.dropdownDateByOne(dd_text_xpath[k], v[i])""")


class GwPO_three():

    def __init__(self, varFile):
        # 配置日志
        if os.name == 'nt':
            logging.basicConfig(filename=varFile, level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
        else:
            logging.basicConfig(filename=varFile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        # print(varFile, datetime.datetime.now())

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

        self.d_g_type_func = {'文本': 'Web_PO.setTextEnterByX(dd_text_xpath[k], v)',
                         '单下拉框': "Web_PO.dropdown(dd_text_xpath[k],  v)",
                         '管理机构': 'self.__gljg(ele, k, v)',
                         '日期': 'Web_PO.dropdownDate1(dd_text_xpath[k], v)'}

    def __handle_signal(self, signum, frame):
        # 定义信号处理函数
        self.logger.info('Received signal: {}'.format(signal.Signals(signum).name))
        self.logger.info('Program is terminating...')
        # 在这里可以添加额外的清理代码或日志记录

    def clsApp(self, varApp):

        '''
        关闭应用程序
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

    def getDecode(self, varKey, varSm2Data):

        # 在线sm2解密数据
        d = {}
        # Web_PO.openURL("https://the-x.cn/zh-cn/cryptography/Sm2.aspx")
        Web_PO.opnLabel("https://the-x.cn/zh-cn/cryptography/Sm2.aspx")
        Web_PO.swhLabel(1)
        # 解密秘钥：124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
        Web_PO.setTextByX("/html/body/div/form/div[1]/div[1]/div[1]/textarea",
                          "124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62")
        Web_PO.setTextByX("/html/body/div/form/div[1]/div[1]/div[2]/textarea", varSm2Data)
        Web_PO.clkByX("/html/body/div/form/div[2]/div[2]/input[2]", 2)
        s_result = Web_PO.getAttrValueByX("/html/body/div/form/div[3]/textarea", "value")
        d_result = eval(s_result)
        d[varKey] = d_result
        Web_PO.cls()
        Web_PO.swhLabel(0)
        return d

    def login(self, varUrl, varUser, varPass):
        # 登录
        Web_PO.openURL(varUrl)
        Web_PO.driver.maximize_window()  # 全屏
        # Web_PO.setTextByX("//input[@placeholder='请输入用户名']", varUser)
        # Web_PO.setTextByX("//input[@placeholder='输入密码']", varPass)
        # Web_PO.clkByX("//button[@type='button']", 2)

        d_ = Web_PO.getValueXpathByLabel("input", "placeholder")
        Web_PO.setTextByX(d_['请输入用户名'], varUser)
        Web_PO.setTextByX(d_['输入密码'], varPass)

        d_ = Web_PO.getTextXpathByLabel("button", "/span")
        Web_PO.clkByX(d_['登录'], 2)

        # 系统接口404
        l_ = Web_PO.getTextByXs("//div")
        if '系统接口404异常' in l_:
            print('系统接口404异常')
            self.logger.error('系统接口404异常')
            Web_PO.cls()
            sys.exit(0)

    def getMenu2Url(self):

        # 获取菜单连接

        # 统计ur数量
        # c = Web_PO.getCount("ul")
        c = Web_PO.getCountByTag("ul")
        varLabelCount = c - 3

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
            Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[" + (str(d_menu[varMenu1])) + "]")
        else:
            Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[" + (str(d_menu[varMenu1])) + "]")
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
                        Web_PO.clk('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[' + str(
                            d_menu2[varMenu2Name]) + ']/li/ul/div[' + str(i) + ']/a', 2)
                        break
                break



    # todo common

    def __loggerPrint(self, varStatus, varInfor):
        # 日志和打印
        if varStatus == 'info':
            self.logger.info(varInfor)
        elif varStatus == 'error':
            self.logger.error(varInfor)
        print(varInfor)

    def export(self, varFile):
        # 导出
        try:
            ele = Web_PO.getSuperEleByX("//form", ".")
            ele2 = Web_PO.eleGetSuperEleByX(ele, ".//span[text()='导出']", "..")
            Web_PO.eleClkByX(ele2, ".", 2)  # 点击导出
            if os.access(varFile, os.F_OK):
                Web_PO.exportExistFile(varFile)
            else:
                Web_PO.exportFile(varFile)
        except Exception as e:
            print(f"导出过程中发生错误: {e}")

    def __gljg(self, ele, k, v):
        # 管理机构
        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//input", 2)
        if isinstance(v, str):
            if v == '招远市卫健局':
                # 卫健局
                Web_PO.clkByX(self.selectors['dropdown_dropdown_1'] + "/label")
                Web_PO.clkTabByX(self.selectors['dropdown_dropdown_1'] + "/label")
            else:
                # 卫生院
                Web_PO.clkByX(self.selectors['dropdown_dropdown_1'])
                l_2 = Web_PO.getTextByXs(self.selectors['dropdown_dropdown_2'])
                # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                if v in l_2:
                    for i in range(len(l_2)):
                        if l_2[i] == v:
                            Web_PO.clkByX(self.selectors['dropdown_dropdown_2'] + "[" + str(i + 1) + "]/label")
                            Web_PO.clkTabByX(self.selectors['dropdown_dropdown_2'] + "[" + str(i + 1) + "]/label")
                            break
        elif isinstance(v, dict):
            # 卫生院
            Web_PO.clkByX(self.selectors['dropdown_dropdown_1'])
            l_2 = Web_PO.getTextByXs(self.selectors['dropdown_dropdown_2'])
            varKey = list(v.keys())[0]
            if varKey in l_2:
                for i in range(len(l_2)):
                    if l_2[i] == varKey:
                        # 卫生室
                        Web_PO.clkByX(self.selectors['dropdown_dropdown_2'] + "[" + str(i + 1) + "]")
                        l_3 = Web_PO.getTextByXs(self.selectors['dropdown_dropdown_3'])
                        # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                        if v[varKey] in l_3:
                            for i in range(len(l_3)):
                                if l_3[i] == v[varKey]:
                                    Web_PO.clkByX(self.selectors['dropdown_dropdown_3'] + "[" + str(i + 1) + "]/label")
                                    Web_PO.clkTabByX(self.selectors['dropdown_dropdown_3'] + "[" + str(i + 1) + "]/label")
                                    break


    def pagination(self, varGoto):

        # 获取页面，跳转页码
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
        return d_

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



    def _jws(self, ele, k, k_sub, v1, _dropdownByX, varLoc):

        if isinstance(v1, list):
            Web_PO.eleRadioSplitLabels(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/div", "无")
            Web_PO.eleRadioSplitLabels(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/div", "有")
            for i in range(len(v1) - 1):
                # +
                Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/i", 2)
            for i in range(len(v1)):
                # 名称
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), "./div[2]/div[" + str(varLoc) + "]/div[2]/div[" + str(i + 1) + "]/div[1]/div[2]/div/div/div/input", v1[i][0])
                # 时间
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), "./div[2]/div[" + str(varLoc) + "]/div[2]/div[" + str(i + 1) + "]/div[2]/div[1]/div/div/div/input", v1[i][1])
        else:
            if v1 != "remain":
                Web_PO.eleRadioSplitLabels(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/div", "无")
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
                l_blood_2.append('Y')
            else:
                l_blood_2.append('N')
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

    def rgb_to_hex(self, rgb):
        # 从rgb字符串中提取红、绿、蓝的值
        r, g, b = map(int, rgb.strip('rgb()').split(', '))
        # 将每个值转换为两位十六进制字符串
        hex_r = '{:02x}'.format(r)
        hex_g = '{:02x}'.format(g)
        hex_b = '{:02x}'.format(b)
        # 组合成完整的十六进制颜色码
        hex_color = '#' + hex_r + hex_g + hex_b
        return hex_color
 
# =========================================================================================================================================
# =========================================================================================================================================
# =========================================================================================================================================


    # todo 2.1.2 基本公卫 - 健康档案管理 - 个人健康档案

    def __setHealthrecord(self, d_):
        # 居民健康档案（新增、编辑）

        try:
            ele = Web_PO.getSuperEleByX("//form", ".")

            for k, v in d_['data'].items():
                if k in [' 性别 ', ' 民族 ', ' 文化程度 ', ' 职业 ', ' 婚姻状况 ', ' 档案是否开放 ']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div/input",
                                        v)
                elif k in [' 现住址 ']:
                    address_selectors = [
                        ".//div[1]/div[2]/div/div/div/div/div/input",
                        ".//div[2]/div[1]/div/div/div/div/div/input",
                        ".//div[2]/div[2]/div/div/div/div/div/input",
                        ".//div[3]/div[1]/div/div/div/div/div/input",
                        ".//div[3]/div[2]/div/div/div/div/div/input"
                    ]
                    for i in range(5):
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), address_selectors[i],
                                            v[i])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[4]/div[2]/div/div/div/input", v[5])

                elif k in [' 姓名 ', ' 本人电话 ', ' 联系人姓名 ', ' 联系人电话 ', ' 工作单位 ']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)

                elif k in [' 出生日期 ', ' 建档日期 ']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)

                elif k in [' 血型 ', ' 常住类型 ', ' 血型 ', ' RH血型 ', ' 厨房排风设施 ', ' 燃料类型 ', ' 饮水 ', ' 厕所 ', ' 禽畜栏 ', ' 更新方式 ']:
                    Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div", v)

                elif k in [' 医疗费用支付方式 ']:
                    for i in range(len(v)):
                        self._eleCheckboxPay(Web_PO.eleCommon(ele, k), v[i])

                elif k in [' 药物过敏史 ']:
                    Web_PO.eleCheckboxLeftLabelAndText(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div[1]/div",
                                                       v, ".//div[2]/div/div/div/div/textarea")

                elif k in [' 暴露史 ']:
                    Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon(ele, k), './/div[2]/div/div/div[1]/div', v)

                elif k in [' 既往史 ']:
                    for k1, v1 in v.items():
                        if k1 == '疾病':
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//div[2]/div[1]/div[1]/div[2]/div/div/div[1]/label",
                                                      list(v1.keys())[0])
                            if list(v1.keys())[0] == "有":
                                for i in range(len(v1['有']) - 1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),
                                                     ".//div[2]/div[1]/div[1]/div[2]/div/div/i", 2)  # +
                                for i in range(len(v1['有'])):
                                    # 疾病名称
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[" + str(
                                        i + 1) + "]/div[1]/div[2]/div/div/div/div/div/input",
                                                        v1['有'][i][0])
                                    # 确诊时间
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[" + str(
                                        i + 1) + "]/div[2]/div[1]/div/div/div/input", v1['有'][i][1])

                        if k1 == '手术':
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//div[2]/div[2]/div[1]/div[2]/div/div/div[1]/label",
                                                      list(v1.keys())[0])
                            if list(v1.keys())[0] == "有":
                                for i in range(len(v1['有']) - 1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),
                                                     ".//div[2]/div[2]/div[1]/div[2]/div/div/i",
                                                     2)  # +
                                for i in range(len(v1['有'])):
                                    # 手术名称
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[" + str(
                                        i + 1) + "]/div[1]/div[2]/div/div/div/input", v1['有'][i][0])
                                    # 手术时间
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[" + str(
                                        i + 1) + "]/div[2]/div[1]/div/div/div/input", v1['有'][i][1])

                        if k1 == '外伤':
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//div[2]/div[3]/div[1]/div[2]/div/div/div/label",
                                                      list(v1.keys())[0])
                            if list(v1.keys())[0] == "有":
                                for i in range(len(v1['有']) - 1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),
                                                     ".//div[2]/div[3]/div[1]/div[2]/div/div/i",
                                                     2)  # +
                                for i in range(len(v1['有'])):
                                    # 外伤名称
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div[2]/div[" + str(
                                        i + 1) + "]/div[1]/div[2]/div/div/div/input", v1['有'][i][0])
                                    # 外伤时间
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div[2]/div[" + str(
                                        i + 1) + "]/div[2]/div[1]/div/div/div/input", v1['有'][i][1])

                        if k1 == '输血':
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//div[2]/div[4]/div[1]/div[2]/div/div/div/label",
                                                      list(v1.keys())[0])
                            if list(v1.keys())[0] == "有":
                                for i in range(len(v1['有']) - 1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),
                                                     ".//div[2]/div[4]/div[1]/div[2]/div/div/i",
                                                     2)  # +
                                for i in range(len(v1['有'])):
                                    # 输血原因
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div[2]/div[" + str(
                                        i + 1) + "]/div[1]/div[2]/div/div/div/input", v1['有'][i][0])
                                    # 输血时间
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[4]/div[2]/div[" + str(
                                        i + 1) + "]/div[2]/div[1]/div/div/div/input", v1['有'][i][1])

                elif k in [' 家族史 ']:
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/label",
                                              list(v.keys())[0])
                    if list(v.keys())[0] == '有':
                        for i in range(len(v['有']) - 1):
                            Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/i", 2)  # +
                        for i in range(len(v['有'])):
                            # 疾病名称
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//div[" + str(i + 1) + "]/div[1]/div[2]/div/div/div/div/div/input",
                                                v['有'][i][0])
                            # 与本人关系
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//div[" + str(i + 1) + "]/div[2]/div[2]/div/div/div/div/div/input",
                                                v['有'][i][1])

                elif k in [' 遗传病史 ']:
                    Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/label", v,
                                                     ".//div[2]/div[2]/div/div/div/input")

                elif k in [' 残疾情况 ']:
                    l_ = []
                    for i in range(len(v)):
                        if isinstance(v[i], list):
                            l_ = v[i]
                            Web_PO.eleCheckboxLeftLabelAndText(Web_PO.eleCommon(ele, k),
                                                               ".//div[2]/div/div/div/div[1]/div", v[i],
                                                               ".//div[2]/div/div/div/div[2]/div/div[1]/input")
                        if isinstance(v[i], dict):
                            # print(l_)
                            # 勾选无残疾时，无法输入残疾证号
                            if "无残疾" not in l_:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                                     ".//div[2]/div[2]/div/div/div/input", v[i][' 残疾证号 '])

                elif k in [' 家庭情况 ']:
                    for k1, v1 in v.items():
                        if k1 in [' 与户主关系 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input",
                                                v1)
                        elif k1 in [' 户主姓名 ', ' 户主身份证号 ', ' 家庭人口数 ', ' 家庭结构 ']:
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                        elif k1 in [' 居住情况 ']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div", v1)

                elif k in [' 管理机构 ']:
                    self.__gljg(ele, k, v)

                elif k in [' 更新内容 ']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input", v)

            if d_['button'] == '仅保存':
                Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='仅保存']", ".."), ".", 2)
            elif d_['button'] == '保存复核':
                Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='保存复核']", ".."), ".", 2)
            elif d_['button'] == '取消':
                Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='取消']", ".."), ".", 2)

            #  关联家庭
            # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='关联家庭']", "../.."), ".//div[3]/div/button[1]", 2)  # 确认
            Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='关联家庭']", "../.."), ".//div[3]/div/button[2]",
                             2)  # 取消

            self.logger.info("保存 => " + str(d_))
        except Exception as e:
            self.logger.error(f"Health record update failed: {e}")

    def __getHealthrecord(self, varStatus='更新信息'):
        # 获取居民健康档案

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

        # 医疗费用支付方式
        d_1 = self._getCheckbox(' 医疗费用支付方式 ')
        if d_1['医疗费用支付方式']['城镇职工基本医疗保险'] == 'Y':
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['城镇职工基本医疗保险'] = {'Y': d_2['医疗费用支付方式'][0]}
            d_.update(d_1)
        if d_1['医疗费用支付方式']['城镇居民基本医疗保险'] == 'Y':
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['城镇居民基本医疗保险'] = {'Y': d_2['医疗费用支付方式'][1]}
            d_.update(d_1)
        if d_1['医疗费用支付方式']['贫困救助'] == 'Y':
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['贫困救助'] = {'Y': d_2['医疗费用支付方式'][2]}
            d_.update(d_1)
        if d_1['医疗费用支付方式']['其他'] == 'Y':
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['其他'] = {'Y': d_2['医疗费用支付方式'][3]}
            # d_1['医疗费用支付方式']['input'] = d_2['医疗费用支付方式'][3]
            d_.update(d_1)

        # 药物过敏史
        d_1 = self._getCheckbox(' 药物过敏史 ')
        d_.update(d_1)
        if d_1['药物过敏史']['其他药物过敏源'] == "Y":
            d_2 = self._getTextarea(' 药物过敏史 ')
            d_1['药物过敏史']['其他药物过敏源'] = {'Y': d_2['药物过敏史'][0]}
            d_.update(d_1)

        # 暴露史
        d_.update(self._getCheckbox(' 暴露史 '))

        # 既往史
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
        d_5['既往史'] = d_1
        d_.update(d_5)

        # 家族史
        d_1 = self._getRadio(' 家族史 ')
        # print(d_1)  # {'家族史': {'有': 1, '无': 0}}
        if d_1['家族史'] == {}:
            d_1['家族史'] = '无'
        elif d_1['家族史']['有'] == 1:
            d_2 = self._getText(' 家族史 ')
            d_1['家族史']['input'] = d_2['家族史']
        d_.update(d_1)

        # 遗传病史
        d_1 = self._getRadio(' 遗传病史 ')
        d_2 = self._getText(' 遗传病史 ', "../..")
        d_1['遗传病史']['疾病名称'] = d_2['遗传病史'][0]
        d_.update(d_1)

        # 残疾情况
        d_1 = self._getCheckbox(' 残疾情况 ')
        d_.update(d_1)
        if d_1['残疾情况']['其他残疾'] == "Y":
            d_2 = self._getText(' 残疾情况 ')
            d_1['残疾情况']['其他残疾'] = {'Y': d_2['残疾情况'][0]}
            d_.update(d_1)
        d_.update(self._getText(' 残疾证号 '))

        # 家庭情况
        d_1 = self._getText(' 与户主关系 ')
        d_1.update(self._getText(' 户主姓名 '))
        d_1.update(self._getText(' 户主身份证号 '))
        d_1.update(self._getText(' 家庭人口数 '))
        d_1.update(self._getText(' 家庭结构 '))
        d_1.update(self._getRadio(' 居住情况 '))
        d_.update({'家庭情况': d_1})

        # 生活环境
        d_1 = self._getRadio(' 厨房排风设施 ')
        d_1.update(self._getRadio(' 燃料类型 '))
        d_1.update(self._getRadio(' 饮水 '))
        d_1.update(self._getRadio(' 厕所 '))
        d_1.update(self._getRadio(' 禽畜栏 '))
        d_.update({'生活环境': d_1})

        # 建档单位
        d_.update(self._getText(' 建档单位 '))
        d_.update(self._getText(' 管理机构 '))
        d_.update(self._getText(' 档案是否开放 '))

        # 建档日期
        d_.update(self._getText(' 建档日期 '))
        d_.update(self._getText(' 建档人 '))

        if varStatus == '更新信息':
            # 更新信息
            d_.update(self._getText(' 更新日期 '))
            d_.update(self._getRadio(' 更新方式 '))
            d_.update(self._getText(' 更新人 '))
            d_.update(self._getText(' 更新内容 ', "../.."))

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='关闭']", ".."), ".", 2)
        return d_

    def _eleCheckboxPay(self, ele, v, default='remain'):
        # 医疗费用支付方式
        # 选择复选框的值

        # 1, 全部不勾选
        if default != "remain":
            # 城镇职工基本医疗保险
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div/label", "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div/label", 1)
            # 城镇居民基本医疗保险
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/label", 1)
            # 贫困救助
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/label", 1)
            # 商业医疗保险
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", 1)
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", 1)
            # 全公费
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[5]/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[5]/label", 1)
            # 全自费
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[6]/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[6]/label", 1)
            # 其他
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[7]/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[7]/label", 1)

        # 更改
        if isinstance(v, list):
            Web_PO.eleCheckboxLeftLabelAndText(ele, ".//div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/div", v,
                                               ".//div[2]/div/div/div/div[2]/div[2]/div/div/div/div/input")

        if isinstance(v, dict):
            for k1, v1 in v.items():
                if k1 == '城镇职工基本医疗保险':
                    Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div")
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/input", v1)
                if k1 == '城镇居民基本医疗保险':
                    Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div")
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[1]/div[3]/div/div/div/div/input", v1)
                if k1 == '贫困救助':
                    Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div")
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[2]/div/div/div/input", v1)
  
    def phs_healthrecord_personal_query(self, d_):

        # 个人健康档案 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, "./div/div", 1)  # 展开

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '建档人', '本人电话']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v[1])
                elif k in ['性别', '人群分类', '档案是否开放', '档案状态', '血型', '常住类型', '是否签约', '是否残疾', '今年是否体检', '既往史', '今年是否已更新', '医疗费用支付方式', '档案缺失项目']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期范围', '今年体检日期', '今年更新日期', '建档日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[2]/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/div/div[2]/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def phs_healthrecord_personal_new(self, d_):

        # 个人健康档案 - 新增

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='新增']", ".."), ".", 2)

        # 居民健康档案
        self.__setHealthrecord(d_)

    def _phs_healthrecord_personal_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '提醒', '性别', '出生日期时间', '年龄', '上次完成检查类型', '上次随访日期', '下次随访日期', '母亲姓名', '母亲联系电话', '父亲姓名', '父亲联系电话', '管理状态', '管理类别', '登记机构', '身份证号', '家庭住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        # print(l_value)
        l_value = List_PO.dels(l_value, '查看')
        l_value = List_PO.dels(l_value, '更新')
        l_value = List_PO.dels(l_value, '更多')
        # print(l_value)
        l_group = (List_PO.split2(l_value, varOperation))
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 处理人群分类数据
        for i in l_group:
            if '\n' in i[3]:
                t = len(i[3].split("\n"))
                for j in range(t):
                    i.pop(4)
                i.pop(4)
            else:
                i.pop(4)
                i.pop(4)
        # print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_healthrecord_personal_operation(self, d_):

        # 个人健康档案 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                if d_['operate'] == ' 查看 ':
                    ele3 = Web_PO.getSuperEleByX("(//div[text()=' 查看 '])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    self.logger.info(str(d_))
                    return self.__getHealthrecord('查看')
                if d_['operate'] == ' 更新 ':
                    ele3 = Web_PO.getSuperEleByX("(//div[text()=' 更新 '])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                elif d_['operate'] == '终结':
                    ele3 = Web_PO.getSuperEleByX("(//div[text()='更多'])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    Web_PO.clkByX("//div[@class='el-popper is-light el-popover' and @role='tooltip' and @aria-hidden='false']/div[1]", 2)
                elif d_['operate'] == '更新历史':
                    ele3 = Web_PO.getSuperEleByX("(//div[text()='更多'])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    Web_PO.clkByX("//div[@class='el-popper is-light el-popover' and @role='tooltip' and @aria-hidden='false']/div[2]", 2)
                elif d_['operate'] == '姓名':
                    Web_PO.clkByX("//tbody/tr[" + str(self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]/td[2]/div", 2)
                else:
                    ele3 = Web_PO.getSuperEleByX("(//div[text()='" + d_['operate'] + "'])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)


            elif d_['operate'] == '更新' and d_['operate2'] in ['仅保存', '保存复核']:
                # 居民健康档案
                self.__setHealthrecord(d_)

            elif d_['operate'] == '终结':
                ele = Web_PO.getSuperEleByX("//span[text()='终结健康档案']", "../..")
                # 判断档案状态
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                for k, v in d_['data']['档案状态'].items():
                    # 选择档案状态
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '档案状态'), ".//div/div/label", k)
                    if k == '暂不管理':
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, '暂不管理原因'), ".//input", _dropdownByX, v['暂不管理原因'])
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, '暂不管理日期'), ".//input", v['暂不管理日期'])
                    elif k == '已死亡':
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, '档案注销日期'), ".//input", v['档案注销日期'])
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, '死亡日期'), ".//input", v['死亡日期'])
                # Web_PO.eleClkByX(ele2, ".//button[1]")  # 确认
                Web_PO.eleClkByX(ele, ".//button[2]")  # 取消

            elif d_['operate'] == '更新历史':
                ele2 = Web_PO.getSuperEleByX("//span[text()='更新历史']", "../..")
                Web_PO.eleClkByX(ele2, ".//button[1]")  # 关闭

            elif d_['operate'] == '姓名' and d_['operate2'] == '更新':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='更新']", ".."), ".", 2)
                # 居民健康档案
                self.__setHealthrecord(d_)

            elif d_['operate'] == '姓名' and d_['operate2'] == '获取':
                self.logger.info(str(d_))
                # 居民健康档案
                return self.__getHealthrecord()

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))




    # todo common

    def __setData2(self, ele, k, v):
        # 日期控件 - 内部调用
        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
        try:
            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[5]/input", v[1])
        except:
            try:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
            except:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])

    def __setAge2(self, ele, k, v):
        # 年龄控件 - 内部调用
        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v[0])
        try:
            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v[1])
        except:
            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])

    def __setAddress3(self, ele, k, v):
        # 地址控件 - 内部调用

        if Web_PO.eleIsEleExistByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input") and Web_PO.eleIsEleExistByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input"):
            Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[1]/div/div/div/div/input", v[0])
            Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input", v[1])
            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
        elif Web_PO.eleIsEleExistByX(Web_PO.eleCommon(ele, k), ".//div/div[2]/div/div/div/input") and Web_PO.eleIsEleExistByX(Web_PO.eleCommon(ele, k), ".//div/div/div[3]/div/input"):
            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div[1]/div/div/div/input", v[0])
            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div[2]/div/div/div/input", v[1])
            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/div/div[3]/div/input", v[2])


    def query(self, d_):
        # common - 查询 - 外部调用
        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '联系电话', '随访医生', '家庭住址', '录入人员', '家庭住址']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '是否终止管理', '档案状态', '管理状态', '数据源', '人群分类',
                            '三高分类',  '并发症筛查', '并发症类型', '当年患者补充表', '评估结果',
                            '随访方式', '随访提醒分类','随访评价结果', '随访评估结果（高血压）', '随访评估结果（糖尿病）', '随访评估结果（高血脂）',
                           '签约类型', '签约状态', '签约机构', '签约团队', '签约服务包', '居民基本情况', '履约情况', '居民基本信息']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期', '签约日期', '评估日期', '填表日期', '采集日期', '随访日期', '上次随访日期', '下次随访日期', '登记日期', '建卡日期', '建档日期','预期服务时间']:
                    self.__setData2(ele, k, v)
                elif k in ['年龄', '登记时年龄']:
                    self.__setAge2(ele, k, v)
                if k in ['现住址']:
                    self.__setAddress3(ele, k, v)
                    # Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[1]/div/div/div/div/input",  v[0])
                    # Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    # # /html/body/div[1]/div/div[3]/section/div/main/form/div/div[7]/div/div/   div/div[2]/div/div/div/input
                    # Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                    # # /html/body/div[1]/div/div[3]/section/div/main/form/div/div[7]/div/   div/div/div[3]/div/input
                elif k in ['管理机构', '档案管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.button1('查询 ')

        # 日志
        self.logger.info("查询 => " + str(d_))

    def batch(self, d_):
        # common - 批量选择 - 外部调用
        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//tbody", ".")
        try:
            if isinstance(d_['option'], str):
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/div/div[1]/div[2]/table/thead/tr/th[1]/div/label', 2)
            elif isinstance(d_['option'], dict):
                Web_PO.eleClkByX(ele, ".//tr[" + str(self._sign_jmsign_signed_operation('更新签约\n解约\n历史记录', d_['option'])) + "]/td[1]/div/label", 2)
            Web_PO.button1('批量更换家医团队')

            # 批量更换家医团队申请
            ele2 = Web_PO.getSuperEleByX("//span[text()='批量更换家医团队申请']", "../..")
            for k,v in d_['data'].items():
                if k == '更换团队':
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele2, k), './/input', v)
                elif k == '签约医生':
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele2, k), ".//input", v)
                elif k == '更换原因':
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele2, k), ".//input", v)
        except:
            self.logger.error("批量")

        # Web_PO.button1('确 认')
        Web_PO.button1('关 闭')


        # 日志
        self.logger.info("查询 => " + str(d_))




    # todo 3.1.2 基本公卫 - 三高共管 - 医防融合信息表

    def _three_ThreeHighs_supplement_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        # print(l_value)
        l_group = (List_PO.split2(l_value, varOperation))
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # # 处理三高分类字段
        for i in l_group:
            i.pop(2)
            i.pop(2)
            i.pop(2)
        # print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_ThreeHighs_supplement_operation(self, d_):

        # 医防融合信息表 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_ThreeHighs_supplement_operation('修改\n删除', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)
                if d_['operate'] == '删除':
                    Web_PO.button1('否')

            elif d_['operate'] == '慢性病患者医防融合信息表':
                Web_PO.button1('编辑')


            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 3.1.3 基本公卫 - 三高共管 - 三高随访管理

    def _newCardiovascularAssessment(self, d_):

        # 新建 心血管评估

        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in [' 现居住区地区域 ', ' 评测结果 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", v)
            if k in [' 是否服用降压药 ', ' 现在是否吸烟 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/label", v)
            elif k in [' 现居住地类型 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/label", v)
            elif k in [' 是否患糖尿病 ', ' 心脑血管家族史(指父母兄弟姐妹中有人患有心肌梗死或脑卒中)']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/label", v)
            elif k in [' 腰围 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/input", v)
            elif k in [' 当前血压水平 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v[0])
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v[1])
            elif k in [' 总胆固醇 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/input", v[0])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/div/div/label", v[1])
            elif k in [' 高密度脂蛋白胆固醇 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v[0])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/div/label", v[1])
            elif k in [' 评估时间 ']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
        Web_PO.button1('取消')

    def _three_ThreeHighs_ThnVisitList_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        # print(l_value)
        l_group = (List_PO.split2(l_value, varOperation))
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # # 处理三高分类字段
        for i in l_group:
            if "\n" not in i[1]:
                i.pop(2)
                i.pop(2)
            else:
                varCountN = len(i[1].split("\n"))
                for _ in range(varCountN+1):
                    i.pop(2)
        # print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_ThreeHighs_ThnVisitList_operation(self, d_):

        # 三高随访管理 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_ThreeHighs_ThnVisitList_operation('详情\n编辑\n删除', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)
                if d_['operate'] == '删除':
                    Web_PO.button1('否')
                    # Web_PO.button1('是')
                if d_['operate'] == '详情':
                    Web_PO.button1('关闭')
                    Web_PO.button1('新增随访')


            elif d_['operate'] == '三高患者评估_心血管评估记录_新增评估':
                self._newCardiovascularAssessment(d_)

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 3.1.4 基本公卫 - 三高共管 - 心血管评估管理

    def _three_ThreeHighs_cardiovascularCheck_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        # print(l_value)
        l_group = (List_PO.split2(l_value, varOperation))
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 处理三高分类字段
        for i in l_group:
            i.pop(2)
            i.pop(2)
            i.pop(2)
            i.pop(2)
            i.pop(2)
            i.pop(2)
            i.pop(2)
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_ThreeHighs_cardiovascularCheck_operation(self, d_):

        # 心血管评估管理 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_ThreeHighs_cardiovascularCheck_operation('详情\n编辑\n删除', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)
                if d_['operate'] == '删除':
                    Web_PO.button1('否')
                    # Web_PO.button1('是')
                if d_['operate'] == '详情':
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    a = Web_PO.eleGetTextByXs(ele, ".//div")
                    b = Web_PO.eleGetTextByXs(ele, ".//span")
                    print("a", a)
                    print("b", b)

            elif d_['operate'] == '编辑':
                self._newCardiovascularAssessment(d_)

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 3.1.6 基本公卫 - 三高共管 - 三高患者管理

    def _yfrh(self, d_):

        # 慢性病患者医防融合信息表

        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in [' 风险评估方式 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", v)
            elif k in [' 风险评估结果 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/label", v)
            elif k in [' 享受医保政策情况 ']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/div/input", v)
            elif k in [' 医保定点医院 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/label", v[0])
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v[1])
            elif k in [' 靶器官 ']:
                for k1, v1 in v.items():
                    if k1 in [' 是否筛查 ']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/label", v1)
                    elif k1 in [' 筛查日期 ']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/input", v1)
                    elif k1 in [' 筛查机构 ']:
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k1), ".//div[6]/div/div/div/input", v1)
                    elif k1 in [' 筛查内容 ']:
                        Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v1,
                                                            ".//div[3]/div/div/div/input")
            elif k in [' 患者最关注并希望得到支持的方面 ']:
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/label",
                                                    v, ".//div[2]/div/div[2]/div/div/div/input")
            elif k in [' 居家健康支持 ']:
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", v,
                                                    ".//div[2]/div[3]/div/div/div/input")
            elif k in [' 自我管理小组 ']:
                for k1, v1 in v.items():
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", k1)
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[7]/div/div/div/div/div/input", v1[2])
                    if k1 in ['已参加(组员)', '已参加(组长)']:
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), './/div[3]/div/div/div/input', v1[0])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), './/div[5]/div/div/div/input', v1[1])
            elif k in [' 填表日期 ']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/input", v)
        Web_PO.button1('关闭')
        # Web_PO.button1('保存')

    def three_ThreeHighs_ThnList_query(self, d_):

        # 三高患者管理 - 查询（部分）
        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['三高分类']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['人群分类']:
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/main/div[1]/form/div/div[7]/div/label[2]/span")
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

    def _three_ThreeHighs_ThnList_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        print(l_value)
        try:
            s_class_warn = Web_PO.eleGetAttrValueByX(ele2, ".//td[3]/div/div/div", "style")
            # print(s_class_warn)  # background: rgb(223, 57, 38); width: 16px; height: 16px;
            s_class_warn = s_class_warn.split("rgb")[1].split(";")[0]
            l_value[2] = hex_color = self.rgb_to_hex(s_class_warn)
            print(l_value)
        except:
            l_value[2] = ''

        # 获取字段和类型字典
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 处理三高分类字段
        for i in l_group:
            i.pop(3)
            i.pop(3)
            i.pop(3)
        for i in l_group:
            varCountN = len(i[3].split("\n"))
            print(varCountN)
            if varCountN > 0:
                for _ in range(varCountN):
                    i.pop(4)
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_ThreeHighs_ThnList_operation(self, d_):

        # 三高患者管理 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_ThreeHighs_ThnList_operation('随访\n风险评估\n新增', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '三高患者评估_心血管评估记录_新增评估':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[1]/div[1]')
                Web_PO.button1(' 新增评估 ')
                # 心血管疾病风险评估记录表
                self._newCardiovascularAssessment(d_)

            elif d_['operate'] == '三高患者评估_随访记录_新增随访':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[1]/div[2]')
                Web_PO.button1(' 新增随访 ')
                ele = Web_PO.getSuperEleByX("//form", ".")
                for k, v in d_['data'].items():
                    if k in ['数据回传公卫随访表']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v, varClass='el-checkbox el-checkbox--large is-checked')
                    elif k in ['随访日期']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
                    elif k in ['随访方式']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/label", v)
                    elif k in ['高血压症状', '糖尿病症状']:
                        Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[1]/label", v, ".//div[2]/div/div/div[2]/div/div/input")
                    elif k in ['高血脂症状']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                    elif k in ['体征']:
                        for k1, v1 in v.items():
                            if k1 in ['血压']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div[1]/div/div/input", v1[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[3]/div/div[1]/div/div/input", v1[1])
                            elif k1 in ['体重']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[5]/div/div[1]/div/div/input", v1[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[6]/div/div[1]/div/div/input", v1[1])
                            elif k1 in ['身高']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div[1]/div/div/input", v1)
                            elif k1 in ['腰围']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[2]/div/div[1]/div/div/input", v1)
                            elif k1 in ['心率']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[4]/div/div[1]/div/div/input", v1)
                            elif k1 in ['足背动脉搏动']:
                                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[4]/div[2]/div/div/div/div/div/div/input",  v1)
                            elif k1 in ['其他体征']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[4]/div[4]/div/div[1]/div/div/input", v1)
                    elif k in ['生活方式指导 ']:
                        for k1, v1 in v.items():
                            if k1 in ['日吸烟量']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div[1]/div/div/input", v1[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[3]/div/div[1]/div/div/input", v1[1])
                            elif k1 in ['日饮酒量']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[5]/div/div[1]/div/div/input", v1[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[6]/div/div[1]/div/div/input", v1[1])
                            elif k1 in ['运动']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div[1]/div/div/input", v1[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[3]/div/div[1]/div/div/input", v1[1])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[4]/div/div[1]/div/div/input", v1[2])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[5]/div/div[1]/div/div/input", v1[3])
                            elif k1 in ['日主食量']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[2]/div/div[1]/div/div/input", v1[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[3]/div/div[1]/div/div/input", v1[1])
                            elif k1 in ['摄盐量分级']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div[5]/div/div[2]/div/div/label", v1[0])
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div[6]/div/div[2]/div/div/label", v1[1])
                            elif k1 in ['心理调整']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[4]/div[2]/div/div/div/div/label", v1)
                            elif k1 in ['随访遵医行为评价']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/div/label", v1)
                    elif k in ['用药情况', '用药调整情况']:
                        if len(v) == 1:
                            for k1, v1 in v[0].items():
                                if k1 == '药品名称':
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div/div/div/div/input",  v1)
                                elif k1 == '用法用量':
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[4]/div/div/div/div/div/div/input",  v1[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[5]/div/div[2]/div/div/input", v1[1])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[5]/div/div[3]/div/div/input", v1[2])
                        else:
                            for _ in range(len(v)-1):
                                Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[6]/div")
                            for i in range(len(v)):
                                for k1, v1 in v[i].items():
                                    if k1 == '药品名称':
                                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[2]/div/div/div/div/div/div/input",  v1)
                                    elif k1 == '用法用量':
                                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[4]/div/div/div/div/div/div/input",  v1[0])
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[5]/div/div[2]/div/div/input", v1[1])
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[5]/div/div[3]/div/div/input", v1[2])
                    elif k in ['用药依从性']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/div/div/div/input",  v)
                    elif k in ['药物不良反应']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/div/div/input",  v[0])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/div/input", v[1])
                    elif k in ['低血糖反应']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/div/div/div/input",  v)
                    elif k in ['辅助检查']:
                        for k1, v1 in v.items():
                            if k1 in ['空腹血糖值']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div[1]/div/div/input", v1)
                            if k1 in ['糖化血红蛋白']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[4]/div/div[1]/div/div/input", v1)
                            if k1 in ['TG']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[6]/div/div[1]/div/div/input", v1)
                            if k1 in ['TC']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[8]/div/div[1]/div/div/input", v1)
                            if k1 in ['HDL-C']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div[1]/div/div/input", v1)
                            if k1 in ['LDL-C']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[4]/div/div[1]/div/div/input", v1)
                            if k1 in ['检查日期']:
                                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[6]/div/div/div/input", v1)
                            if k1 in ['其他']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[2]/div/div/div/input", v1)
                    elif k in ['本年度并发症筛查检查', '本年度并发症评估结果']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                    elif k in ['此次随访分类']:
                        for i in v:
                            for k1, v1 in i.items():
                                if k1 in ['高血压患者']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div[1]/div/div[2]/div/div/label", v1['随访评价结果'])
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div/label", v1['下一步管理措施'])
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div[2]/div/div[4]/div/div/input", v1['下次随访日期'])
                                elif k1 in ['糖尿病患者']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div/label", v1['随访评价结果'])
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/div/label", v1['下一步管理措施'])
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div[2]/div/div[4]/div/div/input", v1['下次随访日期'])
                                elif k1 in ['高血脂患者']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div/div/label", v1['随访评价结果'])
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[2]/div/div[2]/div/div[2]/div/div/label", v1['下一步管理措施'])
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/input", v1['下次随访日期'])
                    elif k in ['转诊情况 ']:
                        for k1, v1 in v.items():
                            if k1 in ['转诊标志']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div/div/label", v1)
                                varSign = 1
                            if varSign == 1:
                                if k1 in ['转诊医疗机构及科室']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[4]/div/div/div/div/input", v1)
                                elif k1 in ['转诊原因']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div/div/input", v1)
                                elif k1 in ['联系人']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[4]/div/div/div/div/input", v1)
                                elif k1 in ['联系人电话']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[6]/div/div/div/div/input", v1)
                                elif k1 in ['转诊结果']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[2]/div/div/div/div/label", v1)
                                elif k1 in ['备注']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[4]/div/div/div/div/input", v1)
                    elif k in ['居民签名']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                Web_PO.button1('取消')
                # Web_PO.button1('保存')

            elif d_['operate'] == '慢性病患者医防融合信息表':
                self._yfrh(d_)

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 3.2.1 基本公卫 - 冠心病患者管理 - 冠心病登记

    def _three_Coronary_CHDregister_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        # 获取字段和类型字典
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_Coronary_CHDregister_operation(self, d_):

        # 冠心病登记 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_Coronary_CHDregister_operation('新增登记', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '个人专项档案_冠心病患者登记':
                # 冠心病患者登记
                self._coronary_patient_registry(d_)

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 3.2.2 基本公卫 - 冠心病患者管理 - 冠心病管理

    def __tjb(self, d_):
        # 体检表
        ele = Web_PO.getSuperEleByX("//div[text()='国家基本公共卫生服务项目健康体检表']", "../..")
        ele4 = Web_PO.getSuperEleByX("//div[text()='辅助检查']", "../../..")

        for k, v in d_['data'].items():
            if k in ['体检来源']:
                Web_PO.eleRadioRightLabel(Web_PO.eleDiv(ele, k), './/div[2]/div/div/div/label', v)
            elif k in ['体检日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)
            elif k in ['责任医生', '体温', '脉率', '呼吸频率', '腰围', '身高', '体重']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
            elif k in ['右侧血压']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
            elif k in ['症状']:
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleP(ele, k, "../.."), './/div[2]/div/div[1]/div/div/label',
                                                    v, './/div[2]/div/div[1]/div/div/div/input')
            elif k in [' 老年人健康', ' 老年人生活自理', '饮酒频率', '是否戒酒', ' 听力 ', ' 运动能力 ', ' 眼底 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), './/div[2]/div/div/div/label', v)
            elif k in ['老年人认知能力', '老年人情感状态']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), './/div[4]/div/div/div/label')
                if isinstance(v, str):
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), './/div[4]/div/div/div/label', v)
                elif isinstance(v, dict):
                    Web_PO.eleRadioRightLabel(Web_PO.eleDiv(ele, k), './/div[4]/div/div/div/label', list(v.keys())[0])
                    Web_PO.eleClsReadonlyByX(Web_PO.eleDiv(ele, k), ".//div[4]/div[2]/div/div/input", 2)
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[4]/div[2]/div/div/input", v[list(v.keys())[0]])
            elif k in ['体育锻炼']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '锻炼频率'), ".//div/div/label")
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '锻炼频率'), ".//div/div/label", v['锻炼频率'])
                if v['锻炼频率'] != '不锻炼':
                    for k1, v1 in v.items():
                        if k1 != '锻炼频率':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div/div/input", v1)
            elif k in [' 饮食习惯 ']:
                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in [' 吸烟情况 ']:
                Web_PO.eleDropdown(Web_PO.eleDiv(ele, k), './/div[2]/div/div/div/div/div/input',
                                    v['吸烟状况'])
                if v['吸烟状况'] != '从不吸':
                    for k1, v1 in v.items():
                        if k1 != '吸烟状况':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div/div/input", v1)
            elif k in [' 饮酒情况 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '饮酒频率'), ".//div/div/label", v['饮酒频率'])
                if v['饮酒频率'] != '从不':
                    for k1, v1 in v.items():
                        if k1 == '日饮酒量' or k1 == '开始饮酒年龄':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div/div/input", v1)
                        elif k1 == '近一年内是否曾醉酒':
                            Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele, '近一年内是否曾醉酒'), ".//div/div/label", v1)
                for k1, v1 in v.items():
                    if k1 == '是否戒酒':
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '是否戒酒'), ".//div/div/label", list(v1.keys())[0])
                        if list(v1.keys())[0] == '已戒酒':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, '戒酒年龄'), ".//div/div/input", v1['已戒酒'])
                    if k1 == '饮酒种类':
                        Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele, '饮酒种类'), ".//div/div/label", v1)
            elif k in ['职业病危害']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[1]/div[1]/div/div/label")
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k), ".//div[2]/div[1]/div[1]/div/div/label",
                                                 list(v.keys())[0])
                for k1, v1 in v.items():
                    if k1 == '有':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[1]/div[2]/div[1]/input", v1[0])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[1]/div[2]/div[2]/input", v1[1])
                    if k1 == '毒物种类':
                        for k2, v2 in v1.items():
                            if k2 == '粉尘':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[2]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[2]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[2]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[2]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '化学有害因素':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[3]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '物理有害因素':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[4]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '生物因素':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[5]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '放射物质类':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[6]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[6]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[6]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[6]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '不详':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[7]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[7]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[7]/div[3]/div/div/label",list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[7]/div[4]/input",v2[2]['防护措施']['有'])
                            if k2 == '其他':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[8]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[8]/div[2]/input", v2[1])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[8]/div[3]/div/div/label[2]", 2)
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[8]/div[4]/input",v2[2]['防护措施']['有'])
                                else:
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[8]/div[3]/div/div/label[1]", 2)
            elif k in [' 口腔 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '口唇'), ".//div/div/label")
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele, '口唇'), ".//div/div/label", v['口唇'])
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele, '咽部'), ".//div/div/label", v['咽部'])
                if '正常' in v['齿列']:
                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/label[1]")
                else:
                    for k1, v1 in v['齿列'].items():
                        if k1 == '缺齿':
                            Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/label[2]")
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[1]/div[1]/div/input",
                                                 v1[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[1]/div[2]/div/input",
                                                 v1[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[4]/div[1]/div/input",
                                                 v1[2])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[4]/div[2]/div/input",
                                                 v1[3])
                        if k1 == '龋齿':
                            Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/label[3]")
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[1]/div[1]/div/input",
                                                 v1[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[1]/div[2]/div/input",
                                                 v1[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[4]/div[1]/div/input",
                                                 v1[2])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[4]/div[2]/div/input",
                                                 v1[3])
                        if k1 == '义齿(假牙)':
                            Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/label[4]")
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[1]/div[1]/div/input",
                                                 v1[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[1]/div[2]/div/input",
                                                 v1[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[4]/div[1]/div/input",
                                                 v1[2])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[4]/div[2]/div/input",
                                                 v1[3])
            elif k in [' 视力 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '口唇'), ".//div/div/label")
                for k1, v1 in v.items():
                    if k1 == '左眼':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/input", v1)
                    if k1 == '右眼':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/input", v1)
                    if k1 == '矫正视力左眼':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/input", v1)
                    if k1 == '矫正视力右眼':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[4]/input", v1)
            elif k in [' 皮肤 ', ' 巩膜 ', ' 淋巴结 ']:
                if '其他' in v:
                    Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                     ".//div[2]/div/div/div/div/input")
                else:
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label",
                                              list(v.keys())[0])
            elif k in [' 肺 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '桶状胸'), ".//div/div/label")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '桶状胸'), ".//div/div/label", v['桶状胸'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '呼吸音'), ".//div/div/label", v['呼吸音'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '罗音'), ".//div/div/label", v['罗音'],
                                                 ".//div/div/div/input")
            elif k in [' 心脏 ']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, '心率'), ".//div/div/input", v['心率'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '心律'), ".//div/div/label", v['心律'])
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '杂音'), ".//div/div/label", v['杂音'],
                                                 ".//div/div/div/input")
            elif k in [' 腹部 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '压痛'), ".//div/div/label")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '压痛'), ".//div/div/label", v['压痛'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '包块'), ".//div/div/label", v['包块'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '肝大'), ".//div/div/label", v['肝大'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '脾大'), ".//div/div/label", v['脾大'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '移动性浊音'), ".//div/div/label", v['移动性浊音'],
                                                 ".//div/div/div/input")
            elif k in [' 下肢水肿 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in [' 足背动脉搏动 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in [' 肛门指诊 ']:
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                 ".//div[2]/div/div/div/div/input")
            elif k in [' 乳腺 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label")
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                    ".//div[2]/div/div/div/div/input")
            elif k in [' 妇科 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '外阴'), ".//div/div/label", v['外阴'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '阴道'), ".//div/div/label", v['阴道'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '宫颈'), ".//div/div/label", v['宫颈'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '宫体'), ".//div/div/label", v['宫体'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '附件'), ".//div/div/label", v['附件'])
            elif k in [' 其他 ']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/textarea", v)
            elif k in [' 脑血管疾病 ', ' 肾脏疾病 ', ' 心血管疾病 ', ' 眼部疾病 ', ' 神经系统疾病 ', ' 其他系统疾病 ']:
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                    ".//div[2]/div/div/div/div/input")
            elif k in [' 住院史 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div[1]/div/div/div/input")
                if len(v) == 1:
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[1]/div/div/div/input",
                                            v[0]['入院日期'])
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[2]/div/div/div/input",
                                            v[0]['出院日期'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[3]/div/div/div/input",
                                         v[0]['原因'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[4]/div/div/div/input",
                                         v[0]['医疗机构及科室名称'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[5]/div/div/div/input",
                                         v[0]['病案号'])
                else:
                    for i in range(len(v) - 1):
                        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div[6]/button")  # 添加
                    for i in range(len(v)):
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k),
                                                ".//div[2]/div/div[" + str(i + 2) + "]/div[1]/div/div/div/input",
                                                v[i]['入院日期'])
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k),
                                                ".//div[2]/div/div[" + str(i + 2) + "]/div[2]/div/div/div/input",
                                                v[i]['出院日期'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[3]/div/div/div/input",
                                             v[i]['原因'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[4]/div/div/div/input",
                                             v[i]['医疗机构及科室名称'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[5]/div/div/div/input",
                                             v[i]['病案号'])
            elif k in [' 家庭病床 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div[1]/div/div/div/input")
                if len(v) == 1:
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[1]/div/div/div/input",
                                            v[0]['建床日期'])
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[2]/div/div/div/input",
                                            v[0]['撤床日期'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[3]/div/div/div/input",
                                         v[0]['原因'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[4]/div/div/div/input",
                                         v[0]['医疗机构及科室名称'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[5]/div/div/div/input",
                                         v[0]['病案号'])
                else:
                    for i in range(len(v) - 1):
                        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div[6]/button")  # 添加
                    for i in range(len(v)):
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k),
                                                ".//div[2]/div/div[" + str(i + 2) + "]/div[1]/div/div/div/input",v[i]['建床日期'])
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k),
                                                ".//div[2]/div/div[" + str(i + 2) + "]/div[2]/div/div/div/input",v[i]['撤床日期'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[3]/div/div/div/input",v[i]['原因'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[4]/div/div/div/input",v[i]['医疗机构及科室名称'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[5]/div/div/div/input",v[i]['病案号'])
            elif k in ['主要用药情况']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/div/input")
                if len(v) == 1:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/div/input",v[0]['药物名称'])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/div/div/div/input",v[0]['途径'])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div/div/div/div/div/input",v[0]['频次'])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[4]/div/div/div/input", v[0]['单次剂量'])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[5]/div/div/div/input",v[0]['剂量单位'])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[6]/div/div/div/input", v[0]['每日剂量'])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[7]/div/div/div/input", v[0]['用药时间'])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[8]/div/div/div/div/div/input",v[0]['服药依从性'])
                else:
                    for i in range(len(v) - 1):
                        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div[9]/button")  # 添加
                    for i in range(len(v)):
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div/div[" + str(i + 2) + "]/div[1]/div/div/div/div/div/input",v[i]['药物名称'])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div/div[" + str(i + 2) + "]/div[2]/div/div/div/div/div/input",v[i]['途径'])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div/div[" + str(i + 2) + "]/div[3]/div/div/div/div/div/input",v[i]['频次'])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[4]/div/div/div/input",v[i]['单次剂量'])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k),
                                                  ".//div[2]/div/div[" + str(i + 2) + "]/div[5]/div/div/div/input", v[i]['剂量单位'])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[6]/div/div/div/input",v[i]['每日剂量'])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[7]/div/div/div/input", v[i]['用药时间'])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div/div[" + str(i + 2) + "]/div[8]/div/div/div/div/div/input",v[i]['服药依从性'])
            elif k in [' 非免疫规划预防接种史 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '主要用药情况'),".//div[4]/div/div[2]/div[1]/div/div/div/div/div/input")
                if len(v) == 1:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, '主要用药情况'),".//div[4]/div/div[2]/div[1]/div/div/div/div/div/input",v[0]['接种名称'])
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, '主要用药情况'),".//div[4]/div/div[2]/div[2]/div/div/div/input", v[0]['接种日期'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, '主要用药情况'), ".//div[4]/div/div[2]/div[3]/div/div/div/input",v[0]['接种机构'])
                else:
                    for i in range(len(v) - 1):
                        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div[1]/div[4]/button")  # 添加
                    for i in range(len(v)):
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, '主要用药情况'),".//div[4]/div/div[" + str(i + 2) + "]/div[1]/div/div/div/div/div/input",v[i]['接种名称'])
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, '主要用药情况'),".//div[4]/div/div[" + str(i + 2) + "]/div[2]/div/div/div/input",v[i]['接种日期'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, '主要用药情况'),".//div[4]/div/div[" + str(i + 2) + "]/div[3]/div/div/div/input",v[i]['接种机构'])

            # //form2
            elif k in ['血常规']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele4, '血红蛋白值 '), ".//div/div/input")
                for k1, v1 in v.items():
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele4, k1), ".//div/div/input", v1)
            elif k in ['尿常规']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele4, '血红蛋白值 '), ".//div/div/input")
                for k1, v1 in v.items():
                    if k1 in ['尿蛋白定性检测结果', '尿糖定性检测结果 ', '尿酮体定性检测结果', '尿潜血定性检测结果', '尿白细胞']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele4, k1), ".//div/div/div/div/input", v1)
                    else:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele4, k1), ".//div/div/input", v1)
            elif k in ['血糖', '肝功能', '肾功能', '血脂']:
                for k1, v1 in v.items():
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele4, k1), ".//div/div/input", v1)
            elif k in ['尿微量白蛋白', '糖化血红蛋白']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele4, k), ".//div[2]/div/div/div/input", v)
            elif k in ['大便潜血']:
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleP(ele4, k, "../.."), ".//div[2]/div/div/div/label", v)
            elif k in ['乙型五项检查']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele4, '乙型肝炎病毒表面抗原检测结果'), ".//div/div/label")
                for k1, v1 in v.items():
                    Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele4, k1), ".//div/div/label", v1)
            elif k in ['心电图', '胸部X线片', 'B超', '宫颈涂片']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon2(ele4, k), ".//div[2]/label")
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele4, k), ".//div[2]/label", list(v.keys())[0])
                if list(v.keys())[0] == '异常':
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele4, k), ".//div[2]/div/textarea", v['异常'])
            elif k in ['其他辅助检查']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele4, k), ".//div[2]/div/textarea", v)

            # 无 form
            elif k in ['健康评价']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='健康评价']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                Web_PO.eleRadioRightLabelByCheck(ele5, ".//div[2]/div[1]/span[1]/label", list(v.keys())[0])
                if list(v.keys())[0] == '有异常':
                    for i in range(len(v['有异常'])):
                        Web_PO.eleClkByX(ele5, ".//div[2]/div[1]/div/button", 2)
                        Web_PO.eleSetTextByX(ele5, ".//div[2]/div[2]/div[1]/div[" + str(i + 1) + "]/div[1]/input", v['有异常'][i])

            elif k in ['健康指导']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='健康指导']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                for i in range(len(v)):
                    if v[i] == '纳入慢性病患者健康管理':
                        Web_PO.eleClkByX(ele5, ".//div[2]/div/div[1]/div/label", 2)
                    elif v[i] == '建议复查':
                        Web_PO.eleClkByX(ele5, ".//div[2]/div/div[2]/label", 2)
                    elif v[i] == '建议转诊':
                        Web_PO.eleClkByX(ele5, ".//div[2]/div/div[3]/label", 2)
            elif k in ['危险因素控制']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='危险因素控制']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                Web_PO.eleCheckboxRightLabel2(ele5, ".//div[2]/div/div[1]/label", v[0])
                if v[1][0] == '减体重':
                    Web_PO.eleClkByX(ele5, ".//div[2]/div/div[2]/label", 2)
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div/div[2]/div/input", v[1][1])
                if v[2][0] == '建议接种疫苗':
                    Web_PO.eleClkByX(ele5, ".//div[2]/div/div[3]/label", 2)
                    Web_PO.eleDropdown(ele5, ".//div[2]/div/div[3]/div/div/div[1]/input",v[2][1])
                if v[3][0] == '其他':
                    Web_PO.eleClkByX(ele5, ".//div[2]/div/div[4]/label", 2)
                    Web_PO.eleSetTextByX(ele5, ".//div[2]/div/div[4]/div/textarea", v[3][1])
            elif k in ['建议']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='建议']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div/textarea", v)
            elif k in ['结果反馈']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='结果反馈']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div[2]/div[1]/span[2]/span/span[2]/span/span[1]/div/input",v['本人'])
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div[2]/div[1]/span[2]/span/span[2]/span/span[3]/div/input",v['家属'])
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div[2]/div[2]/span[2]/span/span[2]/div/input", v['反馈人'])
                Web_PO.eleDropdownDate1(ele5, ".//div[2]/div[2]/div[3]/span[2]/span/span[2]/div/input", v['时间'])
            elif k in ['医生签名']:
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[4]/div[2]/div/div[2]/span[2]/div/input',
                    v['症状'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[6]/div[2]/div/span[2]/div/input',
                    v['一般状况'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[8]/div[2]/div/span[2]/div/input',
                    v['生活方式'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[10]/div[2]/div/span[2]/div/input',
                    v['脏器功能'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[11]/div[2]/div/span[2]/div/input',
                    v['查体'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[12]/div[2]/div/span[2]/div/input',
                    v['皮肤'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[13]/div[2]/div/span[2]/div/input',
                    v['肛门指诊'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[14]/div[2]/div/span[2]/div/input',
                    v['乳腺'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[15]/div[2]/div/span[2]/div/input',
                    v['妇科'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[16]/div[2]/div/span[2]/div/input',
                    v['其他'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[17]/div[2]/div/span[2]/div/input',
                    v[' 现存主要健康问题 '])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[18]/div[2]/div/span[2]/div/input',
                    v['主要用药情况'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[2]/div/div[1]/div[2]/div/span[2]/div/input',
                    v['血常规'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[2]/div/div[2]/div[2]/div/span[2]/div/input',
                    v['尿微量白蛋白'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[2]/div/div[3]/div[2]/div/span[2]/div/input',
                    v['大便潜血'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[1]/div[2]/div/span[2]/div/input',
                    v['心电图'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[2]/div[2]/div/span[2]/div/input',
                    v['胸部X线片'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[3]/div[2]/div/span[2]/div/input',
                    v['B超'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[4]/div[2]/div/span[2]/div/input',
                    v['宫颈涂片'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[5]/div[2]/div/span[2]/div/input',
                    v['其他辅助检查'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[3]/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/span[2]/div/input',
                    v['健康评价'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/span[2]/div/input',
                    v['健康指导'])
        Web_PO.button1('保存')

    def __finalize_record(self, d_):
        # 结案
        ele = Web_PO.getSuperEleByX("//label[text()='结案原因']", "..")
        for k, v in d_['data'].items():
            if k in ["结案原因"]:
                if isinstance(v, dict):
                    Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div/div[1]/label", v, ".//div[2]/input")
                elif isinstance(v, str):
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div/div[1]/label", v)
        Web_PO.button1(' 取消 ')

    def _coronary_patient_registry(self, d_):
        # 冠心病患者登记
        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in ['冠心病诊断', '诊断依据']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/label", v)
            elif k in ['发病日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
            elif k in ['确认日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v)
            elif k in ['登记日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
            elif k in ['开始管理时间']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/input", v)
            elif k in ['确诊医院']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//td[6]/div/div/div/input", v)
            elif k in ['是否首次发病']:
                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[8]/div/label", v)
        # Web_PO.button1('取消')
        Web_PO.button1('保存')

    def _three_Coronary_CHDfiles_operation(self, varOperation, d_option):

        # 获取字段列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        # 获取每行值
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        l_all_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_all_value)
        l_row_group = (List_PO.split2(l_all_value, varOperation))
        for i in l_row_group:
            i.pop(2)
        # print(l_row_group)

        # 获取提醒的颜色列表
        i_tr = Web_PO.eleGetCountByTag(ele2, "tr")
        # print(i_tr)
        l_warn_color = []
        for i in range(i_tr):
            if Web_PO.eleIsEleExistByX(ele2, ".//tr[" + str(i+1) + "]/td[2]/div/div"):
                s_warn = Web_PO.eleGetAttrValueByX(ele2, ".//tr[" + str(i+1) + "]/td[2]/div/div", "style")
                # print(s_warn)
                s_warn_color = s_warn.split("background-color:")[1].split(";")[0]
                s_warn = s_warn_color.strip()
                l_warn_color.append(s_warn)
            else:
                l_warn_color.append('')
        # print(l_warn_color)  # ['red', '', 'red']

        # 将提醒颜色更新到l_group
        for i in range(len(l_row_group)):
            if i < len(l_warn_color):
                l_row_group[i][1] = l_warn_color[i]
        # print(l_row_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_row_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_row_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_Coronary_CHDfiles_operation(self, d_):

        # 冠心病管理 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_Coronary_CHDfiles_operation('访视记录', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '个人专项档案_专项记录_修改':
                Web_PO.button1('修改')
                # 冠心病患者登记
                self._coronary_patient_registry(d_)
            elif d_['operate'] == '个人专项档案_专项记录_结案':
                Web_PO.button1(' 结案 ')
                self.__finalize_record(d_)
            elif d_['operate'] == '个人专项档案_专项记录_删除':
                Web_PO.button1('删除')
                Web_PO.button1('取消')
                # Web_PO.button1('确定')

            elif d_['operate'] == '个人专项档案_评估记录_新增评估':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[2]", 2)
                Web_PO.button1('新增评估')
                ele = Web_PO.getSuperEleByX("//form", ".")
                for k, v in d_['data'].items():
                    if k in ["危险因素控制效果", '非药物治疗效果']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/div/div/input", v)
                    elif k in ['评估医生', '录入人']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/div/div/input", v)
                    elif k in ["药物治疗效果"]:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div/div/input", v)
                    elif k in ['病情转归']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input", v)
                    elif k in ["危险级别转归"]:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['异常详述', '指导意见']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v)
                    elif k in ['评估结果']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['评估日期', '录入日期']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/input", v)
                Web_PO.button1('取消')
                # Web_PO.button1('保存')
            elif d_['operate'] == '个人专项档案_评估记录_结案':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[2]", 2)
                Web_PO.button1('结案')

            elif d_['operate'] == '个人专项档案_随访记录_新增随访':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[3]", 2)
                Web_PO.button1('新增随访')
                ele = Web_PO.getSuperEleByX("//form", ".")
                for k, v in d_['data'].items():
                    if k in ["随访日期", '下次随访时间']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['随访方式']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/label", v)
                    elif k in ['冠心病类型']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['目前症状']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['体征']:
                        for k1, v1 in v.items():
                            if k1 in ['血压']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[6]/td[2]/div/div/div/input", v1[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[6]/td[3]/div/div/div/input", v1[1])
                            if k1 in ['体重']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[6]/td[5]/div/div/div/input", v1)
                            if k1 in ['身高']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[7]/td[2]/div/div/div/input", v1)
                            if k1 in ['空腹血糖']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[8]/td[2]/div/div/div/input", v1)
                            if k1 in ['心率']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[8]/td[4]/div/div/div/input", v1)
                            if k1 in ['其他']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[9]/td[2]/div/div/div/input", v1)
                    elif k in ['生活方式']:
                        for k1, v1 in v.items():
                            if k1 in ['日吸烟量']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[12]/td[2]/div/div/div/input", v1)
                            if k1 in ['日饮酒量']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[12]/td[4]/div/div/div/input", v1)
                            if k1 in [ '运动频率']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[13]/td[2]/div/div/div/input", v1)
                            if k1 in ['每次持续时间']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[13]/td[4]/div/div/div/input", v1)
                            if k1 in ['摄盐量']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//tr[14]/td[2]/div/div/div/label", v1)
                            if k1 in ['心理调整']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//tr[14]/td[4]/div/div/div/label", v1)
                            if k1 in ['遵医行为']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//tr[15]/td[2]/div/div/div/label", v1)
                    elif k in ['服药依从性', '此次随访分类']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['特殊治疗', '非药物治疗措施']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['健康评价']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['医生签名']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input", v)
                    elif k in ['居民（家属）签名']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
                Web_PO.button1("保存")
            elif d_['operate'] == '个人专项档案_随访记录_结案':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[3]", 2)
                Web_PO.button1('结案')

            elif d_['operate'] == '个人专项档案_体检记录_新增体检':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[4]", 2)
                Web_PO.button1('新增体检')
                self.__tjb(d_)

            elif d_['operate'] == '个人专项档案_体检记录_结案':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[4]", 2)
                Web_PO.button1('结案')

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 3.3.1 基本公卫 - 脑卒中患者管理 - 脑卒中登记
    def _stroke_patient_registry(self, d_):
        # 脑卒中登记
        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in ['脑卒中诊断', '诊断依据']:
                Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/div", v)
            elif k in ['诊断分类']:
                Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div", v)
            elif k in ['发病日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
            elif k in ['确认日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v)
            elif k in ['登记日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
            elif k in ['开始管理时间']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/input", v)
            elif k in ['确诊医院']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/input", v)
            elif k in ['是否首次发病']:
                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[8]/div/div/div[1]/div/label", v)
        # Web_PO.button1('取消')
        Web_PO.button1('保存')

    def _three_Stroke_DNTregister_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        # 获取字段和类型字典
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_Stroke_DNTregister_operation(self, d_):

        # 冠心病登记 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_Stroke_DNTregister_operation('新增登记', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '个人专项档案_脑卒中患者登记':
                # 脑卒中患者登记
                self._stroke_patient_registry(d_)

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 3.3.1 基本公卫 - 脑卒中患者管理 - 脑卒中管理

    def _three_Stroke_DNTfiles_operation(self, varOperation, d_option):

        # 获取字段列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        # 获取每行值
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        l_all_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_all_value)
        l_row_group = (List_PO.split2(l_all_value, varOperation))
        for i in l_row_group:
            i.pop(2)
            i.pop(2)
        print(l_row_group)

        # 获取提醒的颜色列表
        i_tr = Web_PO.eleGetCountByTag(ele2, "tr")
        # print(i_tr)
        l_warn_color = []
        for i in range(i_tr):
            if Web_PO.eleIsEleExistByX(ele2, ".//tr[" + str(i+1) + "]/td[3]/div/div/div"):
                s_warn = Web_PO.eleGetAttrValueByX(ele2, ".//tr[" + str(i+1) + "]/td[3]/div/div/div", "style")
                # print(s_warn) # background: rgb(223, 57, 38); width: 16px; height: 16px;
                s_warn_color = s_warn.split("background: ")[1].split(";")[0]
                s_warn = s_warn_color.strip()
                hex_color = self.rgb_to_hex(s_warn)
                # print(hex_color)  # 输出: #df3926
                l_warn_color.append(hex_color)
            else:
                l_warn_color.append('')
        print(l_warn_color)  # ['red', '', 'red']

        # 将提醒颜色更新到l_group
        for i in range(len(l_row_group)):
            if i < len(l_warn_color):
                l_row_group[i][2] = l_warn_color[i]
        print(l_row_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_row_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_row_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_Stroke_DNTfiles_operation(self, d_):

        # 脑卒中管理 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_Stroke_DNTfiles_operation('访视记录', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '个人专项档案_专项记录_修改':
                Web_PO.button1('修改')
                # 冠心病患者登记
                self._coronary_patient_registry(d_)
            elif d_['operate'] == '个人专项档案_专项记录_结案':
                Web_PO.button1(' 结案 ')
                self.__finalize_record(d_)

            elif d_['operate'] == '个人专项档案_评估记录_新增评估':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[2]", 2)
                Web_PO.button1('新增评估')
                ele = Web_PO.getSuperEleByX("//form", ".")
                for k, v in d_['data'].items():
                    if k in ['药物治疗效果','药物依从性', '康复效果评价']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/div/div/input", v)
                    elif k in ["非药物治疗效果", "康复计划执行", "危险因素控制效果"]:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div/div/input", v)
                    elif k in ['评估医生', '录入人']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input", v)
                    elif k in ['危险因素',"调整康复计划"]:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in [ "Rankin评分"]:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['病情转归']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/label", v)
                    elif k in ['脑卒中功能评价', '康复计划调整']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v)
                    elif k in ['评估结果记录','指导建议']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['评估日期']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['录入日期']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[6]/div/div/div/input", v)
                Web_PO.button1('取消')
                # Web_PO.button1('保存')
            elif d_['operate'] == '个人专项档案_评估记录_结案':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[2]", 2)
                Web_PO.button1('结案')

            elif d_['operate'] == '个人专项档案_随访记录_新增随访':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[3]", 2)
                Web_PO.button1('新增随访 ')
                ele = Web_PO.getSuperEleByX("//form", ".")
                for k, v in d_['data'].items():
                    if k in ["随访日期", '下次随访时间']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['随访方式']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/label", v)
                    elif k in ['脑卒中诊断', '脑卒中部位', '个人病史', '脑卒中并发症情况', '新发卒中症状', '康复治疗的方式']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['目前症状']:
                        Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/div", v)
                    elif k in ['药品']:
                        if len(v) > 1:
                            for _ in range(len(v)-1):
                                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div/form/table/tbody/tr[11]/td[10]/div/div', 2)  # +
                        for i in range(len(v)):
                            for k2, v2 in v[i].items():
                                print(v[i])
                                if k2 in ['药品名称1', '药品名称2', '药品名称3', '药品名称4', '药品名称5']:
                                    Web_PO.eleClsReadonlyByX(Web_PO.eleCommon(ele, k2), ".//td[2]/div/div/div/div/div/input", 2)
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k2), ".//td[2]/div/div/div/div/div/input", v2)
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k2), ".//td[2]/div/div/div/div/div/input", v2)
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k2), ".//td[4]/div/div/div/input", v[i]['剂量'])
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k2), ".//td[7]/div/div/div/div/div/input", v[i]['次数'])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k2), ".//td[9]/div/div/div/input", v[i]['已服用时间'])
                    elif k in ['体征']:
                        for k1, v1 in v.items():
                            if k1 in ['身高']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k1), ".//td[2]/div/div/div/input", v1)
                            elif k1 in ['体重']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k1), ".//td[4]/div/div/div/input", v1)
                            elif k1 in ['心率']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k1), ".//td[5]/div/div/div/input", v1)
                            elif k1 in ['血压']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k1), ".//td[2]/div/div/div/input", v1[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k1), ".//td[3]/div/div/div/input", v1[1])
                            elif k1 in ['腰围']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k1), ".//td[5]/div/div/div/input", v1)
                            elif k1 in ['其他']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//tr[24]/td[2]/div/div/div/input", v1)
                    elif k in ['生活方式']:
                        for k1, v1 in v.items():
                            if k1 in ['日吸烟量', '运动频率']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k1), ".//td[2]/div/div/div/input", v1)
                            elif k1 in ['日饮酒量', '每次持续时间']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k1), ".//td[4]/div/div/div/input", v1)
                            elif k1 in ['摄盐量', '遵医行为']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//td[2]/div/div/div/label", v1)
                            elif k1 in ['心理调整']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//td[4]/div/div/div/label", v1)
                    elif k in ['用药情况', '服药依从性', '肢体功能恢复情况']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['生活是否自理', '此次随访分类']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/label", v)
                    elif k in ['其他新发卒中症状']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['健康评价']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['医生签名']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input", v)
                    elif k in ['居民(家属)签名']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/input", v)
                Web_PO.button1("保存")
            elif d_['operate'] == '个人专项档案_随访记录_结案':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[3]", 2)
                Web_PO.button1('结案')

            elif d_['operate'] == '个人专项档案_体检记录_新增体检':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[4]", 2)
                Web_PO.button1('新增体检')
                self.__tjb(d_)
            elif d_['operate'] == '个人专项档案_体检记录_结案':
                Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[4]", 2)
                Web_PO.button1('结案')

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))




    # todo 3.4.1 基本公卫 - 高血脂管理 - 高血脂登记

    def _three_Hyperlipidemia_gxzregister_operation(self, varOperation, d_option):

        # 获取字段列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        # 获取每行值
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        l_all_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_all_value)
        l_row_group = (List_PO.split2(l_all_value, varOperation))
        for i in l_row_group:
            i.pop(2)
            i.pop(2)
        print(l_row_group)

        # 获取提醒的颜色列表
        i_tr = Web_PO.eleGetCountByTag(ele2, "tr")
        # print(i_tr)
        l_warn_color = []
        for i in range(i_tr):
            if Web_PO.eleIsEleExistByX(ele2, ".//tr[" + str(i+1) + "]/td[3]/div/div/div"):
                s_warn = Web_PO.eleGetAttrValueByX(ele2, ".//tr[" + str(i+1) + "]/td[3]/div/div/div", "style")
                # print(s_warn) # background: rgb(223, 57, 38); width: 16px; height: 16px;
                s_warn_color = s_warn.split("background: ")[1].split(";")[0]
                s_warn = s_warn_color.strip()
                hex_color = self.rgb_to_hex(s_warn)
                # print(hex_color)  # 输出: #df3926
                l_warn_color.append(hex_color)
            else:
                l_warn_color.append('')
        print(l_warn_color)  # ['red', '', 'red']

        # 将提醒颜色更新到l_group
        for i in range(len(l_row_group)):
            if i < len(l_warn_color):
                l_row_group[i][2] = l_warn_color[i]
        print(l_row_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_row_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_row_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_Hyperlipidemia_gxzregister_operation(self, d_):

        # 高血脂登记 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_Hyperlipidemia_gxzregister_operation('登记', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '高血脂患者管理卡_修改':
                # Web_PO.button1('修改')
                # self._coronary_patient_registry(d_)
                ele = Web_PO.getSuperEleByX("//form", ".")
                for k, v in d_['data'].items():
                    if k in ['病例来源', '高血脂分层结果']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['居住地址']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[2]/div/div/div/div/div/input", v[0])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[3]/div/div/div/div/div/input", v[1])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[4]/div/div/div/div/div/input", v[2])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[5]/div/div/div/div/div/input", v[3])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[6]/div/div/div/div/div/input", v[4])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k),".//td[7]/div/div/div/input", v[5])
                    elif k in ['确诊日期']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['建卡时间']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['建卡医生']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['开始管理时间']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input", v)
                    elif k in ['是否终止管理']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/label[2]", v[0])
                        if v[0] == '是':
                            Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[6]/div/div/div/input", v[1]['终止管理日期'])

                Web_PO.button1('取消')
                # Web_PO.button1('保存')

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 3.4.2 基本公卫 - 高血脂管理 - 高血脂专项

    def _three_Hyperlipidemia_gxzspecial_operation(self, varOperation, d_option):

        # 获取字段列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        # 获取每行值
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        l_all_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_all_value)
        l_row_group = (List_PO.split2(l_all_value, varOperation))
        for i in l_row_group:
            i.pop(2)
            i.pop(2)
        print(l_row_group)

        # 获取提醒的颜色列表
        i_tr = Web_PO.eleGetCountByTag(ele2, "tr")
        # print(i_tr)
        l_warn_color = []
        for i in range(i_tr):
            if Web_PO.eleIsEleExistByX(ele2, ".//tr[" + str(i+1) + "]/td[3]/div/div/div"):
                s_warn = Web_PO.eleGetAttrValueByX(ele2, ".//tr[" + str(i+1) + "]/td[3]/div/div/div", "style")
                # print(s_warn) # background: rgb(223, 57, 38); width: 16px; height: 16px;
                s_warn_color = s_warn.split("background: ")[1].split(";")[0]
                s_warn = s_warn_color.strip()
                hex_color = self.rgb_to_hex(s_warn)
                # print(hex_color)  # 输出: #df3926
                l_warn_color.append(hex_color)
            else:
                l_warn_color.append('')
        print(l_warn_color)  # ['red', '', 'red']

        # 将提醒颜色更新到l_group
        for i in range(len(l_row_group)):
            if i < len(l_warn_color):
                l_row_group[i][2] = l_warn_color[i]
        print(l_row_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_row_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_row_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_Hyperlipidemia_gxzspecial_operation(self, d_):

        # 高血脂专项 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_Hyperlipidemia_gxzspecial_operation('查看\n随访', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '高血脂患者管理卡_编辑':
                Web_PO.button1('编辑')
                ele = Web_PO.getSuperEleByX("//form", ".")
                for k, v in d_['data'].items():
                    if k in ['病例来源']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['高血脂分层结果']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['居住地址']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[2]/div/div/div/div/div/input", v[0])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[3]/div/div/div/div/div/input", v[1])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[4]/div/div/div/div/div/input", v[2])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[5]/div/div/div/div/div/input", v[3])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),".//td[6]/div/div/div/div/div/input", v[4])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k),".//td[7]/div/div/div/input", v[5])
                    elif k in ['确诊日期']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['建卡时间']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['建卡医生']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input", v)
                    elif k in ['是否终止管理']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/label[2]", v[0])
                        if v[0] == '是':
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/input", v[1]['终止管理日期'])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, '终止管理原因'), ".//td[2]/div/div/div/input", v[1]['终止管理原因'])

                Web_PO.button1('取消')
                # Web_PO.button1('保存')

            elif d_['operate'] == '高血脂患者管理卡_新增':
                Web_PO.button1('修改')
                # self._coronary_patient_registry(d_)

            elif d_['operate'] == '高血脂随访记录_新增':
                Web_PO.button1('新增')
                Web_PO.button1('保存')

            elif d_['operate'] == '高血脂随访记录_引入上次新增':
                Web_PO.button1('引入上次新增')
                Web_PO.button1('保存')


            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))


    # todo 3.4.3 基本公卫 - 高血脂管理 - 高血脂随访

    def _three_Hyperlipidemia_gxzsvisit_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        # 获取字段和类型字典
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def three_Hyperlipidemia_gxzsvisit_operation(self, d_):

        # 高血脂随访 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._three_Hyperlipidemia_gxzsvisit_operation('详情', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '高血脂随访记录':
                # self._stroke_patient_registry(d_)
                ...

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 4.1.2 基本公卫 - 家医签约 - 已签约居民

    def __jmqy(self, d_):
        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in ['居民姓名', '家庭住址']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)
            elif k in ['手机号']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
            elif k in ['居民基本情况']:
                Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div", v)
            elif k in ['签约类型']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in ['服务包选择']:
                Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div", v)
            elif k in ['签约团队']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/div/div/input", v)
            elif k in ['签约医生']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div/input", v)
            elif k in ['公共卫生人员']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div/input", v)
            elif k in ['家庭(责任)护士']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/div/div/input", v)
            elif k in ['签约日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)
            elif k in ['生效日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
            elif k in ['监护人姓名']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
            elif k in ['与乙方关系']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
            elif k in ['联系电话']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/input", v)
            elif k in ['身份证号']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, '监护人姓名'), ".//div[2]/div/div[7]/div/div/div/input", v)
        # Web_PO.button1('关闭')
        Web_PO.button1('保存')

    def _sign_jmsign_signed_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        # 获取字段和类型字典
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def sign_jmsign_signed_operation(self, d_):

        # 已签约居民 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._sign_jmsign_signed_operation('更新签约\n解约\n历史记录', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '更新居民签约':
                self.__jmqy(d_)

            elif d_['operate'] == '解约':
                ele = Web_PO.getSuperEleByX("//div[text()='申请日期']", "../../..")
                for k, v in d_['data'].items():
                    if k in ['申请日期']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v)
                    if k in ['解约原因']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v)
                # Web_PO.button1('提 交')
                Web_PO.button1('关 闭')

            elif d_['operate'] == '历史记录':
                Web_PO.button1('关 闭')

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))


    # todo 4.1.3 基本公卫 - 家医签约 - 履约服务

    def _sign_jmsign_qyservice_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        # 获取字段和类型字典
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def sign_jmsign_qyservice_operation(self, d_):

        # 履约服务 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._sign_jmsign_signed_operation('查看\n履约', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '查看':
                Web_PO.button1('关 闭')

            elif d_['operate'] == '履约':
                Web_PO.button1('取消')

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))


    # todo 4.1.4 基本公卫 - 家医签约 - 归档记录

    def _sign_jmsign_qyfile_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        # 获取字段和类型字典
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def sign_jmsign_qyfile_operation(self, d_):

        # 归档记录 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._sign_jmsign_qyfile_operation('查看', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '查看':
                Web_PO.button1('关 闭')

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 4.1.6 基本公卫 - 家医签约 - 档案未签约

    def _sign_jmsign_ready_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        # 获取字段和类型字典
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def sign_jmsign_ready_operation(self, d_):

        # 档案未签约 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._sign_jmsign_ready_operation('新增签约', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)


            elif d_['operate'] == '签约登记':
                Web_PO.button1('签约登记')
                ele = Web_PO.getSuperEleByX("//form", ".")
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, '身份证号'), ".//div[2]/div/div/div[1]/input", d_['data']['身份证号'])
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, '性别'), ".//div[6]/div/div/div/div/div/input", d_['data']['性别'])
                self.__jmqy(d_)

            elif d_['operate'] == '新增居民签约':
                self.__jmqy(d_)

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))

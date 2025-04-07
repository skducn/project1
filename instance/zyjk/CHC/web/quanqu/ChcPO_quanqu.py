# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-7-25
# Description:
# https://chromedriver.storage.googleapis.com/index.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PO.WebPO import *
Web_PO = WebPO("chrome")

from PO.CaptchaPO import *
Captcha_PO = CaptchaPO()

from PO.Base64PO import *
Base64_PO = Base64PO()

from PO.ListPO import *
List_PO = ListPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.DataPO import *
Data_PO = DataPO()

from PO.SysPO import *
Sys_PO = SysPO()

from PO.HttpPO import *
Http_PO = HttpPO()

from bs4 import BeautifulSoup
import logging, os
import signal
import ddddocr

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 上层 目录的绝对路径
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将 上层 目录添加到 sys.path
sys.path.insert(0, project_dir)

from ConfigparserPO import *

class ChcPO_quanqu():

    def __init__(self, varFile, varMenu, varCookies='cookies.json'):

        # 配置日志
        if os.name == 'nt':
            logging.basicConfig(filename=varFile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
        else:
            logging.basicConfig(filename=varFile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        # print(varFile, datetime.datetime.now())


        Configparser_PO = ConfigparserPO('config.ini')

        # 登录
        self.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"),
                          Configparser_PO.ACCOUNT("password"))

        # 保存当前会话的 Cookies 到文件
        cookies = Web_PO.driver.get_cookies()
        # with open("cookies.json", 'w') as f:
        with open(varCookies, 'w') as f:
            json.dump(cookies, f)


        # 菜单
        d_menu = {'首页': 'http://192.168.0.243:8010/#/index', '健康服务': 'http://192.168.0.243:8010/#/SignManage/service',
                  '健康评估及干预': 'http://192.168.0.243:8010/#/SignManage/signAssess',
                  '慢病管理': 'http://192.168.0.243:8010/#/SignManage/chronic',
                  '老年人体检': 'http://192.168.0.243:8010/#/SignManage/snrExam',
                  '重点人群': 'http://192.168.0.243:8010/#/SignManage/keyPopulation',
                  '居民登记': 'http://192.168.0.243:8010/#/OpManage/register',
                  '健康评估': 'http://192.168.0.243:8010/#/OpManage/assess',
                  '机构维护': 'http://192.168.0.243:8010/#/UserManage/org',
                  '用户维护': 'http://192.168.0.243:8010/#/UserManage/user',
                  '角色维护': 'http://192.168.0.243:8010/#/UserManage/role',
                  '接口管理': 'http://192.168.0.243:8010/#/UserManage/interface',
                  '批量评估': 'http://192.168.0.243:8010/#/UserManage/MassAppraisal',
                  '错误日志': 'http://192.168.0.243:8010/#/UserManage/errorLog',
                  '报告模板引用': 'http://192.168.0.243:8010/#/UserManage/templateReference',
                  '报告模板管理': 'http://192.168.0.243:8010/#/UserManage/templateManage',
                  '常住人口': 'http://192.168.0.243:8010/#/Community/permanent',
                  '家医团队维护': 'http://192.168.0.243:8010/#/Community/team',
                  '家医助手': 'http://192.168.0.243:8010/#/Community/assistant',
                  '干预规则配置': 'http://192.168.0.243:8010/#/Community/interveneRule',
                  '打印': 'http://192.168.0.243:8010/#/Community/print',
                  '停止评估名单': 'http://192.168.0.243:8010/#/Community/stopList',
                  '社区用户维护': 'http://192.168.0.243:8010/#/Community/communityUser',
                  '评估建议': 'http://192.168.0.243:8010/#/Community/SuggestionTemplate',
                  '定时任务': 'http://192.168.0.243:8010/#/monitor/index',
                  '社区健康评估': 'http://192.168.0.243:8010/#/dataStatistics/communityHealth',
                  '全区健康评估': 'http://192.168.0.243:8010/#/dataStatistics/allHealth',
                  '全区评估率': 'http://192.168.0.243:8010/#/dataStatistics/allAssessRate',
                  '社区评估率': 'http://192.168.0.243:8010/#/dataStatistics/communityAssessRate',
                  '档案首页': 'http://192.168.0.243:8010/#/HealthRecord/archiveIndex',
                  '居民评估报告': 'http://192.168.0.243:8010/#/HealthManage/AssessReport'}


        Web_PO.opnLabel(d_menu[varMenu])
        Web_PO.swhLabel(1)

    def __handle_signal(self, signum, frame):
        # 定义信号处理函数
        self.logger.info('Received signal: {}'.format(signal.Signals(signum).name))
        self.logger.info('Program is terminating...')
        # 在这里可以添加额外的清理代码或日志记录


    def clsApp(self, varApp):
        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()

    def login(self, varUrl, varUser, varPass):
        # 登录
        Web_PO.openURL(varUrl)
        Web_PO.driver.maximize_window()  # 全屏
        # Web_PO.setTextByX("//input[@placeholder='请输入用户名']", varUser)
        # Web_PO.setTextByX("//input[@placeholder='输入密码']", varPass)
        # Web_PO.clkByX("//button[@type='button']", 2)

        Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", varUser)
        Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", varPass)
        Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", "1")
        Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 3)

        # d_ = Web_PO.getValueXpathByLabel("input", "placeholder")
        # Web_PO.setTextByX(d_['请输入用户名'], varUser)
        # Web_PO.setTextByX(d_['输入密码'], varPass)
        # d_ = Web_PO.getTextXpathByLabel("button", "/span")
        # Web_PO.clkByX(d_['登录'], 2)

        # 系统接口404
        # l_ = Web_PO.getTextByXs("//div")
        # if '系统接口404异常' in l_:
        #     print('系统接口404异常')
        #     self.logger.error('系统接口404异常')
        #     Web_PO.cls()
        #     sys.exit(0)

    def getMenu2Url(self):

        # 获取菜单链接
        c = Web_PO.getCountByTag("ul")

        # 获取二级菜单名
        Web_PO.clsDisplayByTagName("ul", c)  # 展开所有二级菜单（去掉display：none）
        l_menu2 = Web_PO.getTextByXs("//ul/div/a/li/div/span")
        # print(l_menu2)  # ['健康档案概况', '个人健康档案', '家庭健康档案', ...
        # print(len(l_menu2))

        # 获取二级菜单链接
        l_menu2Url = Web_PO.getAttrValueByXs("//a", "href")
        # print(l_menu2Url) # ['http://192.168.0.203:30080/#/phs/HealthRecord/ehrindex', 'http://192.168.0.203:30080/#/phs/HealthRecord/Personal', ...
        l_menu2Url.pop(0)
        # print(len(l_menu2Url))
        # 生成字典{菜单：URL}
        d_menuUrl = dict(zip(l_menu2, l_menu2Url))
        # print(d_menuUrl)  # {'健康档案概况': 'http://192.168.0.203:30080/#/phs/HealthRecord/ehrindex',...
        return d_menuUrl


        # # 居民健康服务 - 健康评估及干预
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[1]/div/ul/div[2]/li", 2)
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[1]/div/ul/div[2]/li/ul/div[2]/a/li", 2)
        #
        # # # 人群分类
        # # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[3]/div/div/div/div/div/input", 2)
        # # # 老年人
        # # self.Web_PO.clkByX("/html/body/div[2]/div[2]/div/div/div[1]/ul/li[4]", 2)
        # #
        # # # 家庭医生
        # # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input",2)
        # # self.Web_PO.clkByX("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[1]")
        # #
        # # # 本年度上传情况
        # # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input", 2)
        # # self.Web_PO.clkByX("/html/body/div[2]/div[12]/div/div/div[1]/ul/li[1]", 2)
        # #
        # #
        # # # 查询
        # # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[2]/div/button")
        #
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input", 1, 5)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input", 2, 5)
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input", 3, 5)

        # 每次点击列表第一条
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[12]/div/button",2)

        # /html/body/div[1]/div/div[2]/section/div/div/main/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[12]/div/button
        # /html/body/div[1]/div/div[2]/section/div/div/main/div[2]/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr[2]/td[12]/div/button


        # for i in range(10):
        #     dataURI = Web_PO.getAttrValueByX(u"//img[@class='login-code-img']", "src")  # getValueByAttr
        #     imgFile = Base64_PO.base64ToImg(dataURI)
        #     captcha = Captcha_PO.getCaptchaByDdddOcr(imgFile)
        #     File_PO.removeFile('', imgFile)
        #     # print(captcha)
        #     Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", captcha)
        #     Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)
        #     if Web_PO.isBooleanByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button") == False:
        #         break



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
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['人群分类', '家庭医生', '年度评估状态', '重点人群', '本年度上传情况', '已点击上传']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['上次服务日期', '签约日期范围', '最近一次评估日期', '最近一次确认日期']:
                    self.__setData2(ele, k, v)
                elif k in ['年龄', '登记时年龄']:
                    self.__setAge2(ele, k, v)
                if k in ['现住址']:
                    self.__setAddress3(ele, k, v)

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.button1('查询 ')

        # 日志
        self.logger.info("查询 => " + str(d_))



    # todo 2.1 居民健康服务 - 健康服务

    def _signManage_service_operation(self, varOperation, d_option):

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
    def signManage_service_operation(self, d_):

        # 健康服务 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._signManage_service_operation('服务记录\n新增服务', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '服务记录':
                Web_PO.button1('关闭')

            elif d_['operate'] == '新增服务':
                ele = Web_PO.getSuperEleByX("(//form)[last()]", ".")
                for k, v in d_['data'].items():
                    if k in ['服务时间']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)
                    elif k in ['服务形式']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div/div/div/input", v)
                    elif k in ['服务内容']:
                        Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div/div[1]/label", v, './/div/div[2]/div/div/input')
                Web_PO.button1('取消')
                # Web_PO.button1('确认')

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))


    # todo 2.1 居民健康服务 - 健康评估及干预

    def _signManage_signAssess_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '三高分类', '性别', '身份证号', '年龄', '联系电话', '评估日期', '评估结果', '随访人', '评估机构', '操作']

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")

        # 获取字段和类型字典
        l_group = (List_PO.split2(l_value, varOperation))
        # print(l_group)

        for i in l_group:
            if "\n" in i[5]:
                t = len(i[5].split("\n"))
                # print(t)
                for j in range(t + 1):
                    i.pop(6)
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
    def signManage_signAssess_operation(self, d_):

        # 健康评估及干预 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele2 = Web_PO.getSuperEleByX("//main", ".")
                ele3 = Web_PO.eleGetSuperEleByX(ele2, "(.//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._signManage_signAssess_operation('健康评估', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '健康评估之新增评估':
                Web_PO.button1('新增评估')
                Web_PO.button1('确认')

            elif d_['operate'] == '健康评估之重现评估':
                Web_PO.button1('重现评估')

            elif d_['operate'] == '健康评估之删除评估':
                Web_PO.button1('删除评估')
                Web_PO.button1('确认')

            else:
                print("error, 请检查函数名是否正确、operate是否存在!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))











    def clkMenu(self, html_source, varMenuName, t=2):
        """点击菜单"""
        # 1, 获取html_source
        soup = BeautifulSoup(html_source, 'html.parser')

        # 2, 获取菜单和链接，所有a标签的href属性
        d_menuUrl = {}
        for link in soup.find_all('a'):
            key = str(soup.find("a", {'href': link.get('href')}).find_all('span'))
            if key != "[]" and '<span class="menu-title" title="' in key:
                s = BeautifulSoup(key, 'lxml')
                tag = s.span
                # print(tag.get_text())
                d_menuUrl[tag.get_text()] = link.get('href')
        # print(d_menuUrl)  # {'首页': '#/index', '健康服务': '#/SignManage/service', '健康评估及干预': '#/SignManage/signAssess', '慢病管理': '#/SignManage/chronic', '老年人体检': '#/SignManage/snrExam', '重点人群': '#/SignManage/keyPopulation', '居民登记': '#/OpManage/register', '健康评估': '#/OpManage/assess', '机构维护': '#/UserManage/org', '用户维护': '#/UserManage/user', '角色维护': '#/UserManage/role', '接口管理': '#/UserManage/interface', '批量评估': '#/UserManage/MassAppraisal', '错误日志': '#/UserManage/errorLog', '常住人口': '#/Community/permanent', '家医团队维护': '#/Community/team', '家医助手': '#/Community/assistant', '干预规则配置': '#/Community/interveneRule', '停止评估名单': '#/Community/stopList', '社区用户维护': '#/Community/communityUser', '评估建议': '#/Community/SuggestionTemplate', '定时任务': '#/monitor/index', '社区健康评估': '#/dataStatistics/communityHealth', '全区健康评估': '#/dataStatistics/allHealth'}

        for k,v in d_menuUrl.items():
            if k == varMenuName:
                # print("http://192.168.0.243:8010/" + d_menuUrl[varMenuName])
                Web_PO.opn(self.varUrl + d_menuUrl[varMenuName])
        sleep(t)

    def getTechnicalTarget(self):
        """首页，获取首页指标"""
        l1 = Web_PO.getTextListByX("//div[@class='headerdiv']")
        l2 = Web_PO.getTextListByX("//div[@class='box_center']")

        # 签约居民总数（人）
        qyjmzs = l1[0].split("\n")
        print(qyjmzs)

        # 重点人群
        zdrq = l1[1].split("\n")
        print(zdrq)

        # 疾病风险人群\普通人群
        jbfx = l1[2].split("\n")
        print(jbfx)

        # 健康档案完善
        jkdaws = l2[0].split("\n")
        print(jkdaws)

        # 慢病随访
        mbsf = l2[1].split("\n")
        print(mbsf)

        # 老年人体检
        lnrtj = l2[2].split("\n")
        print(lnrtj)

        # 65岁以上重点人群管理
        zdrqgl = l2[3].split("\n")
        print(zdrqgl)

    def _dropDownList(self, varValue, varXpath):
        """下拉框定义"""
        Web_PO.clsReadonlyByX(varXpath)
        Web_PO.setTextByX(varXpath, varValue)

    def healthEvaluateIntervene_search(self, d):
        """健康评估及干预 - 查询"""
        #({'姓名': '儿童', '身份证': '310101', '人群分类': '老年人', '家庭医生': '测试', '签约日期范围start': '2024-05-05',
                           # '签约日期范围end': '2024-05-07', '年度评估状态': '未评估', '管理人群': '高血压', '最近一次评估日期start': '2024-05-05',
                           # '最近一次评估日期end': '2024-05-07', '最近一次确认日期start': '2024-05-05', '最近一次确认日期end': '2024-05-07'})

        if '姓名' in d: Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[1]/div/div/div/input", d['姓名'])
        if '身份证' in d: Web_PO.setTextByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[2]/div/div/div/input", d['身份证'])
        if '人群分类' in d: self._dropDownList(d['人群分类'], "/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[3]/div/div/div/div/div/input")
        if '家庭医生' in d: self._dropDownList(d['家庭医生'], "/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input")
        if '签约日期范围start' in d: Web_PO.setTextEnterByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[5]/div/div/div[1]/input", d['签约日期范围start'])
        if '签约日期范围end' in d: Web_PO.setTextEnterByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[5]/div/div/div[2]/input", d['签约日期范围end'])
        if '年度评估状态' in d: self._dropDownList(d['年度评估状态'], "/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[2]/div[1]/div/div/div/div/div/input")
        if '管理人群' in d: self._dropDownList(d['管理人群'], "/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[2]/div[2]/div/div/div/div/div[2]/input")
        if '最近一次评估日期start' in d: Web_PO.setTextEnterByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[2]/div[3]/div/div/div[1]/input", d['最近一次评估日期start'])
        if '最近一次评估日期end' in d: Web_PO.setTextEnterByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[2]/div[3]/div/div/div[2]/input", d['最近一次评估日期end'])
        if '最近一次确认日期start' in d: Web_PO.setTextEnterByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[2]/div[4]/div/div/div[1]/input", d['最近一次确认日期start'])
        if '最近一次确认日期end' in d: Web_PO.setTextEnterByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[2]/div[4]/div/div/div[2]/input", d['最近一次确认日期end'])

        # 查询
        Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div/div/button")
    def edtBasicInfo(self, idCard):
        # 2，通过身份证打开用户页
        Web_PO.opnLabel('http://172.16.209.10:9071/cdc/a/doctor/archive/detail?personcard=' + str(idCard))
        Web_PO.setTextById('one2', 1)  # 基本信息

        # todo 基本信息

        # {'姓名': '魏梅娣', '民族': '苗族', '文化程度': '小学教育', '职业': '军人', '就业状态': '其他',
        #  '婚姻状况': '离婚', '工作单位': '北京科美有限公司', '手机号': '13011234567', '固定电话': '58776543', '联系人姓名': '魏梅名', '联系人电话': '13356789098',
        #  '血型': 'B型', 'Rh血型': '不详', '医疗费用支付方式': '全自费'}

        # # 姓名
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[1]/td[2]/span/span/input', '魏梅娣')
        # 民族
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[2]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[2]/span/span/input', '苗族')
        # 文化程度
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[4]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[3]/td[4]/span/span/input', '小学教育')
        # 职业
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[4]/td[2]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[4]/td[2]/span/span/input', '军人')
        # 就业状态
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[5]/td[2]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[5]/td[2]/span/span/input', '其他')
        # 婚姻状况
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[2]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[2]/span/span/input', '离婚')
        # 工作单位
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[7]/td[4]/span/span/input', '北京科美有限公司')
        # 手机号
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[8]/td[2]/span/span/input', '13011234567')
        # 固定电话
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[9]/td[2]/span/span/input', '58776543')
        # 联系人姓名
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[10]/td[2]/span/span/input', '魏梅名')
        # 联系人电话
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[10]/td[4]/span/span/input', '13356789098')
        # 血型
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[2]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[2]/span/span/input', 'B型')
        # Rh血型
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[4]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[11]/td[4]/span/span/input', '不详')
        # 医疗费用支付方式
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[12]/td[2]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[12]/td[2]/span/span/input', '全自费')
 
        # 残疾情况
        varStatus = True
        var = {"视力残疾": "2222", "语言残疾": "3333", "其他残疾": "121212"}
        currStatus = Web_PO.isSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]/span/input')  # 无残疾是否勾选
        # cj1,默认无残疾，要求无残疾，不操作
        if currStatus == True:
            if varStatus == True:
                ...
            else:
                # cj2,默认无残疾，要求视力残疾，翻勾选无，勾选视力残疾。
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
                # 遍历勾选
                for k, v in var.items():
                    if k == '视力残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '听力残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '语言残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '肢体残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input',1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '智力残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[6]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '精神残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[7]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '其他残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[4]/span/span/input', v)  # 残疾说明
        if currStatus == False:
            # cj3,默认视力残疾，要求无残疾，勾选无残疾。
            if varStatus == False:
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[1]', 1)  # 无
            # cj4，默认视力残疾，要求精神残疾，操作取消所有勾选，勾选精神残疾。
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input')  # 视力残疾
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input')  # 听力残疾
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input')  # 语言残疾
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input')  # 肢体残疾
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[1]/span/input')  # 智力残疾
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[2]/span/input')  # 精神残疾
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]/span/input')  # 其他残疾

                # 遍历勾选
                for k, v in var.items():
                    if k == '视力残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '听力残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '语言残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '肢体残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[5]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '智力残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[6]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '精神残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[1]/td[7]/span/input', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[4]/span/span/input', v)  # 残疾证号码
                    if k == '其他残疾':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[3]', 1)
                        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/table/tbody/tr[13]/td[2]/table/tbody/tr[2]/td[4]/span/span/input', v)  # 残疾说明

        # todo 户籍地址
        # {'省（自治区、直辖市）': '北京市', '市（地区/州）': '市辖区', '县（区）': '丰台区', '街道（镇）': '南苑街道办事处', '居委（村）': '机场社区居委会', '详细地址': '洪都拉斯100号'}
        var = ['北京市', '市辖区', '丰台区', '南苑街道办事处', '机场社区居委会', '洪都拉斯100号']
        # 省（自治区、直辖市）
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[2]/span/span/input', var[0])
        # 市（地区/州）
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[4]/span/span/input', var[1])
        # 县（区）
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[1]/td[6]/span/span/input', var[2])
        # 街道（镇）
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[2]/span/span/input', var[3])
        # 居委（村）
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[2]/td[4]/span/span/input', var[4])
        # 详细地址
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[1]/tr[3]/td[2]/span/span/input', var[5])

        # todo 居住地址
        # 同户籍地址
        # {'省（自治区、直辖市）': '北京市', '市（地区/州）': '市辖区', '县（区）': '丰台区', '街道（镇）': '南苑街道办事处', '居委（村）': '机场社区居委会', '详细地址': '洪都拉斯100号'}

        varStatus = True
        var = ['北京市', '市辖区', '丰台区', '南苑街道办事处', '机场社区居委会', '洪都拉斯100号']
        currStatus = Web_PO.isSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input')
        if currStatus == True:
            # cj1, 默认是勾选同户籍地址，要求也是勾选同户籍地址，不操作
            if varStatus == True:
                ...
            else:
                # cj2，默认是勾选同户籍地址，要求不勾选同户籍地址，操作反勾选同户籍地址，同时填入一下信息
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input', 1)  # 不勾选同户籍地址
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]/span/span/input', var[0])  # 省（自治区、直辖市）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[4]/span/span/input', var[1])  # 市（地区/州）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[6]/span/span/input', var[2])  # 县（区）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]/span/span/input', var[3])  # 街道（镇）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[4]/span/span/input', var[4])  # 居委（村）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]/span/span/input', var[5])  # 详细地址
        else:
            # cj3，默认是不勾选同户籍地址，要求勾选同户籍地址
            if varStatus == True:
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/thead[3]/tr/th/span/input', 1)
            else:
                # cj4,默认是不勾选同户籍地址，要求更新以下信息。
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[2]/span/span/input', var[0])   # 省（自治区、直辖市）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[4]/span/span/input', var[1])  # 市（地区/州）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[1]/td[6]/span/span/input', var[2])  # 县（区）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[2]/span/span/input', var[3])  # 街道（镇）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[2]/td[4]/span/span/input', var[4])  # 居委（村）
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[2]/tr[3]/td[2]/span/span/input', var[5])  # 详细地址


        # todo 其他信息
        # {'家庭厨房排风设施标识': '烟囱', '家庭燃料类别': '煤', '家庭饮用水类别': '井水', '家庭厕所类别': '马桶', '家庭禽畜栏类别': '室内'}

        # 家庭厨房排风设施标识
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[2]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[2]/span/span/input', '烟囱')
        # 家庭燃料类别
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[4]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[4]/span/span/input', '煤')
        # 家庭饮用水类别
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[6]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[1]/td[6]/span/span/input', '井水')
        # 家庭厕所类别
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[2]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[2]/span/span/input',' 马桶')
        # 家庭禽畜栏类别
        Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[4]/span/span/input')
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[2]/td[4]/span/span/input', '室内')

        # # 药物过敏史
        varStatus = '有'
        var = ['头孢类抗生素', '酒精', {"其他药物过敏原": '3333'}]
        # 判断默认勾选的是无还是有
        currStatus = Web_PO.getAttrValueByX(u'//div[@id="signAllergy"]/table/tbody/tr/td/div/div[1]', '类与实例')
        if currStatus == "mini-radiobuttonlist-item":
            currStatus = '无'
        else:
            currStatus = '有'
        if currStatus == '无':
            # cj1,默认无，要求无，不操作
            if varStatus == '无':
                ...
            else:
                # cj2，默认无，要求有，勾选有，勾选酒精
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)
                for i in range(len(var)):
                    if var[i] == '青霉素抗生素':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[1]/input', 1)
                    if var[i] == '磺胺类抗生素':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[2]/input', 1)
                    if var[i] == '头孢类抗生素':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[3]/input', 1)
                    if var[i] == '含碘药品':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[1]/input', 1)
                    if var[i] == '酒精':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[2]/input', 1)
                    if var[i] =='镇静麻醉剂':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[3]/input', 1)
                    if isinstance(var[i], dict) == True:
                        for k1, v1 in var[i].items():
                            if k1 == '其他药物过敏原':
                                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[4]/input', 1)
                                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[5]/span/input', v1)
        else:
            # cj3,默认有，要求无，勾选无
            if varStatus == '无':
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)
            else:
                # cj4，默认有，取消所有复选框，勾选酒精
                for i in range(1, 3):
                    Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[' + str(i) + ']/input')
                for i in range(1, 4):
                    Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[' + str(i) + ']/input')
                for i in range(len(var)):
                    if var[i] == '青霉素抗生素':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[1]/input', 1)
                    if var[i] == '磺胺类抗生素':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[2]/input', 1)
                    if var[i] == '头孢类抗生素':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[1]/span[3]/input', 1)
                    if var[i] == '含碘药品':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[1]/input', 1)
                    if var[i] == '酒精':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[2]/input', 1)
                    if var[i] =='镇静麻醉剂':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[3]/input', 1)
                    if isinstance(var[i], dict) == True:
                        for k1, v1 in var[i].items():
                            if k1 == '其他药物过敏原':
                                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[4]/input', 1)
                                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[3]/td[2]/table/tbody/tr/td[2]/div[2]/span[5]/span/input', v1)


        # 环境危险因素暴露类别
        varStatus = False
        var = ['毒物', '化学品', {'其他': "11111"}]

        # 判断是否勾选了无
        currStatus = Web_PO.isSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input')
        if currStatus == True:
            # cj1,默认勾选无，要求勾选无，不操作。
            if varStatus == True:
                ...
            # cj2，默认勾选无，要求勾选其他，操作取消无勾选，勾选其他
            elif varStatus == False:
                # 取消无勾选
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)
                for i in range(len(var)):
                    if var[i] == '化学品':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
                    if var[i] == '毒物':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
                    if var[i] == '射线':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
                    if var[i] == '不详':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
                    if isinstance(var[i], dict) == True:
                        for k1, v1 in var[i].items():
                            if k1 == '其他':
                                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
                                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[3]/span/span/input', v1)
        else:
            # cj3，默认不勾选无，要求勾选无，直接勾选无。
            if varStatus == True:
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[1]/span/input', 1)
            else:
                # cj4，默认不勾选无，要求勾选化学，操作取消所有勾选，勾选化学。
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input')  # 化学品
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input')  # 毒物
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input')  # 射线
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input')  # 不详
                Web_PO.clrSelected('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input')  # 其他
                for i in range(len(var)):
                    if var[i] == '化学品':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/span/input', 1)
                    if var[i] == '毒物':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span/input', 1)
                    if var[i] == '射线':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[1]/td[4]/span/input', 1)
                    if var[i] == '不详':
                        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[1]/span/input', 1)
                    if isinstance(var[i], dict) == True:
                        for k1, v1 in var[i].items():
                            if k1 == '其他':
                                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[2]/span/input', 1)
                                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/table/tbody[3]/tr[4]/td[2]/table/tbody/tr[2]/td[3]/span/span/input', v1)



        # todo 疾病信息
        # 疾病史
        # 风险1：不知道当前用户有多少疾病史，默认最多5个，全部关闭。???
        varQty = 5
        var = {'脑卒中': '2010-12-01', '其他法定传染病': ['baidu', '2020-12-10'], '高血压': '2010-12-02', '其他': ['12121', '2020-12-12']}
        for i in range(varQty):
            Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[2]/td[3]/span[1]/span/input')
            tmp = Web_PO.getTextByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[2]/td[3]/span[1]/span/input')
            print(tmp)
            if tmp != "无":
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[2]/td[2]/input', 1)  # -
                Web_PO.clkByX(u"//a[@href='javascript:void(0)']", 2)  # 弹框确认
        x = 1
        for k, v in var.items():
            x = x + 1
            Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[1]/td[2]/input[1]')  # +
            if k == '其他' or k == '其他法定传染病':
                Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input')
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input', k)
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[2]/span/input', v[0])
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v[1])
            else:
                Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input')
                Web_PO.setTextEnterByX('//html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[3]/span[1]/span/input', k)
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[1]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v)


        # 手术史
        varStatus = '有'
        var = {'手术1': '2010-12-01', '手术2': '2010-12-02'}
        # cj1，要求无，点击无，弹出框确认
        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)  # 无
        Web_PO.clkByX(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        # cj2,默认无，要求有，点击有，输入内容
        # cj3，默认有，要求有，修改原有数据
        if varStatus == '有':
            Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)  # 有
            x = 1
            for k, v in var.items():
                x = x + 1
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr/td[2]/input', 1)  # +
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr[' + str(x) + ']/td[3]/span/span/input', k)  # 名称
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[2]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v)  # 手术日期


        # 外伤史
        varStatus = '有'
        var = {'外伤3': '2020-12-01', '外伤4': '2020-12-02'}
        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)  # 无
        Web_PO.clkByX(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        if varStatus == '有':
            Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[1]/input', 1)  # 有
            x = 1
            for k, v in var.items():
                x = x + 1
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr/td[2]/input', 1)  # +
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr[' + str(x) + ']/td[3]/span/span/input', k)  # 名称
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[3]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v)  # 发生日期


        # 输血史
        varStatus = '有'
        var = {'输血4': '2020-12-12', '输血5': '2020-12-13'}
        Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input', 1)  # 无
        Web_PO.clkByX(u"//a[@href='javascript:void(0)']", 1)  # 确定删除记录
        if varStatus == '有':
            Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/div/table/tbody/tr/td/div[1]/div[1]/input',1)  # 有
            x = 1
            for k, v in var.items():
                x = x + 1
                Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr/td[2]/input', 1)  # +
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr[' + str(x) + ']/td[3]/span/span/input', k)  # 数学原因
                Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[4]/tbody/tr[' + str(x) + ']/td[4]/span/span/input', v)  # 输血日期


        # 家族史 {家庭关系：疾病种类}
        var = {"母亲": ['高血压', '糖尿病', {'其他法定传染病':'123'}], "父亲": ['性阻塞性肺疾病', '脑卒中', {'其他': '4444123'}]}
        for k, v in var.items():
            Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr/td[2]/input', 1)  # +
            Web_PO.clsReadonlyByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[3]/span/span/input')  # 家庭关系
            Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[3]/span/span/input', k)  # mother
            for i in range(len(v)):
                if v[i] == '高血压':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[2]/input',1) # 高血压
                if v[i] == '糖尿病':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[3]/input',1) # 糖尿病
                if v[i] == '冠心病':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[4]/input',1) # 冠心病
                if v[i] == '慢性阻塞性肺疾病':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[5]/input',1) # 慢性阻塞性肺疾病
                if v[i] == '恶性肿瘤':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[6]/input',1) # 恶性肿瘤
                if v[i] == '脑卒中':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[7]/input',1) # 脑卒中
                if v[i] == '重性精神疾病':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[8]/input',1) # 重性精神疾病
                if v[i] == '结核病':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[9]/input',1) # 结核病
                if v[i] == '肝炎':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[10]/input',1) # 肝炎
                if v[i] == '先天畸形':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[11]/input',1) # 先天畸形
                if v[i] == '职业病':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[12]/input',1) # 职业病
                if v[i] == '肾脏疾病':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[13]/input',1) # 肾脏疾病
                if v[i] == '贫血':
                    Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[14]/input',1) # 贫血
                if isinstance(v[i], dict) == True:
                    for k1, v1 in v[i].items():
                        if k1 == '其他法定传染病':
                            Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[15]/input',1)  # 其他法定传染病
                            Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[16]/span/input', v1)
                        if k1 == '其他':
                            Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[17]/input',1)  # 其他
                            Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[5]/tbody/tr[2]/td[4]/span[18]/span/input', v1)


        # 遗传性疾病史
        var = '121212'
        Web_PO.setTextEnterByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[3]/table[6]/tbody/tr/td[2]/span/span/textarea', var)

        # 保存
        # Web_PO.setTextById('button1', 1)

        # 关闭
        # Web_PO.clkByX('/html/body/div[1]/div/div[2]/div[2]/div/div/div[4]/a/input', 1)


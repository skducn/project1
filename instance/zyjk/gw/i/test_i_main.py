# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : 公卫接口，使用pytest框架执行公卫接口，生成报告
# 接口文档：http://192.168.0.203:38080/doc.html
# web：http://192.168.0.203:30080  11012, Jinhao123
# 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
# privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681
# publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9
# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2

# 官网：https://docs.qameta.io/allure/#_pytest
# 源码example：https://github.com/allure-examples/allure-examples/

# (py310) localhost-2:i linghuchong$ pytest --help | grep allure
#   --allure-severities=SEVERITIES_SET
#   --allure-epics=EPICS_SET
#   --allure-features=FEATURES_SET
#   --allure-stories=STORIES_SET
#   --allure-ids=IDS_SET  Comma-separated list of IDs.
#   --allure-label=LABELS_SET
#   --allure-link-pattern=LINK_TYPE:LINK_PATTERN
#   --alluredir=DIR       Generate Allure report in the specified directory (may
#   --clean-alluredir     Clean alluredir folder if it exists
#   --allure-no-capture   Do not attach pytest captured logging/stdout/stderr to


# pytest --alluredir ./result  --clean-alluredir
# allure serve ./result
# 对issue号进行bug关联，如@allure.issue('12092', "禅道号：12092")，关联到地址http://103.25.65.103:8089/biz/bug-view-12092.html
# pytest test_i_main.py --alluredir ./result --allure-link-pattern=issue:http://103.25.65.103:8089/biz/bug-view-{}.html

# BLOCKER ("blocker")， 阻塞缺陷（功能未实现，无法下一步）
# CRITICAL ("critical")， 严重缺陷（功能点缺失）
# NORMAL ("normal")， 一般缺陷（边界情况，格式错误）
# MINOR ("minor")， 次要缺陷（界面错误与 ui 需求不符）
# TRIVIAL ("trivial")， 轻微缺陷（必须项无提示，或者提示不规范）
# pytest -vs 文件名 --allure-severities normal,critical --alluredir ./result
# 只执行critical,normal 这2类用例
# pytest test_i_main.py --alluredir ./result --allure-severities=critical,normal --clean-alluredir
# pytest test_i_main.py --alluredir ./result --allure-feature="allure功能介绍" --clean-alluredir


# 使用方法	参数值	参数说明
# @allure.epic()	epic 描述	定义项目，当有多个项目时使用。往下是 Feature
# @allure.feature()	模块名称	用例按照模块区分，有多个模块时给每个起名字
# @allure.story()	用例名称	用例的描述
# @allure.title	用例标题	用例标题
# @allure.testcase()	用例相关链接	自动化用例对应的功能用例存放系统的地址
# @allure.issue()	缺陷地址	对应缺陷管理系统里边的缺陷地址
# @allure.description()	用例描述	对测试用例的详细描述
# @allure.step()	操作步骤	测试用例的操作步骤
# @allure.severity()	用例等级	blocker、critical、normal、minor、trivial
# @allure.link()	定义连接	用于定义一个需要在测试报告中展示的连接
# @allure.attachment()	附件	添加测试报告附件
# *****************************************************************
import pytest, allure

from .GwPO_i import *
Gw_PO_i = GwPO_i()

from .ConfigparserPO import *
config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))
print(f"Config file path: {config_file_path}")
Configparser_PO = ConfigparserPO(config_file_path)
# Configparser_PO = ConfigparserPO('./config.ini')

from PO.SqlserverPO import SqlServerPO
Sqlserver_PO = SqlServerPO(
    Configparser_PO.DB("host"),
    Configparser_PO.DB("user"),
    Configparser_PO.DB("password"),
    Configparser_PO.DB("database"),
    Configparser_PO.DB("charset")
)  # 测试环境

d_ = {
    '登录': {"username": Configparser_PO.ACCOUNT("user"), "password": Configparser_PO.ACCOUNT("password")},
    '获取高血压管理卡基本信息': {'i':"/serverExport/gxy/getEhrInfo?0=", 'p':'{"idCard":"310101195001293595"}'},
    '查询已签约居民': {'i':"/server/tSignInfo/findPage?0=", 'p':'{"current":1,"size":20}', 'd':'{"signStatus":1,"orgCode":"","basicInfoCode":"","basicInfoNames":[],"idcard":"","name":"","teamId":"","teamIds":[],"serviceIds":[],"current":1,"size":10}'}
}



@allure.feature('登录模块')
class TestLogin(object):
    @pytest.mark.run(order=1)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story('获取token')
    def test_login(self):
        d_user_token = Gw_PO_i.curlLogin(Gw_PO_i.encrypt(json.dumps(d_['登录接口'])))  # {'user': '11012', 'token': 'eyJhbG...
        allure.attach(str(d_user_token), name='获取user和token')


@allure.feature('高血压管理卡')
class TestEHR(object):
    @pytest.mark.run(order=4)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://config.net.cn/tools/sm2.html", name="在线SM2公钥私钥对生成")
    @allure.link("http://192.168.0.203:38080/doc.html#/phs-server/REST%20-%20%E9%AB%98%E8%A1%80%E5%8E%8B/createOrUpdateHzglkUsingPOST", name="高血压管理卡 新增或编辑")
    @allure.title("高血压管理卡 新增")
    def test_get_ehr_info(self):
        with allure.step("步骤1：获取高血压管理卡-获取基本信息"):
            allure.attach(d_['获取高血压管理卡基本信息']['p'], name='查询身份证')
        r = Gw_PO_i.curlGET(d_['获取高血压管理卡基本信息']['i'], d_['获取高血压管理卡基本信息']['p'])
        css = r[0].replace(d_['获取高血压管理卡基本信息']['p'], '<span class="red-text">' + d_['获取高血压管理卡基本信息']['p'] + '</span>')
        allure.attach('<style>.red-text {color: red;}}</style>' + css, "未加密的curl", allure.attachment_type.HTML)
        allure.attach(r[1], "加密的curl", allure.attachment_type.HTML)
        with allure.step("步骤2：输出信息"):
            allure.attach(str(r[2]), name='结果')


@allure.feature('已签约居民')
class TestSigned(object):
    @pytest.mark.run(order=8)
    @allure.severity(allure.severity_level.MINOR)
    @allure.link("https://config.net.cn/tools/sm2.html", name="在线SM2公钥私钥对生成")
    @allure.link("http://192.168.0.203:38080/doc.html#/phs-server/REST%20-%20%E9%AB%98%E8%A1%80%E5%8E%8B/createOrUpdateHzglkUsingPOST", name="高血压管理卡 新增或编辑")
    @allure.title("查询已签约居民")
    def test_get_signed_info(self):
        with allure.step("步骤1：查询"):
            allure.attach('默认查询条件')
            # allure.attach(d_['获取高血压管理卡基本信息']['p'], name='查询')
            # allure.attach('{"idCard":"310101195001293595"}', name='查询身份证')
        r = Gw_PO_i.curlPOST(d_['查询已签约居民']['i'], d_['查询已签约居民']['p'], d_['查询已签约居民']['d'])
        css = r[0].replace(d_['查询已签约居民']['p'], '<span class="red-text">' + d_['查询已签约居民']['p'] + '</span>')
        css = css.replace(d_['查询已签约居民']['d'], '<span class="blue-text">' + d_['查询已签约居民']['d'] + '</span>')
        allure.attach('<style>.red-text {color: red;}.blue-text {color: blue;}</style>' + css, "未加密的curl", allure.attachment_type.HTML)
        allure.attach(r[1], "加密的curl", allure.attachment_type.HTML)
        with allure.step("步骤2：输出信息"):
            allure.attach(str(r[2]), name='结果')



@allure.feature('allure功能介绍')
class TestFunction(object):

    def test_step(self):
        # 创建一个包含红色文本的 HTML 字符串
        red_text_html = '<p style="color: red;">这是红色的文本</p>'
        # 使用 allure.attach 方法将 HTML 附件添加到测试报告中
        allure.attach(red_text_html, "红色文本示例", allure.attachment_type.HTML)
        assert True

        with allure.step("步骤1：test1"):
            print("打开页面")
            # 使用 allure.attach 方法将 HTML 附件添加到测试报告中
            allure.attach( '<p style="color: red;">这是红色的文本11</p>', "红色文本示例11", allure.attachment_type.HTML)

            # allure.attach('<span style="color: red;">这是红色的文本</span>', "是否为红色？", allure.attachment_type.HTML)
            allure.attach("这是一堵啊蚊子",name='文本展示')
        with allure.step("步骤1：test2"):
            print("访问链接")
        with allure.step("步骤1：test3"):
            print("关闭")
            allure.attach('<div class="col-xs-4 text-center"><img src="http://103.25.65.103:8089/?mode=getlogo"></div>',name="html展示", attachment_type=allure.attachment_type.HTML)

    @allure.link("http://103.25.65.103:8089/biz/bug-view-12092.html")
    def test_get_tnb1_info(self):
        print('link：超链接功能，显示具体链接')

    @allure.link("http://www.baidu.com", name="百度")
    def test_get_tnb2_info(self):
        print('link：超链接功能，使用别名显示')

    @allure.issue('12092', "禅道号：12092")
    def test_get_issue_info(self):
        print('issue：参数1是bug号，参数2是注释')
        allure.attach.file("/Users/linghuchong/Desktop/test.jpg",name='测试截图', attachment_type=allure.attachment_type.JPG, extension='.JPG')

    @allure.testcase("http://www.jd.com", "测试用例管理平台")
    def test_get_testcase_info(self):
        print('testcase：同link')

    @allure.severity(allure.severity_level.TRIVIAL)
    def test_with_trivial_severity(self):
        print('trivial：')

    @allure.title('这是一个normal级别的问题')
    @allure.severity(allure.severity_level.NORMAL)
    def test_with_normal_severity(self):
        print('normal1212：')

    @allure.severity(allure.severity_level.BLOCKER)
    def test_with_blocker_severity(self):
        print('blocker：')

    @allure.severity(allure.severity_level.CRITICAL)
    def test_with_critical_severity(self):
        print('critical：')

    @allure.severity(allure.severity_level.MINOR)
    def test_with_minor_severity(self):
        print('minor：')




# 步骤2
# params = {"ehrNum":"","cid": r['data']['cid'],"csrq":"2009-05-27T00:00:00.000+08:00","cswhzysc":"","fhcsbz":"","gljbbm":"3","gxylxbm":"","id":"",
#           "jksj":"2025-03-27","jktdbm":"","jktdmc":"","jkyljgdm":"370685008","jkyljgmc":"大秦家卫生院","jkysgh":10180,
#           "jkysxm":"张飞","jyksrq":"","jzdJw":"商业一村居委会","jzdJwbm":"310109011003",
#           "jzdShe":"上海市","jzdShebm":"31","jzdShi":"市辖区","jzdShibm":"310100000000","jzdXia":"虹口区","jzdXiabm":"310109000000",
#           "jzdXng":"广中路街道","jzdXngbm":"310109011000","jzdXx":"多媒体100号","jzsbm":[],"jzsmc":[],"ksxynl":"","ksyjnl":"",
#           "lxdh":"13448117092","sfyjgl":"","sfzzgl":"0","sg":"","shxgdl":"","shxgxy":"","shxgyj":"","tz":"","wfydp":"","wfysp":"",
#           "whysjtzy":"","wxfcbm":"","wxfcmc":"","xb":"1","xbmc":"","xm":"尤亮柏","xxlybm":"","xxlymc":"","xxlysm":"","zhiyemc":"",
#           "zjhm":"310101195001293595","zyblbz":"","zyblysmc":"","zyblyszldm":[],"zyblyszlmc":[],"zzglrq":"","zzglyy":"","shzlnlbm":"",
#           "qzrq":"2025-03-27","sfgxjkda":"1"}
# encrypted_params = gw_i_PO.encrypt(json.dumps(params))
# url = f"/server/gxy/createOrUpdateHzglk' -d '{encrypted_params}'"
# r = Gw_PO_i.curl('POST', url)
# print(r)


# # todo 首页 - 档案概况，三高概况，重点人群分布情况，健康档案
# r = Gw_PO_i.curl('GET', "/server/tHome/getHomePageData")
# print(r)  # {'code': 200, 'msg': None, 'data': {'total': 129, 'familyTotal': 109, 'signTotal': None, 'currentSignTotal': None, 'threeHighResidents': 1, 'residentsOfLianggao': 6, 'gxyTotal': 19, 'tnbTotal': 11, 'gxzTotal': 11, 'dbtTotal': 4, 'chdTotal': 3, 'tbTotal': 5, 'disTotal': 7, 'smiTotal': 9, 'snrTotal': 16, 'pwTotal': 7, 'childTotal': 20, 'gxyTotalRate': 14.73, 'tnbTotalRate': 8.53, 'gxzTotalRate': 8.53, 'dbtTotalRate': 3.1, 'chdTotalRate': 2.33, 'tbTotalRate': 3.88, 'disTotalRate': 5.43, 'smiTotalRate': 6.98, 'snrTotalRate': 12.4, 'pwTotalRate': 5.43, 'childTotalRate': 15.5, 'transferOutNum': 0, 'switchTeamNum': 0, 'rescindNum': 0, 'deathToll': 14, 'notYetManagedToll': 3}}
#
#
# # todo 首页 - 任务提醒
# # r = Gw_PO_i.curl('GET', "/server/tHome/getHomeSumData?0=" + gw_i_PO.encrypt('{"type":"1"}'))
# # print(r)  # {'code': 200, 'msg': None, 'data': {'gxyNum': 10, 'tnbNum': 8, 'childNum': 8, 'pwNum': 3, 'tbNum': 6, 'disNum': 2, 'smiNum': 2}}
# params = {"type": "1"}
# encrypted_params = gw_i_PO.encrypt(json.dumps(params))
# url = f"/server/tHome/getHomeSumData?0={encrypted_params}"
# r = Gw_PO_i.curl('GET', url)
# print(r)




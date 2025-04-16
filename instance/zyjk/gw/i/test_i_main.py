# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : 公卫接口，使用pytest框架执行公卫接口，生成allure报告
# pip install pytest-order
# 接口文档：http://192.168.0.203:38080/doc.html
# web：http://192.168.0.203:30080  11012, Jinhao123
# 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
# privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681
# publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9
# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2

# todo 使用方法：数据源来自数据库（如a_phs_gxy_app表，此表数据由i_gw.xlsx导入），第一步通过d_inner（表和路径或其他字段）定位到记录，第二步执行接口_query(), 第三步更新表。

# todo pytest和allure
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

# todo pytest --alluredir ./result  --clean-alluredir
# todo allure serve ./result
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

# todo 终端执行
# # 第一步：生成 Allure 结果数据
# pytest --alluredir=allure-results --clean-alluredir
# allure serve ./allure-results

# todo flask
# # 第二步：基于结果数据生成 Allure 报告
# pytest --alluredir=allure-results --clean-alluredir
# allure generate allure-results -o allureReport --clean

# *****************************************************************
import sys, os, pytest, allure, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="rubicon")

# 将当前目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from GwPO_i import *
Gw_PO_i = GwPO_i()

from ConfigparserPO import *
config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))
Configparser_PO = ConfigparserPO(config_file_path)

from PO.SqlserverPO import SqlServerPO
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), Configparser_PO.DB("charset"))

# 数据源
# # todo 登录模块
# d_auth = {
#     '登录': {'path': '/auth/login', 'method': 'POST', 'body': '{"username":"11012","password":"Jinhao123"}'},
#     '确认用户是否已经登录': {'path': '/auth/logined', 'method': 'POST', 'body': 'userName=11012'},
#     '登出': {'path': '/auth/logout', 'method': 'DELETE'}
# }
#
# # todo 高血压
# d_gxy = {
#     '高血压管理卡-获取基本信息': {'path': "/serverExport/gxy/getEhrInfo", 'method': 'GET', 'query': '{"idCard":"310101195001293595"}'},
#     '高血压管理卡-详情': {'path': "/server/gxy/hzglk/{id}", 'method': 'GET', 'query': {"id": "190"}},
# }
#
# # todo 签约信息表
# d_tSignInfo = {'分页查询': {'path': "/server/tSignInfo/findPage", 'method': 'POST', 'query': '{"current":1,"size":20}', 'body': '{"signStatus":1,"orgCode":"","basicInfoCode":"","basicInfoNames":[],"idcard":"","name":"","teamId":"","teamIds":[],"serviceIds":[],"current":1,"size":10}'}
# }

# ************************************************************************************************************************
# ************************************************************************************************************************
# ************************************************************************************************************************

def _query(path, method, query):
    d_rps = Gw_PO_i.curl(path, method, query)
    # 未加密的curl
    css = d_rps['unEncryptedCurl'].replace(d_rps['unEncryptedCurl_query'], '<span class="red-text">' + d_rps['unEncryptedCurl_query'] + '</span>')
    allure.attach('<style>.red-text {color: red;}</style>' + css, "未加密的curl", allure.attachment_type.HTML)
    # 加密的curl
    css = d_rps['encryptedCurl'].replace(d_rps['encryptedCurl_query'], '<span class="blue-text">' + d_rps['encryptedCurl_query'] + '</span>')
    allure.attach('<style>.blue-text {color: blue;}</style>' + css, "加密的curl", allure.attachment_type.HTML)
    # 参考
    with allure.step("参考"):
        allure.attach("https://config.net.cn/tools/sm2.html", name='在线SM2公钥私钥对生成')
        allure.attach("00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681", name='私钥')
        allure.attach("047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9", name='公钥')
    # 返回值
    allure.attach(str(d_rps['r']), name='返回值')
    return d_rps['r']

def _query_id(path, method, query):
    d_rps = Gw_PO_i.curl(path, method, query)
    # 未加密的curl
    css = d_rps['unEncryptedCurl'].replace(str(d_rps['unEncryptedCurl_query']), '<span class="red-text">' + str(d_rps['unEncryptedCurl_query']) + '</span>')
    allure.attach('<style>.red-text {color: red;}</style>' + css, "未加密的curl", allure.attachment_type.HTML)
    # 参考
    with allure.step("参考"):
        allure.attach("https://config.net.cn/tools/sm2.html", name='在线SM2公钥私钥对生成')
        allure.attach("00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681", name='私钥')
        allure.attach("047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9", name='公钥')
    # 返回值
    allure.attach(str(d_rps['r']), name='返回值')
    return d_rps['r']

def _body(path, method, body):
    d_rps = Gw_PO_i.curl(path, method, '', body)
    # 未加密的curl
    css = d_rps['unEncryptedCurl'].replace(d_rps['unEncryptedCurl_body'], '<span class="red-text">' + d_rps['unEncryptedCurl_body'] + '</span>')
    allure.attach('<style>.red-text {color: red;}</style>' + css, "未加密的curl", allure.attachment_type.HTML)
    # 加密的curl
    css = d_rps['encryptedCurl'].replace(d_rps['encryptedCurl_body'],'<span class="blue-text">' + d_rps['encryptedCurl_body'] + '</span>')
    allure.attach('<style>.blue-text {color: blue;}</style>' + css, "加密的curl", allure.attachment_type.HTML)
    # 参考
    with allure.step("参考"):
        allure.attach("https://config.net.cn/tools/sm2.html", name='在线SM2公钥私钥对生成')
        allure.attach("00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681", name='私钥')
        allure.attach("047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9", name='公钥')
    # 返回值
    allure.attach(str(d_rps['r']), name='返回值')
    return d_rps['r']

def _noParam(path, method):
    d_rps = Gw_PO_i.curl(path, method, '', '')
    # 参考
    with allure.step("参考"):
        allure.attach("https://config.net.cn/tools/sm2.html", name='在线SM2公钥私钥对生成')
        allure.attach("00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681", name='私钥')
        allure.attach("047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9", name='公钥')
    # 返回值
    allure.attach(str(d_rps['r']), name='返回值')
    return d_rps['r']

def _queryBody(path, method, query, body):
    d_rps = Gw_PO_i.curl(path, method, query, body)
    # 未加密的curl
    css = d_rps['unEncryptedCurl'].replace(d_rps['unEncryptedCurl_query'], '<span class="red-text">' + d_rps['unEncryptedCurl_query'] + '</span>')
    css = css.replace(d_rps['unEncryptedCurl_body'], '<span class="red-text">' + d_rps['unEncryptedCurl_body'] + '</span>')
    allure.attach('<style>.red-text {color: red;}</style>' + css, "未加密的curl", allure.attachment_type.HTML)
    # 加密的curl
    css = d_rps['encryptedCurl'].replace(d_rps['encryptedCurl_query'], '<span class="blue-text">' + d_rps['encryptedCurl_query'] + '</span>')
    css = css.replace(d_rps['encryptedCurl_body'], '<span class="blue-text">' + d_rps['encryptedCurl_body'] + '</span>')
    allure.attach('<style>.blue-text {color: blue;}</style>' + css, "加密的curl", allure.attachment_type.HTML)
    # 参考
    with allure.step("参考"):
        allure.attach("https://config.net.cn/tools/sm2.html", name='在线SM2公钥私钥对生成')
        allure.attach("00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681", name='私钥')
        allure.attach("047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9", name='公钥')
    # 返回值
    allure.attach(str(d_rps['r']), name='返回值')
    return d_rps['r']

def updateDB(d_db):
    # updateDB(d_db) = {'tableName':'a_phs_auth_app','summary':'确认用户是否已经登录','path':'111','tester':'金浩','rpsDetail':json.dumps(d_r)}
    # 更新数据库表
    # 更新返回值描述
    if 'summary' in d_db:
        Sqlserver_PO.execute("update %s set rpsDetail='%s' where summary='%s'" % (d_db['tableName'], d_db['rpsDetail'], d_db['summary']))
        # Sqlserver_PO.execute("update %s set rpsDetail='%s' where summary='%s'" % ('a_phs_auth_app', str(json.dumps(d_r)), '确认用户是否已经登录'))
        if '{"code": 200' in d_db['rpsDetail']:
            # 更新状态
            Sqlserver_PO.execute("update %s set status='%s' where summary='%s'" % (d_db['tableName'], '已通过', d_db['summary']))
        else:
            Sqlserver_PO.execute("update %s set status='%s' where summary='%s'" % (d_db['tableName'], '失败', d_db['summary']))
        # 测试人
        Sqlserver_PO.execute("update %s set tester='%s' where summary='%s'" % (d_db['tableName'], d_db['tester'], d_db['summary']))
        # 更新日期
        Sqlserver_PO.execute("update %s set updateDate=CONVERT(DATE, '%s') where summary='%s'" % (d_db['tableName'], str(Time_PO.getDateByMinus()), d_db['summary']))
        # Sqlserver_PO.execute("update %s set updateDate=CAST('%s' AS DATE) where summary='%s'" % ('a_phs_auth_app', str(Time_PO.getDateByMinus()), '确认用户是否已经登录'))
    elif 'path' in d_db:
        Sqlserver_PO.execute("update %s set rpsDetail='%s' where path='%s'" % (d_db['tableName'], d_db['rpsDetail'], d_db['path']))
        if '{"code": 200' in d_db['rpsDetail']:
            # 更新状态
            Sqlserver_PO.execute("update %s set status='%s' where path='%s'" % (d_db['tableName'], '已通过', d_db['path']))
        else:
            Sqlserver_PO.execute("update %s set status='%s' where path='%s'" % (d_db['tableName'], '失败', d_db['path']))
        # 测试人
        Sqlserver_PO.execute("update %s set tester='%s' where path='%s'" % (d_db['tableName'], d_db['tester'], d_db['path']))
        # 更新日期
        Sqlserver_PO.execute("update %s set updateDate=CONVERT(DATE, '%s') where path='%s'" % (d_db['tableName'], str(Time_PO.getDateByMinus()), d_db['path']))


# 可用参数
dd_ = {}

@allure.feature('登录模块')
class TestAuth(object):
    @pytest.mark.order(order=1)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('这里填写url', name='登录')
    @allure.title('登录')
    def test_auth_login(self):
        r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body,url FROM %s where summary='%s'" % ('a_phs_auth_app', '登录'))[0]
        d_user_token = Gw_PO_i.curlLogin(r['path'], r['body'])
        allure.attach(str(d_user_token), name='返回值')

    @pytest.mark.order(order=2)
    @allure.severity(allure.severity_level.MINOR)
    @allure.link('http://192.168.0.203:38080/doc.html#/phs-auth/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginedUsingPOST', name='确认用户是否已经登录')
    @allure.title('确认用户是否已经登录')
    def test_auth_logined(self):
        d_inner = {'tableName':'a_phs_auth_app', 'summary': '确认用户是否已经登录'}
        r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body,url FROM %s where summary='%s'" % (d_inner['tableName'], d_inner['summary']))[0]
        d_r = _body(r['path'], str(r['method']).upper(), r['body'])
        # 更新数据库表
        updateDB({'tableName':d_inner['tableName'], 'summary': d_inner['summary'], 'tester': '金浩', 'rpsDetail': str(json.dumps(d_r))})

    # @pytest.mark.order(order=3)
    # @allure.severity(allure.severity_level.MINOR)
    # @allure.link("http://192.168.0.203:38080/doc.html#/phs-auth/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/logoutUsingDELETE", name="登出")
    # @allure.title('登出')
    # def test_auth_logout(self):
    #     d_inner = {'tableName':'a_phs_auth_app', 'summary': '登出'}
    #     r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body,url FROM %s where summary='%s'" % (d_inner['tableName'], d_inner['summary']))[0]
    #     d_r = _noParam(r['path'], str(r['method']).upper())
    #     # 更新数据库表
    #     updateDB({'tableName': d_inner['tableName'], 'summary': d_inner['summary'], 'tester': '金浩', 'rpsDetail': str(json.dumps(d_r))})


@allure.feature('高血压')
class TestGXY(object):
    @pytest.mark.order(order=10)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("http://192.168.0.203:38080/doc.html#/phs-server-export/REST%20-%20%E9%AB%98%E8%A1%80%E5%8E%8B/getEhrInfoUsingGET_1", name="高血压管理卡-获取基本信息")
    @allure.title("高血压管理卡-获取基本信息")
    def test_serverExport_gxy_getEhrInfo(self):
        d_inner = {'tableName':'a_phs_gxy_app', 'path': '/serverExport/gxy/getEhrInfo'}
        r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body,url FROM %s where path='%s'" % (d_inner['tableName'], d_inner['path']))[0]
        d_r = _query(r['path'], str(r['method']).upper(), r['query'])
        # 更新数据库表
        updateDB({'tableName': d_inner['tableName'], 'path': d_inner['path'], 'tester': '金浩', 'rpsDetail': str(json.dumps(d_r))})


    @pytest.mark.order(order=41)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("http://192.168.0.203:38080/doc.html#/phs-server/REST%20-%20%E9%AB%98%E8%A1%80%E5%8E%8B/getHzglkInfoByIdUsingGET", name="高血压管理卡-详情")
    @allure.title("高血压管理卡-详情")
    def test_server_gxy_hzglk(self):
        d_inner = {'tableName':'a_phs_gxy_app', 'path': '/server/gxy/hzglk/{id}'}
        r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body,url FROM %s where path='%s'" % (d_inner['tableName'], d_inner['path']))[0]
        d_r = _query_id(r['path'], str(r['method']).upper(), r['query'])
        # 更新数据库表
        updateDB({'tableName': d_inner['tableName'], 'path': d_inner['path'], 'tester': '金浩', 'rpsDetail': str(json.dumps(d_r))})
        d_tmp = {}
        d_tmp['cid'] = d_r['data']['cid']
        s_path = str(r['path']).replace("/", "_").replace("{", "").replace("}", "")
        dd_[s_path] = d_tmp
        allure.attach(str(dd_), name='可用参数')
#
# #
@allure.feature('已签约居民')
class TestSigned(object):
    @pytest.mark.order(order=30)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("http://192.168.0.203:38080/doc.html#/phs-server/REST%20-%20%E7%AD%BE%E7%BA%A6%E4%BF%A1%E6%81%AF%E8%A1%A8/findPageUsingPOST_26", name="分页查询")
    @allure.title("REST - 签约信息表")
    def test_server_tSignInfo_findPage(self):
        d_inner = {'tableName':'a_phs_tSignInfo_app', 'path': '/server/tSignInfo/findPage'}
        r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body,url FROM %s where path='%s'" % (d_inner['tableName'], d_inner['path']))[0]
        d_r = _queryBody(r['path'], str(r['method']).upper(), r['query'], r['body'])
        # 更新数据库表
        updateDB({'tableName': d_inner['tableName'], 'path': d_inner['path'], 'tester': '金浩', 'rpsDetail': str(json.dumps(d_r))})
        d_tmp = {}
        d_tmp['id'] = d_r['data']['records'][0]['id']
        d_tmp['orgCode'] = d_r['data']['records'][0]['orgCode']
        s_path = str(r['path']).replace("/", "_").replace("{", "").replace("}", "")
        dd_[s_path] = d_tmp
        allure.attach(str(dd_), name='可用参数')



# @allure.feature('allure功能介绍')
# class TestFunction(object):
#
#     def test_step(self):
#         # 创建一个包含红色文本的 HTML 字符串
#         red_text_html = '<p style="color: red;">这是红色的文本</p>'
#         # 使用 allure.attach 方法将 HTML 附件添加到测试报告中
#         allure.attach(red_text_html, "红色文本示例", allure.attachment_type.HTML)
#         assert True
#
#         with allure.step("步骤1：test1"):
#             print("打开页面")
#             # 使用 allure.attach 方法将 HTML 附件添加到测试报告中
#             allure.attach( '<p style="color: red;">这是红色的文本11</p>', "红色文本示例11", allure.attachment_type.HTML)
#
#             # allure.attach('<span style="color: red;">这是红色的文本</span>', "是否为红色？", allure.attachment_type.HTML)
#             allure.attach("这是一堵啊蚊子",name='文本展示')
#         with allure.step("步骤1：test2"):
#             print("访问链接")
#         with allure.step("步骤1：test3"):
#             print("关闭")
#             allure.attach('<div class="col-xs-4 text-center"><img src="http://103.25.65.103:8089/?mode=getlogo"></div>',name="html展示", attachment_type=allure.attachment_type.HTML)
#
#     @allure.link("http://103.25.65.103:8089/biz/bug-view-12092.html")
#     def test_get_tnb1_info(self):
#         print('link：超链接功能，显示具体链接')
#
#     @allure.link("http://www.baidu.com", name="百度")
#     def test_get_tnb2_info(self):
#         print('link：超链接功能，使用别名显示')
#
#     @allure.issue('12092', "禅道号：12092")
#     def test_get_issue_info(self):
#         print('issue：参数1是bug号，参数2是注释')
#         allure.attach.file("/Users/linghuchong/Desktop/test.jpg",name='测试截图', attachment_type=allure.attachment_type.JPG, extension='.JPG')
#
#     @allure.testcase("http://www.jd.com", "测试用例管理平台")
#     def test_get_testcase_info(self):
#         print('testcase：同link')
#
#     @allure.severity(allure.severity_level.TRIVIAL)
#     def test_with_trivial_severity(self):
#         print('trivial：')
#
#     @allure.title('这是一个normal级别的问题')
#     @allure.severity(allure.severity_level.NORMAL)
#     def test_with_normal_severity(self):
#         print('normal1212：')
#
#     @allure.severity(allure.severity_level.BLOCKER)
#     def test_with_blocker_severity(self):
#         print('blocker：')
#
#     @allure.severity(allure.severity_level.CRITICAL)
#     def test_with_critical_severity(self):
#         print('critical：')
#
#     @allure.severity(allure.severity_level.MINOR)
#     def test_with_minor_severity(self):
#         print('minor：')
#



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




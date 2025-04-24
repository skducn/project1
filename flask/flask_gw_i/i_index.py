# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : 公卫接口，首页
# 接口文档：http://192.168.0.203:38080/doc.html
# web：http://192.168.0.203:30080  testwjw, Qa@123456
# 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
# privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681
# publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9
# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2
# *****************************************************************
from GwPO_i import *
Gw_PO_i = GwPO_i()
from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), Configparser_PO.DB("charset"))  # 测试环境

# 1，登录 - 获取token
login_data = {
        "username": Configparser_PO.ACCOUNT("user"),
        "password": Configparser_PO.ACCOUNT("password"),
        "code": "",
        "uuid": ""
    }
encrypt_data = Gw_PO_i.encrypt(json.dumps(login_data))
Gw_PO_i.curlLogin(encrypt_data)  # {'user': '11012', 'token': 'eyJhbG...


# todo 新增高血压管理卡
# http://192.168.0.203:38080/doc.html#/phs-server/REST%20-%20%E9%AB%98%E8%A1%80%E5%8E%8B/createOrUpdateHzglkUsingPOST

# 步骤1, 高血压管理卡-获取基本信息
params = '{"idCard":"310101195001293595"}'
encrypted_params = Gw_PO_i.encrypt(params)
r = Gw_PO_i.curl('GET', "/serverExport/gxy/getEhrInfo?0=" + encrypted_params)
print(r)
# {'code': 200, 'msg': None, 'data': {'id': None, 'bbId': None, 'cid': 'dedadc417a84419ea7ac972a31dcf5f3', 'ehrNum': None, 'xm': '尤亮柏', 'xb': '1', 'xbmc': '男', 'csrq': '1950-01-29T00:00:00.000+08:00', 'lxdh': '15831052116', 'zjhm': '310101195001293595', 'zhiyedm': '70000', 'zhiyemc': '军人', 'xxlybm': None, 'xxlymc': None, 'xxlysm': None, 'sg': None, 'tz': None, 'jzsbm': None, 'jzsmc': None, 'shxgxy': None, 'jyksrq': None, 'ksxynl': None, 'shxgyj': None, 'ksyjnl': None, 'sfyjgl': None, 'shxgdl': None, 'zyblbz': None, 'zyblysmc': None, 'zyblyszldm': None, 'zyblyszlmc': None, 'whysjtzy': None, 'cswhzysc': None, 'fhcsbz': None, 'shzlnlbm': None, 'shzlnlmc': None, 'wfysp': None, 'wfydp': None, 'wxfcbm': None, 'wxfcmc': None, 'gljbbm': None, 'gxylxbm': None, 'sfzzgl': None, 'zzglyy': None, 'zzglrq': None, 'jkysgh': None, 'jkysxm': None, 'jksj': None, 'jktdbm': None, 'jktdmc': None, 'jkyljgdm': None, 'jkyljgmc': None, 'jzdShebm': '31', 'jzdShe': '上海市', 'jzdShibm': '310100000000', 'jzdShi': '市辖区', 'jzdXiabm': '310109000000', 'jzdXia': '虹口区', 'jzdXngbm': '310109011000', 'jzdXng': '广中路街道', 'jzdJwbm': '310109011003', 'jzdJw': '商业一村居委会', 'jzdXx': '多媒体100号', 'qzrq': None, 'sfgxjkda': None}}
# 获取cid值，如 r['data']['cid']

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




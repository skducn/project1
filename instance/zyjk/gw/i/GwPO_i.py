# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : gw 公卫接口测试
# 接口文档：http://192.168.0.203:38080/doc.html
# web：http://192.168.0.203:30080  testwjw, Qa@123456

# 在线国密SM2加密/解密 https://the-x.cn/zh-cn/cryptography/Sm2.aspx
# 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
# 密钥：124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# 公钥：04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249

# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2

# todo nacos
# http://192.168.0.223:8848/nacos/	nacos,Zy123456
# phs-test
# phs-gateway-sqlserver.yml
# publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
# privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62

# publicKey: 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9
# privateKey: 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681
# enabled: false    // 改为false无法登录，因为页面加密，用于接口测试
# 安全配置
# # security:
#   验证码
#   # captcha:
#   #   enabled: false    //去掉验证码
# *****************************************************************

import subprocess, json
from PO.WebPO import *

from PO.ColorPO import *
Color_PO = ColorPO()

from .ConfigparserPO import ConfigparserPO
# config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.ini'))
config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))
print(f"Config file path: {config_file_path}")
Configparser_PO = ConfigparserPO(config_file_path)
# Configparser_PO = ConfigparserPO('config.ini')

from PO.TimePO import *
Time_PO = TimePO()

class GwPO_i():

    def __init__(self):
        self.ipAddr = Configparser_PO.HTTP("url")


    def _sm2(self, Web_PO):

        # 在线sm2加密/解密

        Web_PO.openURL("https://config.net.cn/tools/sm2.html")
        # 私钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[1]", Configparser_PO.HTTP("privateKey"))
        # 公钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[2]", Configparser_PO.HTTP("publicKey"))

    def encrypt(self, varSource):

        # 在线sm2加密

        Web_PO = WebPO("noChrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", varSource)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[1]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", "value")
        Web_PO.cls()
        return r

    def decrypt(self, varEncrypt):

        # 在线sm2解密

        # Web_PO = WebPO("noChrome")
        Web_PO = WebPO("chrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", varEncrypt)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[2]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", "value")
        Web_PO.cls()
        return r


    def curlLogin(self, encrypt_data):

        # 登录
        # 注意需要关闭验证码
        d_ = {}
        command = "curl -X POST '" + self.ipAddr + "/auth/login' -d '" + encrypt_data + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json'"
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)  # {'code': 200, 'msg': None, 'data': {'access_token': 'eyJhbGciOiJIUzUxMiJ9.eyJhZmZpbGlhdGVkX2lkIjoiIiwidXNlcl9pZCI6ODIsImNhdGVnb3J5X2NvZGUiOiIxIiwidXNlcl9rZXkiOiIwYzU3YmM3OC05OTNiLTQ1M2ItYjZkMC0yMmNlZTBhMWFkNzMiLCJ0aGlyZF9ubyI6IjEyMzEyMyIsImhvc3BpdGFsX2lkIjoiMDAwMDAwMSIsInVzZXJuYW1lIjoi5YiY5paM6b6ZIiwiaG9zcGl0YWxfbmFtZSI6IumdmeWuieeyvuelnueXhemZoiIsImFmZmlsaWF0ZWRfbmFtZSI6IiJ9.-xh2D7Obdensd3OcL_dqRaA7Qs4I0l0h--3ZYpYifgBZBP16Gzzq24W3IxS8c5ofcQTNyczRK2e3JipcCuyTqg', 'expires_in': 30}}
        try:
            # {'code': 200, 'msg': None, 'data': {'access_token': 'eyJhbGciOiJIUzUxMiJ9.eyJhZmZpbGlhdGVkX2lkIjoiIiwidXNlcl9pZCI6ODIsImNhdGVnb3J5X2NvZGUiOiIxIiwidXNlcl9rZXkiOiIwYzU3YmM3OC05OTNiLTQ1M2ItYjZkMC0yMmNlZTBhMWFkNzMiLCJ0aGlyZF9ubyI6IjEyMzEyMyIsImhvc3BpdGFsX2lkIjoiMDAwMDAwMSIsInVzZXJuYW1lIjoi5YiY5paM6b6ZIiwiaG9zcGl0YWxfbmFtZSI6IumdmeWuieeyvuelnueXhemZoiIsImFmZmlsaWF0ZWRfbmFtZSI6IiJ9.-xh2D7Obdensd3OcL_dqRaA7Qs4I0l0h--3ZYpYifgBZBP16Gzzq24W3IxS8c5ofcQTNyczRK2e3JipcCuyTqg', 'expires_in': 30}}
            self.token = d_r['data']['access_token']
        except:
            # {'code': 500, 'msg': '非法参数！'}
            self.token = d_r['code']

        d_['user'] = Configparser_PO.ACCOUNT("user")
        d_['token'] = self.token
        Color_PO.outColor([{"35": d_}])
        # print("token =>", self.token)
        return d_

    def curlGET(self, varI, varP):

        # 执行接口

        # 未加密
        unencryptedCURL = "curl -X GET '" + self.ipAddr + varI + varP + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
        # print(unencryptedCURL)

        # 已加密
        encryptedCURL = "curl -X GET '" + self.ipAddr + varI + self.encrypt(varP) + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
        # print(command)

        p = subprocess.Popen(encryptedCURL, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)

        print("在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html\n")
        print("privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681\n")
        print("publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9\n")

        return unencryptedCURL, encryptedCURL, d_r
        # print(d_r)  # {'code': 200, 'msg': None, 'data': {'manageEhrNum': 100, 。。。
        # try:
        #     if d_r['code'] == 200:
        #         return d_r
        # except:
        #     # {'code': 500, 'msg': '非法参数！'}
        #     d_r = 500
        # return d_r

    def curlPOST(self, varI, varP, varD):

        # 执行接口

        unencryptedCURL = "curl -X POST '" + self.ipAddr + varI + varP + "' -d '" + varD + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"

        varP = self.encrypt(varP)
        varD = self.encrypt(varD)
        encryptedCURL = "curl -X POST '" + self.ipAddr + varI + varP + "' -d '" + varD + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
        # print(command)
        p = subprocess.Popen(encryptedCURL, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)

        print("在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html\n")
        print("privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681\n")
        print("publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9\n")

        return unencryptedCURL, encryptedCURL, d_r
        #
        # try:
        #     if d_r['code'] == 200:
        #         return d_r, command1
        # except:
        #     # {'code': 500, 'msg': '非法参数！'}
        #     return d_r['code'], command1




    # todo REST-用户信息表

    def getDocByOrg(self):
        # 根据当前所在的机构获取医生
        return self.curl("GET", "/system/sysUser/getDocByOrg")

    def getFamilyDoc(self):
        # 获取家庭医生
        return self.curl("GET", "/system/sysUser/getFamilyDoc")

    def getOrgUser(self):
        # 当前登录用户所在机构及子机构用户
        return self.curl("GET", "/system/sysUser/getOrgUser")

    def getUser(self):
        # 根据用户名获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUser/lbl")

    def getUserByOrg(self):
        # 根据机构获取医生
        return self.curl("GET", "/system/sysUser/getUserByOrg")

    def getVisitUser(self):
        # 根据机构获取医生--随访使用
        return self.curl("GET", "/system/sysUser/getVisitUser")

    def selectUserInfo(self):
        # 根据token获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/selectUserInfo?0=61b9ee3ad031da7b01c6429d5ad3b21757ee9766d5b9e964a77ce621d29bbf7e296f482360155e6e01b29bc557eeedf702b643456ba5b39fe6febf284537a91f88468105d513684ae1abd790025a95df6590470dcc6c5a21c79a105cce1cdbdd5d45")

    def sysUser(self, id):
        # 单条查询
        return self.curl("GET", "/system/sysUser/" + str(id))



    # todo phs-system, REST-系统信息表

    def querySystemRole(self, userId):
        # 获取所有系统的角色
        return self.curl("GET", "/system/sysSystem/querySystemRole?" + str(userId))

    def systemMenuInfoBySystemId(self):
        # 根据系统Id获取所有菜单
        return self.curl("GET", "/system/sysSystem/systemMenuInfoBySystemId?0=950c364d4694618ca13897b742ac7db1752f96c4a778dcb046847e4004d3b62f96e6a125ec604492a0915a47d3b6f6ef87df2f8ec7e718dd308e52f74135ed223adbfeac733f4cc9616f97146cc572d8e748ce23514798982364bd5171e5291ff8c3c34ac2aa8d2d8796e92a4f3d")

    def systemMenuInfo(self, systemId):
        # 获取系统菜单
        return self.curl("GET", "/system/sysSystem/systemMenuInfo?" + str(systemId))

    def systemMenuInfoBySystemId(self, systemId):
        # 根据系统Id获取所有菜单
        return self.curl("GET", "/system/sysSystem/systemMenuInfoBySystemId?" + str(systemId))

    def systemMenuInfoByUserId(self):
        # 根据用户ID获取能够使用的系统及菜单
        return self.curl("GET", "/system/sysSystem/systemMenuInfoByUserId")


    def sysSystem(self, Id):
        # 单条查询
        return self.curl("GET", "/system/sysSystem/?" + str(Id))



    # todo phs-auth, 登录模块

    def logined(self, userName):
        # 确认用户是否已经登录
        return self.curl("POST", '/auth/logined')

    def logout(self):
        # 登出
        return self.curl("DELETE", '/auth/logout')

    def refresh(self):
        # 刷新
        return self.curl("POST", '/auth/refresh')

    def newHypertensionManagementCard(self, s_d_idCard, d_):

        # 新增高血压管理卡

        # 步骤1：通过身份证获取基本信息，从而获取cid值
        # 接口：REST- 高血压，高血压管理卡-获取基本信息
        # http://192.168.0.203:38080/doc.html#/phs-server/REST%20-%20%E9%AB%98%E8%A1%80%E5%8E%8B/getEhrInfoUsingGET_1
        r = self.curl('GET', "/serverExport/gxy/getEhrInfo?0=" + self.encrypt(s_d_idCard))
        print(r) # {'code': 200, 'msg': None, 'data': {'id': None, 'bbId': None, 'cid': 'dedadc417a84419ea7ac972a31dcf5f3', 'ehrNum': None, 'xm': '尤亮柏', 'xb': '1', 'xbmc': '男', 'csrq': '1950-01-29T00:00:00.000+08:00', 'lxdh': '15831052116', 'zjhm': '310101195001293595', 'zhiyedm': '70000', 'zhiyemc': '军人', 'xxlybm': None, 'xxlymc': None, 'xxlysm': None, 'sg': None, 'tz': None, 'jzsbm': None, 'jzsmc': None, 'shxgxy': None, 'jyksrq': None, 'ksxynl': None, 'shxgyj': None, 'ksyjnl': None, 'sfyjgl': None, 'shxgdl': None, 'zyblbz': None, 'zyblysmc': None, 'zyblyszldm': None, 'zyblyszlmc': None, 'whysjtzy': None, 'cswhzysc': None, 'fhcsbz': None, 'shzlnlbm': None, 'shzlnlmc': None, 'wfysp': None, 'wfydp': None, 'wxfcbm': None, 'wxfcmc': None, 'gljbbm': None, 'gxylxbm': None, 'sfzzgl': None, 'zzglyy': None, 'zzglrq': None, 'jkysgh': None, 'jkysxm': None, 'jksj': None, 'jktdbm': None, 'jktdmc': None, 'jkyljgdm': None, 'jkyljgmc': None, 'jzdShebm': '31', 'jzdShe': '上海市', 'jzdShibm': '310100000000', 'jzdShi': '市辖区', 'jzdXiabm': '310109000000', 'jzdXia': '虹口区', 'jzdXngbm': '310109011000', 'jzdXng': '广中路街道', 'jzdJwbm': '310109011003', 'jzdJw': '商业一村居委会', 'jzdXx': '多媒体100号', 'qzrq': None, 'sfgxjkda': None}}

        # 步骤2：新增高血压管理卡，填入cid值
        # 接口：REST- 高血压，高血压管理卡 新增或编辑
        # http://192.168.0.203:38080/doc.html#/phs-server/REST%20-%20%E9%AB%98%E8%A1%80%E5%8E%8B/createOrUpdateHzglkUsingPOST
        d_param = {"ehrNum": "", "cid": r['data']['cid'], "csrq": "2009-05-27T00:00:00.000+08:00", "cswhzysc": "",
                   "fhcsbz": "", "gljbbm": "3", "gxylxbm": "", "id": "",
                   "jksj": str(Time_PO.getDateByMinus()), "jktdbm": "", "jktdmc": "", "jkyljgdm": "370685008",
                   "jkyljgmc": "大秦家卫生院", "jkysgh": 10180,
                   "jkysxm": "张飞", "jyksrq": "", "jzdJw": r['data']['jzdJw'], "jzdJwbm": r['data']['jzdJwbm'],
                   "jzdShe": r['data']['jzdShe'], "jzdShebm": r['data']['jzdShebm'], "jzdShi": r['data']['jzdShi'],
                   "jzdShibm": r['data']['jzdShibm'], "jzdXia": r['data']['jzdXia'], "jzdXiabm": r['data']['jzdXiabm'],
                   "jzdXng": r['data']['jzdXng'], "jzdXngbm": r['data']['jzdXngbm'], "jzdXx": r['data']['jzdXx'],
                   "jzsbm": [], "jzsmc": [], "ksxynl": "", "ksyjnl": "",
                   "lxdh": "13448117092", "sfyjgl": "", "sfzzgl": "0", "sg": "", "shxgdl": "", "shxgxy": "",
                   "shxgyj": "",
                   "tz": "", "wfydp": "", "wfysp": "",
                   "whysjtzy": "", "wxfcbm": "", "wxfcmc": "", "xb": "1", "xbmc": "", "xm": r['data']['xm'],
                   "xxlybm": "",
                   "xxlymc": "", "xxlysm": "", "zhiyemc": "",
                   "zjhm": r['data']['zjhm'], "zyblbz": "", "zyblysmc": "", "zyblyszldm": [], "zyblyszlmc": [],
                   "zzglrq": "",
                   "zzglyy": "", "shzlnlbm": "",
                   "qzrq": "2025-01-01", "sfgxjkda": "1"}
        d_param.update(d_)
        encrypted_params = self.encrypt(json.dumps(d_param))
        url = f"/server/gxy/createOrUpdateHzglk' -d '{encrypted_params}'"
        r = self.curl('POST', url)
        print(r)


# *****************************************************************

if __name__ == "__main__":


    # 登录(testwjw, Qa@123456)
    Gw_PO_i = GwPO_i('9580414215bd76bf8ddd310c894fdfb155f439b427a43fb3dbb13a142055e4b7236fd7498a6e8d2febc7a44688c45d68c11606a34632ce07aa94d037124c0c15c0a19ab3c9f35bab234dd5bc8a3b37d419786c17b2e26d46d0f378e3691f2823e48804aecfb23ebc8511fd66e9b927bb5344d97a9f6c9c001ba4e76865f4890a5c6f7c21810fdedf6bbe85625e6ca990e1fe1cef025760c3382326c993')

    # todo chc-system, REST-用户信息表
    print(Gw_PO_i.getDocByOrg())  # 根据当前所在的机构获取医生
    print(Gw_PO_i.getFamilyDoc())  # 获取家庭医生
    print(Gw_PO_i.getOrgUser())  # 当前登录用户所在机构及子机构用户
    # print(Gw_PO_i.getUser())  # 根据用户名获取用户信息
    # print(Gw_PO_i.getUserByOrg())  # 根据机构获取医生
    # print(Gw_PO_i.getVisitUser())  # 根据机构获取医生--随访使用
    print(Gw_PO_i.selectUserInfo())  # 根据token获取用户信息
    # print(Gw_PO_i.sysUser(id))  # 单条查询


    # todo chc-system, REST-系统信息表
    # print(Gw_PO_i.querySystemRole(userId))  # 获取所有系统的角色
    print(Gw_PO_i.systemMenuInfoBySystemId())  # 根据用户ID获取能够使用的系统
    print(Gw_PO_i.systemMenuInfoByUserId())  # 根据用户ID获取能够使用的系统及菜单
    # print(Gw_PO_i.systemMenuInfo(systemId))  # 获取系统菜单
    # print(Gw_PO_i.systemMenuInfoBySystemId(systemId))  # 根据系统Id获取所有菜单
    # print(Gw_PO_i.sysSystem(Id))  # 单条查询






    # todo chc-auth, 登录模块
    # print(gw_i_PO.logined())  # 确认用户是否已经登录
    print(gw_i_PO.logout())  # 登出
    # print(gw_i_PO.refresh())  # 刷新



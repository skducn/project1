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
from PO.WebPO import *
from PO.ColorPO import *
from ConfigparserPO import ConfigparserPO
from PO.TimePO import *

Color_PO = ColorPO()


# config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.ini'))
config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))
# print(f"Config file path: {config_file_path}")
Configparser_PO = ConfigparserPO(config_file_path)
# Configparser_PO = ConfigparserPO('config.ini')


Time_PO = TimePO()


def _sm2(Web_PO):

    # 在线sm2加密/解密

    Web_PO.openURL("https://config.net.cn/tools/sm2.html")
    # 私钥
    Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[1]", Configparser_PO.HTTP("privateKey"))
    # 公钥
    Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[2]", Configparser_PO.HTTP("publicKey"))


class GwPO_i:

    def __init__(self):
        self.ipAddr = Configparser_PO.HTTP("url")

    def encrypt(self, varSource):

        # 在线sm2加密

        Web_PO = WebPO("noChrome")
        _sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", varSource)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[1]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", "value")
        Web_PO.cls()
        return r

    def decrypt(self, varEncrypt):

        # 在线sm2解密

        # Web_PO = WebPO("noChrome")
        Web_PO = WebPO("chrome")
        _sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", varEncrypt)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[2]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", "value")
        Web_PO.cls()
        return r

    def curlLogin(self, varPath, varBody):
        # 登录
        # 注意需要关闭验证码
        d_ = {}
        command = "curl -X POST '" + self.ipAddr + varPath + "' -d '" + self.encrypt(
            varBody) + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json'"
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        try:
            self.token = d_r['data']['access_token']
        except:
            # {'code': 500, 'msg': '非法参数！'}
            self.token = d_r['code']

        d_['user'] = Configparser_PO.ACCOUNT("user")
        d_['token'] = self.token
        # Color_PO.outColor([{"35": d_}])
        # print("token =>", self.token)
        return d_

    def curl(self, varPath, varMethod, varQuery, varBody=''):

        # 执行接口

        global unEncryptedCurl, encryptedCurl
        d_rps = {}
        if 'GET' in varMethod or 'DELETE' in varMethod:
            if '{' in varPath:
                # 如/server/gxy/hzglk/{id}
                # get未加密
                varQuery = json.loads(varQuery)
                if isinstance(varQuery, dict):
                    key = list(varQuery.keys())[0]
                    varPath = varPath.replace('{' + key + '}', str(varQuery[key]))
                    # print(varPath)  # /server/disManage/register/getInfo/111
                    unEncryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                        self.token) + "'"
                    d_rps['unEncryptedCurl'] = unEncryptedCurl
                    d_rps['unEncryptedCurl_query'] = varQuery[key]
                    p = subprocess.Popen(unEncryptedCurl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = p.communicate()
                    str_r = bytes.decode(out)
                    d_r = json.loads(str_r)
                    d_rps['r'] = d_r
                    return d_rps
                else:
                    print("error, varQuery不是字典！")
            else:
                # get未加密
                if varQuery != '':
                    unEncryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "?0=" + varQuery + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                        self.token) + "'"
                    d_rps['unEncryptedCurl'] = unEncryptedCurl
                    d_rps['unEncryptedCurl_query'] = varQuery
                    # get已加密
                    varQuery = self.encrypt(varQuery)
                    encryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "?0=" + varQuery + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                        self.token) + "'"
                    d_rps['encryptedCurl'] = encryptedCurl
                    d_rps['encryptedCurl_query'] = varQuery
                    p = subprocess.Popen(encryptedCurl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    unEncryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                        self.token) + "'"
                    d_rps['unEncryptedCurl'] = unEncryptedCurl
                    d_rps['unEncryptedCurl_query'] = varQuery
                    p = subprocess.Popen(unEncryptedCurl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                str_r = bytes.decode(out)
                d_r = json.loads(str_r)
                d_rps['r'] = d_r
                return d_rps
        elif 'POST' in varMethod:

            # post未加密
            if varQuery != '' and varBody == '':
                unEncryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "?0=" + varQuery + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                    self.token) + "'"
            elif varQuery != '' and varBody != '':
                unEncryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "?0=" + varQuery + "' -d '" + varBody + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                    self.token) + "'"
            elif varQuery == '' and varBody != '':
                unEncryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "' -d '" + varBody + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                    self.token) + "'"
            d_rps['unEncryptedCurl'] = unEncryptedCurl
            d_rps['unEncryptedCurl_query'] = varQuery
            d_rps['unEncryptedCurl_body'] = varBody
            # post加密
            if varQuery != '' and varBody == '':
                varQuery = self.encrypt(varQuery)
                encryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "?0=" + varQuery + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                    self.token) + "'"
            elif varQuery != '' and varBody != '':
                varQuery = self.encrypt(varQuery)
                varBody = self.encrypt(varBody)
                encryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "?0=" + varQuery + "' -d '" + varBody + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                    self.token) + "'"
            elif varQuery == '' and varBody != '':
                varBody = self.encrypt(varBody)
                encryptedCurl = f"curl -X {varMethod} '" + self.ipAddr + varPath + "' -d '" + varBody + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + str(
                    self.token) + "'"
            d_rps['encryptedCurl'] = encryptedCurl
            d_rps['encryptedCurl_query'] = varQuery
            d_rps['encryptedCurl_body'] = varBody
            p = subprocess.Popen(encryptedCurl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            str_r = bytes.decode(out)
            d_r = json.loads(str_r)
            d_rps['r'] = d_r
            return d_rps

    def curlGET(self, varPath, varQuery):

        # 执行接口

        # 未加密
        unencryptedCURL = "curl -X GET '" + self.ipAddr + varPath + varQuery + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
        # print(unencryptedCURL)

        # 已加密
        encryptedCURL = "curl -X GET '" + self.ipAddr + varPath + self.encrypt(
            varQuery) + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
        # print(command)

        p = subprocess.Popen(encryptedCURL, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)

        print("在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html\n")
        print("privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681\n")
        print(
            "publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9\n")

        return unencryptedCURL, encryptedCURL, d_r
        # print(d_r)  # {'code': 200, 'msg': None, 'data': {'manageEhrNum': 100, 。。。
        # try:
        #     if d_r['code'] == 200:
        #         return d_r
        # except:
        #     # {'code': 500, 'msg': '非法参数！'}
        #     d_r = 500
        # return d_r

    def curlPOST(self, varPath, varQuery, varBody):

        # 执行接口

        unencryptedCURL = "curl -X POST '" + self.ipAddr + varPath + varQuery + "' -d '" + varBody + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"

        varQuery = self.encrypt(varQuery)
        varBody = self.encrypt(varBody)
        encryptedCURL = "curl -X POST '" + self.ipAddr + varPath + varQuery + "' -d '" + varBody + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
        # print(command)
        p = subprocess.Popen(encryptedCURL, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)

        print("在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html\n")
        print("privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681\n")
        print(
            "publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9\n")

        return unencryptedCURL, encryptedCURL, d_r

# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2025-8-4
# Description   : CDRD加密接口测试
# 接口文档：http://192.168.0.243:8083/prod-api/doc.html#
# 接口json：http://192.168.0.243:8083/prod-api/v2/api-docs
# *****************************************************************

import subprocess, requests, json, os


class CdrdPO():

    def __init__(self):

        self.ipPort = "http://192.168.0.243:39210"


    def getTokenByLogin(self):

        # 登录
        # 注意需要关闭验证码
        url = self.ipPort + "/auth/login"
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json"
        }
        data = {
            "password": "Jinhao123",
            "username": "jinhao"
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            d_r = response.json()
            # print(d_r)
            if d_r['code'] == 200:
                self.token = d_r['data']['access_token']
                return self.token
            else:
                return d_r
        except Exception as e:
            print(f"登录请求失败: {e}")
            return None


    def getDepartment(self):

        # 获取科室列表
        url = self.ipPort + "/system/sysDepartment/getList"
        headers = {
            'Accept': '*/*',
            'Authorization': self.token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 检查HTTP错误
            d_r = response.json()
            # print(d_r)
            if d_r['code'] == 200:
                return d_r['data']
            else:
                return d_r
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response.text}")
            return None

    # todo REST-用户信息表

    def getFamilyDoc(self):
        # 获取家庭医生
        return self.curl("GET", "/system/sysUser/getFamilyDoc")

    def getAssistantList(self):
        # 获取家医助手
        return self.curl("GET", "/system/sysUser/getAssistantList")

    def getHealthManagerList(self):
        # 获取健康管理师
        return self.curl("GET", "/system/sysUser/getHealthManagerList")

    def getUser(self):
        # 根据用户名获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUser/lbl")

    def getUserByOrg(self):
        # 根据机构获取医生
        return self.curl("GET", "/system/sysUser/getUserByOrg")

    def getUserConfigByThird(self, orgCode, thridNO):
        # 获取用户配置信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUserConfigByThird")

    def getUserInfoByThirdNo(self, thirdNO):
        # 根据用户名获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUserInfoByThirdNo")

    def getUserInfoByThirdNoAndOrgCode(self, orgCode, thirdNO):
        # 根据用户名和机构号获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUserInfoByThirdNoAndOrgCode")

    def getUserInfoThirdInfo(self, orgCode, thirdNO):
        # 根据用户名获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUserInfoThirdInfo")

    def selectUserInfo(self):
        # 根据token获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/selectUserInfo?0=61b9ee3ad031da7b01c6429d5ad3b21757ee9766d5b9e964a77ce621d29bbf7e296f482360155e6e01b29bc557eeedf702b643456ba5b39fe6febf284537a91f88468105d513684ae1abd790025a95df6590470dcc6c5a21c79a105cce1cdbdd5d45")

    def sysUser(self, id):
        # 单条查询
        return self.curl("GET", "/system/sysUser/" + str(id))



    # todo REST-系统信息表

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

    def sysSystem(self, Id):
        # 单条查询
        return self.curl("GET", "/system/sysSystem/?" + str(Id))



    # todo chc-auth, 登录模块

    def logined(self, userName):
        # 确认用户是否已经登录
        return self.curl("POST", '/auth/logined')

    def logout(self):
        # 登出
        return self.curl("DELETE", '/auth/logout')

    def refresh(self):
        # 刷新
        return self.curl("POST", '/auth/refresh')

    def thirdLogin(self, orgCode, thirdNo):
        # 第三方登录
        return self.curl("POST", '/auth/thirdLogin')


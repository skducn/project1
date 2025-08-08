# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2025-8-4
# Description   : CDRD加密接口测试
# 接口文档：http://192.168.0.243:8083/prod-api/doc.html#
# 接口json：http://192.168.0.243:8083/prod-api/v2/api-docs
# # 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
public_key ='04277bb3ea4a18b9e654d8c4bb1bd516b3a59591c320d6860fb46014c06d7e43074a181598a0c976a4da49050f54c9681b886d6d5e6eba0c2413d37eef7ba4c2e6'
private_key = '5034280c2b74c37289beaaa7edeed5d8fc7e9df12cf95db2800cc4b007e168e3'
# 注意：密文前加上04
# *****************************************************************

import subprocess, requests, json, os
from PO.DataPO import *
Data_PO = DataPO()

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
            # 注意：https://config.net.cn/tools/sm2.html的密文前加上04
            "password": "047e124d08fd45293beb1a6562d1f5a9961e85449187a974bad8405e9104c6f0472a9a7ae1f01397efb4296a75773ba98f868bc71c679c92b5e0a39215f59e773be3609ccda84ffa28cdd8c9f6cfd60a183a39c6172eac306452c030c3672b61976e441bcf301dfe77bd",
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

    def crtUser(self, varQty):

        # 批量创建用户
        # curl -X POST -H  "Accept:*/*" -H  "Authorization:eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoyNiwidXNlcl9rZXkiOiJlNGY0NzM4My01YWFjLTRlYmQtYmNmMS01ZThmZDA1YWQ2MTciLCJleHBpcmF0aW9uIjoiMzAiLCJ1c2VybmFtZSI6ImppbmhhbyJ9.o-8aGdZGBVPIRnXtotU4wPnr6T5SgqCogDRZ1CbTbcGA_IajxRRKjRkDlZpuUTjX4Sj8Pu0LSqK33XpPmP32NA" -H  "Content-Type:application/json" -d "{\"userId\":\"\",\"deptId\":\"\",\"userName\":\"lisi\",\"nickName\":\"lisi\",\"password\":\"\",\"phonenumber\":\"13636371322\",\"email\":\"yoyo@163.com.cn\",\"sex\":\"0\",\"status\":\"0\",\"remark\":\"我是哟哟\",\"postIds\":[],\"roleIds\":[6],\"departmentId\":31,\"departmentName\":\"科室\",\"departmentCode\":\"010\",\"jobNum\":\"3001\"}" "http://192.168.0.243:39210/system/user"
        #  -d "{\"userId\":\"\",\"deptId\":\"\",\"userName\":\"lisi\",\"nickName\":\"lisi\",\"password\":\"\",\"phonenumber\":\"13636371322\",
        #  \"email\":\"yoyo@163.com.cn\",\"sex\":\"0\",\"status\":\"0\",\"remark\":\"我是哟哟\",\"postIds\":[],\"roleIds\":[6],\"departmentId\":31,
        #  \"departmentName\":\"科室\",\"departmentCode\":\"010\",\"jobNum\":\"3001\"}" "http://192.168.0.243:39210/system/user"
        url = self.ipPort + "/system/user"
        headers = {
            'Accept': '*/*',
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }

        for i in range(varQty):

            varUserName = "tester" + str(i)
            varPhone = Data_PO.getPhone()
            varEmail = varPhone + "@163.com"
            varJob = 100000 + i
            data = {
                "userName": varUserName,
                "nickName": varUserName,
                "password": "",
                "phonenumber": varPhone,
                "email": varEmail,
                "sex": "1",
                "status": "0",
                "remark": "我是买手",
                "roleIds": [6],   # sys_role中 role_id=6 测试工程师
                "postIds": [],
                "departmentId": "31",   # sys_department中 department_id=31
                "departmentName": "科室",  # sys_department中 department_name=科室
                "departmentCode": "010",  # # sys_department中 department_code=010
                "jobNum": varJob,
                "pwdUpdateTime": "2033-12-12",
                "pwdNextUpdateTime": "2033-12-12"
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()  # 检查HTTP错误
                d_r = response.json()
                print(d_r)
                if d_r['code'] != 200:
                    return d_r
            except requests.RequestException as e:
                print(f"Request failed: {e}")
                return None
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Response content: {response.text}")
                return None


    def getPatientInfoPage(self):

        # 获取科室列表
        url = self.ipPort + "/cdrdPatientInfo/getPatientInfoPage"
        headers = {
            'Accept': '*/*',
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }

        data = {
            "current":1,
            "size":10,
            "endPatientVisitInTime":"",  # 结束就诊日期
            "patientDiagCode":"",  # ICD10编码
            "patientDiagName":"",  # 患者诊断
            "patientName":"",  # 患者姓名
            "patientOutHospitalDiag":"",  # 出院诊断
            "patientVisitDiag":"",  # 就诊诊断
            "startPatientVisitInTime":""  # 开始就诊日期
        }

        try:
            response = requests.post(url, headers=headers, json=data)
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

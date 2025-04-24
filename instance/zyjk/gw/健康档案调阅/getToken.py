# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 通过jar加密身份证（公卫健康档案身份证号码）生成token
# 生产 http://112.6.6.90:30080/
# 预生产 http://112.6.6.90:30081/
# 测试 http://192.168.0.201:30081/#/visit?idCard=110101199001012678
# 测试 http://192.168.0.201:30081/#/home?idCard=110101199001012678
# sqlserver: 192.168.0.234，sa，Zy_123456789

# 使用方法：用户名 身份证 手机号
# java -jar "generateToken-1.0-SNAPSHOT-jar-with-dependencies.jar"  11  370624196312230011  13863800179
# *****************************************************************

import subprocess, sys
command = "java -jar 'generateToken-1.0-SNAPSHOT-jar-with-dependencies.jar' 11 370624196312230011  13863800179"

p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
s_response = bytes.decode(out)
# print(s_response)  # Generated Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXRpZW50TmFtZSI6IjExIiwiaWRDYXJkIjoiMzcwNjI0MTk2MzEyMjMwMDExIiwiZXhwIjoxNzM3OTg2NTA1LCJpYXQiOjE3Mzc5ODI5MDUsInBob25lTm8iOiIxMzg2MzgwMDE3OSJ9.65w3zc2NbE59E8ft2J4m_oMVgiWq_KwhFpFVcjO2qvk
# print(s_response.split("Generated Token: ")[1])

url = "http://192.168.0.201:30081/#/?username=" + s_response.split("Generated Token: ")[1]
print(url)










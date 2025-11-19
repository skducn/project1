# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理 - 体重状态判断测试流程
# 【腾讯文档】体重管理1.18规则自动化
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=rprd0r

# 接口文档：http://192.168.0.243:8011/doc.html
# http://192.168.0.243:8011/chc-5g/v2/api-docs
# http://192.168.0.243:8011/chc-nehr/v2/api-docs
# http://192.168.0.243:8011/rules/v2/api-docs
# http://192.168.0.243:8011/server/v2/api-docs

# 接口地址：http://192.168.0.243:8014/doc.html#/default/Weight-%E4%BD%93%E9%87%8D%E6%8A%A5%E5%91%8A%E8%AE%B0%E5%BD%95%E8%A1%A8/saveOrUpdateWeightManageUsingPOST

# http://192.168.0.243:8014/auth/v2/api-docs
#***************************************************************

from WeightPO import *
Weight_PO = WeightPO()
import subprocess,json
# 参数
varBMI = 18.4

token = "eyJhbGciOiJIUzUxMiJ9.eyJhZmZpbGlhdGVkX2lkIjoiIiwidXNlcl9pZCI6ODIsImNhdGVnb3J5X2NvZGUiOiI0IiwidXNlcl9rZXkiOiI2ZmU5MjcyYi01ZWJhLTQ5MWMtYjM0ZS01NDZlMmNhMTA5OGMiLCJ0aGlyZF9ubyI6IjEyMzEyMzEiLCJob3NwaXRhbF9pZCI6IjAwMDAwMDEiLCJ1c2VybmFtZSI6IuWwj-iMhOWtkCIsImhvc3BpdGFsX25hbWUiOiLlrp3lsbHnpL7ljLrljavnlJ_mnI3liqHkuK3lv4MiLCJhZmZpbGlhdGVkX25hbWUiOiIifQ.yD5cGEiSdV69YLI2FTPiu8QN2zrNisAaZlMNqD0_q_aQM1HpWZcPUM0tzMQ5BMQudKdhc6dtw9ncVHsfBPOodQ"

# 跑接口
command = 'curl -X POST "http://192.168.0.243:8014/weight/saveOrUpdateWeightManage" -H "Request-Origion:SwaggerBootstrapUi" ' \
          '-H "accept:*/*" -H "Authorization:' + token + '" -H "Content-Type:application/json" ' \
          '-d "{\\"age\\":15,\\"ageFloat\\":0,\\"ageMonth\\":40,\\"basicIntake\\":100,\\"bmi\\":' + str(varBMI) + \
          ',\\"categoryCode\\":\\"4\\",\\"disease\\":\\"无\\",\\"foodAdvice\\":\\"建议饮食\\",\\"height\\":175,\\"hipline\\":33,' \
          '\\"id\\":2,\\"idCard\\":\\"420204202201011268\\",\\"orgCode\\":\\"0000001\\",\\"orgName\\":\\"静安精神病院\\",\\"sex\\":\\"男\\",' \
          '\\"sexCode\\":\\"1\\",\\"sportAdvice\\":\\"建议运动\\",\\"targetWeight\\":50,\\"waistHip\\":0.9,\\"waistline\\":33,\\"weight\\":55,\\"weightRecordId\\":0}"'
# print(command)
p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
str_r = bytes.decode(out)
d_r = json.loads(str_r)
print(d_r)

# 检查


# # # todo 2, 运行主程序
# Weight_PO.main(Configparser_PO.DB("table"), 'all')  # 执行全部记录







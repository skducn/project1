# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-3-6
# Description   : CHC 社区健康包，加密接口测试
# # 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
# *****************************************************************

import subprocess, requests, json
from PO.WebPO import *
from PO.ColorPO import *
Color_PO = ColorPO()

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlserverPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"))  # 测试环境

from BmiAgeSexPO import *
BmiAgeSex_PO = BmiAgeSexPO()

class ChcPO():

    def __init__(self, IDCARD):

        # 登录
        self.ipPort = "http://192.168.0.243:8014"

        # 检查身份证是否存在, WEIGHT_REPORT(体重报告记录表)和QYYH中都必须要有此身份证，且在WEIGHT_REPORT表中获取ID
        self.ID = self.isExist(IDCARD)
        self.IDCARD = IDCARD

    def generate_unmatched_cases2(self, conditions):
        """
        生成不满足指定条件的年龄、BMI、性别组合示例（年龄保留1位小数，BMI保留1位小数）

        参数:
            conditions: 条件列表，每个元素为一个条件子列表
                        格式如: [['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'], ...]

        返回:
            list: 不满足条件的组合示例列表
        """
        # 解析条件中的关键参数
        age_values = set()  # 存储具体的年龄值
        age_ranges = set()  # 存储年龄范围
        bmi_thresholds = {'男': {}, '女': {}}  # 按性别存储不同年龄区间的BMI阈值

        for cond in conditions:
            age_value = None
            age_min = None
            age_max = None
            bmi_min = None
            bmi_max = None
            gender = None

            for c in cond:
                if c.startswith('年龄='):
                    age_value = float(c.split('=')[1])
                    age_values.add(age_value)
                elif c.startswith('年龄>='):
                    age_min = float(c.split('>=')[1])
                elif c.startswith('年龄<'):
                    age_max = float(c.split('<')[1])
                elif c.startswith('BMI>='):
                    bmi_min = float(c.split('>=')[1])
                elif c.startswith('BMI<='):
                    bmi_max = float(c.split('<=')[1])
                elif c.startswith('BMI<'):
                    bmi_max = float(c.split('<')[1])
                elif c.startswith('性别='):
                    gender = c.split('=')[1]

            # 处理具体年龄值的情况
            if age_value is not None and gender is not None:
                bmi_range = {}
                if bmi_min is not None:
                    bmi_range['min'] = bmi_min
                if bmi_max is not None:
                    bmi_range['max'] = bmi_max
                if bmi_range:
                    bmi_thresholds[gender][age_value] = bmi_range
                    age_ranges.add((age_value, age_value))  # 将具体值转换为范围

            # 处理年龄范围的情况
            elif all(x is not None for x in [age_min, age_max, gender]):
                age_range = (age_min, age_max)
                age_ranges.add(age_range)
                bmi_range = {}
                if bmi_min is not None:
                    bmi_range['min'] = bmi_min
                if bmi_max is not None:
                    bmi_range['max'] = bmi_max
                if bmi_range:
                    bmi_thresholds[gender][age_range] = bmi_range

        # 如果没有解析到有效的条件，则返回空列表
        if not age_ranges:
            return []

        # 生成不满足条件的示例组合
        unmatched = []

        # 1. 年龄不在任何有效范围内
        if age_ranges:
            min_age = min(r[0] for r in age_ranges)
            max_age = max(r[1] for r in age_ranges)

            # 年龄低于最小范围
            test_age = round(min_age - 0.5, 1)
            sample_bmi = 15.0
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '男'
            })
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '女'
            })

            # 年龄高于最大范围
            test_age = round(max_age + 0.5, 1)
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '男'
            })
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '女'
            })

        # 2. 年龄在范围内但BMI不满足条件
        for gender in ['男', '女']:
            for age_key, bmi_range in bmi_thresholds[gender].items():
                # 确定测试年龄
                if isinstance(age_key, tuple):  # 年龄范围
                    test_age = round((age_key[0] + age_key[1]) / 2, 1)
                else:  # 具体年龄值
                    test_age = round(age_key, 1)

                # 生成不满足BMI条件的值
                if 'min' in bmi_range and 'max' in bmi_range:
                    # 既有最小值又有最大值，生成范围外的值
                    test_bmi_below = round(bmi_range['min'] - 0.1, 1)
                    test_bmi_above = round(bmi_range['max'], 1)  # 等于最大值时不满足条件
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi_below,
                        '性别': gender
                    })
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi_above,
                        '性别': gender
                    })
                elif 'min' in bmi_range:
                    # 只有最小值，生成小于最小值的BMI
                    test_bmi = round(bmi_range['min'] - 0.1, 1)
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi,
                        '性别': gender
                    })
                elif 'max' in bmi_range:
                    # 只有最大值，生成大于等于最大值的BMI
                    test_bmi = round(bmi_range['max'], 1)
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi,
                        '性别': gender
                    })

        return unmatched

    def _generate_test_data(self, l_interconvert_conditions):
        """生成测试数据"""
        # l_interconvert_conditions = ['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']
        for i in l_interconvert_conditions:
            # if ('>=' in i or '<=' in i) and ('年龄' in i or 'BMI' in i):
            if ('>=' in i or '<=' in i or '=' in i) and ('年龄' in i or 'BMI' in i or '性别' in i):
                return BmiAgeSex_PO.main(l_interconvert_conditions)
        return BmiAgeSex_PO.main(l_interconvert_conditions)

    def _format_conditions(self, l_value):
        """格式化条件"""
        l_conditions = []
        for i in l_value:
            if "BMI" in i or "年龄" in i:
                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                l_conditions.extend(l_split_conditions)
            elif "性别" in i:
                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                l_conditions.extend(l_split_conditions)
        return l_conditions

    def _parse_or_conditions(self, conditions):
        """解析包含or的条件"""
        l_value = conditions.split("or")
        l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
        l_value = [i.split("and") for i in l_value]
        # return [[item.strip() for item in sublist] for sublist in l_value]
        l_l_value = [[item.strip() for item in sublist] for sublist in l_value]

        # l_l_data = []

        # 正向测试（一条或多条）
        for lln, l_value in enumerate(l_l_value):
            # 格式化条件 - 1/2转换列表
            l_conditions = self._format_conditions(l_value)
            # 格式化条件 - 2/2转换位置（左边指标，右边数据）
            l_interconvert_conditions = []
            for i in l_conditions:
                l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                l_interconvert_conditions.extend(l_simple_conditions)
            # print(297, l_interconvert_conditions) # ['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']

            # 合并所有条件（用于反向测试）
            # l_l_data.append(l_interconvert_conditions)

            # 对单组条件（['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']）生成正向测试数据
            d_cases_p = self._generate_test_data(l_interconvert_conditions)
        return d_cases_p

    def _sm2(self, Web_PO):

        # 在线sm2加密/解密

        Web_PO.openURL("https://config.net.cn/tools/sm2.html")
        # 私钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[1]", private_key)
        # 公钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[2]", public_key)

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
        Web_PO = WebPO("noChrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", varEncrypt)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[2]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", "value")
        Web_PO.cls()
        return r



    def curl(self, varName, varMethod, varInterface, varParam=''):
        # curl("保存体重管理报告", "POST", "/server/weight/saveOrUpdateWeightManage",''{"age": 15, "ageFloat": 0')

        if varMethod == "GET":
            if varParam == '':
                command = "curl -X GET " + self.ipPort + varInterface + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
            else:
                command = "curl -X GET " + self.ipPort + varInterface + self.encrypt(varParam) + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
                print(varParam)
        elif varMethod == "POST":
            if varParam == '':
                command = "curl -X POST " + self.ipPort + varInterface + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
            else:
                command = "curl -X POST '" + self.ipPort + varInterface + "' -d '" + varParam + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
                # command = "curl -X POST " + self.ipPort + varInterface + " -d " + self.encrypt(varParam) + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
                if Configparser_PO.SWITCH("interface") == "on":
                    # s = "接口参数 =>" + varParam
                    Color_PO.outColor([{"34": command}])
                # Log_PO.logger.info("生成测试数据集 => " + str(varParam))

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)

        # 输出结果
        if d_r['code'] == 500:
            Color_PO.outColor([{"33": varName}, {"33": "=>"}, {"35": d_r}, {"35": "=>"}, {"34": command}])
        else:
            ...
            # Color_PO.outColor([{"35": varName}, {"35": "=>"}, {"38": d_r}])
            # print(varName + " =>", d_r)
        return d_r

    def curlLogin(self, account):

        # 登录
        # 注意需要关闭验证码
        encrypt_data = self.encrypt(account)

        command = "curl -X POST 'http://192.168.0.243:8011/auth/login' -d '" + encrypt_data + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json'"
        # command = "curl -X POST '" + self.ipPort + "/auth/login' -d '" + encrypt_data + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json'"
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        print(d_r)  # {'code': 200, 'msg': None, 'data': {'access_token': 'eyJhbGciOiJIUzUxMiJ9.eyJhZmZpbGlhdGVkX2lkIjoiIiwidXNlcl9pZCI6ODIsImNhdGVnb3J5X2NvZGUiOiIxIiwidXNlcl9rZXkiOiIwYzU3YmM3OC05OTNiLTQ1M2ItYjZkMC0yMmNlZTBhMWFkNzMiLCJ0aGlyZF9ubyI6IjEyMzEyMyIsImhvc3BpdGFsX2lkIjoiMDAwMDAwMSIsInVzZXJuYW1lIjoi5YiY5paM6b6ZIiwiaG9zcGl0YWxfbmFtZSI6IumdmeWuieeyvuelnueXhemZoiIsImFmZmlsaWF0ZWRfbmFtZSI6IiJ9.-xh2D7Obdensd3OcL_dqRaA7Qs4I0l0h--3ZYpYifgBZBP16Gzzq24W3IxS8c5ofcQTNyczRK2e3JipcCuyTqg', 'expires_in': 30}}
        try:
            self.token = d_r['data']['access_token']
            # print("token => ", self.token)
        except:
            # {'code': 500, 'msg': '非法参数！'}
            self.token = d_r['code']
        return self.token

    def isExist(self, idcard):
        # 检查身份证是否存在，QYYH，WEIGHT_REPORT
        l_d_1 = Sqlserver_PO.select("select count(*) as qty from QYYH where SFZH = '%s' " % (idcard))
        # print(l_d_1[0]['qty'])

        l_d_2 = Sqlserver_PO.select(
            "select ID, count(*) as qty from WEIGHT_REPORT where ID_CARD = '%s' GROUP BY ID" % (idcard))
        # print(l_d_2)
        # print(l_d_2[0]['qty'])
        # print(l_d_2[0]['ID'])

        if l_d_1[0]['qty'] == l_d_2[0]['qty'] and l_d_1[0]['qty'] == 1:
            return l_d_2[0]['ID']
        else:
            print("error, QYYH(SFZH字段) 或 WEIGHT_REPORT(ID_CARD字段)中身份证号不存在或多余1条!")
            sys.exit(0)

        # sys.exit(0)

    def assertWeightStatus(self, idcard, d_case, WEIGHT_STATUS):

        d_ = {}
        # 判断WEIGHT_REPORT 和 QYYH 中 WEIGHT_STATUS 值是否一致且是否与规则要求（体重偏低）一致
        l_d_1 = Sqlserver_PO.select("select WEIGHT_STATUS from QYYH where SFZH = '%s' " % (idcard))
        # print(154, l_d_1[0]['WEIGHT_STATUS'])

        l_d_2 = Sqlserver_PO.select(
            "select WEIGHT_STATUS from WEIGHT_REPORT where ID_CARD = '%s'" % (idcard))
        # print(158, l_d_2[0]['WEIGHT_STATUS'])

        if l_d_1[0]['WEIGHT_STATUS'] == l_d_2[0]['WEIGHT_STATUS'] and l_d_1[0]['WEIGHT_STATUS'] == WEIGHT_STATUS:
            # print("ok => ", case, "=> WEIGHT_STATUS =", WEIGHT_STATUS)
            d_['正向'] = "ok"
            d_['验证'] = d_case
            Color_PO.outColor([{"32": d_}])
            # s = "执行 => " + category + " & " + weightEvaluation + " => " + conditions + " => 验证：" + str(case)
            # Color_PO.outColor([{"35": s}])
        else:
            # s = "error => " + str(d_case) + " => 预期值：WEIGHT_STATUS = " + str(WEIGHT_STATUS) + "，" \
            #     "实际值：WEIGHT_STATUS = " + str(l_d_1[0]['WEIGHT_STATUS']) + "(QYYH) 且 WEIGHT_STATUS = " + str(l_d_2[0]['WEIGHT_STATUS']) + "(WEIGHT_REPORT) "
            # Color_PO.outColor([{"31": s}])
            d_['正向'] = "error"
            d_['验证'] = d_case
            d_['预期值WEIGHT_STATUS'] = WEIGHT_STATUS
            d_['实际值QYYH__WEIGHT_STATUS'] = l_d_1[0]['WEIGHT_STATUS']
            d_['实际值WEIGHT_REPORT__WEIGHT_STATUS'] = l_d_2[0]['WEIGHT_STATUS']
            Color_PO.outColor([{"31": d_}])

            # print("error, QYYH 与 WEIGHT_REPORT 中 WEIGHT_STATUS值不一致 或 WEIGHT_STATUS 不等于预期值!")
            # sys.exit(0)

        # sys.exit(0)

    def main(self, category, weightEvaluation, l_conditions):
        # category = "7-17岁学生"
        # weightEvaluation = "体重偏低"
        # l_conditions = ['(7<= 年龄 < 7.5 and BMI>=18.7 and 性别 = 男)', '(7.5<= 年龄 < 8 and BMI>=19.2 and 性别 = 男)', '(8<= 年龄 < 8.5 and BMI>=19.7 and 性别 = 男)']

        # 字典映射
        d_category = {1: '0-6岁儿童', 2: '7-17岁学生', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}
        categoryCode = next(k for k, v in d_category.items() if v == category)



        # todo 正向（单组）
        # 如：(7<= 年龄 < 8 and 13.9>BMI and 性别 = 男)
        s = "开始 => " + category + " & " + weightEvaluation
        Color_PO.outColor([{"35": s}])

        for index,conditions in enumerate(l_conditions):
        # for conditions in l_conditions:
            l_l_value = self._parse_or_conditions(conditions)
            # print(l_l_value['satisfied'])  # [{'年龄': 7.1, 'BMI': 3.8, '性别': '男'}, {'年龄': 7.0, 'BMI': 3.8, '性别': '男'}]
            l_d_case = l_l_value['satisfied']
            # print("条件" + str(index+1) + " => " +  conditions, "，生成测试数据集 =>", l_d_case)
            print("条件" + str(index+1) + " => " + conditions)

            # l_d_case = [{'年龄': 7, 'BMI': 13.3, '性别': '男'}, {'年龄': 6, 'BMI': 13.3, '性别': '男'}]
            # todo 3 遍历测试数据
            for case in l_d_case:
                if case['性别'] == '男':
                    i_sex = 1
                else:
                    i_sex = 2

                # 人群分类
                if categoryCode == 1:
                    # 儿童
                    age = 0
                    ageFloat = 0
                    ageMonth = case['年龄']
                elif categoryCode == 2:
                    # 学生
                    age = 0
                    ageFloat = case['年龄']
                    ageMonth = 0
                else:
                    # 其他
                    age = case['年龄']
                    ageFloat = 0
                    ageMonth = 0

                # todo 3.1 执行 - 保存体重管理报告接口 (Weight-体重报告记录表)
                result = self.curl("保存体重管理报告", "POST", "/weight/saveOrUpdateWeightManage",
                                     '{\"age\": ' + str(age) + ', \"ageFloat\": ' + str(
                                         ageFloat) + ', \"ageMonth\": ' + str(ageMonth) + ','
                                                                                          '\"basicIntake\": 100, \"bmi\": ' + str(
                                         case['BMI']) + ',\"categoryCode\": \"' + str(categoryCode) + '\",'
                                                                                                      '\"disease\": \"无\",\"foodAdvice\": \"建议饮食\",\"height\": 175,\"hipline\": 33,'
                                                                                                      '\"id\": ' + str(
                                         self.ID) + ',\"idCard": \"' + str(
                                         self.IDCARD) + '\","orgCode\": \"0000001\",\"orgName\": \"静安精神病院\",'
                                                   '\"sex\": \"' + str(case['性别']) + '\","sexCode": \"' + str(
                                         i_sex) + '\",\"sportAdvice\": \"建议运动\",\"targetWeight\": 50,\"waistHip\": 0.90,\"waistline\": 33,\"weight\": 55,\"weightRecordId\": 0}'
                                     )
                # print(result)

                # # todo 3.2 判断WEIGHT_REPORT 和 QYYH 中 WEIGHT_STATUS值是否一致且是否与规则要求（体重偏低）一致
                # # 体重状态：WEIGHT_STATUS = 0-未评估 1-体重偏低 2-正常 3-超重 4-肥胖 5-孕期体重增长过快
                d_weightEvaluation = {0: '未评估', 1: '体重偏低', 2: '正常', 3: '超重', 4: '肥胖', 5: '孕期体重增长过快'}
                weightEvaluationCode = next(k for k, v in d_weightEvaluation.items() if v == weightEvaluation)
                self.assertWeightStatus(self.IDCARD, case, weightEvaluationCode)



        # todo 反向（所有组合）
        # 字符串转换列表，将'(7<= 年龄 < 7.5 and BMI>=18.7 and 性别 = 男)' 转为 ['7<= 年龄 < 7.5 ', ' BMI>=18.7 ', ' 性别 = 男']
        l_l_conditions = []
        d_cases_n = {}
        l_l_data = []
        for s_conditions in l_conditions:
            s_conditions = s_conditions.replace("(", "").replace(")", "").replace(" ", "")
            l_s_conditions = s_conditions.split("and")
            # print(l_s_conditions)
            l_l_conditions.append(l_s_conditions)
        # print(l_l_conditions)  # [['7<=年龄<7.5', 'BMI>=18.7', '性别=男'], ['7.5<=年龄<8', 'BMI>=19.2', '性别=男'], ['8<=年龄<8.5', 'BMI>=19.7', '性别=男']]
        for lln, l_value in enumerate(l_l_conditions):
            # 格式化条件 - 1/2转换列表
            l_conditions2 = self._format_conditions(l_value)
            # 格式化条件 - 2/2转换位置（左边指标，右边数据）
            l_interconvert_conditions = []
            for i in l_conditions2:
                l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                l_interconvert_conditions.extend(l_simple_conditions)
            # print(297, l_interconvert_conditions) # ['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']
            # 合并所有条件（用于反向测试）
            l_l_data.append(l_interconvert_conditions)
        # print(l_l_data)  # [['年龄>=7', '年龄<7.5', 'BMI>=18.7', '性别=男'], ['年龄>=7.5', '年龄<8', 'BMI>=19.2', '性别=男']]
        l_d_cases = self.generate_unmatched_cases2(l_l_data)
        d_cases_n['satisfied'] = []
        d_cases_n['notSatisfied'] = l_d_cases
        # print(310, d_cases_n)  # {'satisfied': [], 'notSatisfied': [{'年龄': 6.5, 'BMI': 15.0, '性别': '男'},

        # print(d_cases_n['notSatisfied'])  # [{'年龄': 6.5, 'BMI': 15.0, '性别': '男'}, {'年龄': 6.5, 'BMI': 15.0, '性别': '女'},
        l_d_case = d_cases_n['notSatisfied']

        # todo 3 遍历测试数据
        for case in l_d_case:
            if case['性别'] == '男':
                i_sex = 1
            else:
                i_sex = 2

            # 人群分类
            if categoryCode == 1:
                # 儿童
                age = 0
                ageFloat = 0
                ageMonth = case['年龄']
            elif categoryCode == 2:
                # 学生
                age = 0
                ageFloat = case['年龄']
                ageMonth = 0
            else:
                # 其他
                age = case['年龄']
                ageFloat = 0
                ageMonth = 0

            # todo 3.1 执行 - 保存体重管理报告接口 (Weight-体重报告记录表)
            result = self.curl("保存体重管理报告", "POST", "/weight/saveOrUpdateWeightManage",
                               '{\"age\": ' + str(age) + ', \"ageFloat\": ' + str(
                                   ageFloat) + ', \"ageMonth\": ' + str(ageMonth) + ','
                                                                                    '\"basicIntake\": 100, \"bmi\": ' + str(
                                   case['BMI']) + ',\"categoryCode\": \"' + str(categoryCode) + '\",'
                                                                                                '\"disease\": \"无\",\"foodAdvice\": \"建议饮食\",\"height\": 175,\"hipline\": 33,'
                                                                                                '\"id\": ' + str(
                                   self.ID) + ',\"idCard": \"' + str(
                                   self.IDCARD) + '\","orgCode\": \"0000001\",\"orgName\": \"静安精神病院\",'
                                                  '\"sex\": \"' + str(case['性别']) + '\","sexCode": \"' + str(
                                   i_sex) + '\",\"sportAdvice\": \"建议运动\",\"targetWeight\": 50,\"waistHip\": 0.90,\"waistline\": 33,\"weight\": 55,\"weightRecordId\": 0}'
                               )
            # print(result)

            # # todo 3.2 判断WEIGHT_REPORT 和 QYYH 中 WEIGHT_STATUS值是否一致且是否与规则要求（体重偏低）一致
            # # 体重状态：WEIGHT_STATUS = 0-未评估 1-体重偏低 2-正常 3-超重 4-肥胖 5-孕期体重增长过快
            d_weightEvaluation = {0: '未评估', 1: '体重偏低', 2: '正常', 3: '超重', 4: '肥胖', 5: '孕期体重增长过快'}
            weightEvaluationCode = next(k for k, v in d_weightEvaluation.items() if v == weightEvaluation)
            self.assertWeightStatus(self.IDCARD, case, weightEvaluationCode)



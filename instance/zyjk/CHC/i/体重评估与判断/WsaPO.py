# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-3-6
# Description   : CHC 社区健康包，加密接口测试
# # 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
# *****************************************************************

from PO.WebPO import *

from PO.ColorPO import *
Color_PO = ColorPO()

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlserverPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database2"))  # 测试环境

from BmiAgeSexPO import *
BmiAgeSex_PO = BmiAgeSexPO()

from BmiPO import *
Bmi_PO = BmiPO()

class WsaPO():

    def __init__(self):

        # 登录
        self.ipPort = "http://192.168.0.243:8014"

        # 检查身份证是否存在, WEIGHT_REPORT(体重报告记录表)和QYYH中都必须要有此身份证，且在WEIGHT_REPORT表中获取ID
        self.IDCARD, self.ID = self.getIdcard()
        self.tableWSA = Configparser_PO.DB("tableWSA")
        self.sheetWSA = Configparser_PO.FILE("sheetWSA")
        self.case = Configparser_PO.FILE("case")

        self.username = Configparser_PO.ACCOUNT("username")
        self.password = Configparser_PO.ACCOUNT("password")
        self.curlLogin()

    def getIdcard(self):
        # 自动获取身份证号，从QYYH和WEIGHT_REPORT中匹配相同身份证，同时获取WEIGHT_REPORT（ID）

        l_d_1 = Sqlserver_PO.select("select SFZH from QYYH ")
        l_d_2 = Sqlserver_PO.select("select ID_CARD from WEIGHT_REPORT ")
        set_QYYH = {item['SFZH'] for item in l_d_1 if item['SFZH'] not in ('', None, 0)}
        set_WEIGHT_REPORT = {item['ID_CARD'] for item in l_d_2 if item['ID_CARD'] not in ('', None, 0)}
        set_ = set_QYYH & set_WEIGHT_REPORT
        if set_:  # 如果交集非空
            IDCARD = list(set_)[0]
            l_d_2 = Sqlserver_PO.select("select ID from WEIGHT_REPORT where ID_CARD='%s'" % (IDCARD))
            ID = l_d_2[0]['ID']
            return IDCARD, ID
        else:  # 如果交集为空（即 set()）
            print("error, QYYH(SFZH字段) 与 WEIGHT_REPORT(ID_CARD字段)中没有相同的身份证号!")
            sys.exit(0)


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
    def curlLogin(self):

        # 登录
        # 注意需要关闭验证码
        # Chc_PO.curlLogin('{"username": "lbl","password": "Qa@123456"}')
        account = '{"username": "' + self.username + '", "password": "' + self.password + '"}'
        encrypt_data = self.encrypt(account)

        command = "curl -X POST 'http://192.168.0.243:8011/auth/login' -d '" + encrypt_data + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json'"
        # command = "curl -X POST '" + self.ipPort + "/auth/login' -d '" + encrypt_data + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json'"
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)  # {'code': 200, 'msg': None, 'data': {'access_token': 'eyJhbGciOiJIUzUxMiJ9.eyJhZmZpbGlhdGVkX2lkIjoiIiwidXNlcl9pZCI6ODIsImNhdGVnb3J5X2NvZGUiOiIxIiwidXNlcl9rZXkiOiIwYzU3YmM3OC05OTNiLTQ1M2ItYjZkMC0yMmNlZTBhMWFkNzMiLCJ0aGlyZF9ubyI6IjEyMzEyMyIsImhvc3BpdGFsX2lkIjoiMDAwMDAwMSIsInVzZXJuYW1lIjoi5YiY5paM6b6ZIiwiaG9zcGl0YWxfbmFtZSI6IumdmeWuieeyvuelnueXhemZoiIsImFmZmlsaWF0ZWRfbmFtZSI6IiJ9.-xh2D7Obdensd3OcL_dqRaA7Qs4I0l0h--3ZYpYifgBZBP16Gzzq24W3IxS8c5ofcQTNyczRK2e3JipcCuyTqg', 'expires_in': 30}}
        try:
            self.token = d_r['data']['access_token']
            # print("token => ", self.token)
        except:
            # {'code': 500, 'msg': '非法参数！'}
            self.token = d_r['code']
        return self.token


    def _assertWeightStatus(self, caseType, l_rule, d_case, WEIGHT_STATUS):

        d_ = {}
        # 判断WEIGHT_REPORT 和 QYYH 中 WEIGHT_STATUS 值是否一致且是否与规则要求（体重偏低）一致
        l_d_1 = Sqlserver_PO.select("select WEIGHT_STATUS from QYYH where SFZH = '%s' " % (self.IDCARD))
        l_d_2 = Sqlserver_PO.select("select WEIGHT_STATUS from WEIGHT_REPORT where ID_CARD = '%s'" % (self.IDCARD))

        # 正向用例
        if caseType == "p":
            if l_d_1[0]['WEIGHT_STATUS'] == l_d_2[0]['WEIGHT_STATUS'] and l_d_1[0]['WEIGHT_STATUS'] == WEIGHT_STATUS:
                # print("ok => ", case, "=> WEIGHT_STATUS =", WEIGHT_STATUS)
                d_['正向'] = "ok"
                d_['验证'] = d_case
                if Configparser_PO.SWITCH("only_print_error") == "off":
                    Color_PO.outColor([{"32": d_}])
                return 1
            else:
                d_['正向'] = "error"
                d_['规则'] = l_rule
                d_['验证'] = d_case
                d_['预期值WEIGHT_STATUS'] = WEIGHT_STATUS
                d_['实际值QYYH__WEIGHT_STATUS'] = l_d_1[0]['WEIGHT_STATUS']
                d_['实际值WEIGHT_REPORT__WEIGHT_STATUS'] = l_d_2[0]['WEIGHT_STATUS']
                Color_PO.outColor([{"31": d_}])
                return d_
        elif caseType == "n":
            # 反向用例
            if l_d_1[0]['WEIGHT_STATUS'] == l_d_2[0]['WEIGHT_STATUS'] and l_d_1[0]['WEIGHT_STATUS'] == WEIGHT_STATUS:
                # print("ok => ", case, "=> WEIGHT_STATUS =", WEIGHT_STATUS)
                d_['反向'] = "error"
                d_['验证'] = d_case
                d_['预期值WEIGHT_STATUS'] = WEIGHT_STATUS
                d_['实际值QYYH__WEIGHT_STATUS'] = l_d_1[0]['WEIGHT_STATUS']
                d_['实际值WEIGHT_REPORT__WEIGHT_STATUS'] = l_d_2[0]['WEIGHT_STATUS']
                Color_PO.outColor([{"31": d_}])
                return d_
            else:
                d_['反向'] = "ok"
                d_['验证'] = d_case
                if Configparser_PO.SWITCH("only_print_error") == "off":
                    Color_PO.outColor([{"36": d_}])
                return 1
    def _curl(self, varName, varMethod, varInterface, varParam=''):
        # _curl("保存体重管理报告", "POST", "/server/weight/saveOrUpdateWeightManage",''{"age": 15, "ageFloat": 0')

        if varMethod == "GET":
            if varParam == '':
                command = "curl -X GET " + self.ipPort + varInterface + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
            else:
                command = "curl -X GET " + self.ipPort + varInterface + self.encrypt(varParam) + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
                # print(varParam)
        elif varMethod == "POST":
            if varParam == '':
                command = "curl -X POST " + self.ipPort + varInterface + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
            else:
                command = "curl -X POST '" + self.ipPort + varInterface + "' -d '" + varParam + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"
                # command = "curl -X POST " + self.ipPort + varInterface + " -d " + self.encrypt(varParam) + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Content-Type:application/json' -H 'Authorization:" + self.token + "'"

        if Configparser_PO.SWITCH("print_curl") == "on":
            Color_PO.outColor([{"34": command}])
        # Log_PO.logger.info("生成测试数据集 => " + str(varParam))

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)
        # 输出结果
        if d_r['code'] != 200:
            Color_PO.outColor([{"33": varName}, {"33": "=>"}, {"35": d_r}, {"35": "=>"}, {"34": command}])
        return d_r
    def _run(self, caseType, l_rule, l_d_case, categoryCode, weightStatusCode):

        l_log = []
        # caseType用例类型 ： p 或 n
        # l_d_case = [{'年龄': 7, 'BMI': 13.3, '性别': '男'}, {'年龄': 6, 'BMI': 13.3, '性别': '男'}]
        # todo 3 遍历测试数据
        for d_case in l_d_case:
            if '性别' in d_case:
                if d_case['性别'] == '男':
                    sex = '男'
                    sexCode = 1
                else:
                    sex = '女'
                    sexCode = 2
            else:
                sex = '男'
                sexCode = 1  # 默认为男

            # 人群分类
            if categoryCode == 1:
                # 儿童
                age = 0
                ageFloat = 0
                ageMonth = d_case['年龄']
            elif categoryCode == 2:
                # 学生
                age = 0
                ageFloat = d_case['年龄']
                ageMonth = 0
            elif categoryCode == 3:
                # 普通人群
                age = 30
                ageFloat = 0
                ageMonth = 0
            elif categoryCode == 4:
                # 老年人
                age = 70
                ageFloat = 0
                ageMonth = 0

            # todo 3.1 执行 - 保存体重管理报告接口 (Weight-体重报告记录表)
            result = self._curl("保存体重管理报告", "POST", "/weight/saveOrUpdateWeightManage",
                                 '{\"age\": ' + str(age) + ', \"ageFloat\": ' + str(
                                     ageFloat) + ', \"ageMonth\": ' + str(ageMonth) + ','
                                                                                      '\"basicIntake\": 100, \"bmi\": ' + str(
                                     d_case['BMI']) + ',\"categoryCode\": \"' + str(categoryCode) + '\",'
                                                                                                  '\"disease\": \"无\",\"foodAdvice\": \"建议饮食\",\"height\": 175,\"hipline\": 33,'
                                                                                                  '\"id\": ' + str(
                                     self.ID) + ',\"idCard": \"' + str(
                                     self.IDCARD) + '\","orgCode\": \"0000001\",\"orgName\": \"静安精神病院\",'
                                               '\"sex\": \"' + str(sex) + '\","sexCode": \"' + str(
                                     sexCode) + '\",\"sportAdvice\": \"建议运动\",\"targetWeight\": 50,\"waistHip\": 0.90,\"waistline\": 33,\"weight\": 55,\"weightRecordId\": 0}'
                                 )
            # print(result)

            # # todo 3.2 判断WEIGHT_REPORT 和 QYYH 中 WEIGHT_STATUS值是否一致且是否与规则要求（体重偏低）一致
            # # 体重状态：WEIGHT_STATUS = 0-未评估 1-体重偏低 2-正常 3-超重 4-肥胖 5-孕期体重增长过快
            result = self._assertWeightStatus(caseType, l_rule, d_case, weightStatusCode)
            if isinstance(result, dict):
                l_log.append(result)
        return l_log

    def _generate_unmatched_data_children(self, l_l_rule2):
        """
        生成不满足指定条件的年龄、BMI、性别组合示例（针对儿童，年龄使用整数）

        参数:
            l_l_rule2: 条件列表，每个元素为一个条件子列表
                        格式如: [['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'], ...]

        返回:
            dict: 包含满足和不满足条件的组合示例字典
        """
        d_cases_n = {}

        # 解析条件中的关键参数
        age_values = set()  # 存储具体的年龄值
        age_ranges = set()  # 存储年龄范围
        bmi_thresholds = {'男': {}, '女': {}}  # 按性别存储不同年龄区间的BMI阈值

        for cond in l_l_rule2:
            age_value = None
            age_min = None
            age_max = None
            bmi_min = None
            bmi_max = None
            gender = None

            for c in cond:
                c = c.replace("月", "")
                if c.startswith('年龄='):
                    age_value = int(float(c.split('=')[1]))  # 转换为整数
                    age_values.add(age_value)
                elif c.startswith('年龄>='):
                    age_min = int(float(c.split('>=')[1]))  # 转换为整数
                elif c.startswith('年龄<'):
                    age_max = int(float(c.split('<')[1]))  # 转换为整数
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

        # 1. 年龄不在任何有效范围内（使用整数）
        if age_ranges:
            min_age = min(r[0] for r in age_ranges)
            max_age = max(r[1] for r in age_ranges)

            # 年龄低于最小范围（使用整数）
            test_age = min_age - 1
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

            # 年龄高于最大范围（使用整数）
            test_age = max_age + 1
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
                # 确定测试年龄（使用整数）
                if isinstance(age_key, tuple):  # 年龄范围
                    test_age = int((age_key[0] + age_key[1]) // 2)  # 使用整数
                else:  # 具体年龄值
                    test_age = int(age_key)  # 使用整数

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

        d_cases_n['satisfied'] = []
        d_cases_n['notSatisfied'] = unmatched
        return d_cases_n
    def _generate_unmatched_data_student(self, l_l_rule2):
        """
        生成不满足指定条件的年龄、BMI、性别组合示例（年龄保留1位小数，BMI保留1位小数）

        参数:
            l_l_rule2: 条件列表，每个元素为一个条件子列表
                        格式如: [['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'], ...]

        返回:
            list: 不满足条件的组合示例列表
        """
        d_cases_n = {}

        # 解析条件中的关键参数
        age_values = set()  # 存储具体的年龄值
        age_ranges = set()  # 存储年龄范围
        bmi_thresholds = {'男': {}, '女': {}}  # 按性别存储不同年龄区间的BMI阈值

        for cond in l_l_rule2:
            age_value = None
            age_min = None
            age_max = None
            bmi_min = None
            bmi_max = None
            gender = None

            for c in cond:
                c = c.replace("月", "")
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

        d_cases_n['satisfied'] = []
        d_cases_n['notSatisfied'] = unmatched
        return d_cases_n
    def _generate_matched_data(self, l_interconvert_conditions):
        # 生成测试数据
        # l_interconvert_conditions = ['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']
        for i in l_interconvert_conditions:
            if ('>=' in i or '<=' in i or '=' in i) and ('年龄' in i or 'BMI' in i or '性别' in i):
                return BmiAgeSex_PO.float(l_interconvert_conditions)
        return BmiAgeSex_PO.float(l_interconvert_conditions)
    def _format_bmi_age_gender(self, l_one_rule):
        """格式化BMI，年龄，性别"""
        # l_value = ['7<=年龄<8', '13.9>BMI', '性别=男']

        # 拆分年龄
        l_one_rule_split = []
        for i in l_one_rule:
            if "BMI" in i or "年龄" in i:
                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                l_one_rule_split.extend(l_split_conditions)
            elif "性别" in i:
                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                l_one_rule_split.extend(l_split_conditions)
        # l_one_rule_split = ['年龄>=7', '年龄<8', '13.9>BMI', '性别=男']

        # 置换位置 -（左边指标，右边数据）
        l_one_rule_split_interconvert = []
        for i in l_one_rule_split:
            l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
            l_one_rule_split_interconvert.extend(l_simple_conditions)
        # print(l_one_rule_split_interconvert)  # ['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']
        return l_one_rule_split_interconvert
    def _s_rule2l_rule(self, f_rule):
        # 将字符串转列表，解析包含or的规则
        # 如：(7<=年龄<8 and 13.9>BMI and 性别=男) or (8<=年龄<9 and 14.0>BMI and 性别=男)

        l_value = f_rule.split("or")
        l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
        l_value = [i.split("and") for i in l_value]
        l_l_rule = [[item.strip() for item in sublist] for sublist in l_value]
        return l_l_rule
    def main_one(self, id):

        # {1: '0-6岁儿童', 2: '7-17岁学生', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}

        l_d_ = Sqlserver_PO.select("select category, categoryCode, weightStatus, weightStatusCode, f_rule from %s where id=%s" % (self.tableWSA, id))
        category = l_d_[0]['category']
        categoryCode = int(l_d_[0]['categoryCode'])
        weightStatus = l_d_[0]['weightStatus']
        weightStatusCode = int(l_d_[0]['weightStatusCode'])
        s_rule = l_d_[0]['f_rule']
        # print("原始 =>", s_rule)

        # 格式化数据1, 将 f_value 转列表
        l_l_rule = self._s_rule2l_rule(s_rule)
        # print("格式化1 =>",  l_l_rule)  #  [['7<=年龄<8', '13.9>BMI', '性别=男'], ['8<=年龄<9', '14.0>BMI', '性别=男']。。。
        # 格式化数据2, 最终
        l_l_rule2 = []
        for lln, l_value in enumerate(l_l_rule):
            # 格式化BMI，年龄，性别
            l_one_rule_split_interconvert = self._format_bmi_age_gender(l_value)
            # print(l_one_rule_split_interconvert)  # ['年龄>=7', '年龄<8', '13.9>BMI', '性别=男']
            l_l_rule2.append(l_one_rule_split_interconvert)
        # print("格式化2 =>",  l_l_rule2)  # [['年龄>=7', '年龄<8', 'BMI<13.9', '性别=男'], ['年龄>=8', '年龄<9', 'BMI<14.0', '性别=男'], ...

        s = "体重状态判断 => {'id': " + str(id) + "} => " + category + " & " + weightStatus + " => " + s_rule
        Color_PO.outColor([{"35": s}])

        l_log = []

        # todo 正向p（单组）
        # 如：(7<= 年龄 < 8 and 13.9>BMI and 性别 = 男)
        if Configparser_PO.SWITCH("run_p") == "on":
            qty_l_l_rule2 = len(l_l_rule2)

            # 对单组条件（['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']）生成正向测试数据
            for index, l_rule in enumerate(l_l_rule2):
                if Configparser_PO.SWITCH("only_print_error") == "off":
                    print("单组" + str(index+1) + "/" + str(qty_l_l_rule2) + " => " + str(l_rule))

                # 生成正向有效数据
                d_cases_p = self._generate_matched_data(l_rule)
                l_d_case = d_cases_p['satisfied']
                # print("生成正向有效数据 =>", l_d_case)  # {'年龄': 6.5, 'BMI': 15.0, '性别': '男'},

                # 跑接口
                l_log_p = self._run("p", str(l_rule), l_d_case, categoryCode, weightStatusCode)
                if l_log_p != []:
                    l_log.append(l_log_p)


        # todo 反向n（全组）
        # 字符串转换列表，将'(7<= 年龄 < 7.5 and BMI>=18.7 and 性别 = 男)' 转为 ['7<= 年龄 < 7.5 ', ' BMI>=18.7 ', ' 性别 = 男']
        if Configparser_PO.SWITCH("run_n") == "on":
            d_cases_n = {}
            if categoryCode == 3 or categoryCode == 4:
                # 普通人群和老年人，只需要处理bmi
                d_cases_n = Bmi_PO.generate_all_cases(l_l_rule2[0])  # {'satisfied': [{'BMI': 14.1}], 'notSatisfied': [{'BMI': 42.1}]}
                l_d_case = d_cases_n['notSatisfied']
            else:
                # 儿童和学生，需要处理年龄和bmi
                # 生成反向不匹配数据
                if categoryCode == 1:
                    # 儿童（月龄0-84）
                    d_cases_n = self._generate_unmatched_data_children(l_l_rule2)
                    l_d_case = d_cases_n['notSatisfied']
                    # 业务逻辑要求，儿童的反向值不能是 小于1个月 或 大于84岁 值
                    l_d_case = [d for d in l_d_case if d['年龄'] >= 1 and d['年龄'] < 85]
                elif categoryCode == 2:
                    # 学生 （年龄大于等于7且小于等于18岁）
                    d_cases_n = self._generate_unmatched_data_student(l_l_rule2)
                    l_d_case = d_cases_n['notSatisfied']
                    # 业务逻辑要求，学生的反向值不能是 小于7岁 或 大于18岁 值
                    l_d_case = [d for d in l_d_case if d['年龄'] >= 7 and d['年龄'] < 18]
                    # print(660, l_d_case)

            if Configparser_PO.SWITCH("only_print_error") == "off":
                print("全组 => " + str(l_l_rule2))
                print("生成反向无效数据 =>", l_d_case)  # [{'年龄': 6.5, 'BMI': 15.0, '性别': '男'}, {'年龄': 6.5, 'BMI': 15.0, '性别': '女'},

            # 跑接口
            l_log_n = self._run("n", l_l_rule2, l_d_case, categoryCode, weightStatusCode)
            if l_log_n != []:
                l_log.append(l_log_n)

        # 写DB
        if l_log == []:
            Sqlserver_PO.execute("update %s set result = '%s', updateDate = GETDATE(), log=Null where id = %s" %(self.tableWSA, 'ok', id))
        else:
            # 将日志列表转换为JSON字符串存储
            log_json = json.dumps(l_log, ensure_ascii=False)
            # 转义单引号以避免SQL语法错误
            escaped_log = log_json.replace("'", "''")
            Sqlserver_PO.execute("update %s set result = '%s', updateDate = GETDATE(), log='%s' where id = %s"
                                 % (self.tableWSA, 'error', escaped_log, id))

    def main_multiple(self, l_id):

        # l_id = [1,2,3,4]
        # {1: '0-6岁儿童', 2: '7-17岁学生', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}

        for id in l_id:
            self.main_one(id)


    def main(self, d_=None):
        # Wsa_PO.main({"id": 1})
        # Wsa_PO.main({"category": '学生'})
        # Wsa_PO.main({"weightStatus": '体重偏低'})
        # Wsa_PO.main({"category": '学生', "weightStatus": '体重偏低'})

        if isinstance(d_, dict):
            if 'id' in d_:
                # 执行多条，如：{'id': [1, 3]}
                if isinstance(d_['id'], list):
                    self.main_multiple(d_['id'])
                else:
                    # 执行一条(id)，如：{'id': 56}
                    # 判断id是否溢出
                    l_d_row = Sqlserver_PO.select("select * from %s" % (self.tableWSA))
                    i_records = len(l_d_row)
                    if d_['id'] > i_records or d_['id'] <= 0:
                        # 异常退出
                        print("[Error] 输入的ID超出" + str(i_records) + "条范围！")
                        sys.exit(0)
                    else:
                        self.main_one(d_['id'])
            elif 'category' in d_ and 'weightStatus' in d_:
                # 执行一条
                # Wsa_PO.main({"category": '学生', "weightStatus": '体重偏低'})
                l_d_ = Sqlserver_PO.select("select id from %s where category='%s' and weightStatus='%s'" % (self.tableWSA, d_['category'], d_['weightStatus']))
                self.main_one(l_d_[0]['id'])
            else:
                # 执行多条
                if 'category' in d_:
                    # Wsa_PO.main({"category": '学生'})  # 执行所有学生
                    l_d_ = Sqlserver_PO.select("select id from %s where category='%s'" % (self.tableWSA, d_['category']))
                    # print(l_d_)  # [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}]
                    l_id = [item['id'] for item in l_d_]
                    # print(l_id)  # 输出：[1, 2, 3, 4]
                    self.main_multiple(l_id)
                elif 'weightStatus' in d_:
                    # Wsa_PO.main({"weightStatus": '体重偏低'}) # 执行所有体重偏低
                    l_d_ = Sqlserver_PO.select("select id from %s where weightStatus='%s'" % (self.tableWSA, d_['weightStatus']))
                    l_id = [item['id'] for item in l_d_]
                    # print(l_id)  # 输出：[1, 2, 3, 4]
                    self.main_multiple(l_id)
                else:
                    print("warning, 参数不正确！")
                    sys.exit(0)
        else:
            # 执行所有，如：{'id': 'all'}
            l_d_ = Sqlserver_PO.select("select id from %s " % (self.tableWSA))
            l_id = [item['id'] for item in l_d_]
            # print(l_id)  # 输出：[1, 2, 3, 4]
            self.main_multiple(l_id)


    def excel2db(self):
        """excel文件导入db"""
        try:

            # 1, db中删除已有的表
            Sqlserver_PO.execute("drop table if exists " + self.tableWSA)

            # 读取 Excel 文件
            df = pd.read_excel(self.case, sheet_name=self.sheetWSA)
            df = df.sort_index()  # 按行索引排序，保持Excel原有顺序
            df = df.dropna(how="all")  # 移除全空行

            # 手动设置字段类型
            # df['conditions'] = df['conditions'].astype(str)  # 改为字符串类型

            # 2, excel导入db
            Sqlserver_PO.df2db(df, self.tableWSA)

            # 3, 设置表注释
            Sqlserver_PO.setTableComment(self.tableWSA, '体重管理_体重状态判断_自动化测试')

            # 4， f_rule，替换换行符为空格
            Sqlserver_PO.execute("UPDATE %s SET f_rule = REPLACE(REPLACE(f_rule, CHAR(10), ' '), CHAR(13), ' ');" % (self.tableWSA))

            # 5, 设置字段类型与描述
            field_definitions = [
                ('result', 'nvarchar(10)', '测试结果'),
                ('updateDate', 'nvarchar(50)', '更新日期'),
                ('log', 'varchar(max)', '日志信息'),
                ('category', 'nvarchar(20)', '人群分类'),
                ('categoryCode', 'varchar(3)', '人群分类编码'),
                ('weightStatus', 'varchar(20)', '体重状态'),
                ('weightStatusCode', 'varchar(3)', '体重状态编码'),
                ('f_rule', 'nvarchar(max)', '体重状态判断规则')
            ]

            for field_name, field_type, comment in field_definitions:
                Sqlserver_PO.setFieldTypeComment(self.tableWSA, field_name, field_type, comment)

            Sqlserver_PO.execute("ALTER TABLE %s ALTER COLUMN updateDate DATE;" % (self.tableWSA))

            # 6, 设置自增主键（最后）
            Sqlserver_PO.setIdentityPrimaryKey(self.tableWSA, "id")

        except Exception as e:
            raise e

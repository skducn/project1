# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-7-1
# Description: 专病库CDRD
# 豆包格式化数据：
# 1，log_client_info	nvarchar	100，请将以上字段类型大小，转换成 字段 类型(大小)的格式
# 2，字段	字段英文名
# 客户端信息	log_client_info ，请将以上字段英文名与字段互换位置，用逗号分隔输出
# 3，请继续优化，将每行数据转换成 Sqlserver_PO.setFieldComment(varTable, '参数1', '参数2'),替换参数1和参数2
# *****************************************************************


# 添加项目根目录到Python路径
import sys
import os
# 获取当前文件路径并向上导航到project目录
dir_path = os.path.dirname(os.path.abspath(__file__))  # 造数据
dir_path = os.path.dirname(dir_path)  # CDRD
dir_path = os.path.dirname(dir_path)  # zyjk
dir_path = os.path.dirname(dir_path)  # instance
dir_path = os.path.dirname(dir_path)  # project
sys.path.append(dir_path)

from PO.SqlserverPO import *
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "GBK")
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_PT", "GBK")

import subprocess

class CdrdPO(object):

    def openSql(self, file_path):
        try:
            # 调用系统命令，通过 PyCharm 打开指定文件
            subprocess.run(
                ["/Applications/PyCharm.app/Contents/MacOS/pycharm", file_path],  # 命令参数：PyCharm路径 + 目标文件路径
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"已打开文件：{file_path}")
        except Exception as e:
            print(f"打开失败：{str(e)}")

    def _ab_admissionCondition(self, varCommon):

        # 创建表，插入数据
        # 入院病情
        Sqlserver_PO.crtTableByCover('ab_admissionCondition',
                                '''id INT IDENTITY PRIMARY KEY,
                                n_key NVARCHAR(10),
                                n_value NVARCHAR(100)
                                ''')
        Sqlserver_PO.execute("INSERT INTO ab_admissionCondition (n_key, n_value) "
                             "VALUES ('1',N'有'),('2',N'临床未确定'),('3',N'情况不明'),('4',N'无')")
        Sqlserver_PO.setTableComment('ab_admissionCondition', varCommon + '(测试用)')
    def _ab_boolean(self, varCommon):

        # 创建表，插入数据
        # 主要诊断标识表
        Sqlserver_PO.crtTableByCover('ab_boolean',
                                '''id INT IDENTITY PRIMARY KEY,
                                n_key NVARCHAR(10),
                                n_value NVARCHAR(100)
                                ''')
        Sqlserver_PO.execute("INSERT INTO ab_boolean (n_key, n_value) "
                             "VALUES ('1',N'是'),('0',N'否')")
        Sqlserver_PO.setTableComment('ab_boolean', varCommon + '(测试用)')
    def _ab_dischargeStatus(self, varCommon):

        # 创建表，插入数据
        # 出院情况
        Sqlserver_PO.crtTableByCover('ab_dischargeStatus',
                                '''id INT IDENTITY PRIMARY KEY,
                                n_key NVARCHAR(10),
                                n_value NVARCHAR(100)
                                ''')
        Sqlserver_PO.execute("INSERT INTO ab_dischargeStatus (n_key, n_value) "
                             "VALUES ('1',N'治愈'),('2',N'好转'),('3',N'未愈'),('4',N'死亡'),('5',N'其他')")
        Sqlserver_PO.setTableComment('ab_dischargeStatus', varCommon + '(测试用)')
    def _ab_diagnosticHistory(self, varCommon):

        # 诊断病史
        varTable = 'ab_diagnosticHistory'
        Sqlserver_PO.crtTableByCover(varTable,
                                '''id INT IDENTITY PRIMARY KEY,
                                diag_class NVARCHAR(50),
                                diag_name NVARCHAR(100),
                                diag_code NVARCHAR(50)
                                ''')

        Sqlserver_PO.setTableComment('ab_diagnosticHistory', varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'diag_class', '诊断类型')
        Sqlserver_PO.setFieldComment(varTable, 'diag_name', '诊断名称')
        Sqlserver_PO.setFieldComment(varTable, 'diag_code', 'ICD10编码')

    def _ab_ethnicGroup(self, varCommon):

        # 创建表，插入数据
        # 种族
        Sqlserver_PO.crtTableByCover('ab_ethnicGroup',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_ethnicGroup (n_key, n_value) "
                             "VALUES ('01',N'汉族'),('02',N'蒙古族'),('03',N'回族'),('04',N'藏族'),('05',N'维吾尔族'),('06',N'苗族'),('07',N'彝族'),('08',N'壮族'),('09',N'布依族'),('10',N'朝鲜族')")
        Sqlserver_PO.setTableComment('ab_ethnicGroup', varCommon + '(测试用)')
    def _ab_hospital(self, varCommon):

        # 创建表，插入数据
        # 医院
        Sqlserver_PO.crtTableByCover('ab_hospital',
                                '''id INT IDENTITY PRIMARY KEY,
                                name NVARCHAR(350)
                                ''')
        Sqlserver_PO.execute("INSERT INTO ab_hospital (name) "
                             "VALUES ('东方医院'),('复旦大学附属眼耳鼻喉科医院'),('上海交通大学医学院附属第九人民医院'),('上海市第一人民医院'),('上海交通大学医学院附属新华医院')")
        Sqlserver_PO.setTableComment('ab_hospital', varCommon + '(测试用)')
    def _ab_job(self, varCommon):

        # 创建表，插入数据
        # 职业
        Sqlserver_PO.crtTableByCover('ab_job',
                                '''id INT IDENTITY PRIMARY KEY,
                                n_value NVARCHAR(100)
                                ''')
        Sqlserver_PO.execute("INSERT INTO ab_job (n_value) "
                             "VALUES (N'军人'),(N'医生'),(N'自由职业者'),(N'技术人员'),(N'工程师'),(N'学生'),(N'老师'),(N'服务人员')")
        Sqlserver_PO.setTableComment('ab_job', varCommon + '(测试用)')
    def _ab_relationship(self, varCommon):

        # 创建表，插入数据
        # 与患者关系
        Sqlserver_PO.crtTableByCover('ab_relationship',
                                '''id INT IDENTITY PRIMARY KEY,
                                n_value NVARCHAR(100)
                                ''')
        Sqlserver_PO.execute("INSERT INTO ab_relationship (n_value) "
                             "VALUES (N'本人'),(N'父亲'),(N'母亲'),(N'配偶'),(N'子女'),(N'兄弟姐妹'),(N'父母'),(N'祖父母'),(N'外祖父母'),(N'子女（多人）'), (N'亲戚'), (N'朋友'), (N'同事'), (N'监护人'), (N'代理人'), (N'其他')")
        Sqlserver_PO.setTableComment('ab_relationship', varCommon + '(测试用)')
    def _ab_marriage(self, varCommon):

        # 创建表，插入数据
        # 婚姻
        Sqlserver_PO.crtTableByCover('ab_marriage',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_marriage (n_key, n_value) "
                             "VALUES ('1',N'未婚'),('2',N'已婚'),('3',N'丧偶'),('4',N'离婚'),('9',N'其他')")
        Sqlserver_PO.setTableComment('ab_marriage', varCommon + '(测试用)')

    def _ab_IDtype(self, varCommon):

        # 创建表，插入数据
        # 证件类型
        Sqlserver_PO.crtTableByCover('ab_IDtype',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_IDtype (n_key, n_value) "
                             "VALUES ('1',N'居民身份证'),('2',N'居民户口簿'),('3',N'护照'),('4',N'军官证'),('5',N'驾驶证'),('6',N'港澳居民来往内地通行证'),('7',N'台湾居民来往内地通行证'),('9',N'其他法定有效证件')")
        Sqlserver_PO.setTableComment('ab_IDtype', varCommon + '(测试用)')
    def _ab_visitType(self, varCommon):

        # 创建表，插入数据
        # 就诊类型
        Sqlserver_PO.crtTableByCover('ab_visitType',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_visitType (n_key, n_value) "
                             "VALUES ('1', N'门诊'), ('2', N'住院')")
        Sqlserver_PO.setTableComment('ab_visitType', varCommon + '(测试用)')
    def _ab_paymentMethod(self, varCommon):

        # 创建表，插入数据
        # 就诊类型
        Sqlserver_PO.crtTableByCover('ab_paymentMethod',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_paymentMethod (n_key, n_value) "
                             "VALUES ('1',N'城镇职工基本医疗保险'),('2',N'城镇居民基本医疗保险'),('3',N'新型农村合作医疗'),('4',N'贫困救助'),('5',N'商业医疗保险'),('6',N'全公费'),('7',N'全自费'),('8',N'其他社会保险(指生育保险、工伤保险、农民工保险等)'),('9',N'其他')")
        Sqlserver_PO.setTableComment('ab_paymentMethod', varCommon + '(测试用)')
    def _ab_dischargeMethod(self, varCommon):

        # 创建表，插入数据
        # 出院方式
        Sqlserver_PO.crtTableByCover('ab_dischargeMethod',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_dischargeMethod (n_key, n_value) "
                             "VALUES ('1', N'医嘱离院'), ('2', N'医嘱转院'), ('3', N'医嘱转社区卫生服务机构/乡镇卫生院'), ('4', N'非医嘱离院'),('5', N'死亡'), ('9', N'其他')")
        Sqlserver_PO.setTableComment('ab_dischargeMethod', varCommon + '(测试用)')
    def _ab_admissionRoute(self, varCommon):

        # 创建表，插入数据
        # 入院途径
        Sqlserver_PO.crtTableByCover('ab_admissionRoute',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_admissionRoute (n_key, n_value) "
                             "VALUES ('1',N'本院急诊诊疗后入院'),('2',N'本院门诊诊疗后入院'),('3',N'其他医疗机构诊治后转诊入院'),('9',N'其他途径入院')")
        Sqlserver_PO.setTableComment('ab_admissionRoute', varCommon + '(测试用)')
    def _ab_drugAllergy(self, varCommon):

        # 创建表，插入数据
        # 药物过敏
        Sqlserver_PO.crtTableByCover('ab_drugAllergy',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_drugAllergy (n_key, n_value) "
                             "VALUES ('1',N'无'),('2',N'有')")
        Sqlserver_PO.setTableComment('ab_drugAllergy', varCommon + '(测试用)')
    def _ab_ABO_bloodType(self, varCommon):

        # 创建表，插入数据
        # 药物过敏
        Sqlserver_PO.crtTableByCover('ab_ABO_bloodType',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_ABO_bloodType (n_key, n_value) "
                             "VALUES ('1',N'A型'),('2',N'B型'),('3',N'O型'),('4',N'AB型'),('5',N'不详'),('6',N'未查')")
        Sqlserver_PO.setTableComment('ab_ABO_bloodType', varCommon + '(测试用)')
    def _ab_rh_bloodType(self, varCommon):

        # 创建表，插入数据
        # 药物过敏
        Sqlserver_PO.crtTableByCover('ab_rh_bloodType',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(10),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("INSERT INTO ab_rh_bloodType (n_key, n_value) "
                             "VALUES ('1',N'阴性'),('2',N'阳性'),('3',N'不详'),('4',N'未查')")
        Sqlserver_PO.setTableComment('ab_rh_bloodType', varCommon + '(测试用)')


    def _ab_visitDiagnosis(self, varCommon):

        # 就诊诊断
        varTable = 'ab_visitDiagnosis'
        Sqlserver_PO.crtTableByCover(varTable,
                                     '''id INT IDENTITY PRIMARY KEY,
                                     patient_visit_diag NVARCHAR(100)
                                     ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_diag', varCommon)

    def _ab_symptom(self, varCommon):

        # 症状信息 - 症状名称，症状编号，具体描述
        varTable = 'ab_symptom'
        Sqlserver_PO.crtTableByCover(varTable,
                                     '''id INT IDENTITY PRIMARY KEY,
                                     patient_symptom_name NVARCHAR(100),
                                     patient_symptom_num NVARCHAR(100),
                                     patient_symptom_description NVARCHAR(1000)
                                     ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_name', '症状名称')
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_num', '症状编号')
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_description', '具体描述')

    def _ab_outHospitalDiag(self, varCommon):

        # 出院诊断
        varTable = 'ab_outHospitalDiag'
        Sqlserver_PO.crtTableByCover(varTable,
                                     '''id INT IDENTITY PRIMARY KEY,
                                     patient_out_hospital_diag NVARCHAR(500),
                                     ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_diag', varCommon)




    def _ab_physicalSign(self, varCommon):

        # 创建表，插入数据
        # 体征
        Sqlserver_PO.crtTableByCover('ab_physicalSign',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(100),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_physicalSign (n_key,n_value) 
                            VALUES ('1',N'体温'),('2',N'脉搏'),('3',N'心率'),('4',N'呼吸'),('5',N'收缩压'),('6',N'舒张压'),('7',N'指尖血氧饱和度'),('8',N'其他')""")
        Sqlserver_PO.setTableComment('ab_physicalSign', varCommon + '(测试用)')
    def _ab_physicalSignUnit(self, varCommon):

        # 创建表，插入数据
        # 体征单位
        Sqlserver_PO.crtTableByCover('ab_physicalSignUnit',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(100),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_physicalSignUnit (n_key,n_value) 
                            VALUES ('1',N'℃'),('2',N'次/分'),('3',N'mmHg'),('4',N'%'),('5',N'其他')""")
        Sqlserver_PO.setTableComment('ab_physicalSignUnit', varCommon + '(测试用)')
    def _ab_lab(self, varCommon):

        # 创建表，插入数据
        # 实验室检查报告表(造数据)
        Sqlserver_PO.crtTableByCover('ab_lab',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     reportname NVARCHAR(100),
                                     sampletype NVARCHAR(100),
                                     projectname NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_lab (reportname,sampletype,projectname) 
                            VALUES ('血生化检测', '全血', '无'), ('凝血功能检验', '全血', '无')""")
        Sqlserver_PO.setTableComment('ab_lab', varCommon + '(测试用)')
    def _ab_drug(self, varCommon):

        # 创建表，插入数据
        # 用药信息表
        Sqlserver_PO.crtTableByCover('ab_drug',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     v1 NVARCHAR(100),
                                     v2 NVARCHAR(100),
                                     v3 NVARCHAR(100),
                                     v4 NVARCHAR(100),
                                     v5 NVARCHAR(100),
                                     v6 NVARCHAR(100),
                                     v7 NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_drug (v1,v2,v3,v4,v5,v6,v7) 
                            VALUES ('氨氯地平片', '5mg', '每日 1 次', '1', '片', '口服', '30片/月'),
        ('厄贝沙坦片', '150mg', '每日 1 次', '1', '片', '口服', '30片/月'),
        ('利伐沙班片', '20mg', '每日 1 次', '1', '片', '口服', '30片/月'),
        ('美托洛尔缓释片', '47.5mg', '每日 1 次', '1', '片', '口服', '30片/月'),
        ('二甲双胍缓释片', '0.5g', '每日 2 次', '1', '片', '口服', '60片/月'),
        ('度拉糖肽注射液', '1.5mg', '每周 1 次', '1', '支', '皮下注射', '4支/月'),
        ('单硝酸异山梨酯片', '20mg', '每日 2 次', '1', '片', '口服', '60片/月'),
        ('阿托伐他汀钙片', '20mg', '每晚 1 次', '1', '片', '口服', '30片/月'),
        ('布地奈德福莫特罗', '160/4.5μg', '每日 2 次', '1', '吸', '吸入', '60吸/月'),
        ('莫西沙星片', '400mg', '每日 1 次', '1', '片', '口服', '7片/疗程'),
        ('阿司匹林肠溶片', '100mg', '每日 1 次', '1', '片', '口服', '30片/月'),
        ('阿托伐他汀钙片', '40mg', '每晚 1 次', '1', '片', '口服', '30片/月'),
        ('奥美拉唑肠溶胶囊', '20mg', '每日 2 次', '1', '粒', '口服', '60粒/月'),
        ('铝碳酸镁咀嚼片', '0.5g', '每日 3 次', '2', '片', '嚼服', '180片/月'),
        ('阿仑膦酸钠片', '70mg', '每周 1 次', '1', '片', '口服', '4片/月'),
        ('骨化三醇软胶囊', '0.25μg', '每日 1 次', '1', '粒', '口服', '30粒/月'),
        ('甲巯咪唑片', '5mg', '每日 3 次', '1', '片', '口服', '90片/月'),
        ('普萘洛尔片', '10mg', '每日 3 次', '1', '片', '口服', '90片/月'),
        ('缬沙坦胶囊', '80mg', '每日 1 次', '1', '粒', '口服', '30粒/月'),
        ('碳酸司维拉姆片', '800mg', '每日 3 次', '1', '片', '口服', '90片/月')""")
        Sqlserver_PO.setTableComment('ab_drug', varCommon + '(测试用)')
    def _ab_dischargeHospital(self, varCommon):

        # 创建表，插入数据
        # 出院记录
        Sqlserver_PO.crtTableByCover('ab_dischargeHospital',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(100),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_dischargeHospital (n_key,n_value) 
                            VALUES ('1',N'出院记录'),('2',N'24小时内入出院记录')""")
        Sqlserver_PO.setTableComment('ab_dischargeHospital', varCommon + '(测试用)')
    def _ab_operationLevel(self, varCommon):

        # 创建表，插入数据
        # 手术级别
        Sqlserver_PO.crtTableByCover('ab_operationLevel',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(100),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_operationLevel (n_key,n_value) 
                            VALUES ('1',N'一级手术'),('2',N'二级手术'),('3',N'三级手术'),('4',N'四级手术')""")
        Sqlserver_PO.setTableComment('ab_operationLevel', varCommon + '(测试用)')
    def _ab_operationType(self, varCommon):

        # 创建表，插入数据
        # 手术类型
        Sqlserver_PO.crtTableByCover('ab_operationType',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(100),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_operationType (n_key,n_value) 
                            VALUES ('1',N'择期手术'),('2',N'急诊手术'),('3',N'限期手术')""")
        Sqlserver_PO.setTableComment('ab_operationType', varCommon + '(测试用)')
    def _ab_operationIncisionHealingGrade(self, varCommon):

        # 创建表，插入数据
        # qiekou切口愈合登记
        Sqlserver_PO.crtTableByCover('ab_operationIncisionHealingGrade',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(100),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_operationIncisionHealingGrade (n_key,n_value) 
                            VALUES ('1',N'0类切口'),('2',N'Ⅰ类切口'),('3',N'Ⅱ类切口'),('4',N'Ⅲ类切口')""")
        Sqlserver_PO.setTableComment('ab_operationIncisionHealingGrade', varCommon + '(测试用)')
    def _ab_loginout(self, varCommon):

        # 创建表，插入数据
        # 登录登出
        Sqlserver_PO.crtTableByCover('ab_loginout',
                                     '''id INT IDENTITY PRIMARY KEY,
                                     n_key NVARCHAR(100),
                                     n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_loginout (n_key,n_value) 
                            VALUES ('登录', '账号密码登录'),('登出', '手动登出')""")
        Sqlserver_PO.setTableComment('ab_loginout', varCommon + '(测试用)')

    def _ab_lab_project(self, varCommon):

        # 创建表，插入数据
        # 实验室检查+项目明细
        # Cdrd_PO._ab_lal_project('实验室检查+项目明细')

        Sqlserver_PO.crtTableByCover('ab_lab_project',
                                     '''id INT IDENTITY PRIMARY KEY,
                                        report_id INT,
                                        report_name NVARCHAR(255),
                                        patient_test_item_name NVARCHAR(255),
                                        patient_test_numerical_value NVARCHAR(50),
                                        patient_test_unit_name NVARCHAR(50),
                                        patient_test_text_value NVARCHAR(50),
                                        patient_test_abnormal_flag NVARCHAR(50),
                                        patient_test_reference_range NVARCHAR(50)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_lab_project (report_id, report_name, patient_test_item_name, patient_test_numerical_value, patient_test_unit_name, patient_test_text_value, patient_test_abnormal_flag, patient_test_reference_range) 
        VALUES (1, '血生化检测','空腹血糖（GLU）', '5.8', 'mmol/L', '正常', '', '3.9-6.1'),
    (2, '血生化检测','糖化血红蛋白（HbA1c）', '6.2', '%', '升高', '异常', '<6.0'),
    (3, '血生化检测','总胆固醇（TC）', '5.9', 'mmol/L', '升高', '异常', '<5.2'),
    (4, '血生化检测','甘油三酯（TG）', '2.3', 'mmol/L', '升高', '异常', '<1.7'),
    (5, '血生化检测','低密度脂蛋白（LDL-C）', '3.8', 'mmol/L', '升高', '异常', '<3.4'),
    (6, '血生化检测','高密度脂蛋白（HDL-C）', '1.1', 'mmol/L', '正常', '', '>=1.0'),
    (7, '血生化检测','血肌酐（Cr）', '78', 'mmol/L', '正常', '', '59-104'),
    (8, '血生化检测','尿素氮（BUN）', '5.6', 'mmol/L', '正常', '', '2.9-8.2'),
    (9, '血生化检测','估算 eGFR', '88', 'mL/min/1.73m2', '正常', '', '>=90'),
    (10, '血生化检测','血尿酸（UA）', '420', 'mmol/L', '升高', '异常', '208-428（男性）'),
    (11, '血生化检测','血钾（K+）', '3.9', 'mmol/L', '正常', '', '3.5-5.3'),
    (12, '血生化检测','血钠（Na+）', '140', 'mmol/L', '正常', '', '137-147'),
    (13, '血生化检测','血氯（Cl-）', '102', 'mmol/L', '正常', '', '99-110'),
    (14, '血生化检测','丙氨酸氨基转移酶（ALT）', '28', 'U/L', '正常', '', '9-50'),
    (15, '血生化检测','天门冬氨酸氨基转移酶（AST）', '25', 'U/L', '正常', '', '15-40'),
    (16, '血生化检测','总蛋白（TP）', '72', 'g/L', '正常', '', '65-85'),
    (17, '血生化检测','白蛋白（ALB）', '45', 'g/L', '正常', '', '40-55'),
    (18, '血生化检测','同型半胱氨酸（Hcy）', '16.5', 'mmol/L', '升高', '异常', '<15'),
    (19, '血生化检测','乳酸脱氢酶（LDH）', '220', 'U/L', '正常', '', '120-250'),
    (20, '血生化检测','C 反应蛋白（CRP）', '8', 'mg/L', '升高', '异常', '<5.0'),
    (1, '凝血功能检验','凝血酶原时间（PT）', '13.5', '秒', '正常', '', '11.0-14.5'),
    (2, '凝血功能检验','活化部分凝血活酶时间（APTT）', '38', '秒', '延长', '异常', '25.0-35.0'),
    (3, '凝血功能检验','国际标准化比值（INR）', '1.15', '-', '正常', '', '0.8-1.2'),
    (4, '凝血功能检验','纤维蛋白原（FIB）', '3.2', 'g/L', '正常', '', '2.0-4.0'),
    (5, '凝血功能检验','D - 二聚体（D-Dimer）', '0.8', 'mg/L', '升高', '异常', '<0.5'),
    (6, '凝血功能检验','抗凝血酶 Ⅲ（AT-Ⅲ）活性', '85', '%', '正常', '', '80-120'),
    (7, '凝血功能检验','血小板计数（PLT）', '210', 'X109/L', '正常', '', '125-350'),
    (8, '凝血功能检验','肌钙蛋白 I（cTnI）', '0.02', 'ug/L', '正常', '', '<0.04'),
    (9, '凝血功能检验','N 末端脑钠肽前体（NT-proBNP）', '450', 'pg/mL', '升高', '异常', '<125'),
    (10, '凝血功能检验','血钾（K+）', '3.9', 'mmol/L', '正常', '', '3.5-5.3'),
    (11, '凝血功能检验','血镁（Mg2+）', '0.75', 'mmol/L', '降低', '异常', '0.7-1.1'),
    (12, '凝血功能检验','甲状腺功能（TSH）', '0.1', 'mIU/L', '降低', '异常', '0.27-4.2'),
    (13, '凝血功能检验','游离甲状腺素（FT4）', '25', 'pmol/L', '升高', '异常', '12.0-22.0'),
    (14, '凝血功能检验','肝功能（ALT）', '32', 'U/L', '正常', '', '9-50'),
    (15, '凝血功能检验','肾功能（eGFR）', '68', 'mL/min', '降低', '异常', '>=90'),
    (16, '凝血功能检验','血尿酸（UA）', '480', 'umol/L', '升高', '异常', '208-428'),
    (17, '凝血功能检验','同型半胱氨酸（Hcy）', '18.5', 'umol/L', '升高', '异常', '<15'),
    (18, '凝血功能检验','糖化血红蛋白（HbA1c）', '6.2', '%', '升高', '异常', '<6.0'),
    (19, '凝血功能检验','C 反应蛋白（CRP）', '8', 'mg/L', '升高', '异常', '<5.0'),
    (20, '凝血功能检验','乳酸脱氢酶（LDH）', '220', 'U/L', '正常', '', '120-250');
""")
        Sqlserver_PO.setTableComment('ab_lab_project', varCommon + '(测试用)')

    def _ab_dischargeRecordType(self, varCommon):

        # 创建表，插入数据
        # Cdrd_PO._ab_dischargeRecordType('出院记录类型')
        Sqlserver_PO.crtTableByCover('ab_dischargeRecordType',
                                     '''id INT IDENTITY PRIMARY KEY,
                                        n_key NVARCHAR(100),
                                        n_value NVARCHAR(100)
                                     ''')
        Sqlserver_PO.execute("""INSERT INTO ab_dischargeRecordType (n_key, n_value) VALUES ('1',N'出院记录'),('2',N'24小时内入出院记录')""")
        Sqlserver_PO.setTableComment('ab_dischargeRecordType', varCommon + '(测试用)')






    def crt_sys_hospital(self, varCommon):

        # 医院信息表

        varTable = 'sys_hospital'
        Sqlserver_PO.crtTableByCover(varTable,
        '''hospital_id INT IDENTITY(1,1) PRIMARY KEY,
        hospital_name NVARCHAR(50),
        hospital_code NVARCHAR(50),
        hospital_picture_address NVARCHAR(max),
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'hospital_id', '医院ID')
        Sqlserver_PO.setFieldComment(varTable, 'hospital_name', '医院名称')
        Sqlserver_PO.setFieldComment(varTable, 'hospital_code', '医院编码')
        Sqlserver_PO.setFieldComment(varTable, 'hospital_picture_address', '图片地址')

    def crt_sys_department(self, varCommon):

        # 科室表
        
        varTable = 'sys_department'
        Sqlserver_PO.crtTableByCover(varTable,
        '''department_id INT IDENTITY(1,1) PRIMARY KEY,
        department_name NVARCHAR(20),
        department_code NVARCHAR(20),
        department_charge_id int,
        department_charge_job_num NVARCHAR(20),
        department_charge_name NVARCHAR(20),
        department_creater_name NVARCHAR(20),
        department_create_time DATETIME
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'department_name', '科室名称')
        Sqlserver_PO.setFieldComment(varTable, 'department_code', '科室编码')
        Sqlserver_PO.setFieldComment(varTable, 'department_charge_id', '科室负责人ID')
        Sqlserver_PO.setFieldComment(varTable, 'department_charge_job_num', '科室负责人工号')
        Sqlserver_PO.setFieldComment(varTable, 'department_charge_name', '科室负责人姓名')
        Sqlserver_PO.setFieldComment(varTable, 'department_creater_name', '创建人')
        Sqlserver_PO.setFieldComment(varTable, 'department_create_time', '创建时间')
    def crt_sys_dept_medgp(self, varCommon):

        # 科室-医疗组

        varTable = 'sys_dept_medgp'
        Sqlserver_PO.crtTableByCover(varTable,
        '''
        department_treat_group_id int IDENTITY(1,1) PRIMARY KEY,
        department_id int,
        department_treat_group_name NVARCHAR(20),
        department_treat_create_time DATETIME
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'department_treat_group_id', '医疗组ID')
        Sqlserver_PO.setFieldComment(varTable, 'department_id', '科室ID')
        Sqlserver_PO.setFieldComment(varTable, 'department_treat_group_name', '医疗组名称')
        Sqlserver_PO.setFieldComment(varTable, 'department_treat_create_time', '医疗组创建时间')
    def crt_sys_dept_medgp_person(self,varCommon):

        # 医疗组-人员

        varTable = 'sys_dept_medgp_person'
        Sqlserver_PO.crtTableByCover(varTable,
        '''
        ID int IDENTITY(1,1) PRIMARY KEY,
        user_id int,
        department_treat_group_id INT,
        user_name NVARCHAR(20),
        user_job_num NVARCHAR(20)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'ID', 'ID')
        Sqlserver_PO.setFieldComment(varTable, 'user_id', '用户ID')
        Sqlserver_PO.setFieldComment(varTable, 'department_treat_group_id', '医疗组ID')
        Sqlserver_PO.setFieldComment(varTable, 'user_name', '姓名')
        Sqlserver_PO.setFieldComment(varTable, 'user_job_num', '工号')



    def crt_sys_user(self, varCommon):

        # 用户表

        varTable = 'sys_user'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            user_id	int	IDENTITY(1,1) PRIMARY KEY,
            nick_name nvarchar(20),
            user_name nvarchar(20),
            user_type	nvarchar(2),
            password	nvarchar(100),
            job_num	nvarchar(20),
            email	nvarchar(50),
            phonenumber	nvarchar(20),
            sex 	varchar(100),
            avatar 	nvarchar(100),
            department_id	int	,
            department_code	nvarchar(20),
            department_name	nvarchar(20),
            status varchar(100),
            remark nvarchar(500),
            create_by	nvarchar(20),
            create_time	datetime	,
            update_by	nvarchar(20),
            update_time	datetime	,
            pwd_update_state varchar(100),
            pwd_update_time	datetime,	
            pwd_next_update_time	datetime	
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'user_id', '用户ID'),
        Sqlserver_PO.setFieldComment(varTable, 'nick_name', '姓名'),
        Sqlserver_PO.setFieldComment(varTable, 'user_name', '账号'),
        Sqlserver_PO.setFieldComment(varTable, 'user_type', '用户类型'),
        Sqlserver_PO.setFieldComment(varTable, 'password', '密码'),
        Sqlserver_PO.setFieldComment(varTable, 'job_num', '工号'),
        Sqlserver_PO.setFieldComment(varTable, 'email', '邮箱'),
        Sqlserver_PO.setFieldComment(varTable, 'phonenumber', '手机号'),
        Sqlserver_PO.setFieldComment(varTable, 'sex', '性别'),
        Sqlserver_PO.setFieldComment(varTable, 'avatar', '头像地址'),
        Sqlserver_PO.setFieldComment(varTable, 'department_id', '所属科室ID'),
        Sqlserver_PO.setFieldComment(varTable, 'department_code', '所属科室code'),
        Sqlserver_PO.setFieldComment(varTable, 'department_name', '所属科室名称'),
        Sqlserver_PO.setFieldComment(varTable, 'status', '账号状态'),
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注'),
        Sqlserver_PO.setFieldComment(varTable, 'create_by', '创建人'),
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间'),
        Sqlserver_PO.setFieldComment(varTable, 'update_by', '更新者'),
        Sqlserver_PO.setFieldComment(varTable, 'update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'pwd_update_state', '密码重置状态'),
        Sqlserver_PO.setFieldComment(varTable, 'pwd_update_time', '密码最后更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'pwd_next_update_time', '密码下次更新时间')
    def crt_sys_user_role(self, varCommon):

        # 用户管理 - 用户角色关系表

        varTable = 'sys_user_role'
        Sqlserver_PO.crtTableByCover(varTable,
        '''
        id int	IDENTITY(1,1) PRIMARY KEY,
        user_id	int	,
        role_id int 	
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'id', 'ID')
        Sqlserver_PO.setFieldComment(varTable, 'user_id', '用户ID')
        Sqlserver_PO.setFieldComment(varTable, 'role_id', '角色ID')
    def crt_sys_security_question(self, varCommon):

        # 用户管理 - 用户问题关系表
        
        varTable = 'sys_user_pwdptc'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            id	int	IDENTITY(1,1) PRIMARY KEY,
            user_id	int	,
            question_id1 int,
            answer1 nvarchar(100),
            question_id2 int, 	
            answer2 nvarchar(100),
            question_id3 int,
            answer3 nvarchar(100), 	
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'user_id', '用户ID')
        Sqlserver_PO.setFieldComment(varTable, 'question_id1', '问题1ID')
        Sqlserver_PO.setFieldComment(varTable, 'answer1', '答案1')
        Sqlserver_PO.setFieldComment(varTable, 'question_id2', '问题2ID')
        Sqlserver_PO.setFieldComment(varTable, 'answer2', '答案2')
        Sqlserver_PO.setFieldComment(varTable, 'question_id3', '问题3ID')
        Sqlserver_PO.setFieldComment(varTable, 'answer3', '答案3')
    def crt_sys_user_pwdptc(self, varCommon):

        # 用户管理 - 用户问题关系表

        varTable = 'sys_user_pwdptc'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            id	int	IDENTITY(1,1) PRIMARY KEY,
            user_id	int	,
            question_id1 int,
            answer1 nvarchar(100),
            question_id2 int, 	
            answer2 nvarchar(100),
            question_id3 int,
            answer3 nvarchar(100), 	
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'user_id', '用户ID')
        Sqlserver_PO.setFieldComment(varTable, 'question_id1', '问题1ID')
        Sqlserver_PO.setFieldComment(varTable, 'answer1', '答案1')
        Sqlserver_PO.setFieldComment(varTable, 'question_id2', '问题2ID')
        Sqlserver_PO.setFieldComment(varTable, 'answer2', '答案2')
        Sqlserver_PO.setFieldComment(varTable, 'question_id3', '问题3ID')
        Sqlserver_PO.setFieldComment(varTable, 'answer3', '答案3')

    def crt_sys_security_question(self, varCommon):

        # 用户密保问题表

        varTable = 'sys_security_question'
        Sqlserver_PO.crtTableByCover(varTable,
        '''
        id	int	IDENTITY(1,1) PRIMARY KEY,
        question nvarchar(100)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'id', 'ID')
        Sqlserver_PO.setFieldComment(varTable, 'question', '问题')




    def crt_sys_role(self, varCommon):

        # 角色管理 - 角色表

        varTable = 'sys_role'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            role_id	int	IDENTITY(1,1) PRIMARY KEY,
            role_name	nvarchar	(20),
            role_key	nvarchar	(20),
            role_sort	int,	
            status	varchar(100),
            menu_check_strictly	int	,
            create_by	nvarchar	(20),
            create_time	datetime,	
            update_by	nvarchar	(20),
            update_time	datetime	,
            remark	nvarchar	(500)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'role_id', '角色ID'),
        Sqlserver_PO.setFieldComment(varTable, 'role_name', '角色名称'),
        Sqlserver_PO.setFieldComment(varTable, 'role_key', '角色权限权限字符串'),
        Sqlserver_PO.setFieldComment(varTable, 'role_sort', '显示顺序'),
        Sqlserver_PO.setFieldComment(varTable, 'status', '角色状态'),
        Sqlserver_PO.setFieldComment(varTable, 'menu_check_strictly', '菜单树选择项是否关联显示'),
        Sqlserver_PO.setFieldComment(varTable, 'create_by', '创建人'),
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间'),
        Sqlserver_PO.setFieldComment(varTable, 'update_by', '更新者'),
        Sqlserver_PO.setFieldComment(varTable, 'update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')
    def crt_sys_role_menu(self, varCommon):

        # 角色管理 - 角色菜单关系表

        varTable = 'sys_role_menu'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            id int	IDENTITY(1,1) PRIMARY KEY,
            role_id	int	,
            menu_id int 	
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'id', 'ID')
        Sqlserver_PO.setFieldComment(varTable, 'role_id', '角色ID')
        Sqlserver_PO.setFieldComment(varTable, 'menu_id', '菜单ID')



    def crt_sys_menu(self, varCommon):

        # 菜单管理 - 菜单表

        varTable = 'sys_menu'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            menu_id	int	IDENTITY(1,1) PRIMARY KEY,
            menu_name	nvarchar	(50),
            parent_id 	int	,
            order_num	int	,
            path	nvarchar	(200),
            component	nvarchar	(255),
            query	nvarchar	(255),
            route_name	nvarchar	(50),
            is_frame	varchar(100)	,
            is_cache	varchar(100)	,
            menu_type	char	(1),
            status	varchar(100)	,
            visible 	varchar(100),	
            perms	nvarchar	(100),
            icon	nvarchar	(100),
            create_by	nvarchar	(64),
            create_time	datetime	,
            update_by	nvarchar	(64),
            update_time	datetime	,
            remark	nvarchar	(500)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'menu_id', '菜单ID')
        Sqlserver_PO.setFieldComment(varTable, 'menu_name', '菜单名称')
        Sqlserver_PO.setFieldComment(varTable, 'parent_id', '父级菜单ID')
        Sqlserver_PO.setFieldComment(varTable, 'order_num', '显示顺序')
        Sqlserver_PO.setFieldComment(varTable, 'path', '路由地址')
        Sqlserver_PO.setFieldComment(varTable, 'component', '组件路径')
        Sqlserver_PO.setFieldComment(varTable, 'query', '路由参数')
        Sqlserver_PO.setFieldComment(varTable, 'route_name', '路由名称')
        Sqlserver_PO.setFieldComment(varTable, 'is_frame', '是否为外链')
        Sqlserver_PO.setFieldComment(varTable, 'is_cache', '是否缓存')
        Sqlserver_PO.setFieldComment(varTable, 'menu_type', '菜单类型')
        Sqlserver_PO.setFieldComment(varTable, 'status', '菜单状态')
        Sqlserver_PO.setFieldComment(varTable, 'visible', '显示状态')
        Sqlserver_PO.setFieldComment(varTable, 'perms', '权限字符')
        Sqlserver_PO.setFieldComment(varTable, 'icon', '菜单图标')
        Sqlserver_PO.setFieldComment(varTable, 'create_by', '创建者')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间')
        Sqlserver_PO.setFieldComment(varTable, 'update_by', '更新者')
        Sqlserver_PO.setFieldComment(varTable, 'update_time', '更新时间')
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')
    def crt_sys_config(self, varCommon):

        # 参数配置

        varTable = 'sys_config'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            config_id int IDENTITY(1,1) PRIMARY KEY,
            config_name	nvarchar	(100),
            config_key 	nvarchar(100),
            config_value	nvarchar(500),
            config_type	varchar(100),
            create_by	nvarchar	(64),
            create_time	datetime,
            update_by	nvarchar	(64),
            update_time	datetime	,
            remark	nvarchar	(500)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'config_id', '参数主键')
        Sqlserver_PO.setFieldComment(varTable, 'config_name', '参数名称')
        Sqlserver_PO.setFieldComment(varTable, 'config_key', '参数键名')
        Sqlserver_PO.setFieldComment(varTable, 'config_value', '参数键值')
        Sqlserver_PO.setFieldComment(varTable, 'config_type', '系统内置')
        Sqlserver_PO.setFieldComment(varTable, 'create_by', '创建者')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间')
        Sqlserver_PO.setFieldComment(varTable, 'update_by', '更新者')
        Sqlserver_PO.setFieldComment(varTable, 'update_time', '更新时间')
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')
    def crt_sys_logininfo(self, varCommon):

        # 登录日志

        varTable = 'sys_logininfo'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            info_id int	IDENTITY(1,1) PRIMARY KEY,
            user_name nvarchar(50),
            nick_name nvarchar(50),
            type nvarchar(50),
            access_time datetime,
            ipaddr nvarchar(128),
            way nvarchar(100),
            status nvarchar(50),
            msg nvarchar(500),
            client_info nvarchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'info_id', '访问ID'),
        Sqlserver_PO.setFieldComment(varTable, 'user_name', '账号'),
        Sqlserver_PO.setFieldComment(varTable, 'nick_name', '姓名'),
        Sqlserver_PO.setFieldComment(varTable, 'type', '登录类型'),
        Sqlserver_PO.setFieldComment(varTable, 'access_time', '访问时间'),
        Sqlserver_PO.setFieldComment(varTable, 'ipaddr', 'IP地址'),
        Sqlserver_PO.setFieldComment(varTable, 'way', '方式'),
        Sqlserver_PO.setFieldComment(varTable, 'status', '结果'),
        Sqlserver_PO.setFieldComment(varTable, 'msg', '备注'),
        Sqlserver_PO.setFieldComment(varTable, 'client_info', '客户端信息')




    def _a_cdrd_patient_info2(self, varCommon):

        # 患者基本信息
        
        varTable = 'CDRD_PATIENT_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_id	int	IDENTITY(1,1) PRIMARY KEY,
                patient_name nvarchar(50),
                patient_sex_key varchar(100),
                patient_sex_value nvarchar(100),
                patient_birth_date Date,
                patient_age int,
                patient_birth_address_province_key varchar(100),
                patient_birth_address_province nvarchar(100),
                patient_birth_address_city_key varchar(100),
                patient_birth_address_city nvarchar(100),
                patient_birth_address_country_key varchar(100),
                patient_birth_address_country nvarchar(100),
                patient_country nvarchar(20),
                patient_native_province_key varchar(100),
                patient_native_province nvarchar(100),
                patient_native_city_key varchar(100),
                patient_native_city nvarchar(100),
                patient_nation_key varchar(100),
                patient_nation_value nvarchar(100),
                patient_profession nvarchar(50),
                patient_marriage_key varchar(100),
                patient_marriage_value nvarchar(100),
                patient_id_type_key varchar(100),
                patient_id_type_value nvarchar(100),
                patient_account_address nvarchar(200),
                patient_contact_relation nvarchar(20),
                patient_update_time datetime,
                patient_data_source_key varchar(100),
                patient_source_id int,
                patient_phone_num varbinary(128),
                patient_home_address varbinary(400),
                patient_id_num nvarchar(100),
                patient_home_phone varbinary(160),
                patient_contact_phone varbinary(160),
                patient_contact_address varbinary(400),
                patient_contact_name varbinary(160)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_name', '姓名'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_sex_key', '性别-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_sex_value', '性别'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_date', '出生日期'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_age', '年龄'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_province_key', '出生地-省-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_province', '出生地-省'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_city_key', '出生地-市-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_city', '出生地-市'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_country_key', '出生地-县-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_country', '出生地-县'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_country', '国籍'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_province_key', '籍贯-省-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_province', '籍贯-省'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_city_key', '籍贯-市-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_city', '籍贯-市'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nation_key', '民族-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nation_value', '民族'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_profession', '职业'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_marriage_key', '婚姻-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_marriage_value', '婚姻'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id_type_key', '证件类型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id_type_value', '证件类型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_account_address', '户口地址'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_relation', '与患者关系'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_data_source_key', '数据来源')
        Sqlserver_PO.setFieldComment(varTable, 'patient_source_id', '源库患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_phone_num', '联系电话'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_home_address', '现住址'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id_num', '证件号码'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_home_phone', '家庭电话'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_phone', '联系人电话'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_address', '联系人地址'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_name', '联系人姓名')
    def crt_cdrdPatientInfo(self, varCommon):

        # 患者基本信息

        varTable = 'CDRD_PATIENT_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_id	int	IDENTITY(1,1) PRIMARY KEY,
                patient_name nvarchar(50),
                patient_sex_key varchar(100),
                patient_sex_value nvarchar(100),
                patient_birth_date Date,
                patient_age int,
                patient_birth_address_province_key varchar(100),
                patient_birth_address_province nvarchar(100),
                patient_birth_address_city_key varchar(100),
                patient_birth_address_city nvarchar(100),
                patient_birth_address_country_key varchar(100),
                patient_birth_address_country nvarchar(100),
                patient_country nvarchar(20),
                patient_native_province_key varchar(100),
                patient_native_province nvarchar(100),
                patient_native_city_key varchar(100),
                patient_native_city nvarchar(100),
                patient_nation_key varchar(100),
                patient_nation_value nvarchar(100),
                patient_profession nvarchar(50),
                patient_marriage_key varchar(100),
                patient_marriage_value nvarchar(100),
                patient_id_type_key varchar(100),
                patient_id_type_value nvarchar(100),
                patient_account_address nvarchar(200),
                patient_contact_relation nvarchar(20),
                patient_update_time datetime,
                patient_data_source_key varchar(100),
                patient_source_id int,
                patient_phone_num nvarchar(128),
                patient_home_address nvarchar(400),
                patient_id_num nvarchar(100),
                patient_home_phone nvarchar(160),
                patient_contact_phone nvarchar(160),
                patient_contact_address nvarchar(400),
                patient_contact_name nvarchar(160)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_name', '姓名'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_sex_key', '性别-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_sex_value', '性别'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_date', '出生日期'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_age', '年龄'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_province_key', '出生地-省-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_province', '出生地-省'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_city_key', '出生地-市-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_city', '出生地-市'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_country_key', '出生地-县-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_country', '出生地-县'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_country', '国籍'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_province_key', '籍贯-省-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_province', '籍贯-省'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_city_key', '籍贯-市-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_city', '籍贯-市'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nation_key', '民族-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nation_value', '民族'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_profession', '职业'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_marriage_key', '婚姻-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_marriage_value', '婚姻'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id_type_key', '证件类型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id_type_value', '证件类型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_account_address', '户口地址'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_relation', '与患者关系'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_data_source_key', '数据来源')
        Sqlserver_PO.setFieldComment(varTable, 'patient_source_id', '源库患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_phone_num', '联系电话'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_home_address', '现住址'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id_num', '证件号码'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_home_phone', '家庭电话'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_phone', '联系人电话'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_address', '联系人地址'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_name', '联系人姓名')


    def crt_testBinary(self):

        # test

        varTable = 'CDRD_test'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                id	int	IDENTITY(1,1) PRIMARY KEY,
                name nvarchar(50),
                content varbinary(160)
            ''')

    def crt_cdrdPatientInfoBinary(self, varCommon):

        # 患者基本信息

        varTable = 'CDRD_PATIENT_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_id	int	IDENTITY(1,1) PRIMARY KEY,
                patient_name nvarchar(50),
                patient_sex_key varchar(100),
                patient_sex_value nvarchar(100),
                patient_birth_date Date,
                patient_age int,
                patient_birth_address_province_key varchar(100),
                patient_birth_address_province nvarchar(100),
                patient_birth_address_city_key varchar(100),
                patient_birth_address_city nvarchar(100),
                patient_birth_address_country_key varchar(100),
                patient_birth_address_country nvarchar(100),
                patient_country nvarchar(20),
                patient_native_province_key varchar(100),
                patient_native_province nvarchar(100),
                patient_native_city_key varchar(100),
                patient_native_city nvarchar(100),
                patient_nation_key varchar(100),
                patient_nation_value nvarchar(100),
                patient_profession nvarchar(50),
                patient_marriage_key varchar(100),
                patient_marriage_value nvarchar(100),
                patient_id_type_key varchar(100),
                patient_id_type_value nvarchar(100),
                patient_account_address nvarchar(200),
                patient_contact_relation nvarchar(20),
                patient_update_time datetime,
                patient_data_source_key varchar(100),
                patient_source_id int,
                patient_phone_num varbinary(128),
                patient_home_address varbinary(400),
                patient_home_phone varbinary(160),
                patient_contact_phone varbinary(160),
                patient_contact_address varbinary(400),
                patient_contact_name varbinary(160),
                patient_id_num varbinary(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_name', '姓名'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_sex_key', '性别-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_sex_value', '性别'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_date', '出生日期'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_age', '年龄'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_province_key', '出生地-省-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_province', '出生地-省'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_city_key', '出生地-市-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_city', '出生地-市'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_country_key', '出生地-县-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_birth_address_country', '出生地-县'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_country', '国籍'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_province_key', '籍贯-省-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_province', '籍贯-省'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_city_key', '籍贯-市-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_native_city', '籍贯-市'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nation_key', '民族-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nation_value', '民族'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_profession', '职业'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_marriage_key', '婚姻-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_marriage_value', '婚姻'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id_type_key', '证件类型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id_type_value', '证件类型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_account_address', '户口地址'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_relation', '与患者关系'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_data_source_key', '数据来源')
        Sqlserver_PO.setFieldComment(varTable, 'patient_source_id', '源库患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_phone_num', '联系电话（AES28）'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_home_address', '现住址（AES28）'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_home_phone', '家庭电话（AES28）'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_phone', '联系人电话（AES28）'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_address', '联系人地址（AES28）'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_contact_name', '联系人姓名（AES28）')
        Sqlserver_PO.setFieldComment(varTable, 'patient_id_num', '身份证号码（AES28）')

    def cre_a_cdrd_patient_info(self, varCommon):
        table = 'a_cdrd_patient_info'

        # 定义字段与注释的映射关系
        field_comments = [
            ('patient_id', '患者ID'),
            ('patient_sex_key', '性别-key'),
            ('patient_sex_value', '性别'),
            ('patient_birth_date', '出生日期'),
            ('patient_age', '年龄'),
            ('patient_birth_address_province_key', '出生地-省-key'),
            ('patient_birth_address_province', '出生地-省'),
            ('patient_birth_address_city_key', '出生地-市-key'),
            ('patient_birth_address_city', '出生地-市'),
            ('patient_birth_address_country_key', '出生地-县-key'),
            ('patient_birth_address_country', '出生地-县'),
            ('patient_country', '国籍'),
            ('patient_native_province_key', '籍贯-省-key'),
            ('patient_native_province', '籍贯-省'),
            ('patient_native_city_key', '籍贯-市-key'),
            ('patient_native_city', '籍贯-市'),
            ('patient_nation_key', '民族-key'),
            ('patient_nation_value', '民族'),
            ('patient_marriage_key', '婚姻-key'),
            ('patient_marriage_value', '婚姻'),
            ('patient_id_type_key', '证件类型-key'),
            ('patient_id_type_value', '证件类型'),
            ('patient_id_num', '证件号码'),
            ('patient_home_phone', '家庭电话'),
            ('patient_account_address', '户口地址'),
            ('patient_contact_name', '联系人姓名'),
            ('patient_contact_relation', '与患者关系'),
            ('patient_contact_phone', '联系人电话'),
            ('patient_contact_address', '联系人地址'),
            ('patient_phone_num', '联系电话'),
            ('patient_home_address', '现住址'),
            ('patient_profession', '职业'),
            ('patient_update_time', '更新时间'),
            ('patient_data_source_key', '数据来源'),
        ]

        # 批量设置字段注释
        for field, comment in field_comments:
            Sqlserver_PO.setFieldComment(table, field, comment)

        # 设置表注释
        Sqlserver_PO.setTableComment(table, varCommon + '(测试用)')

    def index(self, index,table,field):

        # 创建非聚集索引
        # 主键索引：如果字段已经是主键，则自动拥有聚集索引，无需重复创建。
        # 索引维护成本：索引会提升查询性能，但会影响插入 / 更新性能，建议在数据导入完成后创建。

        sql = "CREATE NONCLUSTERED INDEX " + index + " ON " + table + " (" + field + ")"
        Sqlserver_PO.execute(sql)
    def updateStatistics(self, table):

        # 统计信息更新：创建索引后建议更新统计信息：
        # UPDATE STATISTICS a_cdrd_patient_info;
        # UPDATE STATISTICS a_sys_department;
        # UPDATE STATISTICS ab_hospital;
        # UPDATE STATISTICS a_sys_dept_medgp;
        # UPDATE STATISTICS a_sys_dept_medgp_person;
        sql = "UPDATE STATISTICS " + table
        Sqlserver_PO.execute(sql)


    def crt_cdrdPatientDiagInfo(self, varCommon):

        # 诊断表
        varTable = 'CDRD_PATIENT_DIAG_INFO'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_diag_id	int	IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_case_num varchar(100),
                patient_diag_num varchar(100),
                patient_diag_class nvarchar(20),
                patient_diag_name nvarchar(50),
                patient_diag_is_primary_key varchar(100),
                patient_diag_is_primary_value nvarchar(100),
                patient_diag_code varchar(40),
                patient_diag_ata nvarchar(100),
                patient_diag_cas nvarchar(100),
                patient_in_state_key varchar(100),
                patient_in_state_value nvarchar(100),
                patient_outcome_state_key varchar(100),
                patient_outcome_state_value nvarchar(100),
                patient_diag_date datetime,
                patient_diag_delete_state_key varchar(100),
                patient_diag_update_time datetime,
                patient_diag_data_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_id', '诊断病史ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '诊断医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_num', '病案号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_num', '病人诊断序号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_class', '诊断类型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_name', '诊断名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_is_primary_key', '主要诊断-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_is_primary_value', '主要诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_code', 'ICD10编码'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_ata', 'ATA分级'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_cas', 'CAS分级'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_in_state_key', '入院病情-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_in_state_value', '入院病情'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_outcome_state_key', '出院情况-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_outcome_state_value', '出院情况'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_date', '诊断日期'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_delete_state_key', '删除状态'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_diag_data_source_key', '数据来源')
    def crt_cdrdPatientVisitInfo(self, varCommon):

        # 门(急)诊住院就诊信息
        varTable = 'CDRD_PATIENT_VISIT_INFO'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_visit_id int IDENTITY(1,1) PRIMARY KEY,
                patient_visit_type_key varchar(100),
                patient_visit_type_value nvarchar(100),
                patient_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_mz_zy_num varchar(100),
                patient_visit_age int,
                patient_visit_in_dept_num varchar(100),
                patient_visit_in_dept_name nvarchar(50),
                patient_visit_in_ward_name nvarchar(50),
                patient_visit_doc_num varchar(100),
                patient_visit_doc_code varchar(100),
                patient_visit_doc_name nvarchar(50),
                patient_visit_in_time datetime,
                patient_visit_record_num varchar(100),
                patient_visit_main_describe nvarchar(500),
                patient_visit_present_illness nvarchar(max),
                patient_visit_past_illness nvarchar(max),
                patient_visit_personal_illness nvarchar(500),
                patient_visit_menstrual_history nvarchar(500),
                patient_visit_obsterical_history nvarchar(500),
                patient_visit_family_history nvarchar(500),
                patient_visit_physical_examination nvarchar(max),
                patient_visit_speciality_examination nvarchar(max),
                patient_visit_assit_examination nvarchar(max),
                patient_visit_diag nvarchar(1000),
                patient_visit_deal nvarchar(max),
                patient_visit_record_time datetime,
                patient_case_num varchar(100),
                patient_case_health_card_num varchar(100),
                patient_case_medical_payment_type_key varchar(100),
                patient_case_medical_payment_type_value nvarchar(100),
                patient_case_visit_time int,
                patient_case_visit_in_way_key varchar(100),
                patient_case_visit_in_way_value nvarchar(100),
                patient_case_visit_in_days int,
                patient_visit_out_dept_num varchar(100),
                patient_visit_out_dept_name nvarchar(50),
                patient_visit_out_ward_name nvarchar(50),
                patient_visit_out_time datetime,
                patient_case_clinic_diag nvarchar(500),
                patient_case_diag_name nvarchar(500),
                patient_case_drug_allergy_type_key varchar(100),
                patient_case_drug_allergy_type_value nvarchar(100),
                patient_case_drug_allergy_name nvarchar(100),
                patient_case_abo_type_key varchar(100),
                patient_case_abo_type_value nvarchar(100),
                patient_case_rh_type_key varchar(100),
                patient_case_rh_type_value nvarchar(100),
                patient_case_dept_chief_doc_num varchar(100),
                patient_case_dept_chief_doc_code varchar(100),
                patient_case_dept_chief_doc_name nvarchar(20),
                patient_case_director_doc_num varchar(100),
                patient_case_director_doc_code varchar(100),
                patient_case_director_doc_name nvarchar(20),
                patient_case_attend_doc_num varchar(100),
                patient_case_attend_doc_code varchar(100),
                patient_case_attend_doc_name nvarchar(20),
                patient_case_resident_num varchar(100),
                patient_case_resident_code varchar(100),
                patient_case_resident_name nvarchar(20),
                patient_case_out_hospital_type_key varchar(100),
                patient_case_out_hospital_type_value nvarchar(100),
                patient_case_transfer_to_hospital nvarchar(50),
                patient_case_make_over_hospital nvarchar(50),
                patient_case_in_total_cost decimal(20,8),
                patient_case_in_selfpay_cost decimal(20,8),
                patient_visit_update_time datetime,
                patient_visit_data_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_type_key', '就诊类型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_type_value', '就诊类型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_mz_zy_num', '源系统门诊/住院号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_age', '就诊年龄（岁）'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_in_dept_num', '就诊科室编码'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_in_dept_name', '就诊科室'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_in_ward_name', '入院病房'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_doc_num', '就诊医生编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_doc_code', '就诊医生code'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_doc_name', '就诊医生'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_in_time', '就诊日期'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_record_num', '文书编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_main_describe', '主诉'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_present_illness', '现病史'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_past_illness', '既往史'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_personal_illness', '个人史'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_menstrual_history', '月经史'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_obsterical_history', '婚育史'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_family_history', '家族史'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_physical_examination', '体格检查'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_speciality_examination', '专科检查'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_assit_examination', '辅助检查'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_diag', '就诊诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_deal', '处置'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_record_time', '记录时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_num', '病案号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_health_card_num', '健康卡号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_medical_payment_type_key',
                                     '医疗付费方式-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_medical_payment_type_value', '医疗付费方式'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_visit_time', '住院次数'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_visit_in_way_key', '入院途径-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_visit_in_way_value', '入院途径'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_visit_in_days', '实际住院天数'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_out_dept_num', '出院科室编码'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_out_dept_name', '出院科室'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_out_ward_name', '出院病房'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_out_time', '出院日期'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_clinic_diag', '门（急）诊诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_diag_name', '入院诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_drug_allergy_type_key', '药物过敏-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_drug_allergy_type_value', '药物过敏'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_drug_allergy_name', '过敏药物'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_abo_type_key', 'ABO血型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_abo_type_value', 'ABO血型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_rh_type_key', 'Rh血型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_rh_type_value', 'Rh血型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_dept_chief_doc_num', '科主任编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_dept_chief_doc_code', '科主任code'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_dept_chief_doc_name', '科主任'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_director_doc_num', '主任（副主任）医师编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_director_doc_code', '主任（副主任）医师code'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_director_doc_name', '主任（副主任）医师'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_attend_doc_num', '主治医师编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_attend_doc_code', '主治医师code'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_attend_doc_name', '主治医师'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_resident_num', '住院医师编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_resident_code', '住院医师code'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_resident_name', '住院医师'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_out_hospital_type_key', '离院方式-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_out_hospital_type_value', '离院方式'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_transfer_to_hospital', '医嘱转院，拟接收机构'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_make_over_hospital', '医嘱转让社区卫生机构，拟接收机构'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_in_total_cost', '住院费用-总费用'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_case_in_selfpay_cost', '住院费用-自付金额'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_data_source_key', '数据来源')
    def crt_cdrdPatientSymptomInfo(self, varCommon):

        # 症状信息
        varTable = 'CDRD_PATIENT_SYMPTOM_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_symptom_id int IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_symptom_num varchar(100),
                patient_symptom_name nvarchar(50),
                patient_symptom_description nvarchar(max),
                patient_symptom_start_time datetime,
                patient_symptom_end_time datetime,
                patient_symptom_delete_state_key varchar(100),
                patient_symptom_update_time datetime,
                patient_symptom_data_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_id', '症状ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_num', '症状编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_name', '症状名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_description', '具体描述'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_start_time', '出现时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_end_time', '结束时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_delete_state_key', '删除状态'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_symptom_data_source_key', '数据来源')
    def crt_cdrdPatientPhysicalSignInfo(self, varCommon):

        # 体征信息
        varTable = 'CDRD_PATIENT_PHYSICAL_SIGN_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_physical_sign_id int IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_physical_sign_type_key varchar(100),
                patient_physical_sign_type_value nvarchar(100),
                patient_physical_sign_other nvarchar(20),
                patient_physical_sign_value varchar(40),
                patient_physical_sign_unit_key varchar(100),
                patient_physical_sign_unit_value nvarchar(100),
                patient_physical_sign_other_unit nvarchar(20),
                patient_physical_sign_time datetime,
                patient_physical_sign_delete_state_key varchar(100),
                patient_physical_sign_update_time datetime,
                patient_physical_sign_data_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_type_key', '体征-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_type_value', '体征'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_other', '其他体征'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_value', '体征数值'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_unit_key', '体征单位-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_unit_value', '体征单位'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_other_unit', '其他体征单位'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_time', '检测时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_delete_state_key',
                                     '删除状态'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_physical_sign_data_source_key',
                                     '数据来源')
    def crt_cdrdPatientLabExaminationInfo(self, varCommon):

        # 实验室检查报告
        varTable = 'CDRD_PATIENT_LAB_EXAMINATION_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
               patient_lab_examination_id int IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_lab_examination_report_num varchar(100),
                patient_lab_examination_source_report_num varchar(100),
                patient_lab_examination_report_name nvarchar(50),
                patient_lab_examination_sample_type nvarchar(50),
                patient_lab_examination_test_time datetime,
                patient_lab_examination_sampling_time datetime,
                patient_lab_examination_report_time datetime,
                patient_lab_examination_delete_state_key varchar(100),
                patient_lab_examination_update_time datetime,
                patient_lab_examination_data_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_id', '实验室检查ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_report_num',
                                     '报告编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_source_report_num',
                                     '源系统报告编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_report_name',
                                     '报告名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_sample_type',
                                     '样本类型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_test_time',
                                     '检查时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_sampling_time',
                                     '采样时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_report_time',
                                     '报告时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_delete_state_key',
                                     '删除状态'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_update_time',
                                     '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_lab_examination_data_source_key',
                                     '数据来源')
    def crt_cdrdPatientAssitExaminationInfo(self, varCommon):

        # 辅助检查报告
        varTable = 'CDRD_PATIENT_ASSIT_EXAMINATION_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_assit_examination_id int IDENTITY(1,1) PRIMARY KEY,
                patient_assit_examination_type_key varchar(100),
                patient_assit_examination_type_value nvarchar(100),
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_assit_examination_report_num varchar(100),
                patient_assit_examination_source_report_num varchar(100),
                patient_assit_examination_report_name nvarchar(50),
                patient_assit_examination_check_method nvarchar(50),
                patient_assit_examination_body_site nvarchar(50),
                patient_assit_examination_sample_body nvarchar(50),
                patient_assit_examination_eye_find nvarchar(2000),
                patient_assit_examination_microscope_find nvarchar(3000),
                patient_assit_examination_check_find nvarchar(2000),
                patient_assit_examination_check_conclusion nvarchar(2000),
                patient_assit_examination_check_time datetime,
                patient_assit_examination_report_time datetime,
                patient_assit_examination_delete_state_key varchar(100),
                patient_assit_examination_update_time datetime,
                patient_assit_examination_data_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_id', '辅助检查ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_type_key',
                                     '辅助检查类型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_type_value',
                                     '辅助检查类型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '检查医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_report_num',
                                     '报告编号'),
        Sqlserver_PO.setFieldComment(varTable,
                                     'patient_assit_examination_source_report_num', '源系统报告编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_report_name',
                                     '报告名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_check_method',
                                     '检查方法'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_body_site',
                                     '检查部位'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_sample_body',
                                     '取材部位及组织名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_eye_find',
                                     '肉眼所见'),
        Sqlserver_PO.setFieldComment(varTable,
                                     'patient_assit_examination_microscope_find', '镜下所见'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_check_find',
                                     '检查所见'),
        Sqlserver_PO.setFieldComment(varTable,
                                     'patient_assit_examination_check_conclusion', '检查结论'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_check_time',
                                     '检查日期'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_report_time',
                                     '报告日期'),
        Sqlserver_PO.setFieldComment(varTable,
                                     'patient_assit_examination_delete_state_key', '删除状态'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_assit_examination_update_time',
                                     '更新时间'),
        Sqlserver_PO.setFieldComment(varTable,
                                     'patient_assit_examination_data_source_key', '数据来源')
    def crt_cdrdPatientTestProjectInfo(self, varCommon):

        # 检查项目明细
        varTable = 'CDRD_PATIENT_TEST_PROJECT_INFO'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_test_id int IDENTITY(1,1) PRIMARY KEY,
                patient_superior_examination_id int,
                patient_superior_examination_type int,
                patient_report_num varchar(100),
                patient_test_item_num varchar(100),
                patient_test_item_name nvarchar(50),
                patient_test_numerical_value nvarchar(50),
                patient_test_unit_name nvarchar(50),
                patient_test_text_value nvarchar(50),
                patient_test_abnormal_flag nvarchar(50),
                patient_test_reference_range nvarchar(50),
                patient_test_delete_state_key varchar(100),
                patient_test_update_time datetime,
                patient_test_data_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_id', '项目ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_superior_examination_id', '上级检查ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_superior_examination_type', '上级检查类型，实验室检查为1，辅助检查为2'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_report_num', '报告编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_item_num', '项目代码'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_item_name', '项目名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_numerical_value', '定量结果'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_unit_name', '定量结果单位'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_text_value', '定性结果'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_abnormal_flag', '异常标识'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_reference_range', '参考值（范围）'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_delete_state_key', '删除状态'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_test_data_source_key', '数据来源')
    def crt_cdrdPatientClinicAdviceInfo(self, varCommon):

        # 门诊医嘱
        varTable = 'CDRD_PATIENT_CLINIC_ADVICE_INFO'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_clinic_advice_id int IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_outpat_recipe_detail_num varchar(100),
                patient_recipe_class nvarchar(50),
                patient_recipe_name nvarchar(50),
                patient_recipe_drug_flag_key varchar(100),
                patient_recipe_drug_flag_value nvarchar(100),
                patient_recipe_time datetime,
                patient_recipe_exec_dept_name nvarchar(50),
                patient_clinic_advice_update_time datetime,
                patient_clinic_advice_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_clinic_advice_id', '门诊医嘱ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '检查医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_outpat_recipe_detail_num', '处方明细编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_recipe_class', '处方类别'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_recipe_name', '处方名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_recipe_drug_flag_key', '是否药品-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_recipe_drug_flag_value', '是否药品'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_recipe_time', '开方时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_recipe_exec_dept_name', '执行科室'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_clinic_advice_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_clinic_advice_source_key', '数据来源')
    def crt_cdrdPatientHospitalAdviceInfo(self, varCommon):

        # 住院医嘱
        varTable = 'CDRD_PATIENT_HOSPITAL_ADVICE_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_hospital_advice_id int IDENTITY(1,1) PRIMARY KEY,
                patient_hospital_advice_type_key varchar(100),
                patient_hospital_advice_type_value nvarchar(100),
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_hospital_advice_num varchar(100),
                patient_hospital_advice_source_num varchar(100),
                patient_hospital_advice_class nvarchar(50),
                patient_hospital_advice_name nvarchar(50),
                patient_hospital_advice_remark nvarchar(2000),
                patient_hospital_advice_begin_time datetime,
                patient_hospital_advice_end_time datetime,
                patient_hospital_advice_exec_dept_name nvarchar(50),
                patient_hospital_advice_update_time datetime,
                patient_hospital_advice_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_id', '住院医嘱ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_type_key',
                                     '住院医嘱类型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_type_value',
                                     '住院医嘱类型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_num', '医嘱编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_source_num',
                                     '源系统医嘱编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_class', '医嘱类别'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_name', '医嘱名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_remark', '备注'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_begin_time',
                                     '医嘱开始时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_end_time',
                                     '医嘱结束时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_exec_dept_name',
                                     '执行科室'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_update_time',
                                     '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_advice_source_key',
                                     '数据来源')
    def crt_cdrdPatientDrugInfo_test(self, varCommon):

        # 用药信息
        varTable = 'CDRD_PATIENT_DRUG_INFO_test'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_drug_id int IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_superior_advice_id int,
                patient_superior_advice_type int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name varchar(50),
                patient_recipe_advice_num varchar(100),
                patient_drug_name nvarchar(50),
                patient_drug_specs nvarchar(50),
                patient_drug_frequency nvarchar(50),
                patient_drug_once_dose varchar(100),
                patient_drug_dose_unit nvarchar(50),
                patient_drug_usage nvarchar(50),
                patient_drug_qty varchar(100),
                patient_drug_begin_time datetime,
                patient_drug_end_time datetime,
                patient_drug_delete_state_key varchar(100),
                patient_drug_update_time datetime,
                patient_drug_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_id', '用药信息ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_superior_advice_id', '取值门诊医嘱ID或者住院医嘱ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_superior_advice_type', '上级医嘱类型，门诊医嘱为1，住院医嘱为2'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_recipe_advice_num', '处方明细/医嘱编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_name', '药品名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_specs', '规格'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_frequency', '频次'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_once_dose', '每次用量'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_dose_unit', '用量单位'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_usage', '用法'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_qty', '总量'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_begin_time', '开始时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_end_time', '结束时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_delete_state_key', '删除状态'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_source_key', '数据来源')
    def crt_cdrdPatientDrugInfo(self, varCommon):

        # 用药信息
        varTable = 'CDRD_PATIENT_DRUG_INFO'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_drug_id int IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_superior_advice_id int,
                patient_superior_advice_type int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name varchar(50),
                patient_recipe_advice_num varchar(100),
                patient_drug_name nvarchar(50),
                patient_drug_specs nvarchar(50),
                patient_drug_frequency nvarchar(50),
                patient_drug_once_dose varchar(100),
                patient_drug_dose_unit nvarchar(50),
                patient_drug_usage nvarchar(50),
                patient_drug_qty varchar(100),
                patient_drug_begin_time datetime,
                patient_drug_end_time datetime,
                patient_drug_delete_state_key varchar(100),
                patient_drug_update_time datetime,
                patient_drug_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_id', '用药信息ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_superior_advice_id', '取值门诊医嘱ID或者住院医嘱ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_superior_advice_type', '上级医嘱类型，门诊医嘱为1，住院医嘱为2'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_recipe_advice_num', '处方明细/医嘱编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_name', '药品名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_specs', '规格'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_frequency', '频次'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_once_dose', '每次用量'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_dose_unit', '用量单位'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_usage', '用法'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_qty', '总量'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_begin_time', '开始时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_end_time', '结束时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_delete_state_key', '删除状态'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_drug_source_key', '数据来源')
    def crt_cdrdPatientOutHospitalInfo(self, varCommon):

        # 出院记录
        varTable = 'CDRD_PATIENT_OUT_HOSPITAL_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_out_hospital_id int IDENTITY(1,1) PRIMARY KEY,
                patient_out_hospital_type_key varchar(100),
                patient_out_hospital_type_value nvarchar(100),
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_out_hospital_record_num varchar(100),
                patient_out_hospital_main_describe nvarchar(500),
                patient_out_hospital_in_situation nvarchar(max),
                patient_out_hospital_in_diag nvarchar(500),
                patient_out_hospital_diag_process nvarchar(max),
                patient_out_hospital_diag nvarchar(500),
                patient_out_hospital_situation nvarchar(max),
                patient_out_hospital_advice nvarchar(500),
                patient_out_hospital_record_time datetime,
                patient_out_hospital_update_time datetime,
                patient_out_hospital_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_id', '出院记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_type_key', '出院记录类型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_type_value', '出院记录类型-value'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_record_num', '文书编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_main_describe', '主诉'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_in_situation', '入院情况'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_in_diag', '入院诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_diag_process', '诊疗经过'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_diag', '出院诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_situation', '出院情况'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_advice', '出院医嘱'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_record_time', '记录时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_out_hospital_source_key', '数据来源')
    def crt_cdrdPatientOperationInfo(self, varCommon):

        # 手术记录
        varTable = 'CDRD_PATIENT_OPERATION_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_operation_id int IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_operation_num varchar(100),
                patient_operation_source_num varchar(100),
                patient_operation_name nvarchar(50),
                patient_operation_doc_name nvarchar(50),
                patient_operation_assist_I nvarchar(50),
                patient_operation_assist_II nvarchar(50),
                patient_operation_before_diag nvarchar(500),
                patient_operation_during_diag nvarchar(500),
                patient_operation_after_diag nvarchar(500),
                patient_operation_level_key varchar(100),
                patient_operation_level_value nvarchar(100),
                patient_operation_type_key varchar(100),
                patient_operation_type_value nvarchar(100),
                patient_operation_incision_healing_grade_key varchar(100),
                patient_operation_incision_healing_grade_value nvarchar(100),
                patient_operation_anesthesiologist nvarchar(50),
                patient_operation_anesthesia_type nvarchar(50),
                patient_operation_step_process nvarchar(max),
                patient_operation_begin_time datetime,
                patient_operation_end_time datetime,
                patient_operation_delete_state_key varchar(100),
                patient_operation_update_time datetime,
                patient_operation_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_id', '手术记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_num', '手术记录编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_source_num', '源系统手术记录编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_name', '手术名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_doc_name', '主刀/手术者'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_assist_I', 'I助'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_assist_II', 'II助'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_before_diag', '术前诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_during_diag', '术中诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_after_diag', '术后诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_level_key', '手术级别-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_level_value', '手术级别'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_type_key', '手术类型-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_type_value', '手术类型'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_incision_healing_grade_key',
                                     '切口愈合等级-key'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_incision_healing_grade_value',
                                     '切口愈合等级'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_anesthesiologist', '麻醉者'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_anesthesia_type', '麻醉方式'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_step_process', '手术步骤及经过'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_begin_time', '手术开始时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_end_time', '手术结束时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_delete_state_key', '删除状态'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_operation_source_key', '数据来源')
    def crt_cdrdPatientNurseInfo(self, varCommon):

        # 护理记录
        varTable = 'CDRD_PATIENT_NURSE_INFO'

        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_nurse_id int IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_hospital_code varchar(100),
                patient_hospital_name nvarchar(50),
                patient_nurse_record_num varchar(100),
                patient_nurse_record_time datetime,
                patient_nurse_record_name nvarchar(50),
                patient_nurse_value nvarchar(50),
                patient_nurse_unit nvarchar(50),
                patient_nurse_update_time datetime,
                patient_nurse_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_nurse_id', '护理记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_code', '就诊医疗机构编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_name', '医院名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nurse_record_num', '护理记录编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nurse_record_time', '护理记录时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nurse_record_name', '护理记录名称'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nurse_value', '护理值'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nurse_unit', '护理单位'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nurse_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_nurse_source_key', '数据来源')
    def crt_cdrdPatientDeathInfo(self, varCommon):

        # 死亡记录
        varTable = 'CDRD_PATIENT_DEATH_INFO'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
                patient_death_id int IDENTITY(1,1) PRIMARY KEY,
                patient_id int,
                patient_visit_id int,
                patient_hospital_visit_id varchar(100),
                patient_death_record_id varchar(100),
                patient_death_time datetime,
                patient_death_in_situation nvarchar(max),
                patient_death_in_diag nvarchar(500),
                patient_death_diag_process nvarchar(max),
                patient_death_reason nvarchar(500),
                patient_death_diag nvarchar(500),
                patient_death_update_time datetime,
                patient_death_source_key varchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_id', '死亡记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_id', '患者ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_visit_id', '就诊记录ID'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_hospital_visit_id', '就诊编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_record_id', '文书编号'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_time', '死亡时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_in_situation', '入院情况'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_in_diag', '入院诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_diag_process', '诊疗经过（抢救经过）'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_reason', '死亡原因'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_diag', '死亡诊断'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_update_time', '更新时间'),
        Sqlserver_PO.setFieldComment(varTable, 'patient_death_source_key', '数据来源')

    def crt_sys_dict_type(self, varCommon):

        # 数据字典配置 - 字典类型表

        varTable = 'sys_dict_type'
        Sqlserver_PO.crtTableByCover(varTable,
        '''
        dict_id	int	IDENTITY(1,1) PRIMARY KEY,
        dict_name nvarchar(100),
        dict_type nvarchar(100),
        status int,
        create_by nvarchar(64),
        create_time datetime,
        update_by nvarchar(64),
        update_time datetime,
        remark nvarchar(500)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'dict_id', '字典主键')
        Sqlserver_PO.setFieldComment(varTable, 'dict_name', '字典名称')
        Sqlserver_PO.setFieldComment(varTable, 'dict_type', '字典类型')
        Sqlserver_PO.setFieldComment(varTable, 'status', '状态')
        Sqlserver_PO.setFieldComment(varTable, 'create_by', '创建者')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间')
        Sqlserver_PO.setFieldComment(varTable, 'update_by', '更新者')
        Sqlserver_PO.setFieldComment(varTable, 'update_time', '更新时间')
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')

    def importExcel(self, varFile, varSheet):
        # 'CDRB20250623.xlsx', '数据字典表'
        Sqlserver_PO.xlsx2db_deduplicated((varFile, "a_sys_dict_type", "dict_name", "dict1"))

    def crt_sys_dict_data(self, varCommon):

        # 数据字典配置 - 字典数据表

        varTable = 'sys_dict_data'
        Sqlserver_PO.crtTableByCover(varTable,
        '''
        dict_code	int	IDENTITY(1,1) PRIMARY KEY,
        dict_sort int,
        dict_label varchar(100),
        dict_value varchar(100),
        dict_type varchar(100),
        css_class varchar(100),
        list_class varchar(100),
        is_default int,
        status int,
        create_by varchar(64),
        create_time datetime,
        update_by varchar(64),
        update_time datetime,
        remark varchar(500)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'dict_code', '字典编码')
        Sqlserver_PO.setFieldComment(varTable, 'dict_sort', '字典排序')
        Sqlserver_PO.setFieldComment(varTable, 'dict_label', '字典标签')
        Sqlserver_PO.setFieldComment(varTable, 'dict_value', '字典键值')
        Sqlserver_PO.setFieldComment(varTable, 'dict_type', '字典类型')
        Sqlserver_PO.setFieldComment(varTable, 'css_class', '样式属性（其他样式扩展）')
        Sqlserver_PO.setFieldComment(varTable, 'list_class', '表格回显样式')
        Sqlserver_PO.setFieldComment(varTable, 'is_default', '是否默认')
        Sqlserver_PO.setFieldComment(varTable, 'status', '状态')
        Sqlserver_PO.setFieldComment(varTable, 'create_by', '创建者')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间')
        Sqlserver_PO.setFieldComment(varTable, 'update_by', '更新者')
        Sqlserver_PO.setFieldComment(varTable, 'update_time', '更新时间')
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')


    def procedure(self, varProcedure, varDesc):
        # 通用存储过程
        # 创建并执行存储过程，插入N条记录

        # 删除存储过程
        Sqlserver_PO.execute(f"DROP PROCEDURE IF EXISTS dbo.{varProcedure};")

        varParamSql = varProcedure + ".sql"
        with open(varParamSql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        Sqlserver_PO.execute(sql_script)

        # 添加描述
        varDesc_escaped = varDesc.replace("'", "''") # 转义所有单引号
        Sqlserver_PO.execute(f"""EXEC sp_addextendedproperty @name = N'MS_Description', @value = N'{varDesc_escaped}',@level0type = N'Schema', @level0name = 'dbo', @level1type = N'Procedure', @level1name = '{varProcedure}';""")

        import time
        time_start = time.time()
        # 执行存储过程
        # # need @result
        row = Sqlserver_PO.select(f"""DECLARE @R int;
                EXEC {varProcedure} @result = @R OUTPUT;
                SELECT @R as ReturnValue;
                """)
        # print(row)
        print(varProcedure + "(" + varDesc + ") => 生成", int(row[0]['ReturnValue']), "条！")

        time_end = time.time()
        time = time_end - time_start
        # print('耗时：%s 秒' % time)  # 耗时：6.003570795059204 秒
        print(f"\n耗时: {time:.4f} 秒")  # 6.0036 秒

        # varTable = "a_" + varProcedure
        # varTable = varProcedure
        # result = Sqlserver_PO.selectOne("select count(*) as qty from %s" % (varTable))
        # print(result)



    def procedure5(self, varProcedure, varDesc, varQty=1):
        # 通用存储过程
        # 创建并执行存储过程，插入N条记录

        # 删除存储过程（用于）
        Sqlserver_PO.execute(f"DROP PROCEDURE IF EXISTS dbo.{varProcedure};")

        varParamSql = varProcedure + ".sql"
        with open(varParamSql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        Sqlserver_PO.execute(sql_script)

        # 添加描述
        varDesc_escaped = varDesc.replace("'", "''") # 转义所有单引号
        Sqlserver_PO.execute(f"""EXEC sp_addextendedproperty @name = N'MS_Description', @value = N'{varDesc_escaped}',@level0type = N'Schema', @level0name = 'dbo', @level1type = N'Procedure', @level1name = '{varProcedure}';""")

        # 执行存储过程
        # need @result
        row = Sqlserver_PO.select(f"""DECLARE @R int;
        EXEC {varProcedure} @result = @R OUTPUT;
        SELECT @R as ReturnValue;
        """)
        print(varProcedure + "(" + varDesc + ") => 生成", int(row[0]['ReturnValue']) * varQty, "条!")
# EXEC cdrd_patient_diag_info @RecordCount = 5, @result = @output OUTPUT;
#         execParam = "exec " + varProcedure + " @RecordCount=" + str(varQty) + ", @result = @output OUTPUT;"
        # print(varProcedure + "(" + varDesc + ") => 生成", varQty, "条!")
        # Sqlserver_PO.execute(execParam)


    def procedure20(self, varProcedure, varDesc, varQty=None):
        # 通用存储过程
        # 创建并执行存储过程，插入N条记录

        # 删除存储过程（用于）
        Sqlserver_PO.execute(f"DROP PROCEDURE IF EXISTS dbo.{varProcedure};")

        varParamSql = varProcedure + ".sql"
        with open(varParamSql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        Sqlserver_PO.execute(sql_script)

        # 添加描述
        varDesc_escaped = varDesc.replace("'", "''") # 转义所有单引号
        Sqlserver_PO.execute(f"""EXEC sp_addextendedproperty @name = N'MS_Description', @value = N'{varDesc_escaped}', @level0type = N'Schema', @level0name = 'dbo', @level1type = N'Procedure', @level1name = '{varProcedure}';""")

        # 执行存储过程
        if varQty == None:
            # need @result
            row = Sqlserver_PO.select(f"""DECLARE @R int;EXEC {varProcedure} @result = @R OUTPUT;SELECT @R as ReturnValue;""")
            print(varProcedure + "(" + varDesc + ") => 生成", int(row[0]['ReturnValue']) * 20, "条!")
        else:
            # no need @result
            execParam = "exec " + varProcedure + " @RecordCount=" + str(varQty) + ";"
            print(varProcedure + "(" + varDesc + ") => 生成", varQty, "条!")
            Sqlserver_PO.execute(execParam)

    def subProcedure(self, varProcedure, varDesc):
        # 子存储过程
        # 创建存储过程，不执行

        # 删除存储过程（用于添加描述）
        # Sqlserver_PO.execute(f"DROP PROCEDURE IF EXISTS dbo.{varProcedure};")

        varParamSql = varProcedure + ".sql"
        with open(varParamSql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        Sqlserver_PO.execute(sql_script)

        # 添加描述
        varDesc_escaped = varDesc.replace("'", "''")  # 转义所有单引号   //存储过程描述
        Sqlserver_PO.execute(f"""EXEC sp_addextendedproperty @name = N'MS_Description', @value = N'{varDesc_escaped}',@level0type = N'Schema', @level0name = 'dbo', @level1type = N'Procedure', @level1name = '{varProcedure}';""")

        # IF EXISTS (SELECT 1 FROM sys.extended_properties WHERE major_id = OBJECT_ID('dbo.p_outcome_state') AND name = 'MS_Description')
        # 修改
        #     EXEC sp_updateextendedproperty ...
        # ELSE
        # 添加
        #     EXEC sp_addextendedproperty ...

    def subFunction(self, varProcedure):
        # 子存储过程
        # 创建存储过程，不执行

        # 删除存储过程（用于添加描述）
        Sqlserver_PO.execute(f"DROP FUNCTION IF EXISTS dbo.{varProcedure};")

        varParamSql = varProcedure + ".sql"
        with open(varParamSql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        Sqlserver_PO.execute(sql_script)

        # # 添加描述
        # # 转义所有单引号
        # varDesc_escaped = varDesc.replace("'", "''")
        # desc = f"""
        #         EXEC sp_addextendedproperty
        #             @name = N'MS_Description',
        #             @value = N'{varDesc_escaped}',
        #             @level0type = N'Schema',
        #             @level0name = 'dbo',
        #             @level1type = N'Procedure',
        #             @level1name = '{varProcedure}';
        #     """
        # Sqlserver_PO.execute(desc)

        # IF EXISTS (SELECT 1 FROM sys.extended_properties WHERE major_id = OBJECT_ID('dbo.p_outcome_state') AND name = 'MS_Description')
        # 修改
        #     EXEC sp_updateextendedproperty ...
        # ELSE
        # 添加
        #     EXEC sp_addextendedproperty ...




    def procedureMenu(self, varProcedure, varDesc, l_param):
        # 菜单管理 - 创建存储过程
        # Cdrd_PO.procedureMenu("a_sys_menu__data",['无','m', '系统管理'])
        # Cdrd_PO.procedureMenu("a_sys_menu__data",['系统管理', 'c', '用户管理'])
        # Cdrd_PO.procedureMenu("a_sys_menu__data",[ '用户管理', 'f', '查询'])
        # 参数：['C', '医生管理', '系统监控']，三个参数不能少，如果没有父级菜单输入None
        # 参数1：M是目录，C是菜单，F是按钮，层级关系是M-C-F
        # 参数2：menu_user 菜单名称
        # 参数3：parent_id 父级菜单ID
        # 注意：None表示无父级菜单，

        # 删除存储过程（用于添加描述）
        Sqlserver_PO.execute(f"DROP PROCEDURE IF EXISTS dbo.{varProcedure};")

        if len(l_param) != 3:
            print("error, 缺少参数")
            exit(0)
        else:
            execParam = "exec " + varProcedure + " @menuType=" + str(l_param[0]) + ", @menuName=" + str(l_param[1]) + ", @menuParentName=" + str(l_param[2]) + ";"
            print(execParam)

            # if l_param[1] != 'm':
            #     execParam = "exec " + varProcedure + " @menuParentName=" + str(l_param[0]) + ", @menuName=" + str(l_param[2]) + ";"
            # else:
            #     execParam = "exec " + varProcedure + " @menuName=" + str(l_param[2]) + ";"

        varParamSql = varProcedure + ".sql"
        with open(varParamSql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        Sqlserver_PO.execute(sql_script)

        # 添加描述
        # 转义所有单引号
        varDesc_escaped = varDesc.replace("'", "''")
        desc = f"""
                EXEC sp_addextendedproperty 
                    @name = N'MS_Description', 
                    @value = N'{varDesc_escaped}',
                    @level0type = N'Schema', 
                    @level0name = 'dbo', 
                    @level1type = N'Procedure', 
                    @level1name = '{varProcedure}';
            """
        Sqlserver_PO.execute(desc)

        Sqlserver_PO.execute(execParam)  # 执行存储过程, 插入N条记录
    def procedureRoleMenu(self, varProcedure, varDesc, d_):
        #  角色菜单关系表
        # exec a_sys_role_menu__data @roleName=副主任, @menu_id=18;

        # 删除存储过程（用于添加描述）
        Sqlserver_PO.execute(f"DROP PROCEDURE IF EXISTS dbo.{varProcedure};")

        varParamSql = varProcedure + ".sql"
        with open(varParamSql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        Sqlserver_PO.execute(sql_script)

        # 添加描述
        # 转义所有单引号
        varDesc_escaped = varDesc.replace("'", "''")
        desc = f"""
            EXEC sp_addextendedproperty 
                @name = N'MS_Description', 
                @value = N'{varDesc_escaped}',
                @level0type = N'Schema', 
                @level0name = 'dbo', 
                @level1type = N'Procedure', 
                @level1name = '{varProcedure}';
        """
        Sqlserver_PO.execute(desc)

        l_keys = list(d_.keys())  # ['科主任', '副主任', '医疗组长', '主治医生', '门/急诊医生、住院医生', '运营负责人']
        l_l_values = list(d_.values())  # [3, 7, 8,9,10,11,12,13,15,24,25,87,109]
        # print(l_keys)
        # print(l_l_values)
        # sys.exit(0)
        for j in range(len(l_keys)):
            for i in l_l_values[j]:
                execParam = "exec " + varProcedure + " @roleName=" + str(l_keys[j]) + ", @menu_id=" + str(i) + ";"
                # print(execParam)
                Sqlserver_PO.execute(execParam)  # 执行存储过程, 插入N条记录

    def procedureUserRole(self, varProcedure, varDesc):
        #  用户角色关系表
        # Cdrd_PO.procedureUserRole("a_sys_user_role__data", {3: 5})  # 用户3关联角色5
        # d_ = {271: [28, 33]}

        # 删除存储过程（用于添加描述）
        Sqlserver_PO.execute(f"DROP PROCEDURE IF EXISTS dbo.{varProcedure};")

        varParamSql = varProcedure + ".sql"
        with open(varParamSql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        Sqlserver_PO.execute(sql_script)

        # 添加描述
        # 转义所有单引号
        varDesc_escaped = varDesc.replace("'", "''")
        desc = f"""
            EXEC sp_addextendedproperty 
                @name = N'MS_Description', 
                @value = N'{varDesc_escaped}',
                @level0type = N'Schema', 
                @level0name = 'dbo', 
                @level1type = N'Procedure', 
                @level1name = '{varProcedure}';
        """
        Sqlserver_PO.execute(desc)

        # 角色id，来自sys_role表
        l_role_id = [28, 33]

        # 用户id，来自sys_user表
        for i in range(270, 470):
            # 一个用户多个角色
            for j in l_role_id:
                execParam = "exec " + varProcedure + " @user_id=" + str(i) + ", @role_id=" + str(j) + ";"
                # print(execParam)
                Sqlserver_PO.execute(execParam)  # 执行存储过程, 插入N条记录

        # d_ = {270: [28, 33]}   469
        # keys = list(d_.keys())[0]
        # values = list(d_.values())[0]  # [18, 20, 21]

        # if isinstance(values, list):
        #     # 一个用户多个角色
        #     for i in values:
        #         execParam = "exec " + varProcedure + " @user_id=" + str(keys) + ", @role_id=" + str(i) + ";"
        #         print(execParam)
        #         Sqlserver_PO.execute(execParam)  # 执行存储过程, 插入N条记录
        # else:
        #     # 一个用户一个角色
        #     execParam = "exec " + varProcedure + " @user_id=" + str(keys) + ", @role_id=" + str(values) + ";"
        #     print(execParam)
        #     Sqlserver_PO.execute(execParam)  # 执行存储过程, 插入N条记录


    # todo 1.1

    def crt_SnowflakeSequence(self, varCommon):

        # 雪花序列表
        varTable = 'SnowflakeSequence'
        Sqlserver_PO.crtTableByCover(varTable,
                                     '''
                                     CurrentSequence INT NOT NULL DEFAULT 0,
                                     LastTimestamp BIGINT NOT NULL DEFAULT 0
                                     ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'CurrentSequence', '雪花序列')
        Sqlserver_PO.setFieldComment(varTable, 'LastTimestamp', '邮戳')

        # -- 初始化数据
        sql = ''' INSERT INTO SnowflakeSequence (CurrentSequence, LastTimestamp) VALUES (0, 0)'''
        Sqlserver_PO.execute(sql)

    def crt_patient_tag(self, varCommon):

        # 标签表

        varTable = 'patient_tag'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            tag_record_id BIGINT PRIMARY KEY,
            category_source_id int,
            category_key nvarchar(100),
            category_id int,
            tag_id int,
            tag_key nvarchar(100),
            tag_data_id int,
            tag_data_key nvarchar(100),
            create_id int,
            create_by nvarchar(20),
            create_time DATETIME
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'tag_record_id', '标签记录 ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_source_id', '所属业务源数据ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_key', '所属业务标识')
        Sqlserver_PO.setFieldComment(varTable, 'category_id', '所属业务数据记录ID')
        Sqlserver_PO.setFieldComment(varTable, 'tag_id', '标签ID')
        Sqlserver_PO.setFieldComment(varTable, 'tag_key', '标签标识')
        Sqlserver_PO.setFieldComment(varTable, 'tag_data_id', '标签数据ID')
        Sqlserver_PO.setFieldComment(varTable, 'tag_data_key', '标签数据标识')
        Sqlserver_PO.setFieldComment(varTable, 'create_id', '创建人ID')
        Sqlserver_PO.setFieldComment(varTable, 'create_by', '创建人')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间')


    def crt_patient_export(self, varCommon):

        # 导出模板

        varTable = 'patient_export'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            model_id int IDENTITY(1,1) PRIMARY KEY,
            model_name nvarchar(50),
            model_type varchar(100),
            create_by_id int,
            create_by nvarchar(20),
            create_time DATETIME,
            remark nvarchar(500)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'model_id', '模板ID')
        Sqlserver_PO.setFieldComment(varTable, 'model_name', '模板名称')
        Sqlserver_PO.setFieldComment(varTable, 'model_type', '模板类型')
        Sqlserver_PO.setFieldComment(varTable, 'create_by_id', '创建人ID')
        Sqlserver_PO.setFieldComment(varTable, 'create_by', '创建人')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间')
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')

    def crt_patient_export_module(self, varCommon):

        # 导出模块

        varTable = 'patient_export_module'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            module_id int IDENTITY(1,1) PRIMARY KEY,
            model_id int,
            module_tier varchar(100),
            module_fa_key nvarchar(100),
            module_key nvarchar(100),
            lab_examination_export_way varchar(100),
            lab_examination_export_type nvarchar(50),
            assit_examination_export_way varchar(100),
            assit_examination_export_type nvarchar(50),
            physical_sign_export_way varchar(100)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'module_id', '导出模块ID')
        Sqlserver_PO.setFieldComment(varTable, 'model_id', '模板ID')
        Sqlserver_PO.setFieldComment(varTable, 'module_tier', '模块层级')
        Sqlserver_PO.setFieldComment(varTable, 'module_fa_key', '父级模块标识')
        Sqlserver_PO.setFieldComment(varTable, 'module_key', '模块标识')
        Sqlserver_PO.setFieldComment(varTable, 'lab_examination_export_way', '实验室检查明细导出方式')
        Sqlserver_PO.setFieldComment(varTable, 'lab_examination_export_type', '实验室检查明细导出类型')
        Sqlserver_PO.setFieldComment(varTable, 'assit_examination_export_way', '辅助检查明细导出方式')
        Sqlserver_PO.setFieldComment(varTable, 'assit_examination_export_type', '辅助检查明细导出类型')
        Sqlserver_PO.setFieldComment(varTable, 'physical_sign_export_way', '体征检查导出方式')

    def crt_patient_export_field(self, varCommon):

        # 导出数据表

        varTable = 'patient_export_field'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            field_id int IDENTITY(1,1) PRIMARY KEY,
            model_id int,
            module_id int,
            module_key varchar(100),
            field_type nvarchar(100),
            cn_name nvarchar(100),
            en_name varchar(100),
            field_sort nvarchar(50)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'field_id', '导出字段ID')
        Sqlserver_PO.setFieldComment(varTable, 'model_id', '导出模板ID')
        Sqlserver_PO.setFieldComment(varTable, 'module_id', '导出模块ID')
        Sqlserver_PO.setFieldComment(varTable, 'module_key', '模块标识')
        Sqlserver_PO.setFieldComment(varTable, 'field_type', '导出字段类型')
        Sqlserver_PO.setFieldComment(varTable, 'cn_name', '导出字段中文名')
        Sqlserver_PO.setFieldComment(varTable, 'en_name', '导出字段英文名')
        Sqlserver_PO.setFieldComment(varTable, 'field_sort', '导出字段排序')

    def crt_sys_category_mapping(self, varCommon):

        # 字段模块表

        varTable = 'sys_category_mapping'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            id int IDENTITY(1,1) PRIMARY KEY,
            category_class nvarchar(100),
            category_name nvarchar(20),
            category_tier int,
            category_sort int,
            category_status varchar(100),
            category_fa_key varchar(100),
            category_key nvarchar(100)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'id', '当前层模块ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_class', '所属业务类别')
        Sqlserver_PO.setFieldComment(varTable, 'category_name', '模块名称')
        Sqlserver_PO.setFieldComment(varTable, 'category_tier', '模块层级')
        Sqlserver_PO.setFieldComment(varTable, 'category_sort', '模块排序')
        Sqlserver_PO.setFieldComment(varTable, 'category_status', '模块状态')
        Sqlserver_PO.setFieldComment(varTable, 'category_fa_key', '父级模块标识')
        Sqlserver_PO.setFieldComment(varTable, 'category_key', '模块标识')

    def crt_sys_category(self, varCommon):

        # 字段表

        varTable = 'sys_category'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            ID int IDENTITY(1,1) PRIMARY KEY,
            category_class nvarchar(100),
            category_name nvarchar(20),
            category_key nvarchar(100),
            field_sort int,
            field_status varchar(100),
            field_cn_name nvarchar(20),
            field_en_name nvarchar(100)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'ID', '字段ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_class', '所属业务类别')
        Sqlserver_PO.setFieldComment(varTable, 'category_name', '模块名称')
        Sqlserver_PO.setFieldComment(varTable, 'category_key', '模块标识')
        Sqlserver_PO.setFieldComment(varTable, 'field_sort', '字段排序')
        Sqlserver_PO.setFieldComment(varTable, 'field_status', '字段状态')
        Sqlserver_PO.setFieldComment(varTable, 'field_cn_name', '字段中文名')
        Sqlserver_PO.setFieldComment(varTable, 'field_en_name', '字段英文名')

    def crt_patient_extend_field(self, varCommon):

        # 扩展字段表

        varTable = 'patient_extend_field'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            extend_field_record_id int IDENTITY(1,1) PRIMARY KEY,
            category_source_id int,
            category_key nvarchar(100),
            category_id int,
            extend_field_id int,
            extend_field_key nvarchar(100),
            extend_field_text nvarchar(max),
            create_id int,
            create_by nvarchar(20),
            create_time DATETIME
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'extend_field_record_id', '扩展字段记录ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_source_id', '所属业务源数据ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_key', '所属业务标识')
        Sqlserver_PO.setFieldComment(varTable, 'category_id', '所属业务数据记录ID')
        Sqlserver_PO.setFieldComment(varTable, 'extend_field_id', '扩展字段管理ID')
        Sqlserver_PO.setFieldComment(varTable, 'extend_field_key', '字段标识')
        Sqlserver_PO.setFieldComment(varTable, 'extend_field_text', '字段值')
        Sqlserver_PO.setFieldComment(varTable, 'create_id', '创建人ID')
        Sqlserver_PO.setFieldComment(varTable, 'create_by', '创建人')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间')


    def crt_sys_tag_type(self, varCommon):

        # 标签

        varTable = 'sys_tag_type'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            tag_id int IDENTITY(1,1) PRIMARY KEY,
            category_class nvarchar(100),
            category_name nvarchar(20),
            category_key nvarchar(100),
            tag_name nvarchar(20),
            tag_key nvarchar(100),
            tag_sort int,
            status varchar(100),
            create_id int,
            create_time DATETIME,
            update_id int,
            update_time DATETIME,
            remark nvarchar(500)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'tag_id', '标签ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_class', '所属业务类别')
        Sqlserver_PO.setFieldComment(varTable, 'category_name', '所属业务名称')
        Sqlserver_PO.setFieldComment(varTable, 'category_key', '所属业务标识')
        Sqlserver_PO.setFieldComment(varTable, 'tag_name', '标签名称')
        Sqlserver_PO.setFieldComment(varTable, 'tag_key', '标签标识')
        Sqlserver_PO.setFieldComment(varTable, 'tag_sort', '标签排序')
        Sqlserver_PO.setFieldComment(varTable, 'status', '标签状态')
        Sqlserver_PO.setFieldComment(varTable, 'create_id', '创建人ID')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间')
        Sqlserver_PO.setFieldComment(varTable, 'update_id', '更新人ID')
        Sqlserver_PO.setFieldComment(varTable, 'update_time', '更新时间')
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')

    def crt_sys_tag_data(self, varCommon):

        # 标签数据表

        varTable = 'sys_tag_data'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            tag_data_id int IDENTITY(1,1) PRIMARY KEY,
            tag_id int,
            tag_data_name nvarchar(20),
            tag_data_key nvarchar(100),
            tag_data_sort int,
            status varchar(100)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'tag_data_id', '标签数据ID')
        Sqlserver_PO.setFieldComment(varTable, 'tag_id', '标签ID')
        Sqlserver_PO.setFieldComment(varTable, 'tag_data_name', '标签数据名')
        Sqlserver_PO.setFieldComment(varTable, 'tag_data_key', '标签数据标识')
        Sqlserver_PO.setFieldComment(varTable, 'tag_data_sort', '标签数据排序')
        Sqlserver_PO.setFieldComment(varTable, 'status', '标签数据状态')

    def crt_sys_tag_authority(self, varCommon):

        # 标签权限表

        varTable = 'sys_tag_authority'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            tag_authority_id int IDENTITY(1,1) PRIMARY KEY,
            tag_id int,
            authority_relative_module nvarchar(20),
            authority_relative_id int
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'tag_authority_id', '标签权限ID')
        Sqlserver_PO.setFieldComment(varTable, 'tag_id', '标签ID')
        Sqlserver_PO.setFieldComment(varTable, 'authority_relative_module', '权限关联模块')
        Sqlserver_PO.setFieldComment(varTable, 'authority_relative_id', '权限关联ID')

    def crt_sys_extend_field_manage(self, varCommon):

        # 扩展字段管理

        varTable = 'sys_extend_field_manage'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            extend_field_id int IDENTITY(1,1) PRIMARY KEY,
            category_class nvarchar(100),
            category_name nvarchar(20),
            category_key nvarchar(100),
            extend_field_name nvarchar(20),
            extend_field_key nvarchar(100),
            sort int,
            status varchar(100),
            create_id int,
            create_time DATETIME,
            update_id int,
            update_time DATETIME,
            remark nvarchar(500)
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'extend_field_id', '扩展字段管理ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_class', '所属业务类别')
        Sqlserver_PO.setFieldComment(varTable, 'category_name', '所属业务名称')
        Sqlserver_PO.setFieldComment(varTable, 'category_key', '所属业务标识')
        Sqlserver_PO.setFieldComment(varTable, 'extend_field_name', '字段名')
        Sqlserver_PO.setFieldComment(varTable, 'extend_field_key', '字段标识')
        Sqlserver_PO.setFieldComment(varTable, 'sort', '字段排序')
        Sqlserver_PO.setFieldComment(varTable, 'status', '字段状态')
        Sqlserver_PO.setFieldComment(varTable, 'create_id', '创建人ID')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '创建时间')
        Sqlserver_PO.setFieldComment(varTable, 'update_id', '更新人ID')
        Sqlserver_PO.setFieldComment(varTable, 'update_time', '更新时间')
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')

    def crt_sys_extend_field_authority(self, varCommon):

        # 扩展字段权限表

        varTable = 'sys_extend_field_authority'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            extend_field_authority_id int IDENTITY(1,1) PRIMARY KEY,
            extend_field_id int,
            authority_relative_module nvarchar(20),
            authority_relative_id int
        ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'extend_field_authority_id', '扩展字段权限ID')
        Sqlserver_PO.setFieldComment(varTable, 'extend_field_id', '扩展字段管理ID')
        Sqlserver_PO.setFieldComment(varTable, 'authority_relative_module', '权限关联模块')
        Sqlserver_PO.setFieldComment(varTable, 'authority_relative_id', '权限关联ID')

    def crt_sys_task(self, varCommon):

        # 待办任务表

        varTable = 'sys_task'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            task_id int IDENTITY(1,1) PRIMARY KEY,
            category_class nvarchar(100),
            category_name nvarchar(20),
            task_type nvarchar(20),
            task_describe nvarchar(500),
            remark nvarchar(500),
            owner_id int,
            status varchar(100),
            complete_time DATETIME,
            create_time DATETIME,
            link_url varchar(2000)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'task_id', '任务ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_class', '所属业务类别')
        Sqlserver_PO.setFieldComment(varTable, 'category_name', '所属业务名称')
        Sqlserver_PO.setFieldComment(varTable, 'task_type', '任务类型')
        Sqlserver_PO.setFieldComment(varTable, 'task_describe', '任务描述')
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')
        Sqlserver_PO.setFieldComment(varTable, 'owner_id', '当前所有人ID')
        Sqlserver_PO.setFieldComment(varTable, 'status', '任务状态')
        Sqlserver_PO.setFieldComment(varTable, 'complete_time', '任务完成时间')
        Sqlserver_PO.setFieldComment(varTable, 'create_time', '任务创建时间')
        Sqlserver_PO.setFieldComment(varTable, 'link_url', '任务跳转链接')

    def crt_sys_file_download(self, varCommon):

        # 文件下载管理

        varTable = 'sys_file_download'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            file_id int IDENTITY(1,1) PRIMARY KEY,
            model_id int,
            category_class nvarchar(100),
            category_name nvarchar(100),
            file_name nvarchar(100),
            export_params nvarchar(max),
            export_type varchar(255),
            applier_id int,
            apply_time DATETIME,
            deal_status varchar(100),
            file_status varchar(100),
            remark nvarchar(100)
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'file_id', '文件下载ID')
        Sqlserver_PO.setFieldComment(varTable, 'model_id', '模板ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_class', '所属业务类别')
        Sqlserver_PO.setFieldComment(varTable, 'category_name', '所属业务名称')
        Sqlserver_PO.setFieldComment(varTable, 'file_name', '文件名称')
        Sqlserver_PO.setFieldComment(varTable, 'export_params', '导出参数')
        Sqlserver_PO.setFieldComment(varTable, 'export_type', '导出类型')
        Sqlserver_PO.setFieldComment(varTable, 'applier_id', '申请人ID')
        Sqlserver_PO.setFieldComment(varTable, 'apply_time', '申请时间')
        Sqlserver_PO.setFieldComment(varTable, 'deal_status', '文件处理状态')
        Sqlserver_PO.setFieldComment(varTable, 'file_status', '文件失效状态')
        Sqlserver_PO.setFieldComment(varTable, 'remark', '备注')

    def crt_sys_file_download_record(self, varCommon):

        # 文件下载记录

        varTable = 'sys_file_download_record'
        Sqlserver_PO.crtTableByCover(varTable,
            '''
            file_down_id int IDENTITY(1,1) PRIMARY KEY,
            file_id int,
            category_name nvarchar(100),
            file_name nvarchar(100),
            applier_id int,
            apply_time DATETIME,
            downloader_id int,
            download_time DATETIME
            ''')
        Sqlserver_PO.setTableComment(varTable, varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment(varTable, 'file_down_id', '文件下载ID')
        Sqlserver_PO.setFieldComment(varTable, 'file_id', '文件ID')
        Sqlserver_PO.setFieldComment(varTable, 'category_name', '所属业务名称')
        Sqlserver_PO.setFieldComment(varTable, 'file_name', '文件名称')
        Sqlserver_PO.setFieldComment(varTable, 'applier_id', '申请人ID')
        Sqlserver_PO.setFieldComment(varTable, 'apply_time', '申请时间')
        Sqlserver_PO.setFieldComment(varTable, 'downloader_id', '下载人ID')
        Sqlserver_PO.setFieldComment(varTable, 'download_time', '下载时间')


    def insert_cdrdPatientTag(self):

        # 插入数据（标签表 patient_tag）

        # 删除存储过程（用于）
        # Sqlserver_PO.execute(f"DROP PROCEDURE IF EXISTS dbo.{varProcedure};")

        Sqlserver_PO.execute(
            f"""DECLARE @tag_record_id1 BIGINT, @tag_record_id2 BIGINT, @tag_record_id3 BIGINT, @tag_record_id4 BIGINT;
            EXEC GenerateSnowflakeID @machineId = 1, @dataCenterId = 0, @snowflakeId = @tag_record_id1 OUTPUT;
            EXEC GenerateSnowflakeID @machineId = 1, @dataCenterId = 0, @snowflakeId = @tag_record_id2 OUTPUT;
            EXEC GenerateSnowflakeID @machineId = 1, @dataCenterId = 0, @snowflakeId = @tag_record_id3 OUTPUT;
            EXEC GenerateSnowflakeID @machineId = 1, @dataCenterId = 0, @snowflakeId = @tag_record_id4 OUTPUT;
            INSERT INTO patient_tag (tag_record_id,category_source_id,category_key,category_id,tag_id,tag_key,tag_data_id,tag_data_key,create_id,create_by,create_time)
            VALUES (@tag_record_id1, '1', 'cdrd_patient_info', '123', 1, 'patient_deal_way', 1, 'hormone', '3', '张三', GETUTCDATE())
            ,(@tag_record_id2, '1', 'cdrd_patient_info', '123', 1, 'patient_deal_way', 2, 'infliximab', '4', '李四', GETUTCDATE())
            ,(@tag_record_id3, '1', 'cdrd_patient_info', '123', 2, 'progression_of_disease', 3, 'paracmasis', '5', '王五', GETUTCDATE())
            ,(@tag_record_id4, '1', 'cdrd_patient_info', '123', 2, 'progression_of_disease', 4, 'active_stage', '6', '赵六', GETUTCDATE());""")

    def generate_patient_tag_procedure_with_snowflake(self):
        '''创建使用雪花ID的生成标签记录的存储过程'''
        try:
            # 删除已存在的存储过程
            Sqlserver_PO.execute(
                "IF OBJECT_ID('GeneratePatientTagRecords', 'P') IS NOT NULL DROP PROCEDURE GeneratePatientTagRecords")

            # 创建存储过程
            procedure_sql = """
            CREATE PROCEDURE GeneratePatientTagRecords
            AS
            BEGIN
                SET NOCOUNT ON;

                -- 创建临时表存储患者基本信息标签
                CREATE TABLE #PatientTags (
                    id INT IDENTITY(1,1),
                    patient_id INT,
                    tag_id INT,
                    tag_key VARCHAR(100),
                    tag_data_id INT,
                    tag_data_key VARCHAR(100)
                );

                -- 创建临时表存储就诊信息标签
                CREATE TABLE #VisitTags (
                    id INT IDENTITY(1,1),
                    patient_visit_id INT,
                    tag_id INT,
                    tag_key VARCHAR(100),
                    tag_data_id INT,
                    tag_data_key VARCHAR(100)
                );

                -- 插入患者基本信息标签数据
                INSERT INTO #PatientTags (patient_id, tag_id, tag_key, tag_data_id, tag_data_key)
                SELECT 
                    p.patient_id,
                    st.tag_id,
                    st.tag_key,
                    sd.tag_data_id,
                    sd.tag_data_key
                FROM (
                    SELECT TOP 30000 patient_id 
                    FROM cdrd_patient_info 
                    ORDER BY patient_id
                ) p
                CROSS JOIN sys_tag_type st
                INNER JOIN sys_tag_data sd ON st.tag_id = sd.tag_id
                WHERE st.category_key = 'cdrd_patient_info';

                -- 插入就诊信息标签数据
                INSERT INTO #VisitTags (patient_visit_id, tag_id, tag_key, tag_data_id, tag_data_key)
                SELECT 
                    v.patient_visit_id,
                    st.tag_id,
                    st.tag_key,
                    sd.tag_data_id,
                    sd.tag_data_key
                FROM (
                    SELECT TOP 150000 patient_visit_id 
                    FROM cdrd_patient_visit_info 
                    ORDER BY patient_visit_id
                ) v
                CROSS JOIN sys_tag_type st
                INNER JOIN sys_tag_data sd ON st.tag_id = sd.tag_id
                WHERE st.category_key = 'cdrd_patient_visit_info';

                -- 为患者基本信息标签生成雪花ID并插入
                DECLARE @counter INT = 1;
                DECLARE @total INT = (SELECT COUNT(*) FROM #PatientTags);
                DECLARE @tag_record_id BIGINT;
                DECLARE @patient_id INT;
                DECLARE @tag_id INT;
                DECLARE @tag_key VARCHAR(100);
                DECLARE @tag_data_id INT;
                DECLARE @tag_data_key VARCHAR(100);

                WHILE @counter <= @total AND @counter <= 120000
                BEGIN
                    SELECT 
                        @patient_id = patient_id,
                        @tag_id = tag_id,
                        @tag_key = tag_key,
                        @tag_data_id = tag_data_id,
                        @tag_data_key = tag_data_key
                    FROM #PatientTags
                    WHERE id = @counter;

                    -- 生成雪花ID（这里使用简单的方法，实际应调用雪花ID生成器）
                    SET @tag_record_id = @counter + ISNULL((SELECT MAX(tag_record_id) FROM patient_tag), 0);

                    INSERT INTO patient_tag (
                        tag_record_id,
                        category_key,
                        category_source_id,
                        tag_id,
                        tag_key,
                        tag_data_id,
                        tag_data_key,
                        create_time
                    )
                    VALUES (
                        @tag_record_id,
                        'cdrd_patient_info',
                        @patient_id,
                        @tag_id,
                        @tag_key,
                        @tag_data_id,
                        @tag_data_key,
                        GETDATE()
                    );

                    SET @counter = @counter + 1;
                END;

                -- 为就诊信息标签生成雪花ID并插入
                SET @counter = 1;
                SET @total = (SELECT COUNT(*) FROM #VisitTags);

                WHILE @counter <= @total AND @counter <= 300000
                BEGIN
                    SELECT 
                        @patient_id = patient_visit_id,
                        @tag_id = tag_id,
                        @tag_key = tag_key,
                        @tag_data_id = tag_data_id,
                        @tag_data_key = tag_data_key
                    FROM #VisitTags
                    WHERE id = @counter;

                    -- 生成雪花ID（这里使用简单的方法，实际应调用雪花ID生成器）
                    SET @tag_record_id = @counter + ISNULL((SELECT MAX(tag_record_id) FROM patient_tag), 120000);

                    INSERT INTO patient_tag (
                        tag_record_id,
                        category_key,
                        category_source_id,
                        tag_id,
                        tag_key,
                        tag_data_id,
                        tag_data_key,
                        create_time
                    )
                    VALUES (
                        @tag_record_id,
                        'cdrd_patient_visit_info',
                        @patient_id,
                        @tag_id,
                        @tag_key,
                        @tag_data_id,
                        @tag_data_key,
                        GETDATE()
                    );

                    SET @counter = @counter + 1;
                END;

                -- 清理临时表
                DROP TABLE #PatientTags;
                DROP TABLE #VisitTags;

                PRINT '标签记录生成完成';
                DECLARE @patient_count INT;
                DECLARE @visit_count INT;
                DECLARE @total_count INT;

                SELECT @patient_count = COUNT(*) FROM patient_tag WHERE category_key = 'cdrd_patient_info';
                SELECT @visit_count = COUNT(*) FROM patient_tag WHERE category_key = 'cdrd_patient_visit_info';
                SELECT @total_count = COUNT(*) FROM patient_tag;

                PRINT '患者基本信息标签记录数: ' + CAST(@patient_count AS VARCHAR(10));
                PRINT '就诊信息标签记录数: ' + CAST(@visit_count AS VARCHAR(10));
                PRINT '总标签记录数: ' + CAST(@total_count AS VARCHAR(10));
            END
            """

            Sqlserver_PO.execute(procedure_sql)
            print("生成标签记录的存储过程创建成功")

        except Exception as e:
            print(f"创建存储过程时出错: {e}")

    def generate_patient_tag_procedure(self):
        '''创建生成标签记录的存储过程'''
        try:
            # 删除已存在的存储过程
            Sqlserver_PO.execute(
                "IF OBJECT_ID('GeneratePatientTagRecords', 'P') IS NOT NULL DROP PROCEDURE GeneratePatientTagRecords")

            # 创建存储过程
            procedure_sql = """
            CREATE PROCEDURE GeneratePatientTagRecords
            AS
            BEGIN
                SET NOCOUNT ON;

                BEGIN TRY
                    BEGIN TRANSACTION;

                    -- 获取当前最大tag_record_id用于生成新的ID
                    DECLARE @max_tag_record_id BIGINT;
                    SELECT @max_tag_record_id = ISNULL(MAX(tag_record_id), 0) FROM patient_tag;

                    -- 创建临时表存储患者基本信息
                    CREATE TABLE #PatientInfo (
                        patient_id INT
                    );

                    -- 插入患者基本信息（限制5条）
                    INSERT INTO #PatientInfo (patient_id)
                    SELECT TOP 5 patient_id 
                    FROM cdrd_patient_info 
                    ORDER BY patient_id;

                    -- 创建临时表存储就诊信息
                    CREATE TABLE #VisitInfo (
                        patient_visit_id INT
                    );

                    -- 插入就诊信息（限制25条）
                    INSERT INTO #VisitInfo (patient_visit_id)
                    SELECT TOP 25 patient_visit_id 
                    FROM cdrd_patient_visit_info 
                    ORDER BY patient_visit_id;

                    -- 为cdrd_patient_info表中的每个患者生成4条标签记录
                    INSERT INTO patient_tag (
                        tag_record_id,
                        category_key,
                        category_source_id,
                        tag_id,
                        tag_key,
                        tag_data_id,
                        tag_data_key,
                        create_time
                    )
                    SELECT 
                        ROW_NUMBER() OVER (ORDER BY p.patient_id, st.tag_id, sd.tag_data_id) + @max_tag_record_id,
                        'cdrd_patient_info',
                        p.patient_id,
                        st.tag_id,
                        st.tag_key,
                        sd.tag_data_id,
                        sd.tag_data_key,
                        GETDATE()
                    FROM #PatientInfo p
                    CROSS JOIN sys_tag_type st
                    INNER JOIN sys_tag_data sd ON st.tag_id = sd.tag_id
                    WHERE st.category_key = 'cdrd_patient_info';

                    -- 更新最大tag_record_id
                    SELECT @max_tag_record_id = @max_tag_record_id + 20;

                    -- 为cdrd_patient_visit_info表中的每条就诊记录生成2条标签记录
                    INSERT INTO patient_tag (
                        tag_record_id,
                        category_key,
                        category_source_id,
                        tag_id,
                        tag_key,
                        tag_data_id,
                        tag_data_key,
                        create_time
                    )
                    SELECT 
                        ROW_NUMBER() OVER (ORDER BY v.patient_visit_id, st.tag_id, sd.tag_data_id) + @max_tag_record_id,
                        'cdrd_patient_visit_info',
                        v.patient_visit_id,
                        st.tag_id,
                        st.tag_key,
                        sd.tag_data_id,
                        sd.tag_data_key,
                        GETDATE()
                    FROM #VisitInfo v
                    CROSS JOIN sys_tag_type st
                    INNER JOIN sys_tag_data sd ON st.tag_id = sd.tag_id
                    WHERE st.category_key = 'cdrd_patient_visit_info';

                    -- 清理临时表
                    DROP TABLE #PatientInfo;
                    DROP TABLE #VisitInfo;

                    COMMIT TRANSACTION;

                    PRINT '标签记录生成完成';
                END TRY
                BEGIN CATCH
                    IF @@TRANCOUNT > 0
                        ROLLBACK TRANSACTION;

                    DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
                    PRINT '生成标签记录时发生错误: ' + @ErrorMessage;
                    RAISERROR(@ErrorMessage, 16, 1);
                END CATCH
            END
            """

            Sqlserver_PO.execute(procedure_sql)
            print("生成标签记录的存储过程创建成功")

        except Exception as e:
            print(f"创建存储过程时出错: {e}")

    def execute_generate_patient_tag(self):
        '''执行生成标签记录的存储过程'''
        try:
            Sqlserver_PO.execCall("GeneratePatientTagRecords")
            print("标签记录生成成功")

            # 显示生成的记录数
            patient_count = Sqlserver_PO.select(
                "SELECT COUNT(*) as cnt FROM patient_tag WHERE category_key = 'cdrd_patient_info'")[0]['cnt']
            visit_count = Sqlserver_PO.select(
                "SELECT COUNT(*) as cnt FROM patient_tag WHERE category_key = 'cdrd_patient_visit_info'")[0]['cnt']
            total_count = Sqlserver_PO.select("SELECT COUNT(*) as cnt FROM patient_tag")[0]['cnt']

            print(f"患者基本信息标签记录数: {patient_count}")
            print(f"就诊信息标签记录数: {visit_count}")
            print(f"总标签记录数: {total_count}")

        except Exception as e:
            print(f"执行生成标签记录时出错: {e}")


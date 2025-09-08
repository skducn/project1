# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-3-27
# Description   : setData 创建表、存储过程、插入数据
# 性能需求：https://docs.qq.com/doc/DYnZXTVZ1THpPVEVC?g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3#g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3
# gitlab http://192.168.0.241/cdrd_product_doc/product_doc
# 使用豆包，快速格式化一下内容：
# 如：密码最后更新时间	pwd_update_time
# 密码下次更新时间	pwd_next_update_time，请将以上数据中字段与字段英文名互换位置，并用逗号分隔输出
# 请优化，在每一行前加上Sqlserver_PO.setFieldComment('a_sys_user',

# 💡 注意事项
# 主键索引：如果字段已经是主键，则自动拥有聚集索引，无需重复创建。
# 索引维护成本：索引会提升查询性能，但会影响插入/更新性能，建议在数据导入完成后创建。
# 统计信息更新：创建索引后建议更新统计信息：
# UPDATE STATISTICS a_cdrd_patient_info;
# UPDATE STATISTICS a_sys_department;
# UPDATE STATISTICS ab_hospital;
# UPDATE STATISTICS a_sys_dept_medgp;
# UPDATE STATISTICS a_sys_dept_medgp_person;

# 【腾讯文档】专病库性能说明书
# https://docs.qq.com/doc/DYnZXTVZ1THpPVEVC

# gitlab需求：http://192.168.0.241/cdrd_product_doc/product_doc/-/tree/dev
# *********************************************************************

from CdrdPO import *
Cdrd_PO = CdrdPO()

# 子存储过程
# Cdrd_PO.subProcedure("p_abo_type", "Abo血型, {'1': 'A 型', '2': 'B 型', '3': 'O 型', '4': 'AB 型', '5': '不详', '6': '未查'}")
# Cdrd_PO.subProcedure("p_assit_examination_type", "辅助检查类型, {'1': '电生理检查', '2': '放射学检查', '3': '超声检查', '4': '内镜检查', '5': '其他检查', '6': '病理检查'}")
# Cdrd_PO.subProcedure("p_cert_type", "证件类型, {'1': '居民身份证', '2': '居民户口簿', '3': '护照', '4': '军官证', '5': '驾驶证', '6': '港澳居民来往内地通行证', '7': '台湾居民来往内地通行证', '9': '其他法定有效证件'}")
# Cdrd_PO.subProcedure("p_drug_allergy_type", "药物过敏,  {'1': '否', '2': '有'}")
# Cdrd_PO.subProcedure("p_hospital", "医院, ['东方医院','复旦大学附属眼耳鼻喉科医院','上海交通大学医学院附属第九人民医院','上海市第一人民医院','上海交通大学医学院附属新华医院']")
# Cdrd_PO.subProcedure("p_hospital_advice", "住院医嘱类型, {'1': '住院药物医嘱', '2': '住院非药物医嘱'}")
# Cdrd_PO.subProcedure("p_in_state", "入院病情, {'1': '有', '2': '临床未确定', '3': '情况不明', '4': '无'}")
# Cdrd_PO.subProcedure("p_is_cache", "是否缓存, {'0': '缓存', '1': '不缓存'}")
# Cdrd_PO.subProcedure("p_job", "职业, ['军人', '医生', '自由职业者', '技术人员', '工程师', '学生', '老师', '服务人员']")
# Cdrd_PO.subProcedure("p_marriage", "婚姻, {'1': '未婚', '2': '已婚', '3': '丧偶', '4': '离婚', '9': '其他'}")
# Cdrd_PO.subProcedure("p_medical_payment_type", "付费方式, {'1': '城镇职工基本医疗保险', '2': '城镇居民基本医疗保险', '3': '新型农村合作医疗', '4': '贫困救助', '5': '商业医疗保险', '6': '全公费', '7': '全自费', '8': ' 其他社会保险 (指生育保险、工伤保险、农民工保险等)', '9': '其他'}")
# Cdrd_PO.subProcedure("p_nationality", "民族, {'01': ' 汉族 ', '02': ' 蒙古族 ', '03': ' 回族 ', '04': ' 藏族 ', '05': ' 维吾尔族 ', '06': ' 苗族 ', '07': ' 彝族 ', '08': ' 壮族 ', '09': ' 布依族 ', '10': ' 朝鲜族 '}")
# Cdrd_PO.subProcedure("p_operation_incision_healing_grade", "切口愈合登记, {'1': '0 类切口', '2': 'Ⅰ 类切口', '3': 'Ⅱ 类切口', '4': 'Ⅲ 类切口'}")
# Cdrd_PO.subProcedure("p_operation_level", "手术级别, {'1': '一级手术', '2': '二级手术', '3': '三级手术', '4': '四级手术'}")
# Cdrd_PO.subProcedure("p_operation_type", "手术类型, {'1': '择期手术', '2': '急诊手术', '3': '限期手术'}")
# Cdrd_PO.subProcedure("p_out_hospital_type", "出院记录类型, {'1': '出院记录', '2': '24小时内入出院记录'}")
# Cdrd_PO.subProcedure("p_out_hospital_way", "离院方式, {'1': '医嘱离院', '2': '医嘱转院', '3': '医嘱转社区卫生服务机构/乡镇卫生院', '4': '非医嘱离院', '5': '死亡', '9': '其他'}")
# Cdrd_PO.subProcedure("p_outcome_state", "出院情况 ,{'1': ' 治愈 ', '2': ' 好转 ', '3': ' 未愈 ', '4': ' 死亡 ', '5': ' 其他 '}")
# Cdrd_PO.subProcedure("p_patient_relation", "与患者管理, [' 本人 ', ' 父亲 ', ' 母亲 ', ' 配偶 ', ' 子女 ', ' 兄弟姐妹 ', ' 父母 ', ' 祖父母 ', ' 外祖父母 ', ' 子女（多人）', ' 亲戚 ', ' 朋友 ', ' 同事 ', ' 监护人 ', ' 代理人 ', ' 其他 ']")
# Cdrd_PO.subProcedure("p_physical_sign", "体征, {'1': '体温', '2': '脉搏', '3': '心率', '4': '呼吸', '5': '收缩压', '6': '舒张压', '7': '指尖血氧饱和度', '8': '其他'}")
# Cdrd_PO.subProcedure("p_physical_sign_unit", "体征单位, {'1': '℃', '2': '次/分', '3': 'mmHg', '4': '%', '5': '其他'}")
# Cdrd_PO.subProcedure("p_pwd_update_state", "密码重置状态, {'0': '已创建账号，但尚未登录', '1': '已完成首次登录，且完成密码重置及密保问题记录'}")
# Cdrd_PO.subProcedure("p_rh_type", "Rh血型, {'1': '阴性', '2': '阳性', '3': '不详', '4': '未查'}")
# Cdrd_PO.subProcedure("p_sex", "性别, {'0': '男', '1': '女', '2': '不详'}")
# Cdrd_PO.subProcedure("p_status", "状态, {'0': '正常', '1': '停用'}")
# Cdrd_PO.subProcedure("p_trueFalse", "是否, {'0': '是', '1': '否'}")
# Cdrd_PO.subProcedure("p_visible", "是否显示, {'0': '显示', '1': '隐藏'}")
# Cdrd_PO.subProcedure("p_visit_type", "就诊类型, {'1': '门诊', '2': '住院'}")
# Cdrd_PO.subProcedure("p_visit_way", "入院途径, {'1': '本院急诊诊疗后入院', '2': '本院门诊诊疗后入院', '3': '其他医疗机构诊治后转诊入院', '9': '其他途径入院'}")

# Cdrd_PO.subFunction("fn_name")


# todo ab表
# Cdrd_PO._ab_marriage('婚姻')
# Cdrd_PO._ab_IDtype('证件类型')
# Cdrd_PO._ab_ethnicGroup('民族')
# Cdrd_PO._ab_job('职业')
# Cdrd_PO._ab_relationship('与患者关系')
# Cdrd_PO.subProcedure("p_name", "姓名")
# Cdrd_PO.subProcedure("p_birth_place", "出生地-省市县")
# Cdrd_PO.subProcedure("p_address", "住址")
# Cdrd_PO.subProcedure("p_idcard", "身份证")
# Cdrd_PO._ab_admissionCondition('入院病情')
# Cdrd_PO._ab_boolean('布尔值_主要诊断')
# Cdrd_PO._ab_diagnosticHistory('诊断病史')
# Cdrd_PO._ab_dischargeStatus('出院情况')
# Cdrd_PO.index('IX_ab_hospital_name', 'ab_hospital', 'name')
# Cdrd_PO.updateStatistics('ab_hospital')
# Cdrd_PO._ab_visitType('就诊类型')
# Cdrd_PO._ab_paymentMethod('付费方式')
# Cdrd_PO._ab_dischargeMethod('出院方式')
# Cdrd_PO._ab_admissionRoute('入院途径')
# Cdrd_PO._ab_drugAllergy('药物过敏')
# Cdrd_PO._ab_ABO_bloodType('ABO血型')
# Cdrd_PO._ab_rh_bloodType('ABO血型')
# Cdrd_PO._ab_visitDiagnosis('就诊诊断')
# Cdrd_PO._ab_symptom('症状信息')
# Cdrd_PO._ab_lab('实验室检查报告')
# Cdrd_PO._ab_physicalSign('体征')
# Cdrd_PO._ab_physicalSignUnit('体征单位')
# Cdrd_PO._ab_dischargeHospital('出院记录')
# Cdrd_PO._ab_operationLevel('手术级别')
# Cdrd_PO._ab_operationType('手术类型')
# Cdrd_PO._ab_operationIncisionHealingGrade('切口愈合等级')
# Cdrd_PO._ab_loginout('登录登出')
# Cdrd_PO._ab_lab_project('实验室检查+项目明细')
# Cdrd_PO._ab_drug('用药信息')
# Cdrd_PO._ab_dischargeRecordType('出院记录类型')
# Cdrd_PO._ab_hospital('医院')




# todo 1.1 患者基本信息
# 数据量：30000
# # 需求：https://docs.qq.com/doc/DYnZXTVZ1THpPVEVC?g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3#g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3
# Cdrd_PO.crt_cdrdPatientInfoBinary('患者基本信息')
# # 生成30000条
# result = subprocess.run(
#     ["python", "genAES128.py"],  # 命令和参数列表
#     capture_output=True,  # 捕获 stdout 和 stderr
#     text=True  # 输出转为字符串（默认是字节）
# )


# Cdrd_PO.crt_cdrdPatientInfo('患者基本信息')
# Cdrd_PO.procedure("s_cdrd_patient_info", '患者基本信息')  # 存储过程中改成 30000  (弃用)
# Cdrd_PO.index('IX_a_cdrd_patient_info_patient_id', 'a_cdrd_patient_info', 'patient_id')
# Cdrd_PO.updateStatistics('a_cdrd_patient_info')
# Cdrd_PO.openSql("s_cdrd_patient_info.sql")



# todo 1.2 门(急)诊住院就诊信息
# 数据量：每个患者5条（3条门诊，2条住院），共15万
# Cdrd_PO.crt_cdrdPatientVisitInfo('门(急)诊住院就诊信息')
# Cdrd_PO.procedure("s_cdrd_patient_visit_info", '门(急)诊住院就诊信息')
# Cdrd_PO.procedure("s_cdrd_patient_visit_info_5", '门(急)诊住院就诊信息')
# Cdrd_PO.subProcedure("r_visit_info__", "门(急)诊住院就诊信息 - 就诊诊断")
# Cdrd_PO.openSql("s_cdrd_patient_visit_info.sql")


# todo 1.3 诊断表
# 数据量：每个患者5条 = 患者基本信息 * 5(2条患者基本信息，3条就诊记录表) , 共15万
# Cdrd_PO.crt_cdrdPatientDiagInfo('诊断表')
# Cdrd_PO.procedure("s_cdrd_patient_diag_info", '诊断表')
# Cdrd_PO.subProcedure("r_diag_info__", "诊断表 - 诊断类型，诊断名称，ICD10编码")
# ok

# Cdrd_PO.openSql("s_cdrd_patient_diag_info.sql")

#
# todo 1.4 症状信息
# # # 症状信息, 每个患者5条 = 患者基本信息 * 5(2条患者基本信息，3条就诊记录表) , 共15万
# Cdrd_PO.crt_cdrdPatientSymptomInfo('症状信息')
# Cdrd_PO.procedure("s_cdrd_patient_symptom_info", '症状信息')
# Cdrd_PO.subProcedure("r_symptom_info__", "症状信息 - 症状名称，症状编号，具体描述")
# ok

# Cdrd_PO.openSql("s_cdrd_patient_symptom_info.sql")

#
# todo 1.5 体征信息
# 数据量：每个患者5条 = 患者基本信息 * 5(2条患者基本信息，3条就诊记录表) , 共15万
# Cdrd_PO.crt_cdrdPatientPhysicalSignInfo('体征信息')
# Cdrd_PO.procedure("s_cdrd_patient_physical_sign_info", '体征信息')

#
# # #
# todo 1.6 实验室检查报告
# 数据量：每个患者5条 = 患者基本信息 * 5(2条患者基本信息，3条就诊记录表) , 共15万
# Cdrd_PO.crt_cdrdPatientLabExaminationInfo('实验室检查报告')
# Cdrd_PO.procedure("s_cdrd_patient_lab_examination_info", '实验室检查报告')
# Cdrd_PO.subProcedure("r_lab_examination_info__", "实验室检查报告 - 报告名称，样本类型，项目名称")
# Cdrd_PO.openSql("s_cdrd_patient_lab_examination_info.sql")

#
# # #
# todo 1.7 辅助检查报告
# 数据量：每个患者5条 = 患者基本信息 * 5(2条患者基本信息，3条就诊记录表) , 共15万
# Cdrd_PO.crt_cdrdPatientAssitExaminationInfo('辅助检查报告')
# Cdrd_PO.procedure("s_cdrd_patient_assit_examination_info", '辅助检查报告')
# Cdrd_PO.openSql("s_cdrd_patient_assit_examination_info.sql")

#
# # #
# todo 1.8 检查项目明细
# 数据量：每个实验室检查记录对应一份检查项目明细(每份明细预计20条左右数据，总量预计300万左右)  15W * 20 = 300W
# Cdrd_PO.crt_cdrdPatientTestProjectInfo('检查项目明细')
# Cdrd_PO.procedure("s_cdrd_patient_test_project_info", '检查项目明细')
# Cdrd_PO.openSql("s_cdrd_patient_test_project_info.sql")

# #
# # # #
# todo 1.9 门诊医嘱
# 数据量：每名患者3条（共9万）
# Cdrd_PO.crt_cdrdPatientClinicAdviceInfo('门诊医嘱')
# Cdrd_PO.procedure("s_cdrd_patient_clinic_advice_info", '门诊医嘱')
# Cdrd_PO.openSql("s_cdrd_patient_clinic_advice_info.sql")

#
# # #
# todo 1.10 住院医嘱
# 数据量：每名患者2条（共6万）
# Cdrd_PO.crt_cdrdPatientHospitalAdviceInfo('住院医嘱')
# Cdrd_PO.procedure("s_cdrd_patient_hospital_advice_info", '住院医嘱')
# Cdrd_PO.openSql("s_cdrd_patient_hospital_advice_info.sql")

# #
# # # #
# todo 1.11 用药信息 - 慢 耗时: 6432.8538 秒
# 数据量：每名患者8条（共24万），3条只有patientid，5条均有patientid、patient_visit_id
# Cdrd_PO.crt_cdrdPatientDrugInfo_test('用药信息test')
# Cdrd_PO.procedure("s_cdrd_patient_drug_info_test", '用药信息')

# Cdrd_PO.crt_cdrdPatientDrugInfo('用药信息')
# Cdrd_PO.procedure("s_cdrd_patient_drug_info", '用药信息')
# Cdrd_PO.subProcedure("r_drug_info__", "用药信息 - 药物名称	规格	频次	每次用量	用量单位	用法	总量")
# Cdrd_PO.openSql("s_cdrd_patient_drug_info.sql")

#
# # #
# todo 1.12 出院记录
# 数据量：每名患者2条（共6万）？？？
Cdrd_PO.crt_cdrdPatientOutHospitalInfo('出院记录') ？？？
Cdrd_PO.procedure("s_cdrd_patient_out_hospital_info", '出院记录')
# Cdrd_PO.openSql("s_cdrd_patient_out_hospital_info.sql")

# # #
# todo 1.13 手术记录
# 数据量：每个患者5条 = 患者基本信息 * 5(2条患者基本信息，3条就诊记录表) , 共15万
# Cdrd_PO.crt_cdrdPatientOperationInfo('手术记录')
# Cdrd_PO.procedure("s_cdrd_patient_operation_info", '手术记录')
# Cdrd_PO.openSql("s_cdrd_patient_operation_info.sql")


# #
# todo 1.14 护理记录
# 慢212.5745 秒
# 数据量：每条住院记录3条护理记录（共9万）
# Cdrd_PO.crt_cdrdPatientNurseInfo('护理记录')
# Cdrd_PO.procedure("s_cdrd_patient_nurse_info", '护理记录')
# Cdrd_PO.openSql("s_cdrd_patient_nurse_info.sql")


# # #
# todo 1.15 死亡记录
# 数据量：从3万名患者中随机500人有死亡记录，其中200均有patientid、patient_visit_id，剩余300只有patientid
# Cdrd_PO.crt_cdrdPatientDeathInfo('死亡记录')
# Cdrd_PO.procedure("s_cdrd_patient_death_info", '死亡记录')
# Cdrd_PO.openSql("s_cdrd_patient_death_info.sql")


# todo 1。16 标签表
# Cdrd_PO.crt_patient_tag('标签表')
# Cdrd_PO.procedure("s_patient_tag", '标签表')  # 42w
# 30000*4 = 12w
# 150000*2 = 30w
# -----------------------------------------------
# 请编写一个存储过程，用于生成一批数据。
#
# 表patient_tag的表结构字段如下：
# tag_record_id BIGINT PRIMARY KEY,
# category_source_id int,
# category_key nvarchar(100),
# category_id int,
# tag_id int,
# tag_key nvarchar(100),
# tag_data_id int,
# tag_data_key nvarchar(100),
# create_id int,
# create_by nvarchar(20),
# create_time DATETIME
#
# 表sys_tag_type的表结构字段如下：
# tag_id int IDENTITY(1,1) PRIMARY KEY,
# category_class nvarchar(100),
# category_name nvarchar(20),
# category_key nvarchar(100),
# tag_name nvarchar(20),
# tag_key nvarchar(100),
# tag_sort int,
# status varchar(100),
# create_id int,
# create_time DATETIME,
# update_id int,
# update_time DATETIME,
# remark nvarchar(500)
#
# 要求遍历sys_tag_type表中category_key字段的值，如果值等于cdrd_patient_info, 则遍历cdrd_patient_info_5表每条记录，patient_tag表生成数据如下：
# category_source_id字段的值为 cdrd_patient_info_5表中patient_id字段的值，category_key字段的值为cdrd_patient_info,catetory_id字段值为cdrd_patient_info_5表中patient_id字段的值,
# tag_id字段的值为sys_tag_type表中tag_id字段的值，tag_key字段的值为sys_tag_type表中tag_key字段的值，tag_data_id字段的值为sys_tag_data表中匹配一次tag_data_id字段的值，tag_data_key字段的值为sys_tag_data表中匹配一次tag_data_key字段的值，
# create_id字段的值为11，create_by字段的值为tester11，create_time字段的值为当前时间。
#
# 如果值等于cdrd_patient_visit_info, 则遍历cdrd_patient_visit_info_5表每条记录，patient_tag表生成数据如下：
# category_source_id字段的值为 cdrd_patient_visit_info_5表中patient_visit_id字段的值，category_key字段的值为cdrd_patient_visit_info,catetory_id字段值为cdrd_patient_visit_info_5表中patient_visit_id字段的值,
# tag_id字段的值为sys_tag_type表中tag_id字段的值，tag_key字段的值为sys_tag_type表中tag_key字段的值，tag_data_id字段的值为sys_tag_data表中匹配一次tag_data_id字段的值，tag_data_key字段的值为sys_tag_data表中匹配一次tag_data_key字段的值，
# create_id字段的值为11，create_by字段的值为tester11，create_time字段的值为当前时间。
#
# 以上对表patient_tag的数据插入，需要提高效率。
# -----------------------------------------------


# 登录日志
# 数据量：50万
# Cdrd_PO.crt_sys_logininfo('登录登出表')
# Cdrd_PO.procedure("s_sys_logininfo", '登录登出表') # 存储过程中改成 50w
# Cdrd_PO.subProcedure("r_logininfo__", "登录登出 - 登录类型，方式")



# todo 2 标签表
# Cdrd_PO.crt_SnowflakeSequence('雪花序列表')   # 临时中间表
# Cdrd_PO.subProcedure("GenerateSnowflakeID", '雪花')  # 生成雪花
# Cdrd_PO.crt_patient_tag('标签表')
# Cdrd_PO.insert_cdrdPatientTag()  # 插入4条数据
# Cdrd_PO.openSql("GenerateSnowflakeID.sql")


# todo 3-1 标签配置 - 标签表
# Cdrd_PO.crt_sys_tag_type('标签表')
# Sqlserver_PO.execute("insert into sys_tag_type(category_class,category_name,category_key,tag_name,tag_key,tag_sort,status,create_id,create_time,update_id,update_time,remark) "
#                      "values('patient_detail','患者详情患者信息','cdrd_patient_info','治疗方式','patient_deal_way',1,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情患者信息','cdrd_patient_info','疾病进展','progression_of_disease',2,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情患者信息','cdrd_patient_info','随访是否有异常','follow_up_abnormalities',3,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情患者信息','cdrd_patient_info','责任人','person_in_charge',4,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情患者信息','cdrd_patient_visit_info','就诊类型','patient_visit_type',1,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情患者信息','cdrd_patient_visit_info','临床研判','clinical_assessment',2,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')")

#
# todo 3-2 标签配置 - 标签数据表
# Cdrd_PO.crt_sys_tag_data('标签数据表')
# Sqlserver_PO.execute("insert into sys_tag_data(tag_id,tag_data_name,tag_data_key,tag_data_sort,status) "
#                      "values(1,'激素','hormone',1,'0'),(1, '单抗', 'infliximab', 2, '0')"
#                      ",(2,'缓解期','paracmasis',1,'0'),(2, '进行期', 'active_stage', 2, '0'),(2, '早发期', 'early_maturing_variety', 3, '0')"
#                      ",(3,'有','yes',1,'0'),(3, '无', 'no', 2, '0')"
#                      ",(4,'张三','zhangsan',1,'0'),(4, '李四', '李四', 2, '0'),(4,'王五','wangwu',3,'0'),(4, '赵六', 'zhaoliu', 4, '0')"
#                      ",(5,'出诊','visit_first',1,'0'),(5, '复诊', 'visit_again', 2, '0'),(5, '转诊', 'visit_transfer', 3, '0')"
#                      ",(6,'疑似RA','suspected_RA',1,'0'),(6, '强直待排', 'pending_resolution', 2, '0'),(6, '肿瘤疑似', 'tumor_suspected', 3, '0')")


# todo 3-3 标签配置 - 标签权限表
# Cdrd_PO.crt_sys_tag_authority('标签权限表')
#


# todo 4 扩展字段表
# Cdrd_PO.crt_patient_extend_field('扩展字段表')
# Cdrd_PO.procedure("s_patient_extend_field", '扩展字段表')  # 90w = 15W * 6
# --------------------------------------------------------
#请编写一个存储过程，用于生成一批数据。
# 表patient_extend_field的表结构字段如下：
# extend_field_record_id int IDENTITY(1,1) PRIMARY KEY,
# category_source_id int,
# category_key nvarchar(100),
# category_id int,
# extend_field_id int,
# extend_field_key nvarchar(100),
# extend_field_text nvarchar(max),
# create_id int,
# create_by nvarchar(20),
# create_time DATETIME
#
# 表sys_extend_field_manage的表结构字段如下：
# extend_field_id int IDENTITY(1,1) PRIMARY KEY,
# category_class nvarchar(100),
# category_name nvarchar(20),
# category_key nvarchar(100),
# extend_field_name nvarchar(20),
# extend_field_key nvarchar(100),
# sort int,
# status varchar(100),
# create_id int,
# create_time DATETIME,
# update_id int,
# update_time DATETIME,
# remark nvarchar(500)
#
# 要求遍历cdrd_patient_visit_info_5表每条记录, patient_extend_field表生产数据如下：
# category_source_id字段的值为 cdrd_patient_visit_info_5表中patient_id字段的值，
# category_key字段的值为cdrd_patient_visit_info,
# catetory_id字段值为cdrd_patient_info_5表中patient_visit_id字段的值,
# extend_field_key字段值为sys_extend_field_manage中extend_field_key的值，
# extend_field_text字段值为1到100000的随机值，
# create_id字段的值为11，create_by字段的值为tester11，create_time字段的值为当前时间。
#
# 以上对表patient_extend_field的数据插入，需要提高效率。
# --------------------------------------------------------


# todo 5-1 扩展字段配置 - 扩展字段管理
# Cdrd_PO.crt_sys_extend_field_manage('扩展字段管理')
# Sqlserver_PO.execute("insert into sys_extend_field_manage(category_class,category_name,category_key,extend_field_name,extend_field_key,sort,status,create_id,create_time,update_id,update_time,remark) "
#                      "values('patient_detail','患者详情就诊信息','cdrd_patient_visit_info','用药基数','dosage_base',1,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情就诊信息','cdrd_patient_visit_info','眼睑水肿','eyelid_edema',2,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情就诊信息','cdrd_patient_visit_info','眼睑红斑','eyelid_erythema',3,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情就诊信息','cdrd_patient_visit_info','结膜水肿','conjunctival_edema',4,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情就诊信息','cdrd_patient_visit_info','结膜充血','conjunctival_congestion',5,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')"
#                      ",('patient_detail','患者详情就诊信息','cdrd_patient_visit_info','突眼度','exophthalmos_degree',6,'0',1001,GETDATE(),'123',GETDATE(),'自动生成')")

#
# todo 5-2 扩展字段配置 - 扩展字段权限表
# Cdrd_PO.crt_sys_extend_field_authority('扩展字段权限表')




# todo 6-1 导出配置 - 导出模板表
# Cdrd_PO.crt_patient_export('导出模板表')

# todo 6-2 导出配置 - 导出模块表
# Cdrd_PO.crt_patient_export_module('导出模块表')

# todo 6-3 导出配置 - 导出数据表
# Cdrd_PO.crt_patient_export_field('导出数据表')


# todo 7 字段模块表
# Cdrd_PO.crt_sys_category_mapping('字段模块表')
# Sqlserver_PO.execute("insert into sys_category_mapping(category_class,category_name,category_tier,category_sort,category_status,category_fa_key,category_key) "
# "values('patient_detail','患者详情',1,1,'0','','cdrd_patient_info')"
# ",('patient_detail','疾病诊断史',2,1,'0','cdrd_patient_info','cdrd_patient_diag_info')"
# ",('patient_detail','就诊信息',2,2,'0','cdrd_patient_info','cdrd_patient_visit_info')"
# ",('patient_detail','疾病诊断史',3,1,'0','cdrd_patient_visit_info','cdrd_patient_diag_info')"
# ",('patient_detail','症状信息',3,2,'0','cdrd_patient_visit_info','cdrd_patient_symptom_info')"
# ",('patient_detail','体征信息',3,3,'0','cdrd_patient_visit_info','cdrd_patient_physical_sign_info')"
# ",('patient_detail','实验室检查',3,4,'0','cdrd_patient_visit_info','cdrd_patient_lab_examination_info')"
# ",('patient_detail','检查项目明细',4,1,'0','cdrd_patient_lab_examination_info','cdrd_patient_test_project_info')"
# ",('patient_detail','辅助检查',3,5,'0','cdrd_patient_visit_info','cdrd_patient_assit_examination_info')"
# ",('patient_detail','检查项目明细',4,1,'0','cdrd_patient_assit_examination_info','cdrd_patient_test_project_info')"
# ",('patient_detail','门诊医嘱',3,6,'0','cdrd_patient_visit_info','cdrd_patient_clinic_advice_info')"
# ",('patient_detail','用药信息',4,1,'0','cdrd_patient_clinic_advice_info','cdrd_patient_drug_info')"
# ",('patient_detail','住院医嘱',3,7,'0','cdrd_patient_visit_info','cdrd_patient_hospital_advice_info')"
# ",('patient_detail','用药信息',4,1,'0','cdrd_patient_hospital_advice_info','cdrd_patient_drug_info')"
# ",('patient_detail','出院记录',3,8,'0','cdrd_patient_visit_info','cdrd_patient_out_hospital_info')"
# ",('patient_detail','手术信息',3,9,'0','cdrd_patient_visit_info','cdrd_patient_operation_info')"
# ",('patient_detail','护理记录',3,10,'0','cdrd_patient_visit_info','cdrd_patient_nurse_info')"
# ",('patient_detail','死亡记录',3,11,'0','cdrd_patient_visit_info','cdrd_patient_death_info')"
# ",('patient_detail','症状信息',2,3,'0','cdrd_patient_info','cdrd_patient_symptom_info')"
# ",('patient_detail','体征信息',2,4,'0','cdrd_patient_info','cdrd_patient_physical_sign_info')"
# ",('patient_detail','实验室检查',2,5,'0','cdrd_patient_info','cdrd_patient_lab_examination_info')"
# ",('patient_detail','检查项目明细',3,1,'0','cdrd_patient_lab_examination_info','cdrd_patient_test_project_info')"
# ",('patient_detail','辅助检查',2,6,'0','cdrd_patient_info','cdrd_patient_assit_examination_info')"
# ",('patient_detail','检查项目明细',3,1,'0','cdrd_patient_assit_examination_info','cdrd_patient_test_project_info')"
# ",('patient_detail','用药信息',2,7,'0','cdrd_patient_info','cdrd_patient_drug_info')"
# ",('patient_detail','手术信息',2,8,'0','cdrd_patient_info','cdrd_patient_operation_info')"
# ",('patient_detail','死亡记录',2,9,'0','cdrd_patient_info','cdrd_patient_death_info')")


# todo 8 字段表
# Cdrd_PO.crt_sys_category('字段表')
# Sqlserver_PO.xlsx2db_append('sys_category.xlsx', "sys_category", "sheet")


#
# todo 11，文件下载管理
# Cdrd_PO.crt_sys_file_download('文件下载管理')
#
# todo 12，文件下载记录
# Cdrd_PO.crt_sys_file_download_record('文件下载记录')

# todo 13-1，字典类型表
# Cdrd_PO.crt_sys_dict_type('字典类型表')
# Sqlserver_PO.xlsx2db_deduplicated('CDRB20250623.xlsx', "sys_dict_type", "dict_name", "dict1")

# todo 13-2，字典数据表
# Cdrd_PO.crt_sys_dict_data('字典数据表')
# Sqlserver_PO.xlsx2db_append('CDRB20250623.xlsx', "sys_dict_data", "dict2")



# todo 19，医院信息表
# Cdrd_PO.crt_sys_hospital('医院信息表')


# todo 20-1，科室表
# 数据量：20个科室
# Cdrd_PO.crt_sys_department('科室表')
# Cdrd_PO.subProcedure("p_dept", "科室, ['内科','外科','儿科','妇产科','骨科','眼科','耳鼻喉科','口腔科','皮肤科','心血管科','神经科','精神科','放射科','检验科','影像科','重症医学科','麻醉科','急诊科','临床药学','康复科']")
# Cdrd_PO.procedure("s_sys_department", '科室表')
# # Cdrd_PO.index('IX_a_sys_department_department_id', 'a_sys_department', 'department_id')
# # Cdrd_PO.updateStatistics('SYS_DEPARTMENT')


# todo 20-2，科室医疗组
# 数据量：每个科室下2个医疗组
# Cdrd_PO.crt_sys_dept_medgp('科室医疗组')
# Cdrd_PO.procedure("s_sys_dept_medgp", '医疗组')
# # # Cdrd_PO.index('IX_a_sys_dept_medgp_department_id', 'a_sys_dept_medgp', 'department_id')
# # # Cdrd_PO.updateStatistics('a_sys_dept_medgp')


# todo 20-3，医疗组人员
# 数据量：每个医疗组下5名成员
# Cdrd_PO.crt_sys_dept_medgp_person('医疗组人员')
# Cdrd_PO.procedure("s_sys_dept_medgp_person", '医疗组人员')
# # # Cdrd_PO.index('IX_a_sys_dept_medgp_person_department_treat_group_id', 'a_sys_dept_medgp_person', 'department_treat_group_id')
# # # Cdrd_PO.updateStatistics('a_sys_dept_medgp_person')



# todo 21-1，用户表
# Cdrd_PO.crt_sys_user('用户表')
# Cdrd_PO.procedure("s_sys_user", '用户表')
#
# todo 21-2，用户角色关系表
# Cdrd_PO.crt_sys_user_role('用户角色关系表')
# Cdrd_PO.procedureUserRole("s_sys_user_role", '用户角色关系表')  # 一个用户可多个角色，用户3关联角色1，3，4
#
# todo 21-3，用户问题关系表
# Cdrd_PO.crt_sys_user_pwdptc('用户问题关系表')
#
#
# todo 22，用户密保问题表
# Cdrd_PO.crt_sys_security_question('用户密保问题表')


# todo 23，角色管理(ok)
# Cdrd_PO.crt_sys_role('角色表')
# Cdrd_PO.procedure("s_sys_role", '角色表')  #  //参数RecordCount=6忽略，程序写死角色6

# Cdrd_PO.crt_sys_role_menu('角色菜单关系表')
# Cdrd_PO.procedureRoleMenu("s_sys_role_menu", '角色菜单关系表', {'科主任': [3, 7, 8,9,10,11,12,13,15,24,25,86,87,109],
#                                                          '副主任': [3, 7, 8,9,10,11,12,13,15,24,25,86,87,109],
#                                                          '医疗组长': [3, 7, 8,9,10,11,12,13,15,24,25,86,87,109],
#                                                          '主治医生': [3, 7, 8,9,10,11,12,13,15,24,25,86,87,109],
#                                                          '门急诊医生住院医生': [3, 7, 8,9,10,11,12,13,15,24,25,86,87,109],
#                                                          '运营负责人': [3, 7, 8,9,10,11,12,13,15,24,25,86,87,109]})
# 一个角色可多个菜单，如：角色3关联菜单18，20，21


# todo 24，菜单管理
# Cdrd_PO.crt_sys_menu('菜单表')
# Cdrd_PO.procedureMenu("s_sys_menu", '菜单表', ['M', '系统管理', None])
# Cdrd_PO.procedureMenu("s_sys_menu", '菜单表', ['M', '系统监控', None])
# Cdrd_PO.procedureMenu("s_sys_menu", '菜单表', ['M', '系统权限', None])
# Cdrd_PO.procedureMenu("s_sys_menu", '菜单表', ['C', '医生管理', '系统监控'])
# Cdrd_PO.procedureMenu("s_sys_menu", '菜单表', ['C', '客户管理', '系统监控'])
# Cdrd_PO.procedureMenu("s_sys_menu", '菜单表', ['F',  '查询', '用户管理'])
# Cdrd_PO.procedureMenu("s_sys_menu", '菜单表', ['F',  '编辑', '用户管理'])
# Cdrd_PO.procedureMenu("s_sys_menu", '菜单表', ['F',  '新增123', '客户管理'])


# todo 25，参数配置
# Cdrd_PO.crt_sys_config('参数配置')
# Cdrd_PO.procedure("s_sys_config", '参数配置', 4)  # ????

# =======================================================================================================
# =======================================================================================================
# =======================================================================================================




# Cdrd_PO.sys_task('待办任务表')
# Cdrd_PO.sys_file_download('待办任务表')

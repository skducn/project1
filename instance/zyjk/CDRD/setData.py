# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-3-27
# Description   : setData 创建表、存储过程、插入数据

# 使用豆包，快速格式化一下内容：
# 如：密码最后更新时间	pwd_update_time
# 密码下次更新时间	pwd_next_update_time，请将以上数据中字段与字段英文名互换位置，并用逗号分隔输出
# 请优化，在每一行前加上Sqlserver_PO.setFieldComment('a_sys_user',
# *********************************************************************

from CdrdPO import *
Cdrd_PO = CdrdPO()

# 子存储过程
# Cdrd_PO.subProcedure("p_abo_type", "Abo血型, {'1': 'A 型', '2': 'B 型', '3': 'O 型', '4': 'AB 型', '5': '不详', '6': '未查'}")
# Cdrd_PO.subProcedure("p_address", "住址")
# Cdrd_PO.subProcedure("p_assit_examination_type", "辅助检查类型, {'1': '电生理检查', '2': '放射学检查', '3': '超声检查', '4': '内镜检查', '5': '其他检查', '6': '病理检查'}")
# Cdrd_PO.subProcedure("p_birth_place", "出生地-省市县")
# Cdrd_PO.subProcedure("p_cert_type", "证件类型, {'1': '居民身份证', '2': '居民户口簿', '3': '护照', '4': '军官证', '5': '驾驶证', '6': '港澳居民来往内地通行证', '7': '台湾居民来往内地通行证', '9': '其他法定有效证件'}")
# Cdrd_PO.subProcedure("p_dept", "科室, ['内科', '外科', '妇产科', '儿科', '肿瘤科', '五官科', '其他临床科室', '医技科室', '内分泌科', '骨科']")
# Cdrd_PO.subProcedure("p_drug_allergy_type", "药物过敏,  {'1': '否', '2': '有'}")
# Cdrd_PO.subProcedure("p_hospital", "医院, ['东方医院','复旦大学附属眼耳鼻喉科医院','上海交通大学医学院附属第九人民医院','上海市第一人民医院','上海交通大学医学院附属新华医院']")
# Cdrd_PO.subProcedure("p_hospital_advice", "住院医嘱类型, {'1': '住院药物医嘱', '2': '住院非药物医嘱'}")
# Cdrd_PO.subProcedure("p_idcard", "身份证")
# Cdrd_PO.subProcedure("p_in_state", "入院病情, {'1': '有', '2': '临床未确定', '3': '情况不明', '4': '无'}")
# Cdrd_PO.subProcedure("p_is_cache", "是否缓存, {'0': '缓存', '1': '不缓存'}")
# Cdrd_PO.subProcedure("p_job", "职业, ['军人', '医生', '自由职业者', '技术人员', '工程师', '学生', '老师', '服务人员']")
# Cdrd_PO.subProcedure("p_marriage", "婚姻, {'1': '未婚', '2': '已婚', '3': '丧偶', '4': '离婚', '9': '其他'}")
# Cdrd_PO.subProcedure("p_medical_payment_type", "付费方式, {'1': '城镇职工基本医疗保险', '2': '城镇居民基本医疗保险', '3': '新型农村合作医疗', '4': '贫困救助', '5': '商业医疗保险', '6': '全公费', '7': '全自费', '8': ' 其他社会保险 (指生育保险、工伤保险、农民工保险等)', '9': '其他'}")
# Cdrd_PO.subProcedure("p_name", "姓名")
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




# todo 1，专病库字段表
# 患者基本信息
# Cdrd_PO._a_cdrd_patient_info('患者基本信息')
# Cdrd_PO.procedure("cdrd_patient_info", '患者基本信息', 10)
#
# # 诊断表
# Cdrd_PO._a_cdrd_patient_diag_info('诊断表')
# Cdrd_PO.procedure("cdrd_patient_diag_info", '诊断表', 2)
#
#
# # 门(急)诊住院就诊信息
# Cdrd_PO._a_cdrd_patient_visit_info('门(急)诊住院就诊信息')
# Cdrd_PO.procedure("cdrd_patient_visit_info", '门(急)诊住院就诊信息', 3)
#
#
# # # 症状信息
# Cdrd_PO._a_cdrd_patient_symptom_info('症状信息')
# Cdrd_PO.procedure("cdrd_patient_symptom_info", '症状信息', 3)
#
#
# # # 体征信息
# Cdrd_PO._a_cdrd_patient_physical_sign_info('体征信息')
# Cdrd_PO.procedure("cdrd_patient_physical_sign_info", '体征信息', 3)
#
# # #
# # # 实验室检查报告
# Cdrd_PO._a_cdrd_patient_lab_examination_info('实验室检查报告')
# Cdrd_PO.procedure("cdrd_patient_lab_examination_info", '实验室检查报告', 3)
#
# # #
# # # 辅助检查报告
# Cdrd_PO._a_cdrd_patient_assit_examination_info('辅助检查报告')
# Cdrd_PO.procedure("cdrd_patient_assit_examination_info", '辅助检查报告', 3)
#
# # #
# # # 检查项目明细
# Cdrd_PO._a_cdrd_patient_test_project_info('检查项目明细')
# Cdrd_PO.procedure("cdrd_patient_test_project_info", '检查项目明细', 3)
# #
# # # #
# # # # 门诊医嘱
Cdrd_PO._a_cdrd_patient_clinic_advice_info('门诊医嘱')
Cdrd_PO.procedure("cdrd_patient_clinic_advice_info", '门诊医嘱', 3)
#
# # #
# # #  住院医嘱
# # Cdrd_PO._a_cdrd_patient_hosptial_advice_info('住院医嘱')
# Cdrd_PO.procedure("cdrd_patient_hosptial_advice_info", '住院医嘱', 3)
# #
# # # #
# # # #  用药信息
# # Cdrd_PO._a_cdrd_patient_drug_info('用药信息')
# Cdrd_PO.procedure("cdrd_patient_drug_info", '用药信息', 3)
#
# # #
# # # 出院记录
# # Cdrd_PO._a_cdrd_patient_out_hospital_info('出院记录')
# Cdrd_PO.procedure("cdrd_patient_out_hospital_info", '出院记录', 3)
#
# # #
# # # 手术记录
# Cdrd_PO._a_cdrd_patient_operation_info('手术记录')
# Cdrd_PO.procedure("cdrd_patient_operation_info", '手术记录', 3)

# #
# # 护理记录
# Cdrd_PO._a_cdrd_patient_nurse_info('护理记录')
# Cdrd_PO.procedure("cdrd_patient_nurse_info", '护理记录', 3)
#
# # #
# # # 死亡记录
# Cdrd_PO._a_cdrd_patient_death_info('死亡记录')
# Cdrd_PO.procedure("cdrd_patient_death_info", '死亡记录', 3)





# todo 2，数据字典配置
# Cdrd_PO._a_sys_dict_type('字典类型表')
# Sqlserver_PO.xlsx2db_deduplicated('CDRB20250623.xlsx', "a_sys_dict_type", "dict_name", "dict1")

# Cdrd_PO._a_sys_dict_data('字典数据表')
# Sqlserver_PO.xlsx2db_append('CDRB20250623.xlsx', "a_sys_dict_data", "dict2")



# todo 3，医院管理
# Cdrd_PO.dept__a_sys_hopital('医院信息表')



# todo 4，科室管理
# # Cdrd_PO.dept__a_sys_department('科室表')  # 创建或重构科室表
# Cdrd_PO.procedure("sys_department", '科室表', 2)
#
# # Cdrd_PO.dept__a_sys_dept_medgp('医疗组')
# Cdrd_PO.procedure("sys_dept_medgp", '医疗组', 3)
# #
# # Cdrd_PO.dept__a_sys_dept_medgp_person('医疗组人员')
# Cdrd_PO.procedure("sys_dept_medgp_person", '医疗组人员', 3)



# todo 5，用户管理(ok)
# Cdrd_PO.user__a_sys_user('用户表')
# Cdrd_PO.procedure("sys_user", '用户表', 4)

# Cdrd_PO.user__a_sys_user_role('用户角色关系表')
# Cdrd_PO.procedureUserRole("sys_user_role", '用户角色关系表', {3: [1, 3, 4]})  # 一个用户可多个角色，用户3关联角色1，3，4

# Cdrd_PO.user__a_sys_user_pwdptc('用户问题关系表')


# todo 角色管理(ok)
# Cdrd_PO.role__a_sys_role('角色表')
# Cdrd_PO.procedure("sys_role", '角色表', 6)  # exec a_sys_role @RecordCount=6;  //参数RecordCount=6忽略，程序写死角色6

# Cdrd_PO.role__a_sys_role_menu('角色菜单关系表')
# Cdrd_PO.procedureRoleMenu("sys_role_menu", '角色菜单关系表', {'副主任': [18, 20, 21]}) # 一个角色可多个菜单，如：角色3关联菜单18，20，21



# todo 菜单管理
# Cdrd_PO.menu__a_sys_menu('菜单表')
# Cdrd_PO.procedureMenu("sys_menu", '菜单表', ['M', '系统管理', None])
# Cdrd_PO.procedureMenu("sys_menu", '菜单表', ['M', '系统监控', None])
# Cdrd_PO.procedureMenu("sys_menu", '菜单表', ['M', '系统权限', None])
# Cdrd_PO.procedureMenu("sys_menu", '菜单表', ['C', '医生管理', '系统监控'])
# Cdrd_PO.procedureMenu("sys_menu", '菜单表', ['C', '客户管理', '系统监控'])
# Cdrd_PO.procedureMenu("sys_menu", '菜单表', ['F',  '查询', '用户管理'])
# Cdrd_PO.procedureMenu("sys_menu", '菜单表', ['F',  '编辑', '用户管理'])
# Cdrd_PO.procedureMenu("sys_menu", '菜单表', ['F',  '新增123', '客户管理'])



# todo 参数配置
# Cdrd_PO._a_sys_config('参数配置')
# Cdrd_PO.procedure("sys_config", '参数配置', 4)


# todo 登录日志
# Cdrd_PO._a_sys_logininfo('登录登出表')
# Cdrd_PO.procedure("sys_logininfo", '登录登出表', 4)


















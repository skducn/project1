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




# todo 科室管理
# Cdrd_PO.dept__a_sys_department('科室表')  # 创建或重构科室表
# Cdrd_PO.procedure("a_sys_department__data", 1)  # exec a_sys_department__data @RecordCount=1;

# Cdrd_PO.dept__a_sys_dept_medgp('医疗组')
# Cdrd_PO.procedure("a_sys_dept_medgp__data", 1)  # exec a_sys_dept_medgp__data @RecordCount=1;
#
# Cdrd_PO.dept__a_sys_dept_medgp_person('医疗组人员')
# Cdrd_PO.procedure("a_sys_dept_medgp_person__data", 1)  # exec a_sys_dept_medgp_person__data @RecordCount=1;



# todo 用户管理(ok)
# Cdrd_PO.user__a_sys_user('用户表')
# Cdrd_PO.procedure("a_sys_user__data", 1)  # exec a_sys_user__data @RecordCount=1;

# Cdrd_PO.user__a_sys_user_role('用户角色关系表')
# Cdrd_PO.procedureUserRole("a_sys_user_role__data", {3: [1, 3, 4]})  # 一个用户可多个角色，用户3关联角色1，3，4



# todo 角色管理(ok)
# Cdrd_PO.role__a_sys_role('角色表')
#  ('科主任'),('副主任'),('医疗组长'),('主治医生'),('门/急诊医生、住院医生')
# Cdrd_PO.procedure("a_sys_role__data")  # exec a_sys_role__data @RecordCount=6;  //参数RecordCount=6忽略，程序写死角色6

# Cdrd_PO.role__a_sys_role_menu('角色菜单关系表')
# exec a_sys_role_menu__data @roleName=副主任, @menu_id=18;
# exec a_sys_role_menu__data @roleName=副主任, @menu_id=20;
# exec a_sys_role_menu__data @roleName=副主任, @menu_id=21;
# Cdrd_PO.procedureRoleMenu("a_sys_role_menu__data", {'副主任': [18, 20, 21]}) # 一个角色可多个菜单，如：角色3关联菜单18，20，21




# todo 菜单管理
# Cdrd_PO.menu__a_sys_menu('菜单表')
# exec a_sys_menu__data @menuType=M, @menuName=系统管理, @menuParentName=None;
# exec a_sys_menu__data @menuType=M, @menuName=系统监控, @menuParentName=None;
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['M', '系统管理', None])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['M', '系统监控', None])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['M', '系统权限', None])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['C', '医生管理', '系统监控'])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['C', '客户管理', '系统监控'])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['F',  '查询', '用户管理'])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['F',  '编辑', '用户管理'])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['F',  '新增123', '客户管理'])


# todo 参数配置
# Cdrd_PO._a_sys_config('参数配置')


# todo 登录日志
# Cdrd_PO._a_sys_logininfo('登录日志')


# todo 患者基本信息
# Cdrd_PO._a_cdrd_patient_info('患者基本信息')

# todo 诊断表
# Cdrd_PO._a_cdrd_patient_diag_info('诊断表')

# todo 门(急)诊住院就诊信息
# Cdrd_PO._a_cdrd_patient_visit_info('门(急)诊住院就诊信息')

# todo 症状信息
Cdrd_PO._a_cdrd_patient_symptom_info('症状信息')

# todo 体征信息
# Cdrd_PO._a_cdrd_patient_physical_sign_info('体征信息')

# todo 实验室检查报告
# Cdrd_PO._a_cdrd_patient_lab_examination_info('实验室检查报告')

# todo 辅助检查报告
# Cdrd_PO._a_cdrd_patient_assit_examination_info('辅助检查报告')

# todo 检查项目明细
# Cdrd_PO._a_cdrd_patient_test_project_info('检查项目明细')

# todo 门诊医嘱
# Cdrd_PO._a_cdrd_patient_clinic_advice_info('门诊医嘱')

# todo 住院医嘱
# Cdrd_PO._a_cdrd_patient_hosptial_advice_info('住院医嘱')

# todo 用药信息
# Cdrd_PO._a_cdrd_patient_drug_info('用药信息')

# todo 出院记录
# Cdrd_PO._a_cdrd_patient_out_hospital_info('出院记录')

# todo 手术记录
# Cdrd_PO._a_cdrd_patient_operation_info('手术记录')

# todo 护理记录
# Cdrd_PO._a_cdrd_patient_nurse_info('护理记录')

# todo 死亡记录
# Cdrd_PO._a_cdrd_patient_death_info('死亡记录')

















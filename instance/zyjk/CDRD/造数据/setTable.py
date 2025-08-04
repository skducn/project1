# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-3-27
# Description   : setData 创建库表
# *********************************************************************

from PO.SqlserverPO import *

Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")

# # todo 科室管理 - 科室表 a_sys_department
# Sqlserver_PO.crtTableByCover('a_sys_department',
#                                    '''department_id INT IDENTITY(1,1) PRIMARY KEY,
#                                     department_name NVARCHAR(20),
#                                     department_code NVARCHAR(20),
#                                     department_charge_id int,
#                                     department_charge_job_num NVARCHAR(20),
#                                     department_charge_name NVARCHAR(20),
#                                     department_creater_name NVARCHAR(20),
#                                     department_create_time DATETIME
#                                   ''')
# Sqlserver_PO.setTableComment('a_sys_department', '科室表(测试用)')
# Sqlserver_PO.setFieldComment('a_sys_department', 'department_name', '科室名称')
# Sqlserver_PO.setFieldComment('a_sys_department', 'department_code', '科室编码')
# Sqlserver_PO.setFieldComment('a_sys_department', 'department_charge_id', '科室负责人ID')
# Sqlserver_PO.setFieldComment('a_sys_department', 'department_charge_job_num', '科室负责人工号')
# Sqlserver_PO.setFieldComment('a_sys_department', 'department_charge_name', '科室负责人姓名')
# Sqlserver_PO.setFieldComment('a_sys_department', 'department_creater_name', '创建人')
# Sqlserver_PO.setFieldComment('a_sys_department', 'department_create_time', '创建时间')


# # todo 科室管理 - 医疗组 a_sys_dept_medgp
# Sqlserver_PO.crtTableByCover('a_sys_dept_medgp',
#                                    '''department_id int,
#                                     department_treat_group_id int,
#                                     department_treat_group_name NVARCHAR(20),
#                                     department_treat_create_time DATETIME
#                                   ''')
# Sqlserver_PO.setTableComment('a_sys_dept_medgp', '科室-医疗组(测试用)')
# Sqlserver_PO.setFieldComment('a_sys_dept_medgp', 'department_treat_group_id', '医疗组ID')
# Sqlserver_PO.setFieldComment('a_sys_dept_medgp', 'department_treat_group_name', '医疗组名称')
# Sqlserver_PO.setFieldComment('a_sys_dept_medgp', 'department_treat_create_time', '医疗组创建时间')


# todo 科室管理 - 人员 a_sys_dept_medgp_person
Sqlserver_PO.crtTableByCover('a_sys_dept_medgp_person',
                                   '''department_treat_group_id INT,
                                    user_id int,
                                    user_name NVARCHAR(20),
                                    user_job_num NVARCHAR(20)
                                  ''')
Sqlserver_PO.setTableComment('a_sys_dept_medgp_person', '医疗组-人员(测试用)')
Sqlserver_PO.setFieldComment('a_sys_dept_medgp_person', 'user_id', '用户ID')
Sqlserver_PO.setFieldComment('a_sys_dept_medgp_person', 'user_name', '姓名')
Sqlserver_PO.setFieldComment('a_sys_dept_medgp_person', 'user_job_num', '工号')

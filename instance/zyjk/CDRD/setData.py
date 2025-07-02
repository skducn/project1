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
# Cdrd_PO.procedure("a_sys_department__data", 4)  # 创建并执行存储过程，插入N条记录

# Cdrd_PO.dept__a_sys_dept_medgp('医疗组')  # 创建或重构医疗组
# Cdrd_PO.procedure("a_sys_dept_medgp__data", 8)  # 创建并执行存储过程，插入N条记录
#
# Cdrd_PO.dept__a_sys_dept_medgp_person('医疗组人员')  # 创建或重构医疗组人员
# Cdrd_PO.procedure("a_sys_dept_medgp_person__data", 10)  # 创建并执行存储过程，插入N条记录



# todo 用户管理
# Cdrd_PO.user__a_sys_user('用户表')
# Cdrd_PO.procedure("a_sys_user__data", 14)

# Cdrd_PO.user__a_sys_user_role('用户角色关系表')


# todo 角色管理
# Cdrd_PO.role__a_sys_role('角色表')
# Cdrd_PO.procedure("a_sys_role__data")


# Cdrd_PO.role__a_sys_role_menu('角色菜单关系表')


# todo 菜单管理
# Cdrd_PO.menu__a_sys_menu('菜单表')
# 参数：['C', '医生管理', '系统监控']，三个参数不能少，如果没有父级菜单输入None
# 参数1：M是目录，C是菜单，F是按钮，层级关系是M-C-F
# 参数2：menu_user 菜单名称
# 参数3：parent_id 父级菜单ID
# 注意：None表示无父级菜单，
Cdrd_PO.procedureMenu("a_sys_menu__data", ['M', '系统管理1', None])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['M', '系统监控', None])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['M', '系统权限', None])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['C', '医生管理', '系统监控'])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['C', '客户管理', '系统监控'])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['F',  '查询', '用户管理'])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['F',  '编辑', '用户管理'])
# Cdrd_PO.procedureMenu("a_sys_menu__data", ['F',  '新增123', '客户管理'])


# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2025-7-1
# Description: 专病库CDRD
# *****************************************************************

from PO.SqlserverPO import *
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")



class CdrdPO(object):

    def __init__(self):
        ...

    def dept__a_sys_department(self, varCommon):
#
        # 科室管理 - 科室表 a_sys_department
        Sqlserver_PO.crtTableByCover('a_sys_department',
                                           '''department_id INT IDENTITY(1,1) PRIMARY KEY,
                                            department_name NVARCHAR(20),
                                            department_code NVARCHAR(20),
                                            department_charge_id int,
                                            department_charge_job_num NVARCHAR(20),
                                            department_charge_name NVARCHAR(20),
                                            department_creater_name NVARCHAR(20),
                                            department_create_time DATETIME
                                          ''')
        Sqlserver_PO.setTableComment('a_sys_department', varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment('a_sys_department', 'department_name', '科室名称')
        Sqlserver_PO.setFieldComment('a_sys_department', 'department_code', '科室编码')
        Sqlserver_PO.setFieldComment('a_sys_department', 'department_charge_id', '科室负责人ID')
        Sqlserver_PO.setFieldComment('a_sys_department', 'department_charge_job_num', '科室负责人工号')
        Sqlserver_PO.setFieldComment('a_sys_department', 'department_charge_name', '科室负责人姓名')
        Sqlserver_PO.setFieldComment('a_sys_department', 'department_creater_name', '创建人')
        Sqlserver_PO.setFieldComment('a_sys_department', 'department_create_time', '创建时间')
    def dept__a_sys_dept_medgp(self, varCommon):

        # 科室管理 - 医疗组 a_sys_dept_medgp
        Sqlserver_PO.crtTableByCover('a_sys_dept_medgp',
                                           '''department_id int,
                                            department_treat_group_id int,
                                            department_treat_group_name NVARCHAR(20),
                                            department_treat_create_time DATETIME
                                          ''')
        Sqlserver_PO.setTableComment('a_sys_dept_medgp', varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment('a_sys_dept_medgp', 'department_treat_group_id', '医疗组ID')
        Sqlserver_PO.setFieldComment('a_sys_dept_medgp', 'department_treat_group_name', '医疗组名称')
        Sqlserver_PO.setFieldComment('a_sys_dept_medgp', 'department_treat_create_time', '医疗组创建时间')
    def dept__a_sys_dept_medgp_person(self,varCommon):

        # 科室管理 - 人员 a_sys_dept_medgp_person
        Sqlserver_PO.crtTableByCover('a_sys_dept_medgp_person',
                                     '''department_treat_group_id INT,
                                      user_id int,
                                      user_name NVARCHAR(20),
                                      user_job_num NVARCHAR(20)
                                    ''')
        Sqlserver_PO.setTableComment('a_sys_dept_medgp_person', varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment('a_sys_dept_medgp_person', 'user_id', '用户ID')
        Sqlserver_PO.setFieldComment('a_sys_dept_medgp_person', 'user_name', '姓名')
        Sqlserver_PO.setFieldComment('a_sys_dept_medgp_person', 'user_job_num', '工号')


    def user__a_sys_user(self, varCommon):

        # 用户管理 - 用户表
        Sqlserver_PO.crtTableByCover('a_sys_user',
                                     '''
                                       user_id	int	IDENTITY(1,1) PRIMARY KEY,
                                       nick_name nvarchar(20),
                                       user_name nvarchar(20),
    user_type	nvarchar(2),
    password	nvarchar(100),
    job_num	nvarchar(20),
    email	nvarchar(50),
    phonenumber	nvarchar(20),
    sex 	int 	,
    avatar 	nvarchar(100),
    department_id	int	,
    department_code	nvarchar(20),
    department_name	nvarchar(20),
    user_account_state	int	,
    remark	nvarchar(500),
    creater_by	nvarchar(20),
    create_time	datetime	,
    update_by	nvarchar(20),
    update_time	datetime	,
    pwd_update_state	int	,
    pwd_update_time	datetime,	
    pwd_next_update_time	datetime	
                                    ''')
        Sqlserver_PO.setTableComment('a_sys_user', varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment('a_sys_user', 'user_id', '用户ID'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'nick_name', '姓名'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'user_name', '账号'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'user_type', '用户类型'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'password', '密码'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'job_num', '工号'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'email', '邮箱'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'phonenumber', '手机号'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'sex', '性别'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'avatar', '头像地址'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'department_id', '所属科室ID'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'department_code', '所属科室code'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'department_name', '所属科室名称'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'user_account_state', '账号状态'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'remark', '备注'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'creater_by', '创建人'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'create_time', '创建时间'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'update_by', '更新者'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'update_time', '更新时间'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'pwd_update_state', '密码重置状态'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'pwd_update_time', '密码最后更新时间'),
        Sqlserver_PO.setFieldComment('a_sys_user', 'pwd_next_update_time', '密码下次更新时间')
    def user__a_sys_user_role(self, varCommon):

        # 用户管理 - 用户角色关系表
        Sqlserver_PO.crtTableByCover('a_sys_user_role',
                                     '''
                                       user_id	int	,
                                       role_id int 	
                                    ''')
        Sqlserver_PO.setTableComment('a_sys_user_role', varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment('a_sys_user_role', 'user_id', '用户ID')
        Sqlserver_PO.setFieldComment('a_sys_user_role', 'role_id', '角色ID')

    def role__a_sys_role(self, varCommon):

        # 角色管理 - 角色表
        Sqlserver_PO.crtTableByCover('a_sys_role',
                                     '''
                                      role_id	int	,
role_name	nvarchar	(20),
role_key	nvarchar	(20),
role_sort	int,	
status	int	,
menu_check_strictly	int	,
role_creater_name	nvarchar	(20),
role_create_time	datetime,	
update_by	nvarchar	(20),
update_time	datetime	,
remark	nvarchar	(500)
                                    ''')
        Sqlserver_PO.setTableComment('a_sys_role', varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment('a_sys_role', 'role_id', '角色ID'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'role_name', '角色名称'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'role_key', '角色权限权限字符串'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'role_sort', '显示顺序'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'status', '角色状态'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'menu_check_strictly', '菜单树选择项是否关联显示'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'role_creater_name', '创建人'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'role_create_time', '创建时间'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'update_by', '更新者'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'update_time', '更新时间'),
        Sqlserver_PO.setFieldComment('a_sys_role', 'remark', '备注')
    def role__a_sys_role_menu(self, varCommon):

        # 角色管理 - 角色菜单关系表
        Sqlserver_PO.crtTableByCover('a_sys_role_menu',
                                     '''
                                       rold_id	int	,
                                       menu_id int 	
                                    ''')
        Sqlserver_PO.setTableComment('a_sys_role_menu', varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment('a_sys_role_menu', 'rold_id', '角色ID')
        Sqlserver_PO.setFieldComment('a_sys_role_menu', 'menu_id', '菜单ID')


    def menu__a_sys_menu(self, varCommon):

        # 菜单管理 - 菜单表
        Sqlserver_PO.crtTableByCover('a_sys_menu',
                                     '''
                                       menu_id	int	,
menu_name	nvarchar	(50),
parent_id 	int	,
order_num	int	,
path	nvarchar	(200),
component	nvarchar	(255),
query	nvarchar	(255),
route_name	nvarchar	(50),
is_frame	int	,
is_cache	int	,
menu_type	char	(1),
status	int	,
visible 	int,	
perms	nvarchar	(100),
icon	nvarchar	(100),
create_by	nvarchar	(64),
create_time	datetime	,
update_by	nvarchar	(64),
update_time	datetime	,
remark	nvarchar	(500)
                                    ''')
        Sqlserver_PO.setTableComment('a_sys_menu', varCommon + '(测试用)')
        Sqlserver_PO.setFieldComment('a_sys_menu', 'menu_id', '菜单ID'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'menu_name', '菜单名称'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'parent_id', '父级菜单ID'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'order_num', '显示顺序'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'path', '路由地址'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'component', '组件路径'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'query', '路由参数'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'route_name', '路由名称'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'is_frame', '是否为外链'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'is_cache', '是否缓存'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'menu_type', '菜单类型'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'status', '菜单状态'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'visible', '显示状态'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'perms', '权限字符'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'icon', '菜单图标'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'create_by', '创建者'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'create_time', '创建时间'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'update_by', '更新者'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'update_time', '更新时间'),
        Sqlserver_PO.setFieldComment('a_sys_menu', 'remark', '备注')




    def procedure(self, varParam, varQty):
        # 创建存储过程

        varParamSql = varParam + ".sql"
        execParam = "exec " + varParam + " @RecordCount=" + str(varQty) + ";"

        with open(varParamSql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        Sqlserver_PO.execute(sql_script)
        Sqlserver_PO.execute(execParam)  # 执行存储过程, 插入N条记录

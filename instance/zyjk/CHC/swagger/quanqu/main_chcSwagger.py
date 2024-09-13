# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : CHC swagger
# http://192.168.0.243:8011/doc.html
# http://192.168.0.243:8014/doc.html  default
# https://www.sojson.com/

# *********************************************************************
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), Configparser_PO.DB("charset"))  # 测试环境

from instance.zyjk.swagger.SwaggerPO import *
Swagger_PO8011 = SwaggerPO(Configparser_PO.HTTP("url8011"), Configparser_PO.HTTP("homepage"))
Swagger_PO8014 = SwaggerPO(Configparser_PO.HTTP("url8014"), Configparser_PO.HTTP("homepage"))


def importDb8011(d_menu_dboTable):
    # http://192.168.0.243:8011/doc.html
    # 导入数据库
    for k, v in d_menu_dboTable.items():
        Sqlserver_PO.list2db(['tags', 'summary', 'path', 'method', 'consumes', 'query', 'body', 'url'],
                             Swagger_PO8011.getAll(k), v)

def importDb8014(d_menu_dboTable):
    # http://192.168.0.243:8014/doc.html
    # 导入数据库
    for k, v in d_menu_dboTable.items():
        Sqlserver_PO.list2db(['tags', 'summary', 'path', 'method', 'consumes', 'query', 'body', 'url'],
                             Swagger_PO8014.getAll(k), v)


# todo 获取单接口
# Swagger_PO8011.getOne("chc-system", 'REST - 用户信息表', '获取没有绑定家医的医助信息')

# todo 获取全部接口
# Swagger_PO8011.getAll("chc-auth")
# Swagger_PO8011.getAll("chc-job")
# Swagger_PO8011.getAll("chc-system")
# Swagger_PO8011.getAll("chc-server")
# Swagger_PO8011.getAll("chc-rlues")

# Swagger_PO8014.getAll("default")

# todo 导入数据库
# importDb8011({"chc-auth": "a_chc_auth"})
# importDb8011({"chc-job": "a_chc_job"})
# importDb8011({"chc-system": "a_chc_system"})
# importDb8011({"chc-server": "a_chc_server"})
# importDb8011({"chc-rlues": "a_chc_rlues"})

importDb8014({"default": "a_chc_default"})



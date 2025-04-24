# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-4-16
# Description   : 获取数据库表数据，用于筛选，如筛选已通过、失败、未测试的接口
# *********************************************************************

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")

from PO.ColorPO import *
Color_PO = ColorPO()


def getInfo(tableName, l_status, *args):

    for i in l_status:
        if i == '已通过':
            try:
                if len(args) == 1:
                    l_d_ = Sqlserver_PO.select("select tags,summary,path,rpsDetail,%s from %s where status='%s'" % (args[0], tableName, '已通过'))
                elif len(args) == 2:
                    l_d_ = Sqlserver_PO.select("select tags,summary,path,rpsDetail,%s,%s from %s where status='%s'" % (args[0], args[1], tableName, '已通过'))
                elif len(args) == 3:
                    l_d_ = Sqlserver_PO.select("select tags,summary,path,rpsDetail,%s,%s,%s from %s where status='%s'" % (args[0], args[1], args[2], tableName, '已通过'))
                elif len(args) == 4:
                    l_d_ = Sqlserver_PO.select("select tags,summary,path,rpsDetail,%s,%s,%s,%s from %s where status='%s'" % (args[0], args[1], args[2], args[3], tableName, '已通过'))
                else:
                    l_d_ = Sqlserver_PO.select("select tags,summary,path,rpsDetail from %s where status='%s'" % (tableName, '已通过'))
                Color_PO.outColor([{"32": "已通过 =>"}])
                for _ in l_d_:
                    print(_)
            except Exception as e:
                # print(f"字段参数错误: {e}")
                Color_PO.outColor([{"31": f"字段参数错误: {e}"}])

        if i == '失败':
            l_d_ = Sqlserver_PO.select(
                "select tags,summary,path,rpsDetail from %s where status='%s'" % (tableName, '失败'))
            Color_PO.outColor([{"31": "\n失败 =>"}])
            for _ in l_d_:
                print(_)
        if i == '未测试':
            l_d_ = Sqlserver_PO.select("select tags,summary,path,rpsDetail from %s where status is NULL" % (tableName))
            Color_PO.outColor([{"34": "\n未测试(status为空) =>"}])
            for _ in l_d_:
                print(_)
        if i == '未测试2':
            l_d_ = Sqlserver_PO.select(
                "select tags,summary,path,rpsDetail from %s where status is NULL or rpsDetail is NULL" % (tableName))
            Color_PO.outColor([{"35": "\n未测试(status为空、rpsStatus为空) =>"}])
            for _ in l_d_:
                print(_)


# getInfo('a_phs_auth_app', ['已通过', '失败'])
# getInfo('a_phs_auth_app', ['已通过', '未测试'])
getInfo('a_phs_auth_app', ['已通过', '未测试2'], 'url', 'body', 'tester')

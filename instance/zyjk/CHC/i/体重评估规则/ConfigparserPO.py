# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-06-10
# Description   : 配置模块 ConfigParser
# *****************************************************************
import configparser

class ConfigparserPO:

    def __init__(self, file):
        self.cf = configparser.ConfigParser()
        self.cf.read(file, encoding="utf-8-sig")
        self.file = file

    def FILE(self, name):
        value = self.cf.get("FILE", name)
        return value

    def DB(self, name):
        value = self.cf.get("DB", name)
        return value

    def SWITCH(self, name):
        value = self.cf.get("SWITCH", name)
        return value


    def write(self, folder, key, value):
        self.cf[folder][key] = value  #  # Configparser_PO.cf['EXCEL']['sheetName'] = '55'  # 重新赋值
        self.cf.write(open(self.file, 'w'))

if __name__ == '__main__':

    Configparser_PO = ConfigparserPO('config.ini')


    # 获取key的值
    # print(Configparser_PO.cf.get("DB",'host'))  # 192.168.0.234
    # 获取所有key
    # print(Configparser_PO.cf.options('DB'))  # ['host', 'user', 'password', 'database', 'database2', 'tablews', 'tableef', 'tablehi']

    # 直接修改
    # Configparser_PO.write('DB', 'user', 'sa1')
    # print(Configparser_PO.DB('host'))  # sa1


    sectionName = Configparser_PO.cf.sections()  # 获取所有section名
    # print(sectionName)  # ['FILE', 'DB', 'SWITCH']
    # 新增
    if 'FILE' not in sectionName:
        Configparser_PO.cf.add_section('FILE')  # 新增section, 如果已存在则报错
        Configparser_PO.cf.set('FILE', 'testIdcard', '310101198004110014')  # 新增 key和value
        Configparser_PO.cf.write(open('config.ini', 'w'))  # 写保存
    # 修改
    if 'FILE' in sectionName:
        Configparser_PO.cf.set('FILE', 'testIdcard', '310101198004110014')  # 新增 key和value （覆盖）或修改
        Configparser_PO.cf.write(open('config.ini', 'w'))  # 写保存





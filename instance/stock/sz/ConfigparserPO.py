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

    def DATA(self, name):
        value = self.cf.get("DATA", name)
        return value

    def PATH(self, name):
        value = self.cf.get("PATH", name)
        return value


    def write(self, folder, key, value):
        self.cf[folder][key] = value  #  # Configparser_PO.cf['EXCEL']['sheetName'] = '55'  # 重新赋值
        self.cf.write(open(self.file, 'w'))





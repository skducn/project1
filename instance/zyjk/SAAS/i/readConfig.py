# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : 读取 config.ini , configparser
# ConfigParser 是用来读取config.ini配置文件的包
# 问题：UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb8 in position 185: invalid start byte
# 原因：'utf-8’编解码器无法解码位置0的字节0xb8：无效的起始字节；问题原因：函数模板的编码有问题，所以在调用函数的时候出现无法解码；' \
# 解决：设置函数模板的编码方式  encoding="gbk"

# 问题： ConfigParser的value如果包含\r\n的话都会被当成普通字符处理（自动转义成\\r\\n），只有编译器在编译时才会对\r\n等进行转义
# 解决：str.replace("\\n", "\n")
# *****************************************************************

import configparser, codecs

class ReadConfig:
    def __init__(self):
        # fd = open(configPath, "r")
        # data = fd.read()
        #
        # #  remove BOM
        # if data[:3] == codecs.BOM_UTF8:
        #     data = data[3:]
        #     file = codecs.open(configPath, "w")
        #     file.write(data)
        #     file.close()
        # fd.close()

        self.cf = configparser.ConfigParser()
        # self.cf.read('config.ini')
        self.cf.read('config.ini', encoding="gbk")  # 如果config.ini有中文
        # self.cf.read('config.ini', encoding="utf-8-sig")

    def get_default(self, name):
        value = self.cf.get("DEFAULT", name)
        return value

    def get_test(self, name):
        value = self.cf.get("TEST", name)
        return value

    def get_dev(self, name):
        value = self.cf.get("DEV", name)
        return value

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_switch(self, name):
        value = self.cf.get("SWITCH", name)
        return value
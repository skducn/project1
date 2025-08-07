# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-8-6
# Description   : set 创建CDRD_PATIENT_INFO
# *********************************************************************

from PO.SqlserverPO import *

Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "GBK")

import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

from PO.DataPO import *

Data_PO = DataPO()

from PO.TimePO import *

Time_PO = TimePO()


# AES加密函数 (128位 ECB模式)
def aes_encrypt(plaintext, key):
    # ECB模式不需要IV
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # 填充和加密
    padding_length = 16 - (len(plaintext) % 16)
    plaintext += chr(padding_length).encode('GBK') * padding_length
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext  # ECB模式不返回IV


# 将十六进制字符串密钥转换为字节
hex_key = '42656E65746563684031323334353637'
aes_key = bytes.fromhex(hex_key)

print(f"密钥长度: {len(aes_key)} 字节")
print(f"AES密钥 (Base64): {base64.b64encode(aes_key).decode('utf-8')}")

if len(aes_key) != 16:
    raise ValueError("AES-128密钥必须是16字节长度")

# 预先查询基础数据
try:
    l_d_ = Sqlserver_PO.select("select * from SYS_PROVINCE_CITY") or []
    l_d_city = Sqlserver_PO.select("select * from SYS_PROVINCE_CITY_AREA") or []
    l_d_nation = Sqlserver_PO.select(
        "select DICT_LABEL, DICT_VALUE from SYS_DICT_DATA where DICT_TYPE='sys_common_nation'") or []
    l_d_marriage = Sqlserver_PO.select(
        "select DICT_LABEL, DICT_VALUE from SYS_DICT_DATA where DICT_TYPE='patient_marriage'") or []
    l_d_id_type = Sqlserver_PO.select(
        "select DICT_LABEL, DICT_VALUE from SYS_DICT_DATA where DICT_TYPE='patient_id_type'") or []
except Exception as e:
    print(f"查询基础数据失败: {e}")
    l_d_ = []
    l_d_city = []
    l_d_nation = []
    l_d_marriage = []
    l_d_id_type = []

# 提供默认数据
if not l_d_:
    l_d_ = [{'PROVINCECODE': '000000', 'NAME': '未知省份'}]

if not l_d_city:
    l_d_city = [{'CITYCODE': '000000', 'NAME': '未知城市', 'CODE': '000000'}]

if not l_d_nation:
    l_d_nation = [{'DICT_LABEL': '中国', 'DICT_VALUE': '1'}]

if not l_d_marriage:
    l_d_marriage = [{'DICT_LABEL': '未婚', 'DICT_VALUE': '1'}]

if not l_d_id_type:
    l_d_id_type = [{'DICT_LABEL': '身份证', 'DICT_VALUE': '1'}]

for i in range(5):
    print(f"正在处理第 {i + 1} 条记录...")

    # 身份证，出生日期，年龄，性别
    d_gender = {'男': 0, '女': 1}
    idcard = Data_PO.getIdCard()
    t_birthday = Data_PO.getBirthday(idcard)
    birthday = t_birthday[0] + "-" + t_birthday[1] + "-" + t_birthday[2]
    age = Data_PO.getAge(idcard)
    sex = Data_PO.getSex(idcard)

    # 随机选择基础数据
    try:
        random_province = random.choice(l_d_) if l_d_ else {'PROVINCECODE': '000000', 'NAME': '未知省份'}
        random_city = random.choice(l_d_city) if l_d_city else {'CITYCODE': '000000', 'NAME': '未知城市', 'CODE': '000000'}
        random_nation = random.choice(l_d_nation) if l_d_nation else {'DICT_LABEL': '中国', 'DICT_VALUE': '1'}
        random_marriage = random.choice(l_d_marriage) if l_d_marriage else {'DICT_LABEL': '未婚', 'DICT_VALUE': '1'}
        random_id_type = random.choice(l_d_id_type) if l_d_id_type else {'DICT_LABEL': '身份证', 'DICT_VALUE': '1'}
    except Exception as e:
        print(f"选择基础数据失败: {e}")
        continue

    # 职业和关系人
    random_job = random.choice(["工程师", "服务人员", "技术人员", "老师", "军人", "学生"])
    random_relation = random.choice(["同事", "子女", "代理人", "监护人", "其他", "父母", "祖父母", "兄弟姐妹"])

    # 加密字段 (使用GBK编码)
    # 姓名
    random_name = Data_PO.getChineseName()
    random_name_encrypted = aes_encrypt(random_name.encode('GBK'), aes_key)

    # 随机地址
    random_address = random.choice(["南京路100号", "中山路11号", "复兴路44号", "东方路10号", "七浦路89号", "鲁班路54号"])
    random_address_encrypted = aes_encrypt(random_address.encode('GBK'), aes_key)

    # 手机
    random_phone = Data_PO.getPhone()
    random_phone_encrypted = aes_encrypt(random_phone.encode('GBK'), aes_key)

    # 构建SQL语句 - 使用参数化查询插入数据
    sql = '''INSERT INTO CDRD_PATIENT_INFO(
            PATIENT_NAME,
            PATIENT_SEX_KEY,
            PATIENT_SEX_VALUE,
            PATIENT_BIRTH_DATE,
            PATIENT_AGE,
            PATIENT_BIRTH_ADDRESS_PROVINCE_KEY,
            PATIENT_BIRTH_ADDRESS_PROVINCE,
            PATIENT_BIRTH_ADDRESS_CITY_KEY,
            PATIENT_BIRTH_ADDRESS_CITY,
            PATIENT_BIRTH_ADDRESS_COUNTRY_KEY,
            PATIENT_BIRTH_ADDRESS_COUNTRY,
            PATIENT_COUNTRY,
            PATIENT_NATIVE_PROVINCE_KEY,
            PATIENT_NATIVE_PROVINCE,
            PATIENT_NATIVE_CITY_KEY,
            PATIENT_NATIVE_CITY,
            PATIENT_NATION_KEY,
            PATIENT_NATION_VALUE,
            PATIENT_PROFESSION,
            PATIENT_MARRIAGE_KEY,
            PATIENT_MARRIAGE_VALUE,
            PATIENT_ID_TYPE_KEY,
            PATIENT_ID_TYPE_VALUE,
            PATIENT_ACCOUNT_ADDRESS,
            PATIENT_CONTACT_RELATION,
            PATIENT_UPDATE_TIME,
            PATIENT_DATA_SOURCE_KEY,
            PATIENT_SOURCE_ID,
            PATIENT_PHONE_NUM,
            PATIENT_HOME_ADDRESS,
            PATIENT_ID_NUM,
            PATIENT_HOME_PHONE,
            PATIENT_CONTACT_PHONE,
            PATIENT_CONTACT_ADDRESS,
            PATIENT_CONTACT_NAME
        ) values(
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )'''

    # 参数列表
    params = (
        random_name,  # PATIENT_NAME
        d_gender[sex],  # PATIENT_SEX_KEY
        sex,  # PATIENT_SEX_VALUE
        birthday,  # PATIENT_BIRTH_DATE
        age,  # PATIENT_AGE
        random_province.get('PROVINCECODE', '000000'),  # PATIENT_BIRTH_ADDRESS_PROVINCE_KEY
        random_province.get('NAME', '未知省份'),  # PATIENT_BIRTH_ADDRESS_PROVINCE
        random_city.get('CITYCODE', '000000'),  # PATIENT_BIRTH_ADDRESS_CITY_KEY
        random_city.get('NAME', '未知城市'),  # PATIENT_BIRTH_ADDRESS_CITY
        random_city.get('CODE', '000000'),  # PATIENT_BIRTH_ADDRESS_COUNTRY_KEY
        random_city.get('NAME', '未知城市'),  # PATIENT_BIRTH_ADDRESS_COUNTRY
        '中国',  # PATIENT_COUNTRY
        random_province.get('PROVINCECODE', '000000'),  # PATIENT_NATIVE_PROVINCE_KEY
        random_province.get('NAME', '未知省份'),  # PATIENT_NATIVE_PROVINCE
        random_city.get('CITYCODE', '000000'),  # PATIENT_NATIVE_CITY_KEY
        random_city.get('NAME', '未知城市'),  # PATIENT_NATIVE_CITY
        random_nation.get('DICT_VALUE', '1'),  # PATIENT_NATION_KEY
        random_nation.get('DICT_LABEL', '中国'),  # PATIENT_NATION_VALUE
        random_job,  # PATIENT_PROFESSION
        random_marriage.get('DICT_VALUE', '1'),  # PATIENT_MARRIAGE_KEY
        random_marriage.get('DICT_LABEL', '未婚'),  # PATIENT_MARRIAGE_VALUE
        random_id_type.get('DICT_VALUE', '1'),  # PATIENT_ID_TYPE_KEY
        random_id_type.get('DICT_LABEL', '身份证'),  # PATIENT_ID_TYPE_VALUE
        random_address,  # PATIENT_ACCOUNT_ADDRESS
        random_relation,  # PATIENT_CONTACT_RELATION
        Time_PO.getDateTimeByPeriod(0),  # PATIENT_UPDATE_TIME
        '1',  # PATIENT_DATA_SOURCE_KEY
        '',  # PATIENT_SOURCE_ID
        random_phone_encrypted,  # PATIENT_PHONE_NUM (二进制数据流)
        random_address_encrypted,  # PATIENT_HOME_ADDRESS (二进制数据流)
        idcard,  # PATIENT_ID_NUM
        random_phone_encrypted,  # PATIENT_HOME_PHONE (二进制数据流)
        random_phone_encrypted,  # PATIENT_CONTACT_PHONE (二进制数据流)
        random_address_encrypted,  # PATIENT_CONTACT_ADDRESS (二进制数据流)
        random_name_encrypted  # PATIENT_CONTACT_NAME (二进制数据流)
    )

    # 插入数据到表中
    try:
        Sqlserver_PO.execute2(sql, params)
        print(f"第 {i + 1} 条记录插入成功")

        # 验证插入的数据
        print(f"  姓名: {random_name}")
        print(f"  加密姓名长度: {len(random_name_encrypted)} 字节")
        print(f"  加密手机长度: {len(random_phone_encrypted)} 字节")
        print(f"  加密地址长度: {len(random_address_encrypted)} 字节")

    except Exception as e:
        print(f"第 {i + 1} 条记录插入失败: {e}")
        print(f"错误详情: {type(e).__name__}: {e}")

# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-8-6
# Description   : 生成CDRD_PATIENT_INFO AES-128 数据
# *********************************************************************

import pyodbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from PO.SqlserverPO import *
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_PT", "UTF-8")

from PO.DataPO import *
from PO.TimePO import *
Data_PO = DataPO()
Time_PO = TimePO()


def aes_encrypt_with_hex_key(data):
    """使用AES-128 ECB模式和十六进制密钥加密数据"""
    # 将十六进制密钥转换为字节
    key = bytes.fromhex("42656E65746563684031323334353637")

    if len(key) != 16:
        raise ValueError("AES-128需要16字节的密钥")

    # 将数据转换为字节
    data_bytes = data.encode('utf-8')

    # 初始化加密器
    cipher = AES.new(key, AES.MODE_ECB)

    # 对数据进行填充
    padded_data = pad(data_bytes, AES.block_size)

    # 加密
    encrypted_data = cipher.encrypt(padded_data)

    return encrypted_data



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

    # 加密字段
    # 姓名
    random_name = Data_PO.getChineseName()
    random_name_encrypted = aes_encrypt_with_hex_key(random_name)

    # 随机地址
    random_address = random.choice(["南京路100号", "中山路11号", "复兴路44号", "东方路10号", "七浦路89号", "鲁班路54号"])
    random_address_encrypted = aes_encrypt_with_hex_key(random_address)

    # 手机
    random_phone = Data_PO.getPhone()
    random_phone_encrypted = aes_encrypt_with_hex_key(random_phone)


    # 构建SQL语句
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

    # 参数列表 - 明文字段使用字符串，加密字段使用二进制数据
    params = (
        random_name,  # PATIENT_NAME (字符串)
        d_gender[sex],  # PATIENT_SEX_KEY (数字)
        sex,  # PATIENT_SEX_VALUE (字符串)
        birthday,  # PATIENT_BIRTH_DATE (字符串)
        age,  # PATIENT_AGE (数字)
        random_province.get('PROVINCECODE', '000000'),  # PATIENT_BIRTH_ADDRESS_PROVINCE_KEY (字符串)
        random_province.get('NAME', '未知省份'),  # PATIENT_BIRTH_ADDRESS_PROVINCE (字符串)
        random_city.get('CITYCODE', '000000'),  # PATIENT_BIRTH_ADDRESS_CITY_KEY (字符串)
        random_city.get('NAME', '未知城市'),  # PATIENT_BIRTH_ADDRESS_CITY (字符串)
        random_city.get('CODE', '000000'),  # PATIENT_BIRTH_ADDRESS_COUNTRY_KEY (字符串)
        random_city.get('NAME', '未知城市'),  # PATIENT_BIRTH_ADDRESS_COUNTRY (字符串)
        '中国',  # PATIENT_COUNTRY (字符串)
        random_province.get('PROVINCECODE', '000000'),  # PATIENT_NATIVE_PROVINCE_KEY (字符串)
        random_province.get('NAME', '未知省份'),  # PATIENT_NATIVE_PROVINCE (字符串)
        random_city.get('CITYCODE', '000000'),  # PATIENT_NATIVE_CITY_KEY (字符串)
        random_city.get('NAME', '未知城市'),  # PATIENT_NATIVE_CITY (字符串)
        random_nation.get('DICT_VALUE', '1'),  # PATIENT_NATION_KEY (字符串)
        random_nation.get('DICT_LABEL', '中国'),  # PATIENT_NATION_VALUE (字符串)
        random_job,  # PATIENT_PROFESSION (字符串)
        random_marriage.get('DICT_VALUE', '1'),  # PATIENT_MARRIAGE_KEY (字符串)
        random_marriage.get('DICT_LABEL', '未婚'),  # PATIENT_MARRIAGE_VALUE (字符串)
        random_id_type.get('DICT_VALUE', '1'),  # PATIENT_ID_TYPE_KEY (字符串)
        random_id_type.get('DICT_LABEL', '身份证'),  # PATIENT_ID_TYPE_VALUE (字符串)
        random_address,  # PATIENT_ACCOUNT_ADDRESS (字符串)
        random_relation,  # PATIENT_CONTACT_RELATION (字符串)
        Time_PO.getDateTimeByPeriod(0),  # PATIENT_UPDATE_TIME (字符串)
        '1',  # PATIENT_DATA_SOURCE_KEY (字符串)
        '0',  # PATIENT_SOURCE_ID (字符串)
        pyodbc.Binary(random_phone_encrypted),   # (二进制数据流)
        pyodbc.Binary(random_address_encrypted),
        idcard,  # PATIENT_ID_NUM (字符串)
        pyodbc.Binary(random_phone_encrypted),
        pyodbc.Binary(random_phone_encrypted),
        pyodbc.Binary(random_address_encrypted),
        pyodbc.Binary(random_name_encrypted)
    )

    # 插入数据到表中
    try:
        Sqlserver_PO.execute2(sql, params)
        # print(f"第 {i + 1} 条记录插入成功")
        # print(f"  姓名: {random_name}")
    except Exception as e:
        print(f"第 {i + 1} 条记录插入失败: {e}")

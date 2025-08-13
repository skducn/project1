# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-8-6
# Description   : set 创建CDRD_PATIENT_INFO
# *********************************************************************

from PO.SqlserverPO import *
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "UTF-8")
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_PT", "GBK")

# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")

import random


from PO.DataPO import *
Data_PO = DataPO()

from PO.TimePO import *
Time_PO = TimePO()

from Crypto.Cipher import AES
import binascii

def aes128_ecb_encrypt(plaintext, key_hex):
    """
    使用AES128-ECB模式加密数据
    :param plaintext: 要加密的明文
    :param key_hex: 16进制密钥字符串
    :return: 加密后的二进制数据
    """
    # 将16进制密钥转换为字节
    key = binascii.unhexlify(key_hex)

    # 初始化AES加密器(ECB模式不需要IV)
    cipher = AES.new(key, AES.MODE_ECB)

    # 对明文进行PKCS7填充（ECB模式仍需要块对齐）
    padding_length = AES.block_size - (len(plaintext.encode('utf-8')) % AES.block_size)
    padded_plaintext = plaintext.encode('utf-8') + bytes([padding_length]) * padding_length

    # 加密并返回结果
    return cipher.encrypt(padded_plaintext)

# 16进制密钥（16字节，AES128要求）
key_hex = "42656E65746563684031323334353637"

    #         encrypted_data = aes128_ecb_encrypt(plaintext, key_hex)





for _ in range(5):
    # 身份证，出生日期，年龄，性别
    d_gender = {'男': 0, '女': 1}
    idcard = Data_PO.getIdCard()
    t_birthday = Data_PO.getBirthday(idcard)
    birthday = t_birthday[0] + "-" + t_birthday[1] + "-" + t_birthday[2]
    age = Data_PO.getAge(idcard)
    sex = Data_PO.getSex(idcard)
    # 省份
    l_d_ = Sqlserver_PO.select("select * from SYS_PROVINCE_CITY")
    random_province_seq = random.randint(1, len(l_d_)-1)
    # print(l_d_[random_province_seq])
    # print(l_d_[random_province_seq]['PROVINCECODE'])
    # sys.exit(0)

    # 城市
    l_d_city = Sqlserver_PO.select("select * from SYS_PROVINCE_CITY_AREA where PROVINCECODE=%s" % (l_d_[random_province_seq]['PROVINCECODE']))
    random_city_seq = random.randint(1, len(l_d_city)-1)
    # print(l_d_city)
    # sys.exit(0)
    # 国籍
    l_d_nation = Sqlserver_PO.select(
        "select DICT_LABEL, DICT_VALUE from SYS_DICT_DATA where DICT_TYPE='sys_common_nation'")
    random_nation_seq = random.randint(1, 56-1)
    # 职业
    random_job = random.choice(["工程师", "服务人员", "技术人员", "老师", "军人", "学生"])
    # 婚姻
    l_d_marriage = Sqlserver_PO.select(
        "select DICT_LABEL, DICT_VALUE from SYS_DICT_DATA where DICT_TYPE='patient_marriage'")
    random_marriage_seq = random.randint(1, len(l_d_marriage)-1)
    # 身份
    l_d_id_type = Sqlserver_PO.select(
        "select DICT_LABEL, DICT_VALUE from SYS_DICT_DATA where DICT_TYPE='patient_id_type'")
    random_id_type_seq = random.randint(1, len(l_d_id_type)-1)
    # 随机关系人
    random_relation = random.choice(["同事", "子女", "代理人", "监护人", "其他", "父母", "祖父母", "兄弟姐妹"])

    # 加密
    # 姓名
    random_name = Data_PO.getChineseName()
    # data_to_encrypt = random_name.encode('utf-8')
    # data_to_encrypt = random_name.encode('GBK')
    random_name_encrypted  = aes128_ecb_encrypt(random_name, key_hex)
    # random_name_d = aes_decrypt(random_name_encrypted, aes_key)

    # 随机地址
    random_address = random.choice(["南京路100号", "中山路11号", "复兴路44号", "东方路10号", "七浦路89号", "鲁班路54号"])
    # data_to_encrypt = random_address.encode('utf-8')
    # data_to_encrypt = random_address.encode('GBK')
    random_address_encrypted = aes128_ecb_encrypt(random_address, key_hex)
    # random_address_d = aes_decrypt(random_address_encrypted, aes_key)

    # 手机
    random_phone = Data_PO.getPhone()
    # data_to_encrypt = random_phone.encode('utf-8')
    # data_to_encrypt = random_phone.encode('GBK')
    random_phone_encrypted = aes128_ecb_encrypt(random_phone, key_hex)

    # random_phone_d = aes_decrypt(random_phone_encrypted, aes_key)

    # # 将二进制数据转换为十六进制字符串
    # random_phone_encrypted_hex = "0x" + random_phone_encrypted.hex()
    # random_address_encrypted_hex = "0x" + random_address_encrypted.hex()
    # random_name_encrypted_hex = "0x" + random_name_encrypted.hex()


    sql = f'''INSERT INTO CDRD_PATIENT_INFO(
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
        '{Data_PO.getChineseName()}',
        '{d_gender[sex]}',
        '{sex}',
        '{birthday}',
        '{age}',
        '{l_d_[random_province_seq]['PROVINCECODE']}',
        '{l_d_[random_province_seq]['NAME']}',
        '{l_d_city[random_city_seq]['CITYCODE']}',
        '{l_d_city[random_city_seq]['NAME']}',
        '{l_d_city[random_city_seq]['CODE']}',
        '{l_d_city[random_city_seq]['NAME']}',
        N'中国',
        '{l_d_[random_province_seq]['PROVINCECODE']}',
        '{l_d_[random_province_seq]['NAME']}',
        '{l_d_city[random_city_seq]['CITYCODE']}',
        '{l_d_city[random_city_seq]['NAME']}',
        '{l_d_nation[random_nation_seq]['DICT_VALUE']}',
        '{l_d_nation[random_nation_seq]['DICT_LABEL']}',
        '{random_job}',
        '{l_d_marriage[random_marriage_seq]['DICT_VALUE']}',
        '{l_d_marriage[random_marriage_seq]['DICT_LABEL']}',
        '{l_d_id_type[random_id_type_seq]['DICT_VALUE']}',
        '{l_d_id_type[random_id_type_seq]['DICT_LABEL']}',
        '{random_address}',
        '{random_relation}',
        '{Time_PO.getDateTimeByPeriod(0)}',
        '1',
        '',
        random_phone_encrypted,       
        random_address_encrypted,     
        idcard,                       
        random_phone_encrypted,       
        random_phone_encrypted,       
        random_address_encrypted,     
        random_name_encrypted         
    )'''

        # 插入加密后的数据到表中
    Sqlserver_PO.execute(sql)


# {random_phone_encrypted_hex},
# {random_address_encrypted_hex},
# '{idcard}',
# {random_phone_encrypted_hex},
# {random_phone_encrypted_hex},
# {random_address_encrypted_hex},
# {random_name_encrypted_hex}
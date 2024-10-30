#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Project  :app0415
# @File     :todo.py
# @Time     :2024/4/15 19:46
# @Author   :wangting_666


from typing import List, Optional
from pydantic import BaseModel
import pymssql

# MySQL连接配置
config = {
    'host': '192.168.0.234',
    'user': 'sa',
    'password': 'Zy_123456789',
    'database': 'CHC',
    'charset': 'GBK',
    'as_dict': True,
    'tds_version': "7.3",
    'autocommit': True
}


# 连接到MySQL数据库
def connect_to_sqlserver():
    return pymssql.connect(**config)


# 定义WowInfo模型
class WowInfo(BaseModel):
    id: int
    role: str
    role_cn: str
    role_pinyin: str
    zhuangbei: str
    tianfu: str


# 获取所有魔兽职业信息
def get_wowinfo_all() -> List[WowInfo]:
    try:
        conn = connect_to_sqlserver()
        cur = conn.cursor()
        cur.execute("SELECT * FROM a_api_wow_info")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"查不到职业信息: {e}")
        return []


# 获取单个魔兽职业信息
def get_wowinfo(role: str) -> Optional[WowInfo]:
    try:
        conn = connect_to_sqlserver()
        cur = conn.cursor()
        cur.execute("SELECT * FROM a_api_wow_info WHERE role = '%s'" % (role))
        result = cur.fetchone()
        return WowInfo(**result) if result else None
    except Exception as e:
        print(f"查不到职业信息: {e}")
        return None


# 创建魔兽职业信息 (测试失败insert into)
def create_wowinfo(wowinfo: WowInfo) -> WowInfo:
    try:
        conn = connect_to_sqlserver()
        cur = conn.cursor()
        cur.execute("INSERT INTO a_api_wow_info VALUES (wowinfo.id, wowinfo.role, wowinfo.role_cn, wowinfo.role_pinyin, wowinfo.zhuangbei, wowinfo.tianfu)")
        conn.commit()
        return wowinfo
        # with conn.cursor() as cursor:
        #     cursor.execute(
        #         "INSERT INTO a_api_wow_info (id,role, role_cn,role_pinyin,zhuangbei,tianfu) VALUES (%s, %s, %s,%s,%s,%s)",
        #         (wowinfo.id, wowinfo.role, wowinfo.role_cn, wowinfo.role_pinyin, wowinfo.zhuangbei, wowinfo.tianfu))
        #     conn.commit()
        # return wowinfo
    except Exception as e:
        print(f"创建职业信息失败: {e}")
        return None


# 更新魔兽职业信息
def update_wowinfo(id: int, wowinfo: WowInfo) -> Optional[WowInfo]:
    try:
        conn = connect_to_sqlserver()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE a_api_wow_info SET role=%s, role_cn=%s, role_pinyin=%s,zhuangbei=%s,tianfu=%s WHERE id=%s",
                           (wowinfo.role, wowinfo.role_cn, wowinfo.role_pinyin, wowinfo.zhuangbei, wowinfo.tianfu, id))
            conn.commit()
        return wowinfo
    except Exception as e:
        print(f"更新职业信息失败: {e}")
        return None


# 删除魔兽职业信息
def delete_wowinfo(id: int) -> bool:
    try:
        conn = connect_to_sqlserver()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM a_api_wow_info WHERE id = %s", (id,))
            conn.commit()
        return True
    except Exception as e:
        print(f"删除职业信息失败: {e}")
        return False

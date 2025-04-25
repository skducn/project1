# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 请求体
# friends: List[int] 表示接收的列表元素都是int类型
# async def data(user: User): 异步请求，将User实例化为user，这个过程是将User（是json）解析成字典，赋值给user。
# return user，对user对象进行json序列化成字典，返回给客户端。
# age: int = Field(default=0, gt=0, lt=100) 范围约束，表示默认值0，传入的值大于0，小于等于100，如果不符合，则抛出异常。
# Field(regex='^a') 正则校验数据
# https://www.bilibili.com/video/BV1Ya4y1D7et?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=16

# *****************************************************************
from fastapi import APIRouter
from typing import Union, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List

app03 = APIRouter()

# 嵌套
class Addr(BaseModel):
    province: str
    city: str


class User(BaseModel):
    # name: str = Field(regex='^a')
    name: str
    age: int = Field(default=0, gt=0, lt=100)
    birth: Union[date, None] = None
    friends: List[int]
    description: Optional[str] = None
    addr: Addr   # //嵌套

    # 对name进行校验，必须是字母
    @field_validator("name")   # cls是类对象，value是name的值
    def name_must_alpha(cls, value):
        assert value.isalpha(), "name must be alpha"
        return value

# 嵌套对象，把user字典作为列表嵌套到data
class Data(BaseModel):
    data:List[User]

@app03.post("/user")
async def user(user: User):
    print(user, type(user))
    print(user.name, user.birth)
    print(user.dict())
    return user


@app03.post("/data")
async def data(data: Data):
    return data
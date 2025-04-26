# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 响应模型
# https://www.bilibili.com/video/BV1Ya4y1D7et?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=21
# @app07.post("/user02",response_model=UserOut) 这个是路径操作，响应模型是路径操作中的第二参数。
# async def create_user(user: UserIn): 这个是路径函数，user是路径函数的参数
# *****************************************************************
from fastapi import APIRouter, Form, File, UploadFile, Request
from typing import Union, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List
from pydantic import BaseModel, EmailStr

import os
app07 = APIRouter()


class UserIn(BaseModel):
    username:str
    password:str
    email: EmailStr
    fullname : Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    fullname: Optional[str] = None

@app07.post("/user02",response_model=UserOut)
async def create_user(user: UserIn):
    return user

# 逻辑：对UserIn进行数据校验，然后赋值给user（实例），return user 再到中响应模型（UserOut类）进行过滤，输出符合条件的内容。
# 所以最后输出的内容中没有 password:str ， 所user要按照UserOut模型做序列化。

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []

items = {
"foo": {"name": "Foo", "price": 50.2},
"bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
"baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []}
}

#  response_model_exclude_unset=True 表示数据中没有赋值的字段不返回。
#  如只有response_model=Item，则默认返回5个值，即使foo参数只有name和price，结果也返回5个，其他3个默认值。
# 使用response_model_exclude_unset=True ，使用参数foo，结果返回2个值。
# 除此之外，还有response_model_exclude_defaults=True，表示默认值不返回。 response_model_exclude_none=True，表示None值不返回。
# response_model_include={'name','price'} 表示结果只要name和price

# 输入foo，输出name和price
@app07.get("/response_model_exclude_unset/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def response_model_exclude_unset(item_id: str):
    return items[item_id]

# 输入bar，输出name和price
@app07.get("/response_model_include/{item_id}", response_model=Item, response_model_include={'name','price'})
async def response_model_include(item_id: str):
    return items[item_id]

# 输入foo，输出name
@app07.get("/response_model_exclude/{item_id}", response_model=Item, response_model_exclude_unset=True, response_model_exclude={'price'})
async def response_model_exclude(item_id: str):
    return items[item_id]
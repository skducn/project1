# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 请求体
# https://www.bilibili.com/video/BV1Ya4y1D7et?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=16
#
# /application/x-www-form-urlencoded
# https://www.bilibili.com/video/BV1Ya4y1D7et?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=21
# *****************************************************************
from fastapi import APIRouter, Form, File, UploadFile, Request
from typing import Union, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List

import os
app07 = APIRouter()
from pydantic import BaseModel


class UserIn(BaseModel):
    username:str
    password:str
    email: EmailStr
    fullname : Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    fullname: Optional[str] = None

@app07.post("/user",response_model=UserOut)
async def create_user(user: UserIn):
    return user


# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 请求体
# https://www.bilibili.com/video/BV1Ya4y1D7et?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=16
#
# /application/x-www-form-urlencoded

# *****************************************************************
from fastapi import APIRouter, Form
from typing import Union, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List


app04 = APIRouter()
@app04.post("/regin")
async def region(username:str=Form(), password:str=Form()):
    print(f"username:{username}, password:{password}")
    return {
        "username": username
    }


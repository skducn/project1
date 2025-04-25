# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 请求体
# https://www.bilibili.com/video/BV1Ya4y1D7et?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=16
#
# /application/x-www-form-urlencoded

# *****************************************************************
from fastapi import APIRouter, Form, File, UploadFile, Request
from typing import Union, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List

import os
app06 = APIRouter()


@app06.post("/request")
async def request(request: Request):
    print(f"url:{request.url}")
    print(f"客户ip:{request.client.host}")
    print(f"客户宿主:{request.headers.get('user-agent')}")
    print(f"客户cookies:{request.cookies}")
    return {
        "url": request.url,
        "客户ip": request.client.host,
        "客户宿主": request.headers.get('user-agent'),
        "客户cookies": request.cookies
    }


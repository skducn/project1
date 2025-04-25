# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 请求体
# https://www.bilibili.com/video/BV1Ya4y1D7et?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=16
#
# /application/x-www-form-urlencoded

# *****************************************************************
from fastapi import APIRouter, Form, File, UploadFile
from typing import Union, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List

import os
app05 = APIRouter()

# 上传一个文件，适用于小文件
@app05.post("/file")
async def file(file: bytes = File()):
    print(f"file:{file}")
    return {
        "file": len(file)
    }

# 上传多个文件，并输出数量及每个文件的大小，适用于小文件
@app05.post("/files")
async def files(files: list[bytes] = File()):
    print(f"files:{files}")
    for f in files:
        print(len(f))  # 获取每个文件的大小
    return {
        "files": len(files)   # 获取文件数量
    }

# 通过文件句柄实现, 1个文件，将文件上传到本地imgs中。
@app05.post("/uploadfile")
async def uploadfile(file: UploadFile):

    p = os.path.join("imgs", file.filename)

    with open(p, "wb") as f:
        for line in file.file:
            f.write(line)

    print(f"files:{file}")  # files:UploadFile(filename='16.jpg', size=355385, headers=Headers({'content-disposition': 'form-data; name="file"; filename="16.jpg"', 'content-type': 'image/jpeg'}))
    return {
        "file": file.filename  # 获取文件名
    }

# 通过文件句柄实现, N个文件，将文件上传到本地imgs中。
@app05.post("/uploadfiles")
async def uploadfiles(uploadfiles: list[UploadFile] ):
    # print(f"files:{uploadfiles}")

    return {
        "name": [file.filename for file in uploadfiles]
    }
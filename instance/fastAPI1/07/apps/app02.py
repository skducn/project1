# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: fastAPI 实例
# uvicorn test1:app --reload
# 路径参数path，查询参数query
# Union 是当有多种可能的数据类型时使用，比如函数有可能根据不同情况有时返回 str 或返回 list，那么就可以写成 Union [list, str]
# Optional 是 Union 的一个简化，当 数据类型中有可能是 None 时，比如有可能是 str 也有可能是 None，则 Optional [str]，相当于 Union [str, None]
# 如：xl: Union[str, None] 表示 xl参数既可以是str类型也可以是None
# *****************************************************************
from fastapi import APIRouter
from typing import Union, Optional

app02 = APIRouter()

# xl,gj可以设置默认值，如果没有默认值则是必填项。
@app02.get("/jobs/{kd}")
async def get_jobs(kd, xl: Union[str, None] = None, gj:Optional[str] = None):

    return {
        "kd": kd,
        "xl": xl,
        "gj": gj}


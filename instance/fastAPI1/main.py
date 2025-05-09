# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: fastAPI 实例
# uvicorn test1:app --reload
# uvicorn相当于封装了一个socket，将浏览器的请求发到uvicorn后，再转发web应用app上
# (py310) localhost-2:fastAPI1 linghuchong$ uvicorn test1:app --reload
# INFO:     Will watch for changes in these directories: ['/Users/linghuchong/Downloads/51/Python/project/instance/fastAPI1']
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [48850] using StatReload
# INFO:     Started server process [48852]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.

# Swagger UI: http://127.0.0.1:8001/docs
# ReDoc: http://127.0.0.1:8001/redoc

# include_router 将不同子应用的路由进行分发和解耦
# *****************************************************************
from fastapi import FastAPI
from apps.app01.urls import shop
from apps.app02.urls import user

# app = FastAPI()
# 返回交互式API文档
app = FastAPI(docs_url="/docs", redoc_url="/redoc")

app.include_router(shop, prefix="/shop", tags=['购物中心接口'])
app.include_router(user, prefix="/user", tags=['用户接口'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
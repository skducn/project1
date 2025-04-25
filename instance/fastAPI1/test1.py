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

# app = FastAPI()
# 返回交互式API文档
app = FastAPI(docs_url="/docs", redoc_url="/redoc")

@app.get("/")
def home():
    return {"Hello": "World123"}

@app.get("/shop")
async def shop():
    return {"shop": "ttttttt"}

@app.post("/items", tags=['这是一个items接口'], summary='关于items的summary', description='关于items的description',
          response_description="返回值的descrpition", deprecated=True)
async def itmes():
    return {"shop": "13123"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test1:app", host="127.0.0.1", port=8001, reload=True)
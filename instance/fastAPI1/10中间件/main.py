# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import Response, PlainTextResponse
app = FastAPI()
import time

# 执行顺序是，从下往上。所以先执行m1，在执行m2

# 声明中间件的装饰器
@app.middleware("http")
async def m2(request:Request, call_next):
    # 请求代码块
    print("m2 request")
    response = await call_next(request)
    response.headers['author'] = 'jin'
    # 响应代码块
    print("m2 response")
    return response

# 声明中间件的装饰器
@app.middleware("http")
async def m1(request:Request, call_next):
    # 请求代码块
    print("m1 request")

    # ip拦截
    # if request.client.host in ['127.0.0.1',  ]:
    #     # return Response("你无权访问")
    #     return PlainTextResponse("你无权访问", status_code=403, media_type="text/plain; charset=utf-8")

    # 权限设置，拦截/user请求
    # if request.url.path in ["/user"]:
    #     return PlainTextResponse("你无权访问", status_code=403, media_type="text/plain; charset=utf-8")

    # 计算请求时间 end-start
    start =time.time()
    response = await call_next(request)

    # 响应代码块
    end = time.time()
    response.headers['ProcessTimer'] = str(end - start)
    print("m1 response", str(end - start))
    return response


@app.get("/user")
def get_user():
    time.sleep(3)
    print("getuser函数执行")
    return {
        "user": "current user"
    }

@app.get("/item/{item_id}")
def get_itme(item_id: int):
    time.sleep(2)

    print("getitem函数执行")

    return {
        "item_id": item_id
    }

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8020, reload=True, workers=1)
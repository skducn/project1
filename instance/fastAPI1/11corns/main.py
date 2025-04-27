# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import Response, PlainTextResponse
app = FastAPI()
import time

@app.get("/user")
def get_user():
    print("getuser函数执行")
    return {
        "user": "current user"
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8020, reload=True, workers=1)
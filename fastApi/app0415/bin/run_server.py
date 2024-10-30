#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Project  :app0415
# @File     :run_server.py
# @Time     :2024/4/15 19:46
# @Author   :wangting_666


import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

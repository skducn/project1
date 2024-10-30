#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Project  :app0415
# @File     :config.py
# @Time     :2024/4/15 19:46
# @Author   :wangting_666

# pip install -U pydantic
# pip install pydantic-settings

# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TodoApp"
    log_level: str = "INFO"


settings = Settings()

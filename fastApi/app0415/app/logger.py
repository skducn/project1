#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Project  :app0415
# @File     :logger.py
# @Time     :2024/4/15 19:46
# @Author   :wangting_666

import logging
from config.config import settings
import os

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(filename=os.path.join(log_dir, "app.log"), level=settings.log_level)
logger = logging.getLogger(__name__)

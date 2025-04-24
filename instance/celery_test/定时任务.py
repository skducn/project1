# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-18
# Description: # 定时任务
# 视频：https://www.bilibili.com/video/BV1bvPXeeEqL?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=8
# 步骤：在celery.py中设置定时任务，如下
# 1, 启动worker监控
# celery -A celeryPO worker -l info  //for mac
# celery -A celeryPO worker -l info -P eventlet   //for win
# 2，后台调用celery.py调用config.py
# ***************************************************************u**

import os

# 启动beat，提交定时任务
# 每隔3秒，beat负责向broker提交一个任务，worker执行任务
os.system('celery -A celeryPO.celery beat -l debug')
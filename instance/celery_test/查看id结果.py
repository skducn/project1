# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-18
# Description: # 获取结果
# 视频：https://www.bilibili.com/video/BV1bvPXeeEqL?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=8
# 步骤：
# 1，执行任务
# 2, 启动worker监控
# celery -A celeryPO worker -l info  //for mac
# celery -A celeryPO worker -l info -P eventlet   //for win
# 3, 提供任务id
# ***************************************************************u**
from celeryPO.celery import app
from celery.result import AsyncResult

id = 'ea1b2177-1ee4-451c-8497-cf2b5c4c9ea5'

if __name__ == '__main__':
    result = AsyncResult(id=id, app=app)
    if result.successful():
        result = result.get()
        print(result)
    elif result.failed():
        print('任务失败')
    elif result.status == 'PENDING':
        print('任务等待中被执行')
    elif result.status == 'RETRY':
        print('任务异常后正在重试')


# 步骤：
# 1、执行test_task
# 2、执行 celery -A clelryPO worker -l info
# 3、执行get_result  获取结果crawl_baidu()返回值

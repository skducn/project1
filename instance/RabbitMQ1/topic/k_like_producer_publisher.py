# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-18
# Description: # topic exchange 关键字模糊匹配之发布者
# 功能：发布者对模糊匹配成功的队列发送消息，消费者去消费。
# 视频：https://www.bilibili.com/video/BV1hS4y1R7f2?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=6
# ***************************************************************u**
import pika

# 有密码
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

# 工作原理：
# 1, 声明了一个exchange，指定topic类型
channel.exchange_declare(exchange='m3', exchange_type='topic')

# 2，发送消息到队列
# routing_key='old.alex', 对接收者1 k_like_consumer_subscriber1.py发送消息
# routing_key='old.alex.py', 对接收者2 k_like_consumer_subscriber2.py发送消息
message = 'Hello, RabbitMQ!'
channel.basic_publish(exchange='m3',
                      routing_key='old.alex.py',
                      body='x2'
                      )
print(f" [x] Sent555 '{message}'")

# 关闭连接
connection.close()
    
# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-18
# Description: # publish/Subscribe 发布者/订阅者
# 视频：https://www.bilibili.com/video/BV1hS4y1R7f2?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=4
# 步骤：
# 1，执行 k_like_consumer_subscriber1.py  订阅者1
# 2，执行 k_like_consumer_subscriber2.py  订阅者2
# 3，执行 producer_publisher.py  发布者，发布消息后订阅1和订阅者2都收到消息（消费）

# brew services start rabbitmq
# http://localhost:15672/#/queues  guest，guest
# ***************************************************************u**
import pika

# # 连接到 RabbitMQ 服务器
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()

# 有密码
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

# 1，声明exchange
channel.exchange_declare(exchange='m1', exchange_type='fanout')

# 2，发送消息到队列
message = 'Hello, RabbitMQ!'
channel.basic_publish(exchange='m1',
                      routing_key='',
                      body=message
                      )
print(f" [x] Sent '{message}'")

# 关闭连接
connection.close()
    
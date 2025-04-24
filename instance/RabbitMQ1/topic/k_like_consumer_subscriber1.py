# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-18
# Description: # topic exchange 关键字模糊匹配之接收者1, routing_key='old.*'
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

# 2, 随机生成一个队列queue
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 3, 让exchange和queue进行绑定，路由键为old.* ，表示命中old.后一个字符串，如 old.test, old.hello
channel.queue_bind(exchange='m3', queue=queue_name, routing_key='old.*')

# 4, 定义一个回调函数来处理接收到的消息
def callback(ch, method, properties, body):
    print(method.routing_key)
    print(f" [x] Received '{body.decode()}'")
    # int("213wqeqwe")
    # ch.basic_ack(delivery_tag=method.delivery_tag)


# 5，告诉 RabbitMQ 这个回调函数将从队列中接收消息
channel.basic_consume(queue=queue_name,
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')

# 6, 开始消费消息
channel.start_consuming()

import pika

# 连接到 RabbitMQ 服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明一个队列
channel.queue_declare(queue='hello')

# 定义一个回调函数来处理接收到的消息
def callback(ch, method, properties, body):
    print(f" [x] Received '{body.decode()}'")

# 告诉 RabbitMQ 这个回调函数将从队列中接收消息
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费消息
channel.start_consuming()
    
import pika
import sys

# 连接到 RabbitMQ 服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明一个直连交换机
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# 创建一个临时队列
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 获取要绑定的路由键
severities = sys.argv[1:]
if not severities:
    sys.stderr.write(f"Usage: {sys.argv[0]} [info] [warning] [error]\n")
    sys.exit(1)

# 绑定队列到交换机，并指定路由键
for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

# 定义一个回调函数来处理接收到的消息
def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body.decode()}")

# 告诉 RabbitMQ 这个回调函数将从队列中接收消息
channel.basic_consume(queue=queue_name,
                      auto_ack=True,
                      on_message_callback=callback)

# 开始消费消息
channel.start_consuming()
    
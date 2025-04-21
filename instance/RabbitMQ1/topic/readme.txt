# todo topic 关键字模糊匹配发布
参考：https://www.rabbitmq.com/tutorials/tutorial-five-python
视频：https://www.bilibili.com/video/BV1hS4y1R7f2?spm_id_from=333.788.videopod.episodes&vd_source=be21f48b876460dfe25064d745fdc372&p=6

# 启动服务， brew services start rabbitmq
# 后台查看， http://localhost:15672/#/queues  guest，guest

# todo 功能：发布者对模糊匹配成功的队列发送消息，消费者去消费。
# 步骤：
# 1，执行 k_like_consumer_subscriber1.py  订阅者1
# 2，执行 k_like_consumer_subscriber2.py  订阅者2
# 3，执行 producer_publisher.py  发布者
工作原理：发布者按照路由键规则发送消息到队列，消费者去消费。
exchange类型：exchange_type='topic'
路由键规则：routing_key='old.alex.py' ， 对应消费者路由键模糊设置 routing_key='old.#'
路由键规则：routing_key='old.alex' ， 对应消费者路由键模糊设置 routing_key='old.*'

总结：
topics是关键字模糊匹配发布/消费
exchagne是消息中间件，即生产者将消息发送到中间件后通过routing_key（过滤一下）将消息传递给与他关联的消息队列，消费者去消息队列中消费。
routing_key有三种：fanout、direct、topic

1，hello world
一个生产者对应一个消费者，没有exchange，即一个生产者、一个队列、一个消费者，用于一个人完成一件事。

2，work queue
一个生产者对应多个消费者，没有exchange，即一个生产者、一个队列、N个消费者，一般用于N个消费者去完成一个队列中的任务，共同完成同一件事。

3，publish/subscribe
一个生产者（发布者）对应一个exchange（消息中间件），即一个生产者、N个队列、N个消费者，一般用于通知群发所有消费者，即每个人完成各自队列中相同的任务。

4，routing
一个生产者（发布者）对应一个exchange（消息中间件），即一个生产者、N个队列、N个消费者，一般用于按照固定条件群发给不同的消费者，即每个人完成各自队列中不同的任务。

5，topic
一个生产者（发布者）对应一个exchange（消息中间件），即一个生产者、N个队列、N个消费者，一般用于按照模糊条件群发给不同的消费者，即每个人完成各自队列中不同的任务。



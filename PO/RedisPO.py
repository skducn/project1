# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2021-3-5
# Description: redis
# ***************************************************************

"""
1，获取所有的keys
2，获取指定长度的keys
"""

import redis


class RedisPO:
    def __init__(self, varHost, varPass, varPort, varDB, varDecode=False):
        self.r = redis.Redis(
            host=varHost,
            password=varPass,
            port=varPort,
            db=varDB,
            decode_responses=varDecode,
        )

    def getKeys(self, varType=0):

        """1，获取所有的keys"""

        list1 = []
        for i in self.r.keys():
            if varType == 0:
                list1.append(i)
            else:
                list1.append(str(i, encoding="utf-8"))
        return list1

    def getKeysBySize(self, varLen, varType=0):

        """2，获取指定长度的keys"""

        list1 = []
        for i in self.r.keys():
            if len(i) == varLen:
                if varType == 0:
                    list1.append(i)
                else:
                    list1.append(str(i, encoding="utf-8"))
        return list1


if __name__ == "__main__":

    # 命令行先执行：redis-server
    # redis-server --loglevel verbose  //启用 Redis 日志查看详细错误信息：

    # 测试连接
    #      redis-cli -h 127.0.0.1 -p 6379
    #      成功连接后可执行命令如 keys * 查看所有键


    # Redis_PO = RedisPO("192.168.0.213", "", 6379, 0, False)
    Redis_PO = RedisPO("127.0.0.1", "", 6379, 0, False)

    print("1，获取所有的keys".center(100, "-"))
    try:
        list1 = Redis_PO.getKeys()
        print(list1)
    except redis.ConnectionError as e:
        print(f"Redis 连接失败: {e}")

    print("2，获取指定长度的keys".center(100, "-"))
    list1 = Redis_PO.getKeysBySize(32)
    print(list1)
    list1 = Redis_PO.getKeysBySize(32, "str")
    print(list1)

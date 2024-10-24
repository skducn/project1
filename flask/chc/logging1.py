import logging1 as lg
import os


class logging_():
    def __init__(self,path, delete=True):
        self.path = path  # 日志文件存放位置
        name = 'log.log'  # 日志文件名称
        self.log_ = os.path.join(self.path, name)  # 进入文件目录
        if delete == True:
            open(f"{path}/{name}", "w").close  # 为True时清空文本

        # 创建一个日志处理器
        self.logger = lg.getLogger('logger')
        # 设置日志等级，低于设置等级的日志被丢弃
        self.logger.setLevel(lg.DEBUG)
        # 设置输出日志格式
        self.fmt = lg.Formatter("[%(asctime)s] - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
        # 创建一个文件处理器
        self.fh = lg.FileHandler(self.log_, encoding='utf-8')
        # 设置文件输出格式
        self.fh.setFormatter(self.fmt)
        # 将文件处理器添加到日志处理器中
        self.logger.addHandler(self.fh)
        # 创建一个控制台处理器
        self.sh = lg.StreamHandler()
        # 设置控制台输出格式
        self.sh.setFormatter(self.fmt)
        # 将控制台处理器添加到日志处理器中
        self.logger.addHandler(self.sh)

        # 关闭文件
        self.fh.close()


# 使用
if __name__ == '__main__':
    _path = os.path.dirname(__file__)  # 获取当前文件的路径
    lg = logging_(_path).logger  # 实例化封装类
    lg.info('1111')
    lg.debug('2222')
    lg.error('33333')
    lg.warning('44444')

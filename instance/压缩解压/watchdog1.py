# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2024-11-15
# Description: 压缩与解压
# 十个 Python文件压缩与解压实战技巧 http://www.51testing.com/html/43/n-7803343.html
# 使用watchdog库，我们可以创建一个脚本，实时监控指定文件夹，一旦有新文件添加，立即自动压缩。
# pip3 install watchdog
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import zipfile
import os
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        zip_name = os.path.splitext(event.src_path)[0] + '.zip'
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            zipf.write(event.src_path)
            print(f"{event.src_path} has been compressed to {zip_name}")

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/Users/linghuchong/Downloads/51/Python/project/PO/1', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
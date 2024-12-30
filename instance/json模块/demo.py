# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-12-29
# Description: 正则表达式
# http://www.51testing.com/html/80/15326880-7803906.html
# *****************************************************************

import json

# 使用 default 参数处理日期和时间对象。
from datetime import datetime
def json_default(value):
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"Type {type(value)} not serializable")
data = {
    "name": "Alice",
    "timestamp": datetime.now()
}
json_str = json.dumps(data, default=json_default)
print(json_str)  # {"name": "Alice", "timestamp": "2024-12-30T14:12:52.921283"}


# 使用 object_hook 参数自定义解码器。
def custom_decoder(obj):
    if 'timestamp' in obj:
        obj['timestamp'] = datetime.fromisoformat(obj['timestamp'])
    return obj
json_str = '{"name": "Alice", "timestamp": "2023-10-01T12:00:00"}'
data = json.loads(json_str, object_hook=custom_decoder)
print(data)  # 输出: {'name': 'Alice', 'timestamp': datetime.datetime(2023, 10, 1, 12, 0)}

# 列表格式化
data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]
json_str = json.dumps(data)
print(json_str) # [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]


# 字典中None转字符串后null
data = {
   "name": "Alice",
   "age": None
}
json_str = json.dumps(data)
print(json_str)  # 输出: {"name": "Alice", "age": null}


# 处理大文件
# 处理大文件时，使用流式处理。
# https://www.cnblogs.com/ellisonzhang/p/10273843.html 参考yield
import json
def read_large_json_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            yield data
for item in read_large_json_file('large_data.json'):
    print(item)







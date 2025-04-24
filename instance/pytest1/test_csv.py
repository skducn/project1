# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-4-7
# Description: 获取csv
# https://www.bilibili.com/video/BV1gB4y1v7Ki?spm_id_from=333.788.videopod.sections&vd_source=be21f48b876460dfe25064d745fdc372
#***************************************************************

import csv

def get_csv():
    with open('test.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

if __name__ == '__main__':
    get_csv()

# ['test', 'linux', '¥5000']
# ['百度', 'python', '$3000']
# ['百慕大', 'windows', '¥222']
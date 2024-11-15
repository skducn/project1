# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2024-11-15
# Description: 压缩与解压
# 十个 Python文件压缩与解压实战技巧 http://www.51testing.com/html/43/n-7803343.html
# 将大文件分割成多个ZIP分卷。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import zipfile

def split_large_file(zip_name, files_to_compress, max_size=1024*1024):  # 1MB per part
    with zipfile.ZipFile(zip_name + ".part01.zip", 'w') as zipf:
        for i, filename in enumerate(files_to_compress, start=1):
            if zipf.getinfo(filename).file_size > max_size:
                raise ValueError("File too large to split.")
            zipf.write(filename)
            if zipf.filesize > max_size:
                zipf.close()
                new_part_num = i // max_size + 1
                zip_name_new = zip_name + f".part{new_part_num:02d}.zip"
                with zipfile.ZipFile(zip_name_new, 'w') as new_zipf:
                    new_zipf.comment = zipf.comment
                    for j in range(i):
                        new_zipf.write(zip_name + f".part{j+1:02d}.zip")
                    new_zipf.write(filename)
                break
    print(f"{zip_name} split into parts successfully.")

split_large_file('/Users/linghuchong/Downloads/51/Python/project/PO/3/large_file.zip',['/Users/linghuchong/Downloads/51/Python/project/PO/3/test.pdf'])
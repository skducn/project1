# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2024-11-15
# Description: 压缩与解压
# 十个 Python文件压缩与解压实战技巧 http://www.51testing.com/html/43/n-7803343.html
# 在使用zipfile时，可以通过设置压缩级别来平衡压缩比和压缩速度。级别范围是0到9，0表示存储（不压缩），9表示最大压缩。
# 　　with zipfile.ZipFile('compressed.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
# 　　    zipf.write('file_to_compress.txt')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 　目标: 将多个文件或目录打包成一个ZIP文件。
import zipfile, os

# def create_zip(varZipName, varFilePath, l_files):
#     # 将文件压缩为zip
#     with zipfile.ZipFile(varZipName, 'w') as zipf:
#         os.chdir(varFilePath)
#         for file in l_files:
#             zipf.write(file)
#     print(f"{varZipName} created successfully.")
#
# # 将文件压缩为example.zip
# create_zip('/Users/linghuchong/Downloads/51/Python/project/PO/zip/example.zip', "/Users/linghuchong/Downloads/51/Python/project/PO/zip/", ['DomPO.py', 'DrissionPO.py'])


# def compress_directory(zip_name, directory):
#     # 将指定目录里文件压缩为zip
#     with zipfile.ZipFile(zip_name, 'w') as zipf:
#         for root, dirs, files in os.walk(directory):
#             # os.chdir(root)
#             for file in files:
#                 zipf.write(os.path.join(root, file))
#                 # zipf.write(file)
#     print(f"{zip_name} created successfully.")
#
# # 将zip目录里文件和文件夹压缩为1directory.zip
# compress_directory('/Users/linghuchong/Downloads/51/Python/project/PO/1directory.zip',  '/Users/linghuchong/Downloads/51/Python/project/PO/zip/')


# def extract_zip(zip_name, extract_to):
#     # 将zip解压到指定目录
#     with zipfile.ZipFile(zip_name, 'r') as zipf:
#         zipf.extractall(extract_to)
#     print(f"{zip_name} extracted successfully to {extract_to}.")
#
# # 将zip解压到指定目录
# extract_zip('/Users/linghuchong/Downloads/51/Python/project/PO/1directory.zip', '/Users/linghuchong/Downloads/51/Python/project/PO/1')


# def list_files_in_zip(zip_name):
#     with zipfile.ZipFile(zip_name, 'r') as zipf:
#         print("Files in ZIP:", zipf.namelist())
#
# # 查看zip文件列表
# list_files_in_zip('/Users/linghuchong/Downloads/51/Python/project/PO/1directory.zip')


import tarfile
# def create_tar_gz(tar_name, source_dir):
#     with tarfile.open(tar_name, 'w:gz') as tar:
#         tar.add(source_dir, arcname=os.path.basename(source_dir))
#     print(f"{tar_name} created successfully.")
#
# # 创建一个gzip压缩的tar文件
# create_tar_gz('/Users/linghuchong/Downloads/51/Python/project/PO/example.tar.gz', '/Users/linghuchong/Downloads/51/Python/project/PO/1')


# def extract_tar_gz(tar_name, extract_to=''):
#     with tarfile.open(tar_name, 'r:gz') as tar:
#         tar.extractall(extract_to)
#     print(f"{tar_name} extracted successfully.")
#
# # 解压.tar.gz文件到当前目录。
# extract_tar_gz('/Users/linghuchong/Downloads/51/Python/project/PO/example.tar.gz')
# # 解压.tar.gz文件到指定目录。
# extract_tar_gz('/Users/linghuchong/Downloads/51/Python/project/PO/example.tar.gz', '/Users/linghuchong/Downloads/51/Python/project/PO/')


from zipfile import ZIP_DEFLATED
# def create_protected_zip(zip_name, directory, password):
#     with zipfile.ZipFile(zip_name, 'w', compression=ZIP_DEFLATED) as zipf:
#         for root, dirs, files in os.walk(directory):
#             for file in files:
#                 zipf.write(os.path.join(root, file))
#         #
#         # for file in files:
#         #     zipf.write(file)
#         zipf.setpassword(bytes(password, 'utf-8'))
#     print(f"{zip_name} created successfully with password protection.")
#
# # 压缩并加密ZIP文件（没有密码设置）
# create_protected_zip('/Users/linghuchong/Downloads/51/Python/project/PO/1directory.zip', '/Users/linghuchong/Downloads/51/Python/project/PO/1', 'jinhao')
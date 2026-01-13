# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 文件对象层 (获取路径、目录和文件信息、操作文件、系统级别)
# *********************************************************************

"""
# todo 1 读取
1.1 读取大文件 getBigFile()

# todo 2 转换
2.1 字典转json文件，dict2jsonfile("output.json", {1:"a"})
2.2 字典转json文件2，dict2jsonfile2("output.json", {1: "a"})
2.3 json文件转字典，jsonfile2dict("output.json")
2.4 字典转pickle，dict2picklefile("output.pickle", {1: "a"})
2.5 字典转pickle2，dict2picklefile2("output.pickle", {1: "a"})
2.6 字典转yaml，dict2yamlfile1("output.pickle", {1: "a"})
2.7 字典转yaml2，dict2yamlfile2("output.pickle", {1: "a"})

# todo 3 操作目录、文件、内容
3.1 pathlib自动创建目录、新建文件及内容(拼接) setFolderFileTextByConcat()
3.2 pathlib自动创建目录、新建文件及内容(非拼接) setFolderFileText()
3.3 新建文件 newFile()
3.4 复制目录 copyFolder()
3.5 复制文件 copyFile()
3.6 文件改名/移动 renameFile()
3.7 删除指定文件 delFiles()
3.8 级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）delFilesByLayer()
3.9 获取当前目录指定扩展名的文件列表 getFileListByExt()

# todo 4 文件属性
4.1 判断文件类型 isFileType()
4.2.1 判断文件是否存在 print(os.access("d:\\a.jpg", os.F_OK))
4.2.2 判断文件是否可读 print(os.access("d:\\a.jpg", os.R_OK))
4.2.3 判断文件是否可以写入 print(os.access("d:\\a.jpg", os.W_OK))
4.2.4 判断文件是否可以执行  print(os.access("d:\\a.jpg", os.X_OK))

"""


import os, shutil, glob, sys, pathlib, mimetypes
import json
import pickle
import yaml
from pathlib import Path


class FilePO():


    def getBigFile(self, varFilePath):
        # 1.1 读取大文件

        with open(varFilePath, 'rb') as file:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break
                # 处理这个块


    def dict2jsonfile(self, varFilePath, d_content):
        # 2.1 字典转json文件
        # 方法1: 使用json.dump()将字典直接写入文件
        # dict2jsonfile("output.json", {1:"a"})

        with open(varFilePath, "w", encoding='utf-8') as file:
            json.dump(d_content, file, ensure_ascii=False)

    def dict2jsonfile2(self, varFilePath, d_content):
        # 2.2 字典转json文件2
        # 方法2: 先将字典转换为JSON字符串，再写入文件
        # dict2jsonfile2("output.json", {1:"a"})

        json_str = json.dumps(d_content, ensure_ascii=False)  # 确保中文字符正确显示
        with open(varFilePath, "w", encoding='utf-8') as file:
            file.write(json_str)

    def jsonfile2dict(self, varFilePath):
        # 2.3 json文件转字典
        # jsonfile2dict("output.json")

        with open(varFilePath, "r", encoding='utf-8') as file:
            data = file.read()
        return json.loads(data)


    def dict2picklefile(self, varFilePath, d_content):
        # 2.4 字典转pickle
        # 方法1: 使用pickle.dump()将字典直接写入文件
        # dict2picklefile("output.pickle",  {1:"a"})

        with open(varFilePath, "wb") as file:
            pickle.dump(d_content, file, protocol=pickle.HIGHEST_PROTOCOL)

    def dict2picklefile2(self, varFilePath, d_content):
        # 2.5 字典转pickle2
        # 方法2: 先将字典序列化为字节流，再写入文件
        # dict2picklefile2("output.pickle", {1:"a"})

        data_bytes = pickle.dumps(d_content, protocol=pickle.HIGHEST_PROTOCOL)
        with open(varFilePath, "wb") as file:
            file.write(data_bytes)

    def dict2yamlfile(self, varFilePath, d_content):
        # 2.6 字典转yaml
        # 方法1: 使用yaml.dump()将字典直接写入文件
        # dict2yamlfile("output.yaml", {1:"a"})

        with open(varFilePath, "w") as file:
            yaml.dump(d_content, file, allow_unicode=True)  # 允许Unicode字符

    def dict2yamlfile2(self, varFilePath, d_content):
        # 2.7字典转yaml2
        # 方法2: 先将字典转换为YAML格式字符串，再写入文件
        # dict2yamlfile2("output.yaml", {1:"a"})

        yaml_str = yaml.dump(d_content, allow_unicode=True) # 允许Unicode字符
        with open(varFilePath, "w", encoding='utf-8') as file:
            file.write(yaml_str)


    def setFolderFileTextByConcat(self, l_pathFolder, d_file_text):
        # 3.1 pathlib自动创建目录、新建文件及内容(拼接)
        # Pathlib模块(Python 3.4 +) 取代传统os.path操作，提供面向对象的路径管理
        # 返回内容
        # setFolderFileTextByConcat(["/Users/linghuchong/Desktop/data", "raw23"], {"input23.txt": "Hello Pathlib\n金浩"})

        data_path = Path(os.path.join(*l_pathFolder)) / list(d_file_text.keys())[0]
        data_path.parent.mkdir(parents=True, exist_ok=True)  # 创建多级目录
        data_path.write_text(list(d_file_text.values())[0])  # 写入文本
        return data_path.read_text()
        # print(data_path.read_text())  # 读取文本

    def setFolderFileText(self, varPathFolder, d_file_text):
        # 3.2 pathlib自动创建目录、新建文件及内容(非拼接)
        # Pathlib模块(Python 3.4 +) 取代传统os.path操作，提供面向对象的路径管理
        # 返回内容
        # setFolderFileText("/Users/linghuchong/Desktop/data/raw23", {"input23.txt": "Hello Pathlib\n金浩"})

        data_path = Path(varPathFolder) / list(d_file_text.keys())[0]
        data_path.parent.mkdir(parents=True, exist_ok=True)  # 创建多级目录
        data_path.write_text(list(d_file_text.values())[0])  # 写入文本
        return data_path.read_text()
        # print(data_path.read_text())  # 读取文本

    def newFile(self, varPath, varFile, text=""):
        # 3.3 新建文件 (自动创建目录、文件、内容)
        # File_PO.newFile("c:\\a", '13.txt')  # 在c:\a目录下新建13.txt文件，如果a目录不存在则自动创建目录
        # File_PO.newFile("c:\\a", '13.txt' '你好')  # 在c:\a目录下新建13.txt文件，并写入内容"你好"
        # File_PO.newFile("c:\\a", '13.txt')  # 在c:\a目录下新建13.txt文件

        if not os.path.exists(varPath):
            os.makedirs(varPath)
        file = open(varPath + "/" + varFile, "w")
        file.write(text)
        file.close()

    def copyFolder(self, srcFolderPath, tgtFolderPath, varMode="i"):
        # 3.4 复制目录
        # File_PO.copyFolder("c:\\a\123", "d:\\b\\444", 'i')  # 如果目录444已存在，则不覆盖
        # File_PO.copyFolder("c:\\a\123", "d:\\b\\444", 'w')  # 如果目录444已存在，则覆盖（w = 覆盖）

        if not os.path.exists(tgtFolderPath):
            shutil.copytree(srcFolderPath, tgtFolderPath)
        else:
            if varMode == "w":
                # 覆盖
                shutil.rmtree(tgtFolderPath)
                shutil.copytree(srcFolderPath, tgtFolderPath)

    def copyFile(self, srcFilePath, tgtFilePath, varMode="i"):
        # 3.5 复制文件
        # File_PO.copyFile("c:\\a\123.txt", "d:\\b\\444.txt", 'i')  # 如444.txt文件已存在，则忽略
        # File_PO.copyFile("c:\\a\123.txt", "d:\\b\\444.txt", 'w')  # 如444.txt文件已存在，则覆盖（w = 覆盖）

        if os.path.exists(tgtFilePath):
            if varMode == "w":
                # 覆盖
                os.remove(tgtFilePath)
                shutil.copyfile(srcFilePath, tgtFilePath)
        else:
            shutil.copyfile(srcFilePath, tgtFilePath)

    def renameFile(self, old_name, new_name):
        # 3.6 文件改名 / 移动

        try:
            os.rename(old_name, new_name)
            print(f"文件 {old_name} 已成功重命名为 {new_name}")
        except FileNotFoundError:
            print(f"错误: 未找到文件 {old_name}")
        except FileExistsError:
            print(f"错误: 文件 {new_name} 已存在")
        except PermissionError:
            print("错误: 没有权限重命名该文件")
        except Exception as e:
            print(f"错误: 发生了未知错误: {e}")

    def delFiles(self, varPath, varFile):
        # 3.7 删除指定文件
        # File_PO.delFile("c:\\a", "13.txt")  # 删除13.txt文件
        # File_PO.delFile("./data", [".txt", ".jpg"])  # 删除所有txt和jpg文件
        list1 = []
        if isinstance(varFile, list):
            # for i in range(len(varFile)):
            #     varFilePath = varPath + "/" + varFile[i]
            #     os.remove(varFilePath)
        # if "*." in varFilePath:
            list1 = File_PO.getListFile(varPath, varFile)
            for i in range(len(list1)):
                os.remove(list1[i])
        else:
            varFilePath = varPath + "/" + varFile
            os.remove(varFilePath)

    def delFilesByLayer(self, varPath):
        # 3.8 级联删除目录下所有文件
        # 包括子目录下的文件，但保留所有子目录架构

        ls = os.listdir(varPath)
        for i in ls:
            c_path = os.path.join(varPath, i)
            if os.path.isdir(c_path):
                self.delFilesByLayer(c_path)
            else:
                os.remove(c_path)


    def getFileListByExt(self, varPath, varExt):
        # 3.9 获取当前目录指定扩展名的文件列表
        # getFileListByExt("./data", [".png", ".jpg"]) # 遍历当前目录data下扩展名是png和jpg
        # ['./data/logo.png', './data/1.jpg']

        varPathList = []
        try:
            file = os.listdir(varPath)
            for im_name in file:
                if os.path.isdir(os.path.join(varPath, im_name)):
                    self.getFileListByExt(os.path.join(varPath, im_name), varExt)
                else:
                    # 根据后缀判断是否为 .png, .jpg
                    ext = os.path.splitext(im_name)[1]
                    if ext in varExt:
                        name = os.path.join(varPath, im_name)  # 构造完整路径
                        varPathList.append(name)
            return varPathList
        except Exception as e:
            print(e)


    def isFileType(self, varFilePath):
        # 4.1 判断文件类型
        # 根据文件的MIME类型判断文件类型
        # isFileType("/path/to/file.jpg")  # 返回: image
        # isFileType("/path/to/file.txt")  # 返回: text
        # isFileType("/path/to/file.pdf")  # 返回: application
        # isFileType("/path/to/unknown")    # 返回: unknown

        if not os.path.exists(varFilePath):
            return "file not found"

        # 获取文件的MIME类型
        mime_type, encoding = mimetypes.guess_type(varFilePath)

        if mime_type is None:
            return "unknown"

        # 根据MIME类型的主要类别进行分类
        main_type = mime_type.split('/')[0]

        return main_type


if __name__ == "__main__":

    File_PO = FilePO()



    # print("3.4 复制目录".center(100, "-"))
    # File_PO.copyFolder("/Users/linghuchong/Downloads/1", "/Users/linghuchong/Downloads/51/2")  # 如果目标目录已存在，则不覆盖。
    # File_PO.copyFolder("/Users/linghuchong/Downloads/1", "/Users/linghuchong/Downloads/51/2", 'w')  # 如果目标目录已存在，则覆盖。

    # print("3.5 复制文件".center(100, "-"))
    # File_PO.copyFile("/Users/linghuchong/Downloads/1.doc", "/Users/linghuchong/Downloads/2.doc")
    # File_PO.copyFile("/Users/linghuchong/Downloads/1.doc", "/Users/linghuchong/Downloads/2.doc", 'w')  # 目标目录已存在，则覆盖

    # print("3.7 删除指定文件".center(100, "-"))
    # File_PO.delFiles(os.getcwd() + "/filepo/filepo2", "13.txt")  # 删除1个文件
    # File_PO.delFiles(os.getcwd() + "/filepo/filepo2", [".txt",'.jpg'])  # 批量删除指定类型的文件
    # File_PO.delFiles('', "/Users/linghuchong/Downloads/51/Python/project/PO/captcha.gif")  # 删除当前路径下所有文件

    # print("3.8 级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）".center(100, "-"))
    # File_PO.delFilesByLayer("d:/test1")

    # print("3.9 获取当前目录指定扩展名的文件列表".center(100, "-"))
    # print(File_PO.getFileListByExt("./data", [".png", ".jpg"]))  # 遍历当前目录data下扩展名是png和jpg


    # print("4.1 判断文件类型".center(100, "-"))
    # print(File_PO.isFileType("./data/logo.png"))  # 输出: image
    # print(File_PO.isFileType("./data/idCard.txt"))  # 输出: text
    # print(File_PO.isFileType("./data/excel.py"))  # 输出: text
    # print(File_PO.isFileType("./data/data.yaml"))  # 输出: unknown 或具体类型

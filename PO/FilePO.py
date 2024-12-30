# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 文件对象层 (获取路径、目录和文件信息、操作文件、系统级别)
# *********************************************************************
"""
写入文件
字典转json文件，dict2jsonfile("output.json", {1:"a"})
字典转json文件2，dict2jsonfile2("output.json", {1: "a"})
json文件转字典，jsonfile2dict("output.json")
字典转pickle，dict2picklefile("output.pickle", {1: "a"})
字典转pickle2，dict2picklefile2("output.pickle", {1: "a"})
字典转yaml，dict2yamlfile1("output.pickle", {1: "a"})
字典转yaml2，dict2yamlfile2("output.pickle", {1: "a"})

读取文件
读取大文件 readBigFile()


3，目录与文件
3.2 获取路径下目录及文件清单（包括路径） getWalk()

3.16 遍历目录中指定扩展名文件
3.17 判断文件的存在、读、写、执行
	文件是否存在 print(os.access("d:\\a.jpg", os.F_OK))
	文件是否可读 print(os.access("d:\\a.jpg", os.R_OK))
	文件是否可以写入 print(os.access("d:\\a.jpg", os.W_OK))
	文件是否可以执行  print(os.access("d:\\a.jpg", os.X_OK))
3.18 判断文件类型 isFileType()

4，操作目录文件
4.5 newFile  新建文件
4.3 copyFolder  复制目录
4.6 copyFile  复制文件
4.7 renameFile  文件改名/移动
4.12  delFilesByLayer  级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）
"""

import os, shutil, glob, sys, pathlib, mimetypes
import json, pickle, yaml



class FilePO:

    def readBigFile(self, varFilePath):
        # 读取大文件
        # readBigFile()
        with open(varFilePath, 'rb') as file:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break
                # 处理这个块



    def dict2jsonfile(self, varFilePath, d_content):
        # 方法1: 使用json.dump()将字典直接写入文件
        # dict2jsonfile("output.json", {1:"a"})
        with open(varFilePath, "w", encoding='utf-8') as file:
            json.dump(d_content, file, ensure_ascii=False)

    def dict2jsonfile2(self, varFilePath, d_content):
        # 方法2: 先将字典转换为JSON字符串，再写入文件
        # dict2jsonfile2("output.json", {1:"a"})
        json_str = json.dumps(d_content, ensure_ascii=False)  # 确保中文字符正确显示
        with open(varFilePath, "w", encoding='utf-8') as file:
            file.write(json_str)

    def jsonfile2dict(self, varFilePath):
        # json文件转字典
        # jsonfile2dict("output.json")
        with open(varFilePath, "r", encoding='utf-8') as file:
            c = file.read()
            return json.loads(c)


    def dict2picklefile(self, varFilePath, d_content):
        # 方法1: 使用pickle.dump()将字典直接写入文件
        # dict2picklefile("output.pickle",  {1:"a"})
        with open(varFilePath, "wb") as file:
            pickle.dump(d_content, file, protocol=pickle.HIGHEST_PROTOCOL)

    def dict2picklefile2(self, varFilePath, d_content):
        # 方法2: 先将字典序列化为字节流，再写入文件
        # dict2picklefile2("output.pickle", {1:"a"})
        data_bytes = pickle.dumps(d_content, protocol=pickle.HIGHEST_PROTOCOL)
        with open(varFilePath, "wb") as file:
            file.write(data_bytes)

    def dict2yamlfile(self, varFilePath, d_content):
        # 方法1: 使用yaml.dump()将字典直接写入文件
        # dict2yamlfile("output.yaml", {1:"a"})
        with open(varFilePath, "w") as file:
            yaml.dump(d_content, file, allow_unicode=True)  # 允许Unicode字符

    def dict2yamlfile2(self, varFilePath, d_content):
        # 方法2: 先将字典转换为YAML格式字符串，再写入文件
        # dict2yamlfile2("output.yaml", {1:"a"})
        yaml_str = yaml.dump(d_content, allow_unicode=True) # 允许Unicode字符
        with open(varFilePath, "w", encoding='utf-8') as file:
            file.write(yaml_str)



    # 3.16 遍历目录中指定扩展名文件(级联目录)
    def getfilelist(self, varPathList, varPath, EXTEND):
        file = os.listdir(varPath)
        for im_name in file:
            if os.path.isdir(os.path.join(varPath, im_name)):
                self.getfilelist(varPathList, os.path.join(varPath, im_name), EXTEND)
            else:
                # 根据后缀判断是否为图片
                ext = os.path.splitext(im_name)[1]
                if ext in EXTEND:
                    name = os.path.join(varPath, im_name)
                    filelist.append(name)

    def newFile(self, varPath, varFile, text=""):
        # 新建文件 (自动创建目录、文件、内容)
        # File_PO.newFile("c:\\a", '13.txt')  # 在c:\a目录下新建13.txt文件，如果a目录不存在则自动创建目录
        # File_PO.newFile("c:\\a", '13.txt' '你好')  # 在c:\a目录下新建13.txt文件，并写入内容"你好"
        # File_PO.newFile("c:\\a", '13.txt')  # 在c:\a目录下新建13.txt文件
        if not os.path.exists(varPath):
            os.makedirs(varPath)
        file = open(varPath + "/" + varFile, "w")
        file.write(text)
        file.close()


    def copyFolder(self, srcFolderPath, tgtFolderPath, varMode="i"):
        # 复制目录
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
        # 复制文件
        # File_PO.copyFile("c:\\a\123.txt", "d:\\b\\444.txt", 'i')  # 如444.txt文件已存在，则忽略
        # File_PO.copyFile("c:\\a\123.txt", "d:\\b\\444.txt", 'w')  # 如444.txt文件已存在，则覆盖（w = 覆盖）
        if os.path.exists(tgtFilePath):
            if varMode == "w":
                # 覆盖
                os.remove(tgtFilePath)
                shutil.copyfile(srcFilePath, tgtFilePath)
        else:
            shutil.copyfile(srcFilePath, tgtFilePath)

    def delFile(self, varPath, varFile):
        # 删除文件
        # File_PO.delFile("c:\\a", "13.txt")  # 删除13.txt文件
        # File_PO.delFile("c:\\a", "*.txt")  # 删除所有txt文件
        list1 = []
        varFilePath = varPath + "/" + varFile
        if "*." in varFilePath:
            list1 = File_PO.getListFile(varFilePath)
            for i in range(len(list1)):
                os.remove(list1[i])
        else:
            os.remove(varFilePath)


    def delFilesByLayer(self, varPath):
        # 级联删除目录下所有文件
        # 包括子目录下的文件，但保留所有子目录架构
        ls = os.listdir(varPath)
        for i in ls:
            c_path = os.path.join(varPath, i)
            if os.path.isdir(c_path):
                self.delFilesByLayer(c_path)
            else:
                os.remove(c_path)


if __name__ == "__main__":

    File_PO = FilePO()

    # print("3.16 遍历目录中指定扩展名文件".center(100, "-"))
    # filelist = []
    # File_PO.getfilelist(filelist, "../test/upload", [".png", ".jpg"])
    # print(filelist)



    # print("4.3 复制目录".center(100, "-"))
    # File_PO.copyFolder("/Users/linghuchong/Downloads/1", "/Users/linghuchong/Downloads/51/2")  # 如果目标目录已存在，则不覆盖。
    # File_PO.copyFolder("/Users/linghuchong/Downloads/1", "/Users/linghuchong/Downloads/51/2", 'w')  # 如果目标目录已存在，则覆盖。

    # print("4.6 复制文件".center(100, "-"))
    # File_PO.copyFile("/Users/linghuchong/Downloads/1.doc", "/Users/linghuchong/Downloads/2.doc")
    # File_PO.copyFile("/Users/linghuchong/Downloads/1.doc", "/Users/linghuchong/Downloads/2.doc", 'w')  # 目标目录已存在，则覆盖


    # print("4.10 删除文件（支持通配符）".center(100, "-"))
    # File_PO.delFile(os.getcwd() + "/filepo/filepo2", "13.txt")  # 删除1个文件
    # File_PO.delFile(os.getcwd() + "/filepo/filepo2", "*.txt")  # 批量删除文件
    # File_PO.delFile(os.getcwd(), "*.*")  # 删除当前路径下所有文件
    # File_PO.delFile('', "/Users/linghuchong/Downloads/51/Python/project/PO/captcha.gif")  # 删除当前路径下所有文件



    # print("4.12 级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）".center(100, "-"))
    # File_PO.delFilesByLayer("d:/test1")


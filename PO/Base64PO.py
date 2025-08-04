# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2023-11-15
# Description   : base64 对象
# *********************************************************************

"""
1，图片转base64 imgToBase64()
2，将base64转图片 base64ToImg()

"""

import base64, re, os

class Base64PO:

    def imgToBase64(self, file):

        # 1 图片转base64

        d = {}
        # 1、读取文件
        with open(file, "rb") as f:
            img = f.read()

        # 2、获取图片的base64编码
        base64Data = base64.b64encode(img).decode()
        # print(base64Data)  # /9j/4AAQSkZJRgABAgAAAQABA...
        d['base64'] = base64Data

        # 3、拼接base64编码成 data URI scheme
        dataURI = "data:image/{ext};base64,{data}".format(ext=file.split(".")[-1], data=base64Data)

        d['dataUri'] = dataURI
        return d


    def base64ToImg(self, dataURI, file='base64'):

        # 2 base64转图片

        # 1、获取base64编码信息及文件扩展名
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", dataURI, re.DOTALL)
        # print(result)  # <re.Match object; span=(0, 4646), match='data:image/gif;base64,/9j/4AAQSkZJRgABAgAAAQABAAD>
        if result:
            fileExt = result.groupdict().get("ext")  # gif
            base64Data = result.groupdict().get("data")  # /9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDB ....
        else:
            # raise Exception("Do not parse!")
            raise ValueError("无法解析 dataURI 格式")

        # 2、解码base64
        # img = base64.urlsafe_b64decode(base64Data)
        img = base64.b64decode(base64Data)

        # 3、生成图片
        # pathFile = "{}.{}".format(os.getcwd() + "/" + file, fileExt)
        # pathFile = os.path.join(os.getcwd(), f"{file}.{fileExt}")
        default_filename = "output_image"
        pathFile = os.path.join(os.getcwd(), f"{file or default_filename}.{fileExt}")
        with open(pathFile, "wb") as f:
            f.write(img)

        return pathFile



if __name__ == "__main__":

    Base64_PO = Base64PO()

    # print("1, 图片转base64".center(100, "-"))
    # print(Base64_PO.imgToBase64("Base64.gif"))


    print("2, base64转图片".center(100, "-"))
    # dataURI = '''data:image/gif;base64,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'''
    dataURI = '''data:image/gif;base64,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'''
    pathFile = Base64_PO.base64ToImg(dataURI, "./data/base64")
    print(pathFile)  # /Users/linghuchong/Downloads/51/Python/project/PO/./data/base64.gif

    # pathFile = Base64_PO.base64ToImg(dataURI)
    # print(pathFile)  # /Users/linghuchong/Downloads/51/Python/project/PO/captcha.gif




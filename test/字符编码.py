# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2017-4-6
# Description: unicode 编码与解码
# 中文\unicode编码在线转换工具, https://atool.vip/unicode
# 在线base64编码解码、base64加密解密 - https://atool.vip/base64
# 乱码解析 http://www.mytju.com/classCode/tools/messyCodeRecover.asp
# 在线编码转换工具  https://www.w3cschool.cn/tools/index?name=decode_encode_tool

# gb18030编码是现代汉字在计算机中的一种编码方式，它是GB2312和GBK的扩展，支持包括繁体字在内的更多汉字字符。
# utf-8编码是一种通用的字符编码方式，它可以表示世界上几乎所有的字符，包括汉字和各种特殊字符。
# ascii,ISO-8859-1,utf-16

# x = x.encode("gbk").decode("utf-8", errors="ignore")  # UnicodeEncodeError: 'gbk' codec can't encode character '\ue7d2' in position 35: illegal multibyte sequence


# 数据源，读取本地文件内容或者从网络上内容，对象为str类型；
# 编码转换过程，将str类型转换成其他编码类型，先将str转Unicode,再将unicode转其他特定的编码类型, 如：utf-8、gb2312等；

# gb18030转utf-8
s_gb18030 = '"鍡紝鏅氫笂濂斤紝鎴戞槸濯涘獩銆�"'
s_utf8 = s_gb18030.encode("GB18030").decode("utf-8", errors="ignore")
print(s_utf8)  # "嗨，晚上好，我是媛媛〄17"

# utf-8转gb18030
s_gb18030 = s_utf8.encode("utf-8").decode("GB18030", errors="ignore")
print(s_gb18030)  # "鍡紝鏅氫笂濂斤紝鎴戞槸濯涘獩銆17"

# unicode转gb2312,utf-8，即为unicode编码encode
s = '中国'
s_gb2312 = s.encode('gb2312')
s_utf8 = s.encode('utf-8')
print(s_gb2312)  # b'\xd6\xd0\xb9\xfa'
print(s_utf8)  # b'\xe4\xb8\xad\xe5\x9b\xbd'

# utf-8,gb2312转unicode，即为unicode解码decode
print(s_utf8.decode('utf-8'))  # 中国
print(s_gb2312.decode('gb2312'))  # 中国

# utf-8转gb2312，即先将utf8解码为unicode，再unicode编码为gb2312
print(s_utf8.decode('utf-8').encode('gb2312'))  # b'\xd6\xd0\xb9\xfa'

#
# # 文件编码与print函数
# # 建立一个文件test.txt，文件格式用ANSI，内容为: abc中文
# # text.py 内容如下：
# # coding=gbk
# # print open("Test.txt").read()
# # 结果：abc中文
# # 把文件格式改成UTF-8，结果：abc涓枃
# # 显然，这里需要解码：
# # coding=gbk
# import codecs
# # print open("Test.txt").read().decode("utf-8")
# # 结果：abc中文
# # 上面的test.txt我是用Editplus来编辑的，但当我用Windows自带的记事本编辑并存成UTF-8格式时，
# # 运行时报错：
# # Traceback (most recent call last):
# #   File "ChineseTest.py", line 3, in <module>
# #     print open("Test.txt").read().decode("utf-8")
# # UnicodeEncodeError: 'gbk' codec can't encode character u'/ufeff' in position 0: illegal multibyte sequence
# # 原来，某些软件，如notepad，在保存一个以UTF-8编码的文件时，会在文件开始的地方插入三个不可见的字符（0xEF 0xBB 0xBF，即BOM）。
# # 因此我们在读取时需要自己去掉这些字符，python中的codecs module定义了这个常量：
# # # coding=gbk
# # import codecs
# # data = open("Test.txt").read()
# # if data[:3] == codecs.BOM_UTF8:
# #   data = data[3:]
# # print data.decode("utf-8")
# # 结果：abc中文
#
#


# # 2、[python]去掉 unicode 字符串前面的 u
# # https://mozillazg.com/2013/12/python-raw-unicode.html
# # unicode.encode('raw_unicode_escape')
# print "~~~~~~~"
# a = ['你好']
# print a
print(u"你好".encode('raw_unicode_escape'))
print(u'\xe4\xbd\xa0\xe5\xa5\xbd'.encode('raw_unicode_escape'))


# # 5、自动编码转换
stri = "金浩"
def autoUnicode(stri):
   """Auto converter encodings to unicode
   It will test utf8,gbk,big5,jp,kr to converter"""
   for c in ('utf-8', 'gbk', 'big5', 'jp', 'euc_kr', 'utf16', 'utf32'):
       try:
            return stri.decode(c)
       except:
            pass
   return stri
# print(autoUnicode(stri))
print(autoUnicode(b'\xe4\xb8\xad\xe5\x9b\xbd'))
article/details/48841593